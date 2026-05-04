# AGENTS.md — VisGen Agent Guide

This file contains context and conventions for AI agents working on the VisGen codebase.

## Project Overview

VisGen is a Python tool for generating audio-reactive visualizer videos. It extracts audio via FFmpeg, performs FFT analysis frame-by-frame, and composites circular bar visualizers onto a canvas using PIL. Final output is encoded with FFmpeg (H.264 + AAC).

## Architecture

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `audio.py` | `AudioProcessor` — extracts mono audio with FFmpeg, computes per-frame FFT bar values with optional smoothing. |
| `background.py` | `Background` ABC + `ColorBackground` + `ImageBackground`. Handles solid colors, image loading, resize modes (cover/contain/stretch), and effects (blur, grayscale, sepia). |
| `colors.py` | `ColorScheme` dataclass — holds all color values and provides `bar_with_intensity()`. |
| `overlay.py` | `TextOverlay`, `TimedText` (dataclasses), `BaseOverlay` (ABC), `ImageOverlay`, `VideoOverlay`. All non-text overlays inherit from `BaseOverlay` and implement `draw(canvas, current_time, fps)`. |
| `renderer.py` | `AudioVisualizerVideo` — the main orchestrator. Manages frame loop, calls `Background.render()`, renders visualizers, draws overlays, encodes video, muxes audio. |
| `utils.py` | `get_font()` (TTF fallback chain), `resolve_position()` (string → pixel coordinates). |
| `visualizer.py` | `CircularVisualizer` — loads a circular-masked image, renders FFT bars around it with glow effects and border ring. |

### Key Design Decisions

1. **Frame-by-frame rendering with temporary PNGs** — We write each frame to disk as a PNG, then invoke FFmpeg to encode. This is simple, debuggable, and avoids dealing with video codecs in Python.
2. **PIL for compositing, OpenCV only for saving** — PIL handles alpha blending, text, and image pasting better than OpenCV. We convert to OpenCV only for `cv2.imwrite`.
3. **FFmpeg as external dependency** — Audio extraction, video encoding, and audio muxing all shell out to `ffmpeg`. It must be in `PATH`.
4. **Modular visualizers** — `CircularVisualizer` is self-contained. `AudioVisualizerVideo` can accept a list of them via `visualizers=` and `render_multi()` composites them together.
5. **Backward compatibility** — `image_path` in `AudioVisualizerVideo.__init__` auto-creates a single `CircularVisualizer`. `self.visualizer` is kept as an alias to `self.visualizers[0]`.

## Code Conventions

- **Typing**: Use `from __future__ import annotations` style (Python 3.12+). Use `|` unions, not `Optional` / `Union` in new code.
- **Formatting**: 4-space indents. Black-compatible.
- **Imports**: Standard lib → third-party → local modules.
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes.
- **Constants**: No hardcoded paths in modules (except temp dir prefix `/tmp/visualizer_frames`).

## Extending VisGen

### Adding a new Background effect

1. Subclass `Background` in `background.py`
2. Implement `render(width, height, frame_idx) -> Image.Image`
3. Done — `AudioVisualizerVideo` accepts any `Background` instance

### Adding a new Overlay type

1. Subclass `BaseOverlay` in `overlay.py`
2. Implement `draw(self, canvas, current_time, fps)`
3. Add to `OverlayType` union if needed
4. `AudioVisualizerVideo._draw_media_overlays()` will pick it up automatically

### Adding a new Visualizer shape

1. Create a new module (e.g. `waveform.py`)
2. Implement a class with a `render(canvas, center_x, center_y, bar_values, frame_idx, ...)` method matching `CircularVisualizer.render()` signature
3. Pass it to `render_single(visualizer=...)` or `render_multi(configs=[...])`

## Known Limitations

- `VideoOverlay` uses OpenCV `VideoCapture` with frame seeking. For many video overlays this may be slow. If performance becomes an issue, pre-extract overlay video frames to a temp directory.
- `render_multi()` computes FFT bar values independently per visualizer. If many visualizers share the same `bar_count`, this is slightly redundant but the cost is negligible (FFT on ~1470 samples).
- Temp frames are written to `/tmp/visualizer_frames*`. The renderer cleans them up after encoding, but a crash may leave them behind.

## Testing

There is no test suite yet. Validate changes by:

1. Syntax check: `python -m py_compile src/visgen/*.py`
2. Import check: `python -c "from visgen import *"`
3. Run a minimal example from `main.py`

## Build

```bash
# Install in editable mode
pip install -e ".[dev]"

# The package is built with uv_build (see pyproject.toml)
```

## Dependencies

Runtime:
- `numpy` — FFT and array math
- `opencv-python` — Frame I/O (PNG writing)
- `Pillow` — Image compositing, text, effects

System:
- `ffmpeg` — Audio extraction, video encoding, audio muxing

## Notes for Agents

- **Do not** change `self.visualizer` alias behavior — external users may rely on it.
- **Do not** remove `render_quad_repeated_bars` or `render_quad_repeated_bars_multi_color` — these implement a unique single-circle algorithm that `render_multi` cannot replace.
- When adding examples to `main.py`, keep them self-contained and use `assets/` as the default asset directory.
- If you add new overlay types, remember to call `.release()` in `_release_overlays()` if they hold resources (like `VideoOverlay` does).
