from .audio import AudioProcessor
from .background import Background, ColorBackground, ImageBackground
from .colors import ColorScheme
from .overlay import BaseOverlay, ImageOverlay, TextOverlay, TimedText, VideoOverlay
from .renderer import AudioVisualizerVideo
from .utils import resolve_position
from .visualizer import CircularVisualizer

__all__ = [
    "AudioProcessor",
    "Background",
    "ColorBackground",
    "ImageBackground",
    "ColorScheme",
    "BaseOverlay",
    "ImageOverlay",
    "TextOverlay",
    "TimedText",
    "VideoOverlay",
    "AudioVisualizerVideo",
    "resolve_position",
    "CircularVisualizer",
]


def main() -> None:
    print("Hello from visgen! Use AudioVisualizerVideo to create visualizer videos.")
