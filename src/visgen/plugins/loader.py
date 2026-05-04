"""Plugin discovery and loading for VisGen."""

import importlib.util
import os
import sys
from pathlib import Path
from typing import Iterator

from .base import Plugin, registry


def discover_plugins(path: str | Path | None = None) -> Iterator[type[Plugin]]:
    """Discover Plugin subclasses in a directory.

    Each `.py` file in the directory is imported and scanned for Plugin subclasses.
    """
    if path is None:
        path = Path.home() / ".visgen" / "plugins"
    path = Path(path)

    if not path.exists():
        return

    for file in path.glob("*.py"):
        if file.name.startswith("_"):
            continue
        module_name = f"visgen_user_plugin_{file.stem}"
        spec = importlib.util.spec_from_file_location(module_name, file)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, Plugin)
                and attr is not Plugin
            ):
                yield attr


def load_plugins(path: str | Path | None = None) -> list[Plugin]:
    """Discover, instantiate, and register all plugins from a directory."""
    loaded: list[Plugin] = []
    for cls in discover_plugins(path):
        try:
            instance = cls()
            instance.initialize()
            registry.register_plugin(instance)

            # If the plugin exposes effects via class attributes, auto-register them
            for attr_name in dir(instance):
                if attr_name.startswith("_"):
                    continue
                attr = getattr(instance, attr_name)
                if isinstance(attr, type):
                    from ..effects.base import FrameEffect
                    from ..bars.base import BarEffect

                    if issubclass(attr, FrameEffect) and attr is not FrameEffect:
                        registry.register_frame_effect(attr.__name__, attr)
                    elif issubclass(attr, BarEffect) and attr is not BarEffect:
                        registry.register_bar_effect(attr.__name__, attr)

            loaded.append(instance)
        except Exception as exc:
            print(f"[visgen] Failed to load plugin {cls.__name__}: {exc}")
    return loaded
