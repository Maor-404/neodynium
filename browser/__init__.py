"""
Neodynium Package
-----------------
This package contains the core modules that power Neodynium Browser,
including the main window, engine, and extension manager.

This file exposes high-level imports so other modules can
import Neodynium components cleanly, e.g.:
    from browser import BrowserWindow

It also stores version information for the application.
"""

__version__ = "0.1.0"
__author__ = "Neodynium Community"
__description__ = "A lightweight, extensible Python-based web browser."

# Re-export key classes for cleaner imports
from .core.window import BrowserWindow
from .core.engine import BrowserEngine
from .core.extension_manager import ExtensionManager

__all__ = [
    "BrowserWindow",
    "BrowserEngine",
    "ExtensionManager",
    "__version__",
    "__author__",
    "__description__",
]