from dataclasses import dataclass
from typing import Tuple


@dataclass
class ColorScheme:
    """Color configuration for all visualizer parts."""

    bg: Tuple[int, int, int] = (10, 10, 20)
    bar: Tuple[int, int, int] = (0, 200, 255)
    bar_glow: Tuple[int, int, int] = (0, 200, 255)
    circle_border: Tuple[int, int, int] = (100, 100, 120)
    divider: Tuple[int, int, int] = (40, 40, 60)
    cross: Tuple[int, int, int] = (60, 60, 80)

    def bar_with_intensity(self, intensity: float) -> Tuple[int, int, int]:
        """Get bar color scaled by intensity."""
        return tuple(int(c * (0.3 + 0.7 * intensity)) for c in self.bar)
