# motion-assets

Optimized motion assets for apps, websites, interfaces, presentations, bots, and creative projects.

This repository collects small animation resources converted from GIFs/videos into portable, production-ready formats with fidelity, compatibility, and performance in mind.

## First asset

### Neon Triangle Morph

![Neon Triangle Morph](assets/effects/neon-triangle-morph/motion.gif)

```html
<picture>
  <source srcset="assets/effects/neon-triangle-morph/motion-transparent.webp" type="image/webp" />
  <img src="assets/effects/neon-triangle-morph/motion.gif" alt="Neon Triangle Morph" width="96" height="96" />
</picture>
```

## Repository layout

```text
assets/
  loaders/
  icons/
  transitions/
  stickers/
  logos/
  effects/
  backgrounds/
  ui-feedback/
packages/
examples/
docs/
site/
```

## Format strategy

- **Animated WebP**: preferred for modern environments.
- **GIF**: broad compatibility fallback.
- **MP4**: best for larger motion when transparency is not needed.
- **APNG/Lottie/SVG**: optional per asset when useful.

## Licensing

Each asset has its own `metadata.json` and README. Do not assume an asset is open for commercial use unless its metadata says so.
