"""Base class for bar-value effects."""

from abc import ABC, abstractmethod

import numpy as np


class BarEffect(ABC):
    """An effect that modifies FFT bar values before rendering."""

    @abstractmethod
    def process(
        self,
        bar_values: np.ndarray,
        frame_idx: int,
        audio_chunk: np.ndarray | None = None,
    ) -> np.ndarray:
        """Process and return modified bar values."""
        ...

    def reset(self) -> None:
        """Called at the start of a new render."""
        pass
