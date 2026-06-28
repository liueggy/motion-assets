# Conversion Spec

1. Inspect source metadata with `ffprobe`.
2. Extract frames and verify timing.
3. Crop excess canvas using a union bounding box with margin.
4. Preserve alpha when available; otherwise create transparent variants conservatively.
5. Keep a background-preserving version when it is closer to the source or avoids edge halos.
6. Export WebP + GIF by default; add MP4/APNG when useful.
7. Generate metadata and usage snippets.
8. Verify frame count, dimensions, archive integrity, and preview availability.
