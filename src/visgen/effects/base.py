"""Base class for post-processing frame effects."""

from abc import ABC, abstractmethod

import numpy as np
from PIL import Image


class FrameEffect(ABC):
    """A post-processing effect applied to the final frame before encoding."""

    @abstractmethod
    def apply(
        self,
        frame: Image.Image,
        frame_idx: int,
        bar_values: np.ndarray | None = None,
    ) -> Image.Image:
        """Process and return the modified frame."""
        ...

    def reset(self) -> None:
        """Called at the start of a new render. Override if your effect has state."""
        pass
