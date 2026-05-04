from .audio import AudioProcessor
from .background import Background, ColorBackground, ImageBackground
from .bars import BarEffect, BounceEffect, MirrorEffect, SmoothDecayEffect
from .colors import ColorScheme
from .effects import FrameEffect, GlowEffect, VignetteEffect, ShakeEffect, ZoomPulseEffect
from .overlay import BaseOverlay, ImageOverlay, TextOverlay, TimedText, VideoOverlay
from .plugins import Plugin, PluginMeta, PluginRegistry, load_plugins, discover_plugins
from .renderer import AudioVisualizerVideo
from .utils import resolve_position
from .visualizer import CircularVisualizer

__all__ = [
    "AudioProcessor",
    "Background",
    "ColorBackground",
    "ImageBackground",
    "BarEffect",
    "BounceEffect",
    "MirrorEffect",
    "SmoothDecayEffect",
    "ColorScheme",
    "FrameEffect",
    "GlowEffect",
    "VignetteEffect",
    "ShakeEffect",
    "ZoomPulseEffect",
    "BaseOverlay",
    "ImageOverlay",
    "TextOverlay",
    "TimedText",
    "VideoOverlay",
    "Plugin",
    "PluginMeta",
    "PluginRegistry",
    "load_plugins",
    "discover_plugins",
    "AudioVisualizerVideo",
    "resolve_position",
    "CircularVisualizer",
]


def main() -> None:
    print("Hello from visgen! Use AudioVisualizerVideo to create visualizer videos.")
