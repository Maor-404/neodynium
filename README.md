# Neodynium

Neodynium is a lightweight, community‑driven web browser written in Python using PyQtWebEngine.  
Its goal is to be fully extensible, open, and customizable — a browser built *by developers, for developers*.

## ✨ Features (Current & Planned)

### ✅ Current
- Basic browser window (PyQt5 + QWebEngineView)
- Navigation controls (Back, Forward, Reload, Home)
- Project structure ready for modular development

### 🚧 In Development
- Extension Manager
- Public Extension Store
- Installer‑generated AppData directory
- User profiles and settings
- Theme support
- JavaScript injection API
- Python‑based plugin system

### 🧩 Future Goals
- Tabbed browsing
- Built‑in adblocker
- Customizable UI themes
- Developer tools panel
- Sync system for settings and extensions

---

## 📁 Project Structure


MyBrowser/
│
├── browser/
│   ├── main.py
│   ├── core/
│   │   ├── window.py
│   │   ├── engine.py
│   │   └── extension_manager.py
│   └── extensions/
│
├── extension_store/
│   ├── README.md
│   └── index.json
│
└── requirements.txt


---

## 🗂️ AppData (Created by Installer)

The browser will automatically create its AppData directory on first launch:


%APPDATA%/Neodynium/
    profiles/default/
    extensions/
    logs/
    updates/


This keeps user data separate from the program files.

---

## 🛠️ Requirements

Install dependencies:


pip install -r requirements.txt


---

## 🤝 Contributing

Contributions are welcome.  
You can help by:

- Building extensions  
- Improving the browser core  
- Adding features  
- Reporting bugs  
- Writing documentation  

---

## 📜 License

This project is licensed under the MIT License.  
See the `LICENSE` file for details.

## 📝 Note

This README was generated with the assistance of AI to speed up documentation and improve clarity.
