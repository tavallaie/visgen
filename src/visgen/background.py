import cv2
import numpy as np
from PIL import Image, ImageFilter
from abc import ABC, abstractmethod

from .utils import open_image
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
            self._source = open_image(self.image_path, "RGB")
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


class VideoBackground(Background):
    """Video background with fit modes and optional looping."""

    def __init__(
        self,
        video_path: str,
        fit_mode: Literal["cover", "contain", "stretch"] = "cover",
        loop: bool = False,
        opacity: float = 1.0,
        fps: float = 30.0,
    ):
        self.video_path = video_path
        self.fit_mode = fit_mode
        self.loop = loop
        self.opacity = max(0.0, min(1.0, opacity))
        self.fps = fps
        self._cap: Optional[cv2.VideoCapture] = None
        self._video_fps: float = 30.0
        self._total_frames: int = 0
        self._width: int = 0
        self._height: int = 0

    def _get_cap(self) -> cv2.VideoCapture:
        if self._cap is None:
            self._cap = cv2.VideoCapture(self.video_path)
            self._video_fps = self._cap.get(cv2.CAP_PROP_FPS) or 30.0
            self._total_frames = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self._width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self._height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return self._cap

    def _resize(self, img: Image.Image, width: int, height: int) -> Image.Image:
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

    def render(self, width: int, height: int, frame_idx: int = 0) -> Image.Image:
        cap = self._get_cap()
        if not cap.isOpened():
            return Image.new("RGB", (width, height), (0, 0, 0))

        time = frame_idx / self.fps
        bg_frame_idx = int(time * self._video_fps)

        if self.loop and self._total_frames > 0:
            bg_frame_idx = bg_frame_idx % self._total_frames
        elif bg_frame_idx >= self._total_frames:
            bg_frame_idx = max(0, self._total_frames - 1)

        cap.set(cv2.CAP_PROP_POS_FRAMES, bg_frame_idx)
        ret, frame = cap.read()
        if not ret:
            return Image.new("RGB", (width, height), (0, 0, 0))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = self._resize(img, width, height)

        if self.opacity < 1.0:
            img = img.convert("RGBA")
            alpha = img.getchannel("A")
            alpha = alpha.point(lambda p: int(p * self.opacity))
            img.putalpha(alpha)
            bg = Image.new("RGBA", (width, height), (0, 0, 0, 255))
            img = Image.alpha_composite(bg, img).convert("RGB")

        return img

    def release(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None
