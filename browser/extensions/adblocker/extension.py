"""
AdBlocker Extension
-------------------
Blocks common ad domains by rewriting URLs.
"""

import logging


class Extension:
    def __init__(self, window):
        self.window = window
        self.ad_domains = [
            "ads.google.com",
            "doubleclick.net",
            "googlesyndication.com",
            "amazon-adsystem.com"
        ]
        logging.info("AdBlocker extension initialized")

    def on_load(self):
        logging.info("AdBlocker extension loaded")

    def rewrite_url(self, url: str) -> str:
        """
        Blocks ad URLs by returning a blank page.
        """
        for domain in self.ad_domains:
            if domain in url:
                logging.info("Blocked ad URL: %s", url)
                return "about:blank"
        return url

    def on_page_load(self, url: str):
        logging.info("AdBlocker: Page loaded: %s", url)
