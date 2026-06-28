#!/usr/bin/env python3
"""Convert a short video/GIF into a motion-assets entry.

Usage:
  python3 scripts/add_motion_asset.py INPUT SLUG CATEGORY NAME DESCRIPTION TAGS_CSV
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageStat


def run(cmd: list[str], cwd: Path | None = None) -> str:
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
    return p.stdout


def probe(path: Path) -> dict:
    return json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-print_format', 'json', str(path)]))


def bg_color(im: Image.Image) -> tuple[int, int, int]:
    w, h = im.size
    s = max(8, min(w, h) // 36)
    boxes = [(0, 0, s, s), (w - s, 0, w, s), (0, h - s, s, h), (w - s, h - s, w, h)]
    means = []
    for box in boxes:
        stat = ImageStat.Stat(im.crop(box).convert('RGB'))
        means.append(tuple(int(x) for x in stat.mean))
    r, g, b = (sum(p[i] for p in means) // len(means) for i in range(3))
    return int(r), int(g), int(b)


def detect_crop(sample_paths: list[Path], src_size: tuple[int, int], square: bool) -> tuple[tuple[int, int, int, int], tuple[int, int, int]]:
    first = Image.open(sample_paths[0]).convert('RGB')
    bg = bg_color(first)
    boxes = []
    for path in sample_paths:
        im = Image.open(path).convert('RGB')
        pix = im.load()
        w, h = im.size
        xs, ys = [], []
        for y in range(h):
            for x in range(w):
                r, g, b = pix[x, y]
                diff = max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2]))
                sat = max(r, g, b) - min(r, g, b)
                bright = max(r, g, b)
                if diff > 18 or (sat > 22 and bright > 28):
                    xs.append(x)
                    ys.append(y)
        if xs:
            boxes.append((min(xs), min(ys), max(xs) + 1, max(ys) + 1))
    w, h = src_size
    if not boxes:
        return (0, 0, w, h), bg
    x0, y0, x1, y1 = min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)
    margin = 24
    if square:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        side = min(max(w, h), max(x1 - x0, y1 - y0) + margin * 2)
        x0, y0 = int(round(cx - side / 2)), int(round(cy - side / 2))
        x1, y1 = x0 + int(side), y0 + int(side)
        if x0 < 0:
            x1 -= x0; x0 = 0
        if y0 < 0:
            y1 -= y0; y0 = 0
        if x1 > w:
            x0 -= x1 - w; x1 = w
        if y1 > h:
            y0 -= y1 - h; y1 = h
        x0, y0 = max(0, x0), max(0, y0)
    else:
        x0, y0, x1, y1 = max(0, x0 - margin), max(0, y0 - margin), min(w, x1 + margin), min(h, y1 + margin)
    # x264 even dimensions
    if (x1 - x0) % 2:
        x1 -= 1
    if (y1 - y0) % 2:
        y1 -= 1
    return (x0, y0, x1, y1), bg


def main() -> None:
    if len(sys.argv) < 7:
        print(__doc__)
        sys.exit(2)
    src = Path(sys.argv[1]).resolve()
    slug, category, name, desc = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    tags = [t.strip() for t in sys.argv[6].split(',') if t.strip()]
    repo = Path(__file__).resolve().parents[1]
    dest = repo / 'assets' / category / slug
    work = repo / '.work' / 'assets' / slug
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    dest.mkdir(parents=True, exist_ok=True)
    meta = probe(src)
    st = meta['streams'][0]
    fmt = meta['format']
    w, h = int(st['width']), int(st['height'])
    duration = float(fmt.get('duration') or 0)
    frames = int(st.get('nb_frames') or round(duration * 30))
    # sample at 10 fps for crop/contact; full conversion is handled directly by ffmpeg.
    sample_dir = work / 'samples'
    sample_dir.mkdir()
    run(['ffmpeg', '-y', '-i', str(src), '-vf', 'fps=10', str(sample_dir / 'sample_%04d.png')])
    samples = sorted(sample_dir.glob('sample_*.png'))
    square = w == h or category in {'loaders', 'icons', 'stickers'}
    crop, bg = detect_crop(samples, (w, h), square)
    x0, y0, x1, y1 = crop
    cw, ch = x1 - x0, y1 - y0
    vf = f'crop={cw}:{ch}:{x0}:{y0}'
    # Preserve-background formats. These are robust and avoid transparency halos.
    run(['ffmpeg', '-y', '-i', str(src), '-vf', vf, '-loop', '0', '-lossless', '1', '-compression_level', '6', str(dest / 'motion.webp')])
    run(['ffmpeg', '-y', '-i', str(src), '-vf', vf, str(dest / 'motion.gif')])
    run(['ffmpeg', '-y', '-i', str(src), '-vf', f'{vf},format=yuv420p', '-movflags', '+faststart', '-an', '-c:v', 'libx264', '-crf', '23', '-preset', 'slow', str(dest / 'motion.mp4')])
    run(['ffmpeg', '-y', '-i', str(src), '-vf', vf, '-frames:v', '1', str(dest / 'poster.png')])
    shutil.copy2(src, dest / 'source.mp4')
    # Transparent file is intentionally omitted unless a clean alpha mask is manually verified.
    data = {
        'id': slug,
        'name': name,
        'category': category,
        'tags': tags,
        'description': desc,
        'duration': round(duration, 3),
        'frames': frames,
        'dimensions': [cw, ch],
        'formats': ['webp', 'gif', 'mp4'],
        'transparent': False,
        'loop': True,
        'recommendedUse': ['ui', 'software', 'web', 'app', 'presentation', 'bot', 'creative-project'],
        'source': 'user-provided video converted by Hermes Agent',
        'license': 'unknown',
        'backgroundColor': '#%02x%02x%02x' % bg,
        'crop': list(crop),
    }
    (dest / 'metadata.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    (dest / 'README.md').write_text(f'''# {name}\n\n{desc}\n\n## Files\n\n| File | Use |\n|---|---|\n| `motion.webp` | Preferred animated WebP |\n| `motion.gif` | Broad fallback |\n| `motion.mp4` | Video format for playback |\n| `poster.png` | Static preview frame |\n| `source.mp4` | Original source backup |\n| `metadata.json` | Machine-readable metadata |\n\n## HTML\n\n```html\n<picture>\n  <source srcset="./motion.webp" type="image/webp" />\n  <img class="motion-asset" src="./motion.gif" alt="{name}" width="96" height="96" />\n</picture>\n```\n\n## License\n\nSource license is currently unknown; treat as demo/personal-use until rights are confirmed.\n''')
    print(json.dumps({'slug': slug, 'category': category, 'dimensions': [cw, ch], 'frames': frames, 'duration': duration, 'crop': crop}, ensure_ascii=False))


if __name__ == '__main__':
    main()
