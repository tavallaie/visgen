import numpy as np
from PIL import Image, ImageFilter
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Literal, Union, List


class Background(ABC):
    """Base class for video backgrounds."""

    @abstractmethod
    def render(self, width: int, height: int, frame_idx: int = 0) -> Image.Image:
        """Return a PIL Image for the given frame size."""
        ...


class ColorBackground(Background):
    """Solid color background."""

    def __init__(self, color: Tuple[int, int, int] = (10, 10, 20)):
        self.color = color

    def render(self, width: int, height: int, frame_idx: int = 0) -> Image.Image:
        frame = np.full((height, width, 3), self.color, dtype=np.uint8)
        return Image.fromarray(frame)


class ImageBackground(Background):
    """Image background with optional effects (blur, grayscale, sepia)."""

    def __init__(
        self,
        image_path: str,
        effect: Optional[Union[Literal["blur", "grayscale", "sepia"], List[Literal["blur", "grayscale", "sepia"]]]] = None,
        blur_radius: float = 5.0,
        opacity: float = 1.0,
        fit_mode: Literal["cover", "contain", "stretch"] = "cover",
    ):
        self.image_path = image_path
        self.effect = effect
        self.blur_radius = blur_radius
        self.opacity = max(0.0, min(1.0, opacity))
        self.fit_mode = fit_mode
        self._source: Optional[Image.Image] = None

    def _load_source(self) -> Image.Image:
        if self._source is None:
            self._source = Image.open(self.image_path).convert("RGB")
        return self._source

    def _resize(self, width: int, height: int) -> Image.Image:
        img = self._load_source()
        src_w, src_h = img.size

        if self.fit_mode == "stretch":
            return img.resize((width, height), Image.LANCZOS)

        if self.fit_mode == "contain":
            scale = min(width / src_w, height / src_h)
            new_w, new_h = int(src_w * scale), int(src_h * scale)
            resized = img.resize((new_w, new_h), Image.LANCZOS)
            canvas = Image.new("RGB", (width, height), (0, 0, 0))
            canvas.paste(resized, ((width - new_w) // 2, (height - new_h) // 2))
            return canvas

        # cover
        scale = max(width / src_w, height / src_h)
        new_w, new_h = int(src_w * scale), int(src_h * scale)
        resized = img.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - width) // 2
        top = (new_h - height) // 2
        return resized.crop((left, top, left + width, top + height))

    def _apply_sepia(self, img: Image.Image) -> Image.Image:
        pixels = np.array(img.convert("RGB"), dtype=np.float32)
        tr = pixels[:, :, 0] * 0.393 + pixels[:, :, 1] * 0.769 + pixels[:, :, 2] * 0.189
        tg = pixels[:, :, 0] * 0.349 + pixels[:, :, 1] * 0.686 + pixels[:, :, 2] * 0.168
        tb = pixels[:, :, 0] * 0.272 + pixels[:, :, 1] * 0.534 + pixels[:, :, 2] * 0.131
        sepia_pixels = np.stack([tr, tg, tb], axis=2).clip(0, 255).astype(np.uint8)
        return Image.fromarray(sepia_pixels)

    def render(self, width: int, height: int, frame_idx: int = 0) -> Image.Image:
        img = self._resize(width, height)

        effects = [self.effect] if isinstance(self.effect, str) else (self.effect or [])
        for eff in effects:
            if eff == "blur":
                img = img.filter(ImageFilter.GaussianBlur(radius=self.blur_radius))
            elif eff == "grayscale":
                img = img.convert("L").convert("RGB")
            elif eff == "sepia":
                img = self._apply_sepia(img)

        if self.opacity < 1.0:
            img = img.convert("RGBA")
            alpha = img.getchannel("A")
            alpha = alpha.point(lambda p: int(p * self.opacity))
            img.putalpha(alpha)
            bg = Image.new("RGBA", (width, height), (0, 0, 0, 255))
            img = Image.alpha_composite(bg, img).convert("RGB")

        return img
