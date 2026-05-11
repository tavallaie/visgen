# VisGen — Audio Visualizer Generator

Generate beautiful, customizable audio visualizer videos with Python. FFT-reactive circular bars, multiple visualizers, rich overlays, post-processing effects, and a plugin system — all composable on a single canvas.

## Features

| Feature | Description |
| --------- | ------------- |
| **Circular FFT Visualizer** | Animated bars reacting to audio frequencies around a circular image |
| **Multiple Visualizers** | Render several visualizers on the same canvas via `render_multi()` |
| **Background Effects** | Solid colors, images with chained effects (blur, grayscale, sepia), opacity, fit modes |
| **Overlays** | Text (static & timed), images, and video overlays with time ranges, opacity, anchoring |
| **Positioning** | Named positions (`center`, `top-left`, `bottom-right`...) or exact `(x, y)` pixels |
| **Frame Effects** | Post-processing plugins: glow, vignette, shake, zoom pulse |
| **Bar Effects** | Pre-processing plugins: bounce, mirror, smooth decay |
| **Plugin System** | Drop `.py` files in `~/.visgen/plugins/` or use entry points |
| **Quad Modes** | One-circle repeated-bar quadrants with single or multi-color schemes |
| **Quality Output** | H.264 + AAC via FFmpeg |

## Installation

**Requirements:** Python 3.12+, FFmpeg in `PATH`

From PyPI:

```bash
pip install visgen
```

Or with `uv`:

```bash
uv add visgen
```

For local development:

```bash
git clone https://github.com/yourname/visgen.git
cd visgen
pip install -e ".[dev]"
```

**Runtime dependencies:** `numpy`, `opencv-python`, `Pillow`

## Quick Start

```python
from visgen import AudioVisualizerVideo

viz = AudioVisualizerVideo(
    audio_path="song.wav",
    image_path="cover.jpg",
    output_path="output.mp4",
)
viz.render_single()
```

## API Reference

### AudioVisualizerVideo

```python
AudioVisualizerVideo(
    audio_path: str,
    image_path: str | None = None,           # used if visualizers not given
    output_path: str = "output.mp4",
    duration: float | None = None,            # default = full audio length
    fps: int = 30,
    circle_radius: int = 150,
    bar_count: int = 64,
    bar_max_length: int = 200,
    colors: ColorScheme | None = None,
    smooth_factor: float = 0.3,
    background: Background | None = None,
    visualizers: list[CircularVisualizer] | None = None,
    frame_effects: list[FrameEffect] | None = None,
    bar_effects: list[BarEffect] | None = None,
)
```

> **Note:** Either `image_path` or `visualizers` must be provided.

### Render Methods

| Method | Description |
| -------- | ------------- |
| `render_single(position=..., overlays=..., visualizer=...)` | One visualizer on canvas |
| `render_multi(configs=[(viz, pos, angle), ...])` | Multiple visualizers, same canvas, same audio |
| `render_quad_repeated_bars(...)` | One circle, full bars repeated per quadrant |
| `render_quad_repeated_bars_multi_color(...)` | Same with per-quadrant colors |

### Backgrounds

```python
from visgen import ColorBackground, ImageBackground

# Solid color
ColorBackground(color=(15, 15, 30))

# Image with single effect
ImageBackground("bg.jpg", effect="blur", blur_radius=10.0, fit_mode="cover")

# Image with chained effects (applied in order)
ImageBackground("bg.jpg", effect=["blur", "grayscale"], blur_radius=12.0)

# Image with opacity
ImageBackground("bg.jpg", effect="sepia", opacity=0.6, fit_mode="cover")
```

**Fit modes:** `cover` | `contain` | `stretch`

**Effects:** `blur` | `grayscale` | `sepia`

### Overlays

```python
from visgen import TextOverlay, TimedText, ImageOverlay, VideoOverlay

# Static text
TextOverlay(text="Title", position=(540, 80), font_size=60, anchor="mm")

# Timed lyrics
TimedText(start_time=2.0, end_time=5.0, text="Lyrics", position=(540, 980))

# Static image
ImageOverlay("logo.png", position=(100, 100), size=(120, 120), anchor="mm")

# Timed image
ImageOverlay("badge.png", position=(500, 500), start_time=1.0, end_time=6.0)

# Looping video
VideoOverlay("loop.mp4", position=(900, 900), size=(200, 200), loop=True)
```

**Anchors:** `mm` (center) | `lt` (top-left) | `rb` (bottom-right) | `lb` | `rt`

### Positioning

```python
viz.render_single(position="center")        # named position
viz.render_single(position="bottom-right")  # corner
viz.render_single(position=(300, 800))      # exact pixels
```

**Named positions:** `center`, `top-left`, `top-right`, `bottom-left`, `bottom-right`, `top-center`, `bottom-center`, `left-center`, `right-center`

### Frame Effects (Post-Processing)

Applied to the final frame before encoding.

```python
from visgen import GlowEffect, VignetteEffect, ShakeEffect, ZoomPulseEffect

viz = AudioVisualizerVideo(
    audio_path="song.wav",
    image_path="cover.jpg",
    output_path="out.mp4",
    frame_effects=[
        GlowEffect(strength=0.4, radius=10.0),
        VignetteEffect(strength=0.5),
    ],
)
viz.render_single()
```

### Bar Effects (Pre-Processing)

Modify FFT bar values before rendering.

```python
from visgen import BounceEffect, SmoothDecayEffect

viz = AudioVisualizerVideo(
    audio_path="song.wav",
    image_path="cover.jpg",
    output_path="out.mp4",
    bar_effects=[
        BounceEffect(speed=0.15, amplitude=0.2),
        SmoothDecayEffect(decay=0.9),
    ],
)
viz.render_single()
```

## Examples

### Multiple visualizers side by side

```python
from visgen import AudioVisualizerVideo, CircularVisualizer, ColorScheme

left = CircularVisualizer("cover1.jpg", 140, 64, 180, colors=ColorScheme(bar=(0, 200, 255)))
right = CircularVisualizer("cover2.jpg", 140, 64, 180, colors=ColorScheme(bar=(255, 100, 100)))

video = AudioVisualizerVideo(
    audio_path="song.wav",
    output_path="duo.mp4",
    visualizers=[left, right],
)
video.render_multi([
    (left, (300, 540), 0),
    (right, (780, 540), np.pi),
])
```

### Custom inline effects

```python
from visgen import FrameEffect, BarEffect
import numpy as np
from PIL import Image

class GreenTint(FrameEffect):
    def apply(self, frame, frame_idx, bar_values=None):
        arr = np.array(frame, dtype=np.float32)
        arr[:, :, 1] *= 1.15
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

class SquashBars(BarEffect):
    def process(self, bar_values, frame_idx, audio_chunk=None):
        return np.power(bar_values, 1.5)

viz = AudioVisualizerVideo(
    audio_path="song.wav",
    image_path="cover.jpg",
    output_path="out.mp4",
    frame_effects=[GreenTint()],
    bar_effects=[SquashBars()],
)
viz.render_single()
```

### Plugin discovery

```python
from visgen.plugins import load_plugins, registry

# Auto-discovers Plugin subclasses in ~/.visgen/plugins/
load_plugins()

# Inspect registered extensions
print(registry.frame_effects)
print(registry.bar_effects)

# Instantiate by name
effect = registry.create_frame_effect("GlowEffect", strength=0.5)
```

## Running the Examples

```bash
python -m visgen.main
```

`src/visgen/main.py` contains **38 example functions**. Control which run by editing the `EXAMPLES` list at the bottom of the file:

```python
EXAMPLES = [
    example_01_minimal,
    example_04_image_bg_blur,
    example_31_frame_effects,
]
```

## File Structure

```bash
src/visgen/
├── __init__.py           # Public exports
├── main.py               # 38 runnable example functions
├── audio.py              # AudioProcessor (FFmpeg extraction + FFT)
├── background.py         # Background ABC, ColorBackground, ImageBackground
├── colors.py             # ColorScheme dataclass
├── overlay.py            # TextOverlay, TimedText, ImageOverlay, VideoOverlay
├── renderer.py           # AudioVisualizerVideo (main composer)
├── utils.py              # Font loader & position resolver
├── visualizer.py         # CircularVisualizer
├── bars/                 # Bar-value pre-processing effects
│   ├── base.py           # BarEffect ABC
│   ├── builtin.py        # BounceEffect, MirrorEffect, SmoothDecayEffect
│   └── __init__.py
├── effects/              # Frame post-processing effects
│   ├── base.py           # FrameEffect ABC
│   ├── builtin.py        # GlowEffect, VignetteEffect, ShakeEffect, ZoomPulseEffect
│   └── __init__.py
└── plugins/              # Plugin discovery & registry
    ├── base.py           # Plugin, PluginMeta, PluginRegistry
    ├── loader.py         # discover_plugins(), load_plugins()
    └── __init__.py
```

## License

MIT
