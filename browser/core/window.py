"""
BrowserWindow
-------------
The main window of Neodynium .

Handles:
- Navigation UI
- URL bar
- WebEngineView
- Integration with BrowserEngine
- Extension hooks
"""

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QMainWindow,
    QToolBar,
    QAction,
    QLineEdit,
    QMenuBar,
    QMenu,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QTabBar,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

from .engine import BrowserEngine
from .extension_manager import ExtensionManager


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Neodynium Browser")
        self.resize(1200, 800)

        # Core components
        self.engine = BrowserEngine()
        self.extension_manager = ExtensionManager(self)

        # Load extensions
        self.extension_manager.load_extensions()

        # Tab widget for multiple tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Create first tab
        self.new_tab()

        # Navigation bar
        self._create_navbar()

        # Menu bar
        self._create_menu_bar()

        # Load homepage
        self.navigate_home()

    # ------------------------------------------------------------
    # Navigation Bar
    # ------------------------------------------------------------

    def _create_navbar(self):
        nav = QToolBar("Navigation")
        self.addToolBar(nav)

        # Back
        back = QAction("Back", self)
        back.triggered.connect(self.view.back)
        nav.addAction(back)

        # Forward
        forward = QAction("Forward", self)
        forward.triggered.connect(self.view.forward)
        nav.addAction(forward)

        # Reload
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.view.reload)
        nav.addAction(reload_btn)

        # Home
        home = QAction("Home", self)
        home.triggered.connect(self.navigate_home)
        nav.addAction(home)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_from_bar)
        nav.addWidget(self.url_bar)

    # ------------------------------------------------------------
    # Tab Management
    # ------------------------------------------------------------

    def new_tab(self):
        view = QWebEngineView()
        view.urlChanged.connect(self._update_url_bar)
        view.loadFinished.connect(self._page_loaded)
        index = self.tabs.addTab(view, "New Tab")
        self.tabs.setCurrentIndex(index)
        return view

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    @property
    def view(self):
        return self.tabs.currentWidget()

    # ------------------------------------------------------------
    # Navigation Logic
    # ------------------------------------------------------------

    def navigate_home(self):
        url = self.engine.get_home_url()
        self._navigate(url)

    def navigate_from_bar(self):
        text = self.url_bar.text().strip()
        if not text:
            return

        url = self.engine.normalize_url(text)
        url = self.extension_manager.apply_url_hooks(url)
        self._navigate(url)

    def _navigate(self, url: str):
        self.view.setUrl(QUrl(url))

    # ------------------------------------------------------------
    # UI Sync
    # ------------------------------------------------------------

    def _update_url_bar(self, qurl):
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)

    # ------------------------------------------------------------
    # Menu Bar
    # ------------------------------------------------------------

    def _create_menu_bar(self):
        menubar = self.menuBar()

        # Bookmarks menu
        bookmarks_menu = menubar.addMenu('Bookmarks')
        add_bookmark_action = QAction('Add Bookmark', self)
        add_bookmark_action.triggered.connect(self.add_bookmark)
        bookmarks_menu.addAction(add_bookmark_action)

        show_bookmarks_action = QAction('Show Bookmarks', self)
        show_bookmarks_action.triggered.connect(self.show_bookmarks)
        bookmarks_menu.addAction(show_bookmarks_action)

        # History menu
        history_menu = menubar.addMenu('History')
        show_history_action = QAction('Show History', self)
        show_history_action.triggered.connect(self.show_history)
        history_menu.addAction(show_history_action)

        clear_history_action = QAction('Clear History', self)
        clear_history_action.triggered.connect(self.clear_history)
        history_menu.addAction(clear_history_action)

    def add_bookmark(self):
        url = self.view.url().toString()
        title = self.view.title() or url
        self.engine.add_bookmark(url, title)

    def show_bookmarks(self):
        # Placeholder: implement bookmark dialog
        pass

    def show_history(self):
        # Placeholder: implement history dialog
        pass

    def clear_history(self):
        self.engine.clear_history()

    # ------------------------------------------------------------
    # Page Load Hook
    # ------------------------------------------------------------

    def _page_loaded(self):
        url = self.view.url().toString()
        self.engine.add_to_history(url)
        self.extension_manager.notify_page_loaded(url)
