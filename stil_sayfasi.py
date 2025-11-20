# stil_sayfasi.py
# Pardus Yardımcı (PY) - Modern ve Responsive Tasarım

PYQT6_STIL = """
/* --- GENEL PENCERE AYARLARI --- */
QMainWindow, QWidget {
    background-color: #1E1E1E; /* Modern Mat Siyah/Gri */
    color: #E0E0E0; /* Kırık Beyaz Yazı (Göz yormaz) */
    font-family: "Segoe UI", "Roboto", "Ubuntu", sans-serif;
    font-size: 10pt;
}

/* --- YAN MENÜ (SIDEBAR) --- */
QWidget#YanMenu {
    background-color: #252526; /* Menü biraz daha açık gri */
    border-right: 1px solid #333333;
}

QLabel#UygulamaBaslik {
    color: #33AADD; /* PARDUS TURKUAZI */
    font-size: 22pt;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 20px;
}

/* --- MENÜ BUTONLARI --- */
QPushButton#MenuDugmesi {
    background-color: transparent;
    color: #AAAAAA;
    border: none;
    padding: 12px 20px;
    text-align: left;
    border-radius: 8px;
    margin: 2px 10px;
    font-size: 11pt;
}
QPushButton#MenuDugmesi:hover {
    background-color: #333333;
    color: white;
}
QPushButton#MenuDugmesi:checked {
    background-color: #33AADD; /* Seçili iken Pardus Mavisi */
    color: #FFFFFF;
    font-weight: bold;
}
QPushButton#MenuDugmesi:checked:hover {
    background-color: #2988b3;
}

/* --- İÇERİK BAŞLIKLARI --- */
QLabel#SayfaBaslik {
    color: #33AADD;
    font-size: 24pt;
    font-weight: 300; /* İnce ve modern font */
    margin-bottom: 20px;
    border-bottom: 1px solid #333333;
    padding-bottom: 10px;
}

/* --- KART GÖRÜNÜMÜ (GROUPBOX) --- */
QGroupBox {
    background-color: #2D2D30; /* Kart Arka Planı */
    border: 1px solid #3E3E42;
    border-radius: 10px;
    margin-top: 30px; /* Başlık için pay */
    font-weight: bold;
    color: #33AADD;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 10px;
    background-color: transparent;
    color: #33AADD;
    font-size: 11pt;
}

/* --- PROGRESS BAR (DİSK VE CPU) --- */
QProgressBar {
    border: none;
    border-radius: 6px;
    background-color: #1E1E1E;
    text-align: center;
    color: white;
    height: 20px; /* Daha ince ve şık */
    font-size: 9pt;
}
QProgressBar::chunk {
    background-color: #33AADD; /* Pardus Mavisi Dolgu */
    border-radius: 6px;
}

/* --- LİSTE VE SCROLL ALANLARI --- */
QListWidget, QScrollArea {
    background-color: #1E1E1E;
    border: 1px solid #333333;
    border-radius: 8px;
    outline: none;
}
QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #2A2A2A;
}
QListWidget::item:selected {
    background-color: #33AADD;
    color: white;
    border-radius: 4px;
}

/* --- SCROLLBAR (KAYDIRMA ÇUBUĞU) ÖZELLEŞTİRME --- */
QScrollBar:vertical {
    border: none;
    background: #1E1E1E;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #424242;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #33AADD;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* --- GENEL BUTONLAR (AKSİYON BUTONLARI) --- */
QPushButton {
    background-color: #3E3E42;
    color: white;
    border: 1px solid #555555;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #33AADD;
    border-color: #33AADD;
}
QPushButton:pressed {
    background-color: #206b8c;
}

/* --- INPUT ALANLARI --- */
QLineEdit {
    background-color: #1E1E1E;
    border: 1px solid #444444;
    border-radius: 6px;
    padding: 8px;
    color: white;
    selection-background-color: #33AADD;
}
QLineEdit:focus {
    border: 1px solid #33AADD;
}

/* --- TOOLTIP --- */
QToolTip {
    background-color: #33AADD;
    color: white;
    border: none;
    padding: 5px;
    border-radius: 4px;
}
"""