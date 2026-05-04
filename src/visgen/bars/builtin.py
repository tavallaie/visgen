"""Built-in bar effects for VisGen."""

import numpy as np

from .base import BarEffect


class BounceEffect(BarEffect):
    """Add a sinusoidal bounce to bars for extra liveliness."""

    def __init__(self, speed: float = 0.1, amplitude: float = 0.15):
        self.speed = speed
        self.amplitude = amplitude

    def process(
        self,
        bar_values: np.ndarray,
        frame_idx: int,
        audio_chunk: np.ndarray | None = None,
    ) -> np.ndarray:
        bounce = 1.0 + self.amplitude * np.sin(frame_idx * self.speed)
        return bar_values * bounce


class MirrorEffect(BarEffect):
    """Mirror the right half of bars from the left half."""

    def process(
        self,
        bar_values: np.ndarray,
        frame_idx: int,
        audio_chunk: np.ndarray | None = None,
    ) -> np.ndarray:
        n = len(bar_values)
        half = n // 2
        mirrored = bar_values.copy()
        mirrored[half:] = mirrored[:half][::-1]
        return mirrored


class SmoothDecayEffect(BarEffect):
    """Additional exponential decay on bar fall-off."""

    def __init__(self, decay: float = 0.85):
        self.decay = decay
        self._peak: np.ndarray | None = None

    def reset(self) -> None:
        self._peak = None

    def process(
        self,
        bar_values: np.ndarray,
        frame_idx: int,
        audio_chunk: np.ndarray | None = None,
    ) -> np.ndarray:
        if self._peak is None:
            self._peak = bar_values.copy()
        self._peak = np.maximum(bar_values, self._peak * self.decay)
        return self._peak
