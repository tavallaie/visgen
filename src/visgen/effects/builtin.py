"""Built-in frame effects for VisGen."""

import numpy as np
from PIL import Image, ImageFilter, ImageDraw

from .base import FrameEffect


class GlowEffect(FrameEffect):
    """Add a soft glow overlay based on bar intensity."""

    def __init__(self, strength: float = 0.3, radius: float = 8.0):
        self.strength = strength
        self.radius = radius

    def apply(
        self,
        frame: Image.Image,
        frame_idx: int,
        bar_values: np.ndarray | None = None,
    ) -> Image.Image:
        if bar_values is None or len(bar_values) == 0:
            return frame
        intensity = float(np.mean(bar_values))
        if intensity < 0.1:
            return frame
        glow = frame.filter(ImageFilter.GaussianBlur(radius=self.radius))
        glow = Image.blend(frame, glow, self.strength * intensity)
        return glow


class VignetteEffect(FrameEffect):
    """Darken the corners of the frame."""

    def __init__(self, strength: float = 0.4, radius: float = 1.2):
        self.strength = strength
        self.radius = radius

    def apply(
        self,
        frame: Image.Image,
        frame_idx: int,
        bar_values: np.ndarray | None = None,
    ) -> Image.Image:
        w, h = frame.size
        # Create radial gradient mask
        x = np.linspace(-1, 1, w)
        y = np.linspace(-1, 1, h)
        xv, yv = np.meshgrid(x, y)
        dist = np.sqrt(xv**2 + yv**2) / self.radius
        mask = np.clip(1 - dist, 0, 1)
        mask = (mask * 255).astype(np.uint8)
        mask_img = Image.fromarray(mask, mode="L").resize((w, h), Image.LANCZOS)

        black = Image.new("RGB", (w, h), (0, 0, 0))
        vignette = Image.composite(frame, black, mask_img)
        return Image.blend(frame, vignette, self.strength)


class ShakeEffect(FrameEffect):
    """Shake the frame based on bass intensity."""

    def __init__(self, max_offset: int = 10, bass_bins: int = 8):
        self.max_offset = max_offset
        self.bass_bins = bass_bins

    def apply(
        self,
        frame: Image.Image,
        frame_idx: int,
        bar_values: np.ndarray | None = None,
    ) -> Image.Image:
        if bar_values is None or len(bar_values) == 0:
            return frame
        bass = float(np.mean(bar_values[: self.bass_bins]))
        if bass < 0.15:
            return frame
        dx = int(self.max_offset * bass * np.sin(frame_idx * 0.8))
        dy = int(self.max_offset * bass * np.cos(frame_idx * 0.6))
        return frame.transform(
            frame.size,
            Image.AFFINE,
            (1, 0, dx, 0, 1, dy),
            resample=Image.BILINEAR,
        )


class ZoomPulseEffect(FrameEffect):
    """Subtle zoom pulse tied to overall audio intensity."""

    def __init__(self, max_zoom: float = 0.05):
        self.max_zoom = max_zoom

    def apply(
        self,
        frame: Image.Image,
        frame_idx: int,
        bar_values: np.ndarray | None = None,
    ) -> Image.Image:
        if bar_values is None or len(bar_values) == 0:
            return frame
        intensity = float(np.mean(bar_values))
        zoom = 1.0 + self.max_zoom * intensity
        w, h = frame.size
        new_w, new_h = int(w * zoom), int(h * zoom)
        zoomed = frame.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - w) // 2
        top = (new_h - h) // 2
        return zoomed.crop((left, top, left + w, top + h))
