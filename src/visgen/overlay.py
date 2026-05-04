from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Optional
import cv2
from PIL import Image

from .utils import open_image


@dataclass
class TextOverlay:
    """Static text that appears for the entire video."""

    text: str
    position: Tuple[int, int]
    color: Tuple[int, int, int] = (255, 255, 255)
    font_size: int = 40
    font_path: Optional[str] = None
    anchor: str = "mm"
    bg_color: Optional[Tuple[int, int, int]] = None
    bg_padding: int = 10
    bg_radius: int = 0


@dataclass
class TimedText:
    """Text that appears only during a specific time range (seconds)."""

    start_time: float
    end_time: float
    text: str
    position: Tuple[int, int]
    color: Tuple[int, int, int] = (255, 255, 255)
    font_size: int = 40
    font_path: Optional[str] = None
    anchor: str = "mm"
    bg_color: Optional[Tuple[int, int, int]] = None
    bg_padding: int = 10
    bg_radius: int = 0


class BaseOverlay(ABC):
    """Base class for image/video overlays with optional time range."""

    def __init__(
        self,
        position: Tuple[int, int],
        size: Optional[Tuple[int, int]] = None,
        opacity: float = 1.0,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        anchor: str = "mm",
    ):
        self.position = position
        self.size = size
        self.opacity = max(0.0, min(1.0, opacity))
        self.start_time = start_time
        self.end_time = end_time
        self.anchor = anchor

    def is_visible(self, current_time: float) -> bool:
        if self.start_time is not None and current_time < self.start_time:
            return False
        if self.end_time is not None and current_time > self.end_time:
            return False
        return True

    @abstractmethod
    def draw(self, canvas: Image.Image, current_time: float, fps: int) -> None:
        ...

    def _paste(self, canvas: Image.Image, img: Image.Image) -> None:
        """Paste image onto canvas respecting anchor."""
        x, y = self.position
        if self.anchor == "mm":
            x -= img.width // 2
            y -= img.height // 2
        elif self.anchor == "lt":
            pass
        elif self.anchor == "rb":
            x -= img.width
            y -= img.height
        elif self.anchor == "lb":
            y -= img.height
        elif self.anchor == "rt":
            x -= img.width
        canvas.paste(img, (x, y), img if img.mode == "RGBA" else None)


class ImageOverlay(BaseOverlay):
    """Image overlay with optional time range and opacity."""

    def __init__(
        self,
        image_path: str,
        position: Tuple[int, int],
        size: Optional[Tuple[int, int]] = None,
        opacity: float = 1.0,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        anchor: str = "mm",
    ):
        super().__init__(position, size, opacity, start_time, end_time, anchor)
        self.image_path = image_path
        self._image: Optional[Image.Image] = None

    def _get_image(self) -> Image.Image:
        if self._image is None:
            img = open_image(self.image_path, "RGBA")
            if self.size:
                img = img.resize(self.size, Image.LANCZOS)
            if self.opacity < 1.0:
                alpha = img.getchannel("A")
                alpha = alpha.point(lambda p: int(p * self.opacity))
                img.putalpha(alpha)
            self._image = img
        return self._image

    def draw(self, canvas: Image.Image, current_time: float, fps: int) -> None:
        if not self.is_visible(current_time):
            return
        img = self._get_image()
        self._paste(canvas, img)


class VideoOverlay(BaseOverlay):
    """Video overlay with optional time range, opacity, and looping."""

    def __init__(
        self,
        video_path: str,
        position: Tuple[int, int],
        size: Optional[Tuple[int, int]] = None,
        opacity: float = 1.0,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        anchor: str = "mm",
        loop: bool = False,
    ):
        super().__init__(position, size, opacity, start_time, end_time, anchor)
        self.video_path = video_path
        self.loop = loop
        self._cap: Optional[cv2.VideoCapture] = None
        self._video_fps: float = 30.0
        self._total_frames: int = 0
        self._cached_frame: Optional[Image.Image] = None
        self._cached_idx: int = -1

    def _get_cap(self) -> cv2.VideoCapture:
        if self._cap is None:
            self._cap = cv2.VideoCapture(self.video_path)
            self._video_fps = self._cap.get(cv2.CAP_PROP_FPS) or 30.0
            self._total_frames = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return self._cap

    def _get_frame(self, current_time: float) -> Optional[Image.Image]:
        cap = self._get_cap()
        if not cap.isOpened():
            return None

        overlay_time = current_time
        if self.start_time is not None:
            overlay_time = current_time - self.start_time

        if overlay_time < 0:
            return None

        frame_idx = int(overlay_time * self._video_fps)

        if self.loop and self._total_frames > 0:
            frame_idx = frame_idx % self._total_frames

        if not self.loop and frame_idx >= self._total_frames:
            return None

        if self._cached_idx == frame_idx and self._cached_frame is not None:
            return self._cached_frame

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            return None

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(frame)
        if self.size:
            img = img.resize(self.size, Image.LANCZOS)
        if self.opacity < 1.0:
            alpha = img.getchannel("A")
            alpha = alpha.point(lambda p: int(p * self.opacity))
            img.putalpha(alpha)

        self._cached_frame = img
        self._cached_idx = frame_idx
        return img

    def draw(self, canvas: Image.Image, current_time: float, fps: int) -> None:
        if not self.is_visible(current_time):
            return
        img = self._get_frame(current_time)
        if img is None:
            return
        self._paste(canvas, img)

    def release(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None
