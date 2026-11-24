THEMES = {
    "Dark": {
        "bg_main": "#0D1117",
        "bg_surface": "#161B22",
        "bg_input": "#0D1117",
        "border": "#30363D",
        "text_primary": "#E6EDF3",
        "text_secondary": "#8B949E",
        "accent": "#58A6FF",
        "accent_hover": "#79C0FF",
        "btn_bg": "#21262D",
        "btn_hover": "#30363D",
    },
    "Light": {
        "bg_main": "#F6F8FA",
        "bg_surface": "#FFFFFF",
        "bg_input": "#F6F8FA",
        "border": "#D0D7DE",
        "text_primary": "#1F2328",
        "text_secondary": "#656D76",
        "accent": "#0969DA",
        "accent_hover": "#0550AE",
        "btn_bg": "#F3F4F6",
        "btn_hover": "#E5E7EB",
    },
    "Pink": {
        "bg_main": "#1A1016",
        "bg_surface": "#261720",
        "bg_input": "#1A1016",
        "border": "#4A2B3D",
        "text_primary": "#FCE7F3",
        "text_secondary": "#D8A7C0",
        "accent": "#F472B6",
        "accent_hover": "#F9A8D4",
        "btn_bg": "#36202D",
        "btn_hover": "#4A2B3D",
    },
    "Nord": {
        "bg_main": "#2E3440",
        "bg_surface": "#3B4252",
        "bg_input": "#2E3440",
        "border": "#4C566A",
        "text_primary": "#ECEFF4",
        "text_secondary": "#D8DEE9",
        "accent": "#88C0D0",
        "accent_hover": "#8FBCBB",
        "btn_bg": "#434C5E",
        "btn_hover": "#4C566A",
    },
    "Matcha": {
        "bg_main": "#111916",
        "bg_surface": "#182420",
        "bg_input": "#111916",
        "border": "#2C423A",
        "text_primary": "#E6F2EC",
        "text_secondary": "#95B3A6",
        "accent": "#52B788",
        "accent_hover": "#74C69D",
        "btn_bg": "#21332C",
        "btn_hover": "#2C423A",
    },
}


def get_theme(theme_name):
    return THEMES.get(theme_name, THEMES["Dark"])


def build_global_stylesheet(theme_name):
    t = get_theme(theme_name)
    return f"""
        QMainWindow, QWidget#centralWidget {{
            background-color: {t["bg_main"]};
            color: {t["text_primary"]};
        }}

        QFrame#sidebar {{
            background-color: {t["bg_surface"]};
            border-right: 1px solid {t["border"]};
        }}

        QFrame#sidebar QPushButton {{
            background-color: transparent;
            color: {t["text_secondary"]};
            border: 1px solid transparent;
            border-radius: 6px;
            padding: 10px;
            text-align: left;
            font-size: 14px;
        }}

        QFrame#sidebar QPushButton:hover {{
            background-color: {t["btn_bg"]};
            color: {t["text_primary"]};
            border: 1px solid {t["border"]};
        }}

        QFrame#sidebar QPushButton:checked {{
            background-color: {t["btn_bg"]};
            color: {t["text_primary"]};
            border: 1px solid {t["border"]};
            font-weight: 600;
        }}

        QFrame#settingsCard {{
            background-color: {t["bg_surface"]};
            border: 1px solid {t["border"]};
            border-radius: 10px;
        }}

        QLabel {{
            color: {t["text_primary"]};
            background-color: transparent;
            border: none;
        }}

        QLineEdit, QComboBox {{
            background-color: {t["bg_input"]};
            color: {t["text_primary"]};
            border: 1px solid {t["border"]};
            border-radius: 6px;
            padding: 8px 10px;
            font-size: 13px;
        }}

        QLineEdit:focus, QComboBox:focus {{
            border: 1px solid {t["accent"]};
        }}

        QComboBox QAbstractItemView {{
            background-color: {t["bg_surface"]};
            color: {t["text_primary"]};
            border: 1px solid {t["border"]};
            selection-background-color: {t["btn_hover"]};
        }}

        QPushButton {{
            background-color: {t["btn_bg"]};
            color: {t["text_primary"]};
            border: 1px solid {t["border"]};
            border-radius: 6px;
            padding: 8px 14px;
            font-size: 13px;
        }}

        QPushButton:hover {{
            background-color: {t["btn_hover"]};
        }}

        QPushButton#primaryBtn {{
            background-color: {t["accent"]};
            color: {t["bg_main"]};
            border: 1px solid {t["accent"]};
            font-weight: 600;
        }}

        QPushButton#primaryBtn:hover {{
            background-color: {t["accent_hover"]};
        }}

        QScrollArea {{
            background-color: transparent;
            border: none;
        }}
    """