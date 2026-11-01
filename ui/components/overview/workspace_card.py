
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class WorkspaceCard(QFrame):

    def __init__(self, title, description, icon_text, parent=None):
        super().__init__(parent)

        self.setFixedHeight(190)

        self.setStyleSheet("""
            QFrame {
                background-color: #161B22;
                border: 1px solid #30363D;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(10)

        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet("""
            font-size: 28px;
            color: #58A6FF;
            background-color: transparent;
            border: none;
        """)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #E6EDF3;
            background-color: transparent;
            border: none;
        """)

        description_label = QLabel(description)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("""
            font-size: 13px;
            color: #8B949E;
            background-color: transparent;
            border: none;
        """)

        action_label = QLabel("Open workspace →")
        action_label.setStyleSheet("""
            font-size: 13px;
            font-weight: bold;
            color: #58A6FF;
            background-color: transparent;
            border: none;
        """)

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addStretch()
        layout.addWidget(action_label)