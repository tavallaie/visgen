import numpy as np
from PIL import Image, ImageDraw
from typing import Optional

from .colors import ColorScheme


class CircularVisualizer:
    """Renders a single circular audio visualizer."""

    def __init__(
        self,
        image_path: str,
        circle_radius: int = 150,
        bar_count: int = 64,
        bar_max_length: int = 200,
        gap: int = 25,
        colors: Optional[ColorScheme] = None,
    ):
        self.circle_radius = circle_radius
        self.bar_count = bar_count
        self.bar_max_length = bar_max_length
        self.gap = gap
        self.colors = colors or ColorScheme()
        self.image = self._load_circle_image(image_path)
        self.inner_radius = circle_radius + gap

    def _load_circle_image(self, image_path: str) -> Image.Image:
        """Load and mask image into a circle."""
        img = Image.open(image_path).convert("RGBA")
        size = self.circle_radius * 2
        img = img.resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)
        return img

    def render(
        self,
        canvas: Image.Image,
        center_x: int,
        center_y: int,
        bar_values: np.ndarray,
        frame_idx: int = 0,
        phase_offset: float = 0.0,
        animated: bool = True,
    ) -> None:
        """Draw the visualizer onto an existing canvas."""
        draw = ImageDraw.Draw(canvas)

        for i in range(self.bar_count):
            angle = (2 * np.pi * i / self.bar_count) - (np.pi / 2) + phase_offset

            val = bar_values[i]
            if animated:
                val *= 0.7 + 0.3 * np.sin(frame_idx * 0.05 + i * 0.1)

            bar_length = val * self.bar_max_length

            x1 = center_x + self.inner_radius * np.cos(angle)
            y1 = center_y + self.inner_radius * np.sin(angle)
            x2 = center_x + (self.inner_radius + bar_length) * np.cos(angle)
            y2 = center_y + (self.inner_radius + bar_length) * np.sin(angle)

            intensity = val
            r, g, b = self.colors.bar_with_intensity(intensity)

            bar_width = max(2, int(8 * (1 - 0.3 * intensity)))
            draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=bar_width)

            # Glow at bar end
            glow_radius = int(3 + 5 * intensity)
            gx, gy = int(x2), int(y2)
            for gr in range(glow_radius, 0, -1):
                alpha = int(50 * (1 - gr / glow_radius) * intensity)
                if alpha > 5:
                    bbox = (gx - gr, gy - gr, gx + gr, gy + gr)
                    draw.ellipse(bbox, fill=(r, g, b, alpha))

        # Paste circular image
        img_pos = (center_x - self.circle_radius, center_y - self.circle_radius)
        canvas.paste(self.image, img_pos, self.image)

        # Border ring
        bw = 4
        bbox = (
            center_x - self.circle_radius - bw,
            center_y - self.circle_radius - bw,
            center_x + self.circle_radius + bw,
            center_y + self.circle_radius + bw,
        )
        draw.ellipse(bbox, outline=self.colors.circle_border, width=bw)
