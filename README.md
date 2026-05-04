# VisGen — Audio Visualizer Generator

Generate beautiful, customizable audio visualizer videos with Python. React to music with circular FFT bars, overlay text, images, and videos, and position everything exactly where you want.

![visgen-demo](https://via.placeholder.com/800x400?text=VisGen+Demo)

## Features

- **Circular FFT Visualizer** — Animated bars reacting to audio frequencies around a circular image
- **Multiple Visualizers** — Render several visualizers on the same canvas, each with its own image, colors, size, and position
- **Customizable Backgrounds** — Solid colors, images with blur/grayscale/sepia effects, opacity control, and fit modes (cover/contain/stretch)
- **Rich Overlays** — Text (static & timed), images, and video overlays with optional time ranges, opacity, and positioning
- **Flexible Positioning** — Named positions (`center`, `top-left`, `bottom-right`, etc.) or exact pixel coordinates
- **Quad Modes** — Repeated bars in quadrants with single or multi-color schemes
- **High Quality Output** — H.264 encoding via FFmpeg with AAC audio muxing

## Installation

### Requirements

- Python 3.12+
- FFmpeg (must be in your `PATH`)

### From source

```bash
git clone https://github.com/yourname/visgen.git
cd visgen
pip install -e ".[dev]"
```

### Dependencies

```
numpy
opencv-python
Pillow
```

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

## API Overview

### `AudioVisualizerVideo`

Main composer class.

```python
AudioVisualizerVideo(
    audio_path: str,                    # Path to audio file
    image_path: str | None = None,      # Default image for single visualizer
    output_path: str = "output.mp4",
    duration: float | None = None,      # Trim to N seconds (default: full audio)
    fps: int = 30,
    circle_radius: int = 150,
    bar_count: int = 64,
    bar_max_length: int = 200,
    colors: ColorScheme | None = None,
    smooth_factor: float = 0.3,
    background: Background | None = None,
    visualizers: list[CircularVisualizer] | None = None,
)
```

**Either `image_path` or `visualizers` must be provided.**

### Render Methods

| Method | Description |
|--------|-------------|
| `render_single(position=..., overlays=..., visualizer=...)` | One visualizer on canvas |
| `render_multi(configs=[(viz, pos, angle), ...])` | Multiple visualizers on same canvas |
| `render_quad_repeated_bars(...)` | One circle, full bars repeated per quadrant |
| `render_quad_repeated_bars_multi_color(...)` | Same with per-quadrant colors |

### Backgrounds

```python
from visgen import ColorBackground, ImageBackground

# Solid color
ColorBackground(color=(15, 15, 30))

# Image with effects
ImageBackground(
    "bg.jpg",
    effect="blur",          # "blur" | "grayscale" | "sepia"
    blur_radius=10.0,
    opacity=0.7,
    fit_mode="cover",       # "cover" | "contain" | "stretch"
)
```

### Overlays

```python
from visgen import TextOverlay, TimedText, ImageOverlay, VideoOverlay

# Static text
TextOverlay(text="Title", position=(540, 80), font_size=60)

# Timed lyrics
TimedText(start=2.0, end=5.0, text="Lyrics", position=(540, 980))

# Static image
ImageOverlay("logo.png", position=(100, 100), size=(120, 120))

# Timed image
ImageOverlay("badge.png", position=(500, 500), start_time=1.0, end_time=6.0)

# Looping video
VideoOverlay("loop.mp4", position=(900, 900), size=(200, 200), loop=True)
```

### Positioning

Position can be:
- A tuple `(x, y)` — exact pixels
- A string — `"center"`, `"top-left"`, `"top-right"`, `"bottom-left"`, `"bottom-right"`, `"top-center"`, `"bottom-center"`, `"left-center"`, `"right-center"`

```python
viz.render_single(position="bottom-right")
viz.render_single(position=(300, 800))
```

## Examples

### Two visualizers side by side

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

### Blurred background + overlays

```python
from visgen import AudioVisualizerVideo, ImageBackground, TextOverlay, ImageOverlay

viz = AudioVisualizerVideo(
    audio_path="song.wav",
    image_path="cover.jpg",
    output_path="fancy.mp4",
    background=ImageBackground("bg.jpg", effect="blur", blur_radius=12.0),
)
viz.render_single(
    position="center",
    overlays=[
        TextOverlay("My Track", (540, 80), font_size=55),
        ImageOverlay("logo.png", (100, 100), size=(100, 100)),
    ],
)
```

### Timed lyrics

```python
from visgen import TimedText

viz.render_single(overlays=[
    TimedText(0.0, 3.5, "First line", (540, 980)),
    TimedText(4.0, 7.5, "Second line", (540, 980)),
    TimedText(8.0, 11.5, "Third line", (540, 980)),
])
```

### Video overlay (looping)

```python
from visgen import VideoOverlay

viz.render_single(overlays=[
    VideoOverlay("loop.mp4", position=(900, 900), size=(200, 200), loop=True),
])
```

## Running the Examples

```bash
python -m visgen.main
```

`src/visgen/main.py` contains 30+ runnable examples. Each one is live — they will all execute sequentially. Make sure you have asset files in an `assets/` folder or update the paths.

## File Structure

```
src/visgen/
├── __init__.py      # Public exports
├── main.py          # Usage examples
├── audio.py         # Audio extraction & FFT analysis
├── background.py    # Background classes (color, image, effects)
├── colors.py        # ColorScheme dataclass
├── overlay.py       # Text, Image, Video overlays
├── renderer.py      # Main video composer
├── utils.py         # Font loading & position resolver
└── visualizer.py    # CircularVisualizer rendering
```

## License

MIT
