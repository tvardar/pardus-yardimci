# stil_sayfasi.py

def get_stil(tema="Koyu"):
    if tema == "Açık":
        c_bg = "#F5F7FA"; c_panel = "#FFFFFF"; c_text = "#2C3E50"; c_subtext = "#7F8C8D"
        c_border = "#BDC3C7"; c_accent = "#2980B9"; c_hover = "#ECF0F1"; c_input = "#FFFFFF"
    else:
        c_bg = "#1E1E1E"; c_panel = "#252526"; c_text = "#E0E0E0"; c_subtext = "#AAAAAA"
        c_border = "#3E3E42"; c_accent = "#33AADD"; c_hover = "#333333"; c_input = "#333333"

    return f"""
    QMainWindow, QWidget {{ background-color: {c_bg}; color: {c_text}; font-family: "Segoe UI", sans-serif; font-size: 10pt; }}
    QWidget#YanMenu {{ background-color: {c_panel}; border-right: 1px solid {c_border}; }}
    QPushButton {{ background-color: {c_panel}; color: {c_text}; border: 1px solid {c_border}; padding: 8px 16px; border-radius: 6px; }}
    QPushButton:hover {{ background-color: {c_hover}; border-color: {c_accent}; }}
    QPushButton#MenuDugmesi {{ background-color: transparent; color: {c_subtext}; border: none; padding: 12px 20px; text-align: left; border-radius: 0px; border-left: 4px solid transparent; }}
    QPushButton#MenuDugmesi:hover {{ background-color: {c_hover}; color: {c_text}; }}
    QPushButton#MenuDugmesi:checked {{ background-color: {c_hover}; color: {c_accent}; font-weight: bold; border-left: 4px solid {c_accent}; }}
    QGroupBox {{ background-color: {c_panel}; border: 1px solid {c_border}; border-radius: 8px; margin-top: 25px; font-weight: bold; color: {c_accent}; }}
    QGroupBox::title {{ subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; left: 10px; }}
    QLineEdit, QListWidget, QTableWidget {{ background-color: {c_input}; border: 1px solid {c_border}; color: {c_text}; border-radius: 4px; gridline-color: {c_border}; }}
    QHeaderView::section {{ background-color: {c_bg}; padding: 5px; border: none; color: {c_accent}; font-weight: bold; border-bottom: 1px solid {c_border}; }}
    QProgressBar {{ background-color: {c_bg}; border: 1px solid {c_border}; border-radius: 4px; text-align: center; color: {c_text}; }}
    QProgressBar::chunk {{ background-color: {c_accent}; border-radius: 3px; }}
    QFrame#SayfaBasligi {{ background-color: {c_panel}; border-bottom: 2px solid {c_border}; border-radius: 8px; }}
    QLabel#BaslikMetni {{ color: {c_accent}; font-size: 22pt; font-weight: 300; }}
    QComboBox {{ background-color: {c_input}; border: 1px solid {c_border}; padding: 5px; border-radius: 4px; color: {c_text}; }}
    QComboBox QAbstractItemView {{ background-color: {c_input}; color: {c_text}; selection-background-color: {c_accent}; selection-color: white; }}
    QTabWidget::pane {{ border: 1px solid {c_border}; }}
    QTabBar::tab {{ background: {c_bg}; color: {c_text}; padding: 8px 20px; border: 1px solid {c_border}; border-bottom: none; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; }}
    QTabBar::tab:selected {{ background: {c_panel}; color: {c_accent}; font-weight: bold; border-bottom: 2px solid {c_panel}; }}
    """