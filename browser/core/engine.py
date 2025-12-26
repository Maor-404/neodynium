"""
BrowserEngine
-------------
This module contains the core logic for Neodynium.

The BrowserEngine is responsible for:
- URL normalization
- Homepage logic
- Search engine handling (future)
- Integration with settings
- Providing hooks for extensions
- Acting as a central logic layer between the UI and the browser backend
"""

import re
import logging
import json
import os


class BrowserEngine:
    """
    The central logic engine for Neodynium.
    This class does not handle UI — only logic and decisions.
    """

    def __init__(self, settings: dict | None = None):
        """
        Initialize the engine with optional settings.
        If settings are missing, defaults are used.
        """
        self.settings = settings or {
            "homepage": "https://www.google.com",
            "search_engine": "google",
            "theme": "light"
        }

        # Predefined search engines (expandable)
        self.search_engines = {
            "google": "https://www.google.com/search?q={query}",
            "duckduckgo": "https://duckduckgo.com/?q={query}",
            "bing": "https://www.bing.com/search?q={query}"
        }

        logging.info("BrowserEngine initialized with settings: %s", self.settings)

        # Initialize bookmarks and history
        self.bookmarks = []
        self.history = []
        self.load_bookmarks()
        self.load_history()

    # ------------------------------------------------------------
    # Homepage
    # ------------------------------------------------------------

    def get_home_url(self) -> str:
        """
        Returns the homepage URL from settings.
        """
        return self.settings.get("homepage", "https://www.google.com")

    # ------------------------------------------------------------
    # URL Normalization
    # ------------------------------------------------------------

    def normalize_url(self, text: str) -> str:
        """
        Converts user input into a valid URL.
        Handles:
        - Missing protocol
        - Search queries
        - Raw domains
        - IP addresses
        - Localhost
        """

        text = text.strip()
        logging.info("Normalizing URL: %s", text)

        # If it already looks like a URL with protocol
        if text.startswith(("http://", "https://")):
            return text

        # If it's a localhost or IP address
        if re.match(r"^(localhost|\d{1,3}(\.\d{1,3}){3})(:\d+)?$", text):
            return f"http://{text}"

        # If it looks like a domain
        if "." in text and " " not in text:
            return f"https://{text}"

        # Otherwise treat it as a search query
        return self.build_search_url(text)

    # ------------------------------------------------------------
    # Search Engine Logic
    # ------------------------------------------------------------

    def build_search_url(self, query: str) -> str:
        """
        Builds a search URL using the selected search engine.
        """
        engine = self.settings.get("search_engine", "google")

        if engine not in self.search_engines:
            logging.warning("Unknown search engine '%s', falling back to Google", engine)
            engine = "google"

        template = self.search_engines[engine]
        url = template.format(query=query.replace(" ", "+"))

        logging.info("Search URL built: %s", url)
        return url

    # ------------------------------------------------------------
    # Bookmarks Management
    # ------------------------------------------------------------

    def add_bookmark(self, url: str, title: str):
        """
        Adds a bookmark.
        """
        if not any(b['url'] == url for b in self.bookmarks):
            self.bookmarks.append({'url': url, 'title': title})
            self.save_bookmarks()
            logging.info("Bookmark added: %s", title)

    def remove_bookmark(self, url: str):
        """
        Removes a bookmark.
        """
        self.bookmarks = [b for b in self.bookmarks if b['url'] != url]
        self.save_bookmarks()
        logging.info("Bookmark removed: %s", url)

    def get_bookmarks(self):
        """
        Returns the list of bookmarks.
        """
        return self.bookmarks

    def load_bookmarks(self):
        """
        Loads bookmarks from file.
        """
        bookmarks_file = os.path.join(os.path.expanduser("~"), ".neodynium", "bookmarks.json")
        if os.path.exists(bookmarks_file):
            try:
                with open(bookmarks_file, 'r') as f:
                    self.bookmarks = json.load(f)
            except Exception as e:
                logging.error("Failed to load bookmarks: %s", e)

    def save_bookmarks(self):
        """
        Saves bookmarks to file.
        """
        bookmarks_file = os.path.join(os.path.expanduser("~"), ".neodynium", "bookmarks.json")
        os.makedirs(os.path.dirname(bookmarks_file), exist_ok=True)
        try:
            with open(bookmarks_file, 'w') as f:
                json.dump(self.bookmarks, f)
        except Exception as e:
            logging.error("Failed to save bookmarks: %s", e)

    # ------------------------------------------------------------
    # History Management
    # ------------------------------------------------------------

    def add_to_history(self, url: str):
        """
        Adds a URL to history.
        """
        if not self.history or self.history[-1] != url:
            self.history.append(url)
            if len(self.history) > 100:  # Limit history size
                self.history.pop(0)
            self.save_history()
            logging.info("Added to history: %s", url)

    def get_history(self):
        """
        Returns the browsing history.
        """
        return self.history

    def clear_history(self):
        """
        Clears the browsing history.
        """
        self.history = []
        self.save_history()
        logging.info("History cleared")

    def load_history(self):
        """
        Loads history from file.
        """
        history_file = os.path.join(os.path.expanduser("~"), ".neodynium", "history.json")
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    self.history = json.load(f)
            except Exception as e:
                logging.error("Failed to load history: %s", e)

    def save_history(self):
        """
        Saves history to file.
        """
        history_file = os.path.join(os.path.expanduser("~"), ".neodynium", "history.json")
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        try:
            with open(history_file, 'w') as f:
                json.dump(self.history, f)
        except Exception as e:
            logging.error("Failed to save history: %s", e)

    # ------------------------------------------------------------
    # Extension Hooks
    # ------------------------------------------------------------

    def apply_extension_hooks(self, url: str) -> str:
        """
        Applies extension-based URL rewriting.
        Extensions can modify URLs before loading.
        """
        # This will be implemented when extensions are loaded
        return url
