from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt

class WorkspaceCard(QFrame):

    clicked = Signal()

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
        icon_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addWidget(title_label)
        title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addWidget(description_label)
        description_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addStretch()
        layout.addWidget(action_label)
        action_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)