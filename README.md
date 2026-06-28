# motion-assets

Optimized motion assets for apps, websites, interfaces, presentations, bots, and creative projects.

This repository collects small animation resources converted from GIFs/videos into portable, production-ready formats with fidelity, compatibility, and performance in mind.

## Assets

| Asset | Category | Tags | Description |
|---|---|---|---|
| [Glitch Black Orb](assets/effects/glitch-black-orb/) | `effects` | glitch, black-orb, chromatic-aberration, abstract, flicker | A black circular orb with subtle jittering edges and chromatic glitch artifacts. |
| [Neon Energy Vortex](assets/effects/neon-energy-vortex/) | `effects` | neon, vortex, energy, particles, abstract | A looping abstract neon energy vortex made of colorful swirling particle trails on a black background. |
| [Neon Grid Ripple](assets/effects/neon-grid-ripple/) | `effects` | neon, grid, ripple, glitch, pixel-art | A looping neon pixel-art grid surface ripples and deforms like a glowing digital membrane. |
| [Neon Triangle Morph](assets/effects/neon-triangle-morph/) | `effects` | neon, triangle, morph, loop, geometric | Use motion-black.webp for exact black-background rendering; use motion-transparent.webp for overlays. |
| [Particle Vortex](assets/effects/particle-vortex/) | `effects` | particle, vortex, spiral, galaxy, energy | A dark particle vortex animation showing swirling galaxy-like energy motion. |
| [Purple Energy Ring](assets/effects/purple-energy-ring/) | `effects` | purple, energy, ring, portal, magic | A looping purple glowing energy ring animation suitable for magic portals, sci-fi effects, or charge-up VFX. |
| [Wireframe Torus Spin](assets/effects/wireframe-torus-spin/) | `effects` | wireframe, torus, rotating, particle, hologram | A dark sci-fi rotating wireframe torus rendered as a subtle holographic particle mesh. |
| [Neon Orb Spinner](assets/loaders/neon-orb-spinner/) | `loaders` | neon, spinner, loading, glow, sci-fi | A glowing blue-purple circular spinner animation with rotating dots and energy-ring effects. |
| [Spinning Pixel Heart](assets/stickers/spinning-pixel-heart/) | `stickers` | pixel-art, heart, love, voxel, pink | A neon pink pixel-art voxel heart spins with motion blur on a dark background. |

## Basic usage

```html
<picture>
  <source srcset="assets/effects/neon-triangle-morph/motion-transparent.webp" type="image/webp" />
  <img src="assets/effects/neon-triangle-morph/motion.gif" alt="Motion asset" width="96" height="96" />
</picture>
```

For assets without a verified transparent variant, use `motion.webp` as the preferred file and `motion.gif` as fallback.

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
