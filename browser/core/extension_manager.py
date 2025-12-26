"""
ExtensionManager
----------------
Handles loading, managing, and interacting with browser extensions.

Extensions live in:
    browser/extensions/<extension_name>/

Each extension must contain:
    extension.py  -> defines a class named Extension

This manager dynamically imports and initializes them.
"""

import os
import importlib
import logging


class ExtensionManager:
    """
    Manages extensions for Neodynium Browser.
    """

    def __init__(self, window):
        self.window = window
        self.extensions = []
        self.extensions_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "extensions"
        )

        logging.info("ExtensionManager initialized. Path: %s", self.extensions_path)

    # ------------------------------------------------------------
    # Extension Loading
    # ------------------------------------------------------------

    def load_extensions(self):
        """
        Loads all extensions from the extensions folder.
        """
        if not os.path.exists(self.extensions_path):
            logging.warning("Extensions folder missing: %s", self.extensions_path)
            return

        for folder in os.listdir(self.extensions_path):
            ext_dir = os.path.join(self.extensions_path, folder)
            ext_file = os.path.join(ext_dir, "extension.py")

            if not os.path.isdir(ext_dir):
                continue
            if not os.path.exists(ext_file):
                continue

            module_name = f"browser.extensions.{folder}.extension"

            try:
                module = importlib.import_module(module_name)
                if not hasattr(module, "Extension"):
                    logging.error("Extension '%s' missing Extension class", folder)
                    continue

                ext_class = module.Extension
                ext_instance = ext_class(self.window)

                self.extensions.append(ext_instance)
                logging.info("Loaded extension: %s", folder)

                # Call optional hook
                if hasattr(ext_instance, "on_load"):
                    ext_instance.on_load()

            except Exception as e:
                logging.error("Failed to load extension '%s': %s", folder, e)

    # ------------------------------------------------------------
    # Hooks for future features
    # ------------------------------------------------------------

    def apply_url_hooks(self, url: str) -> str:
        """
        Allows extensions to modify URLs before loading.
        """
        for ext in self.extensions:
            if hasattr(ext, "rewrite_url"):
                try:
                    url = ext.rewrite_url(url)
                except Exception as e:
                    logging.error("Extension URL hook failed: %s", e)
        return url

    def apply_engine_hooks(self, url: str) -> str:
        """
        Applies engine-level hooks for URL modification.
        """
        # Placeholder for engine hooks
        return url

    def notify_page_loaded(self, url: str):
        """
        Called when a page finishes loading.
        """
        for ext in self.extensions:
            if hasattr(ext, "on_page_load"):
                try:
                    ext.on_page_load(url)
                except Exception as e:
                    logging.error("Extension on_page_load failed: %s", e)