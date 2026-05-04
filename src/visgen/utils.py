import io
import os
from typing import Tuple, Union
from PIL import Image, ImageFont


Position = Union[Tuple[int, int], str]


def _is_svg(path: str) -> bool:
    """Peek at file header to detect SVG/XML content."""
    try:
        with open(path, "rb") as f:
            header = f.read(512)
    except Exception:
        return False
    # SVG may start with XML declaration or whitespace, then <svg
    return b"<svg" in header or b"<SVG" in header


def _load_svg(path: str, mode: str) -> Image.Image:
    """Rasterise an SVG to a PIL Image via CairoSVG."""
    try:
        import cairosvg
    except ImportError as exc:
        raise RuntimeError(
            "SVG support requires 'cairosvg'. Install it with: uv pip install cairosvg"
        ) from exc
    png_data = cairosvg.svg2png(url=path)
    return Image.open(io.BytesIO(png_data)).convert(mode)


def open_image(path: str, mode: str = "RGBA") -> Image.Image:
    """Open an image file. Supports all PIL formats plus SVG via CairoSVG."""
    # Fast path: explicit SVG extension
    if path.lower().endswith(".svg"):
        return _load_svg(path, mode)

    # Fast path: let PIL handle regular raster images (PNG, JPG, WEBP, GIF, BMP, …)
    try:
        return Image.open(path).convert(mode)
    except Exception:
        # If PIL chokes, check whether the file is actually an SVG with a wrong/missing extension
        if _is_svg(path):
            return _load_svg(path, mode)
        raise


def get_font(font_path: str | None, font_size: int):
    """Load a TrueType font or fall back to default."""
    if font_path and os.path.exists(font_path):
        return ImageFont.truetype(font_path, font_size)
    for fallback in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]:
        if os.path.exists(fallback):
            return ImageFont.truetype(fallback, font_size)
    return ImageFont.load_default()


def resolve_position(
    position: Position,
    canvas_width: int,
    canvas_height: int,
    obj_width: int = 0,
    obj_height: int = 0,
) -> Tuple[int, int]:
    """Resolve a position string or tuple to absolute (x, y) coordinates.

    Supported strings:
        "center", "top-left", "top-right", "bottom-left", "bottom-right",
        "top-center", "bottom-center", "left-center", "right-center"
    """
    if isinstance(position, tuple):
        return position

    pos = position.lower().replace("_", "-")
    w, h = canvas_width, canvas_height
    ow, oh = obj_width, obj_height

    if pos == "center":
        return (w // 2, h // 2)
    elif pos in ("top-left", "tl"):
        return (0, 0)
    elif pos in ("top-right", "tr"):
        return (w - ow, 0)
    elif pos in ("bottom-left", "bl"):
        return (0, h - oh)
    elif pos in ("bottom-right", "br"):
        return (w - ow, h - oh)
    elif pos in ("top-center", "tc"):
        return (w // 2, 0)
    elif pos in ("bottom-center", "bc"):
        return (w // 2, h - oh)
    elif pos in ("left-center", "lc"):
        return (0, h // 2)
    elif pos in ("right-center", "rc"):
        return (w - ow, h // 2)
    else:
        raise ValueError(f"Unknown position: {position}")
