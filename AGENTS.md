# AGENTS.md — VisGen Agent Guide

Context and conventions for AI agents working on the VisGen codebase.

## Project Overview

VisGen is a Python 3.10+ tool for generating audio-reactive visualizer videos. It extracts mono audio via FFmpeg, performs per-frame FFT analysis, and composites circular bar visualizers onto a canvas using PIL. Final output is H.264 video with AAC audio via FFmpeg.

## Architecture

### Module Map

| Module | Responsibility |
|--------|---------------|
| `audio.py` | `AudioProcessor` — extracts raw mono audio with FFmpeg, computes FFT bar values per frame with optional temporal smoothing. |
| `background.py` | `Background` ABC, `ColorBackground`, `ImageBackground`. Image backgrounds support resize modes (`cover`/`contain`/`stretch`) and chained effects (`blur`, `grayscale`, `sepia`). |
| `bars/base.py` | `BarEffect` ABC — pre-processing hook that mutates FFT bar values before visualizer rendering. |
| `bars/builtin.py` | Built-in bar effects: `BounceEffect`, `MirrorEffect`, `SmoothDecayEffect`. |
| `colors.py` | `ColorScheme` dataclass — holds palette values and `bar_with_intensity()`. |
| `effects/base.py` | `FrameEffect` ABC — post-processing hook applied to the final PIL frame before encoding. |
| `effects/builtin.py` | Built-in frame effects: `GlowEffect`, `VignetteEffect`, `ShakeEffect`, `ZoomPulseEffect`. |
| `overlay.py` | `TextOverlay` & `TimedText` (dataclasses), `BaseOverlay` ABC, `ImageOverlay`, `VideoOverlay`. Non-text overlays implement `draw(canvas, current_time, fps)`. |
| `plugins/base.py` | `Plugin` ABC, `PluginMeta`, `PluginRegistry` — central registry for backgrounds, overlays, visualizers, frame effects, bar effects, and plugin instances. |
| `plugins/loader.py` | `discover_plugins()` and `load_plugins()` — scans `~/.visgen/plugins/` for `Plugin` subclasses, instantiates them, and auto-registers any attached effect classes. |
| `renderer.py` | `AudioVisualizerVideo` — orchestrates the full pipeline: frame loop → background → bar effects → visualizer(s) → overlays → frame effects → encode → mux. |
| `utils.py` | `get_font()` (TTF fallback chain), `resolve_position()` (named string → pixel coordinates). |
| `visualizer.py` | `CircularVisualizer` — loads a circular-masked center image and renders FFT bars with glow + border ring. |

### Design Decisions

1. **Temp PNG frame sequence** — Each frame is written to `/tmp/visualizer_frames*/` as a PNG, then FFmpeg encodes the sequence. Simple, debuggable, avoids video codec bindings in Python.
2. **PIL for compositing, OpenCV only for saving** — PIL handles alpha blending, text, masks, and image pasting. OpenCV is used only for `cv2.imwrite` (BGR conversion).
3. **FFmpeg as external dependency** — Audio extraction, video encoding, and audio muxing all shell out to `ffmpeg`. Must be in `PATH`.
4. **Effect pipeline** — Bar effects run immediately after FFT (pre-render). Frame effects run after all overlays (post-render). Both are lists applied sequentially.
5. **Modular visualizers** — `CircularVisualizer` is self-contained. `AudioVisualizerVideo` accepts a list via `visualizers=` and `render_multi()` composites them together, each with independent `prev_bars` smoothing state.
6. **Backward compatibility** — `image_path` in `AudioVisualizerVideo.__init__` auto-creates a single `CircularVisualizer`. `self.visualizer` is kept as an alias to `self.visualizers[0]`.
7. **Plugin discovery** — `~/.visgen/plugins/*.py` files are dynamically imported at runtime. Plugins can expose effect classes as attributes for auto-registration.

## Code Conventions

- **Typing**: Python 3.10+ style. Use `|` unions (e.g., `str | None`), not `Optional` / `Union` in new code.
- **Formatting**: 4-space indents. Black-compatible.
- **Imports**: Standard library → third-party → local modules.
- **Naming**: `snake_case` functions/variables, `PascalCase` classes.
- **No hardcoded paths** in modules (except temp prefix `/tmp/visualizer_frames`).

## Extending VisGen

### Adding a Background

1. Subclass `Background` in `background.py`.
2. Implement `render(width, height, frame_idx) -> Image.Image`.
3. Pass to `AudioVisualizerVideo(background=...)`. No registration needed.

### Adding an Overlay

1. Subclass `BaseOverlay` in `overlay.py`.
2. Implement `draw(self, canvas, current_time, fps)`.
3. `AudioVisualizerVideo._draw_media_overlays()` will pick it up automatically via `isinstance(item, BaseOverlay)`.
4. If the overlay holds resources (like `VideoOverlay`), add cleanup in `_release_overlays()`.

### Adding a Frame Effect

1. Subclass `FrameEffect` in `effects/base.py` or a new module.
2. Implement `apply(self, frame, frame_idx, bar_values=None) -> Image.Image`.
3. If stateful, implement `reset()` to clear state at render start.
4. Pass to `AudioVisualizerVideo(frame_effects=[...])`.

### Adding a Bar Effect

1. Subclass `BarEffect` in `bars/base.py` or a new module.
2. Implement `process(self, bar_values, frame_idx, audio_chunk=None) -> np.ndarray`.
3. `audio_chunk` is the raw mono audio samples for the current frame.
4. If stateful, implement `reset()`.
5. Pass to `AudioVisualizerVideo(bar_effects=[...])`.

### Adding a Plugin

1. Subclass `Plugin` in `plugins/base.py`.
2. Define `meta = PluginMeta(name="...", version="...")`.
3. Optionally implement `initialize(config)` and `shutdown()`.
4. Drop the `.py` file in `~/.visgen/plugins/`. It will be auto-discovered by `load_plugins()`.
5. Expose effect classes as class attributes for auto-registration.

## Testing

No test suite exists. Validate changes by:

```bash
# Syntax check all modules
python -m py_compile src/visgen/*.py src/visgen/*/*.py

# Import check
python -c "from visgen import *"

# Run a minimal example
python -c "from visgen.main import example_01_minimal; example_01_minimal()"
```

## Build

```bash
pip install -e ".[dev]"
```

Built with `uv_build` (see `pyproject.toml`).

## Dependencies

| Type | Package | Purpose |
|------|---------|---------|
| Runtime | `numpy` | FFT, array math |
| Runtime | `opencv-python` | Frame I/O (PNG writing) |
| Runtime | `Pillow` | Image compositing, text, effects |
| System | `ffmpeg` | Audio extraction, video encoding, audio muxing |

## Agent Notes

- **Do not** remove or change the `self.visualizer` alias behavior — external users may rely on it.
- **Do not** remove `render_quad_repeated_bars` or `render_quad_repeated_bars_multi_color` — they implement a unique single-circle algorithm that `render_multi` cannot replace.
- When adding examples to `main.py`, define them as standalone functions (`def example_NN_name() -> None:`) and add them to the `EXAMPLES` list at the bottom.
- When adding new overlay types that hold resources, remember to call `.release()` in `_release_overlays()`.
- The `BarEffect.process` signature includes `audio_chunk`. Make sure renderer.py fetches `self.audio.get_chunk(frame_idx)` and passes it through.
- `ImageBackground.effect` accepts `str | list[str]` for chained effects. Keep the loop in `render()` sequential.
