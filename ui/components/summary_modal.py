from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget)
from ui.theme import get_theme


class SummaryWorker(QThread):
    finished = Signal(dict)
    failed = Signal(str)

    def __init__(self, summary_service, repo, mode="simple"):
        super().__init__()
        self.summary_service = summary_service
        self.repo = repo
        self.mode = mode

    def run(self):
        try:
            if self.mode == "simple":
                result = self.summary_service.generate_simple_summary(self.repo)
            else:
                result = self.summary_service.generate_simple_summary(self.repo)
            self.finished.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))


class SummaryModal(QDialog):
    def __init__(self, summary_service, repo, mode="simple", theme_name="Dark", parent=None):
        super().__init__(parent)
        self.summary_service = summary_service
        self.repo = repo
        self.mode = mode
        self.theme_name = theme_name
        self._current_body_text = ""

        self.setWindowTitle(f"{repo.get('name', 'Repository')} — Summary")
        self.setMinimumSize(560, 400)
        self.resize(620, 440)

        self._build_ui()
        self._start_generation()

    def _build_ui(self):
        t = get_theme(self.theme_name)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {t['bg_main']};
                color: {t['text_primary']};
            }}
            QFrame#summaryBodyCard {{
                background-color: {t['bg_surface']};
                border: 1px solid {t['border']};
                border-radius: 10px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 20)
        layout.setSpacing(14)

        # Header
        self.title_label = QLabel(self.repo.get("name", "Repository"))
        self.title_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {t['text_primary']};")
        layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("Generating simple summary...")
        self.subtitle_label.setStyleSheet(f"font-size: 13px; color: {t['text_secondary']};")
        layout.addWidget(self.subtitle_label)

        # Content Card with ScrollArea
        card = QFrame()
        card.setObjectName("summaryBodyCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 16, 18, 16)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.body_label = QLabel("Inspecting repository README and structure...")
        self.body_label.setWordWrap(True)
        self.body_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.body_label.setStyleSheet(f"""
            font-size: 14px;
            line-height: 1.55;
            color: {t['text_primary']};
            background: transparent;
        """)
        scroll_layout.addWidget(self.body_label)

        scroll.setWidget(scroll_content)
        card_layout.addWidget(scroll)
        layout.addWidget(card, 1)

        # Footer Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.copy_btn = QPushButton("Copy Summary")
        self.copy_btn.setEnabled(False)
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.clicked.connect(self._copy_to_clipboard)

        btn_row.addStretch()
        btn_row.addWidget(self.copy_btn)

        close_btn = QPushButton("Close")
        close_btn.setObjectName("primaryBtn")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)

        layout.addLayout(btn_row)

    def _start_generation(self):
        self.worker = SummaryWorker(self.summary_service, self.repo, self.mode)
        self.worker.finished.connect(self._on_summary_ready)
        self.worker.failed.connect(self._on_summary_failed)
        self.worker.start()

    def _on_summary_ready(self, result):
        self.title_label.setText(result.get("title", self.repo.get("name", "Repository")))
        self.subtitle_label.setText(result.get("subtitle", "Simple Summary"))
        body = result.get("body", "")
        self._current_body_text = body
        self.body_label.setText(body)
        self.copy_btn.setEnabled(bool(body))

    def _on_summary_failed(self, error_msg):
        self.subtitle_label.setText("Could not generate summary")
        self.body_label.setText(f"Something went wrong while reading this repository:\n\n{error_msg}")

    def _copy_to_clipboard(self):
        if not self._current_body_text:
            return
        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText(self._current_body_text)
            self.copy_btn.setText("Copied!")