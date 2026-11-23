# Veya

A clean, dark-themed desktop Git & workspace utility built with Python and PySide6. Veya bridges command-line Git workflows and a distraction-free GUI composer so you can inspect repositories, stage files, commit, and push without leaving your workspace.

## Features

- **Dual Workflow Modes**
  - **CLI Workspace:** Integrated terminal-style command interface supporting directory navigation (`cd`, `pwd`, `ls`) and core Git operations (`status`, `add`, `restore`, `commit`, `push`, `pull`).
  - **GUI Workspace:** Minimalist composer card with live staged/unstaged file detection, multi-select file staging/unstaging modals, commit message editor, and one-click push.
- **Modular Service Architecture:** Clean separation between PySide6 UI views (`ui/`) and subprocess-backed CLI/Git wrappers (`services/`).
- **Zero-Config Workspace Switching:** Switch active repositories on the fly from either mode.

## Project Structure

```text
veya/
├── main.py                  # Application entry point
├── services/
│   └── cli/
│       ├── git/             # Git CLI subprocess wrappers & porcelain parser
│       └── navigation/      # Directory navigation & filesystem handlers
└── ui/
    ├── dialogs/             # Workspace & file-picker modal dialogs
    ├── pages/               # Overview, CLI Workspace, and GUI Workspace views
    └── main_window.py       # Top-level window & stacked view router
```

## Getting Started

### Prerequisites
- Python 3.10+
- Git installed and available in your system `PATH`

### Installation

```bash
git clone [https://github.com/](https://github.com/)Abhiyanshu-Sharma/veya.git
cd veya
python -m venv .venv
.venv\Scripts\activate
pip install PySide6
python main.py
```

## License

MIT License