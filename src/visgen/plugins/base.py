"""Plugin base classes and registry for VisGen."""

from abc import ABC
from dataclasses import dataclass, field
from typing import Callable, TypeVar

from ..background import Background
from ..overlay import BaseOverlay


T = TypeVar("T")


@dataclass
class PluginMeta:
    """Metadata describing a plugin."""

    name: str
    version: str
    author: str = ""
    description: str = ""


class Plugin(ABC):
    """Base class for all VisGen plugins."""

    meta: PluginMeta

    def initialize(self, config: dict | None = None) -> None:
        """Called once when the plugin is loaded."""
        pass

    def shutdown(self) -> None:
        """Called once when the application exits."""
        pass


class PluginRegistry:
    """Central registry for all VisGen extensions."""

    def __init__(self) -> None:
        self._backgrounds: dict[str, type[Background]] = {}
        self._overlays: dict[str, type[BaseOverlay]] = {}
        self._visualizers: dict[str, type] = {}
        self._frame_effects: dict[str, type] = {}
        self._bar_effects: dict[str, type] = {}
        self._plugins: dict[str, Plugin] = {}

    # -- Registration --

    def register_background(self, name: str, cls: type[Background]) -> None:
        self._backgrounds[name] = cls

    def register_overlay(self, name: str, cls: type[BaseOverlay]) -> None:
        self._overlays[name] = cls

    def register_visualizer(self, name: str, cls: type) -> None:
        self._visualizers[name] = cls

    def register_frame_effect(self, name: str, cls: type) -> None:
        self._frame_effects[name] = cls

    def register_bar_effect(self, name: str, cls: type) -> None:
        self._bar_effects[name] = cls

    def register_plugin(self, plugin: Plugin) -> None:
        self._plugins[plugin.meta.name] = plugin

    # -- Retrieval --

    def get_background(self, name: str) -> type[Background] | None:
        return self._backgrounds.get(name)

    def get_overlay(self, name: str) -> type[BaseOverlay] | None:
        return self._overlays.get(name)

    def get_visualizer(self, name: str) -> type | None:
        return self._visualizers.get(name)

    def get_frame_effect(self, name: str) -> type | None:
        return self._frame_effects.get(name)

    def get_bar_effect(self, name: str) -> type | None:
        return self._bar_effects.get(name)

    def get_plugin(self, name: str) -> Plugin | None:
        return self._plugins.get(name)

    # -- Listing --

    @property
    def backgrounds(self) -> dict[str, type[Background]]:
        return dict(self._backgrounds)

    @property
    def overlays(self) -> dict[str, type[BaseOverlay]]:
        return dict(self._overlays)

    @property
    def visualizers(self) -> dict[str, type]:
        return dict(self._visualizers)

    @property
    def frame_effects(self) -> dict[str, type]:
        return dict(self._frame_effects)

    @property
    def bar_effects(self) -> dict[str, type]:
        return dict(self._bar_effects)

    @property
    def plugins(self) -> dict[str, Plugin]:
        return dict(self._plugins)

    # -- Factory helpers --

    def create_background(self, name: str, **kwargs) -> Background | None:
        cls = self._backgrounds.get(name)
        return cls(**kwargs) if cls else None

    def create_frame_effect(self, name: str, **kwargs):
        cls = self._frame_effects.get(name)
        return cls(**kwargs) if cls else None

    def create_bar_effect(self, name: str, **kwargs):
        cls = self._bar_effects.get(name)
        return cls(**kwargs) if cls else None


# Global registry instance
registry = PluginRegistry()
