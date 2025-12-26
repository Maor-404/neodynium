"""
Neodynium - Main Entry Point
----------------------------
This file launches the browser, initializes the application environment,
sets up logging, loads settings, and creates the main window.

This is the central startup script for the entire project.
"""

import sys
import os
import json
import logging
from datetime import datetime

from PyQt5.QtWidgets import QApplication
from browser.core.window import BrowserWindow


# ------------------------------------------------------------
# 1. Paths & Environment Setup
# ------------------------------------------------------------

def get_appdata_root() -> str:
    """
    Returns the AppData path for Neodynium Browser.
    The installer will create this folder; we only reference it here.
    """
    base = os.getenv("APPDATA")
    if not base:
        raise RuntimeError("APPDATA environment variable not found.")
    return os.path.join(base, "Neodynium Browser")


def ensure_runtime_environment():
    """
    Ensures that the runtime environment is valid.
    Does NOT create AppData folders — the installer handles that.
    Only checks for existence and warns if missing.
    """
    root = get_appdata_root()

    if not os.path.exists(root):
        print("[WARNING] AppData folder not found. "
            "This usually means the installer has not run yet.")
        print(f"Expected path: {root}")

    return root


# ------------------------------------------------------------
# 2. Logging Setup
# ------------------------------------------------------------

def setup_logging(appdata_root: str):
    """
    Sets up logging to AppData/logs/browser.log if available.
    If AppData is missing, logs to console only.
    """
    log_path = os.path.join(appdata_root, "logs", "browser.log")

    # Fallback if installer hasn't created the folder yet
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        print("[WARNING] Log directory missing. Logging to console only.")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )
        return

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info("=== Neodynium Started ===")
    logging.info(f"Timestamp: {datetime.now()}")


# ------------------------------------------------------------
# 3. Settings Loader
# ------------------------------------------------------------

def load_settings(appdata_root: str) -> dict:
    """
    Loads settings.json from the default profile.
    If missing, returns default settings.
    """
    settings_path = os.path.join(appdata_root, "profiles", "default", "settings.json")

    if not os.path.exists(settings_path):
        print("[INFO] No settings.json found. Using default settings.")
        return {
            "homepage": "https://www.google.com",
            "search_engine": "google",
            "theme": "light"
        }

    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load settings.json: {e}")
        return {}


# ------------------------------------------------------------
# 4. Application Startup
# ------------------------------------------------------------

def main():
    # Initialize Qt application
    app = QApplication(sys.argv)

    # Prepare environment
    appdata_root = ensure_runtime_environment()

    # Logging
    setup_logging(appdata_root)
    logging.info("Environment initialized.")

    # Load settings
    settings = load_settings(appdata_root)
    logging.info(f"Settings loaded: {settings}")

    # Create main window
    window = BrowserWindow()
    window.show()
    logging.info("Main window created.")

    # Start event loop
    exit_code = app.exec_()
    logging.info(f"Neodynium exited with code {exit_code}")
    sys.exit(exit_code)


# ------------------------------------------------------------
# 5. Entry Point
# ------------------------------------------------------------

if __name__ == "__main__":
    main()