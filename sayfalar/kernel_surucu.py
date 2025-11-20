# sayfalar/kernel_surucu.py
# DÜZELTME: Butonların görünürlüğü ve düzeni sağlandı.

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QListWidget, QPushButton, QMessageBox, QTabWidget, QGroupBox)
from gorsel_araclar import KernelYoneticisi
import subprocess


class KernelSurucuSayfasi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Kernel ve Sürücü Merkezi"))

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # --- TAB 1: KERNEL ---
        tab_k = QWidget()
        l_k = QVBoxLayout(tab_k)

        # Listeler (Üstte, Esnek)
        h_lists = QHBoxLayout()

        grp1 = QGroupBox("Kurulu Kerneller")
        l1 = QVBoxLayout(grp1)
        self.list_kurulu = QListWidget()
        l1.addWidget(self.list_kurulu)
        h_lists.addWidget(grp1)

        grp2 = QGroupBox("Depo (APT)")
        l2 = QVBoxLayout(grp2)
        self.list_repo = QListWidget()
        l2.addWidget(self.list_repo)
        h_lists.addWidget(grp2)

        l_k.addLayout(h_lists, stretch=1)  # Listeler alanı kaplasın

        # Butonlar (Altta, Sabit)
        btn_layout = QHBoxLayout()

        btn_sil = QPushButton("🗑️ Seçili Kerneli KALDIR")
        btn_sil.setStyleSheet("background-color: #a54949; padding: 10px;")
        btn_sil.clicked.connect(self.kernel_kaldir)

        btn_kur = QPushButton("⬇️ Seçili Kerneli KUR")
        btn_kur.setStyleSheet("background-color: #27ae60; padding: 10px;")
        btn_kur.clicked.connect(self.kernel_kur)

        btn_layout.addWidget(btn_sil)
        btn_layout.addWidget(btn_kur)

        l_k.addLayout(btn_layout)  # Butonları en alta ekle
        self.tabs.addTab(tab_k, "Kernel Yönetimi")

        # --- TAB 2: SÜRÜCÜ ---
        tab_d = QWidget()
        l_d = QVBoxLayout(tab_d)

        self.lbl_durum = QLabel("Durum: Bekleniyor...")
        l_d.addWidget(self.lbl_durum)

        self.list_driver = QListWidget()
        l_d.addWidget(self.list_driver)

        btn_tara = QPushButton("🔄 Donanımı Tara")
        btn_tara.setMinimumHeight(40)
        btn_tara.clicked.connect(self.verileri_yukle)
        l_d.addWidget(btn_tara)

        self.tabs.addTab(tab_d, "Sürücü Bulucu")

        # Backend
        self.manager = KernelYoneticisi()
        self.manager.veri_sinyali.connect(self.arayuzu_doldur)
        self.verileri_yukle()

    def verileri_yukle(self):
        self.lbl_durum.setText("Taranıyor...")
        self.manager.start()

    def arayuzu_doldur(self, veri):
        self.list_kurulu.clear()
        aktif = veri.get("aktif_kernel", "")
        for k in veri.get("kurulu_kerneller", []):
            self.list_kurulu.addItem(f"{k} {'(AKTİF)' if k in aktif else ''}")

        self.list_repo.clear()
        for k in veri.get("mevcut_kerneller", []):
            self.list_repo.addItem(k)

        self.list_driver.clear()
        eksikler = veri.get("eksik_suruculer", [])
        if not eksikler:
            self.list_driver.addItem("✅ Tüm sürücüler tam görünüyor.")
            self.lbl_durum.setText("Sistem Temiz")
        else:
            self.lbl_durum.setText(f"{len(eksikler)} öneri bulundu.")
            for d in eksikler:
                self.list_driver.addItem(f"{d['icon']} {d['ad']} -> {d['paket']}")

    def kernel_kur(self):
        item = self.list_repo.currentItem()
        if item: self.cmd(["apt", "install", "-y", item.text()])

    def kernel_kaldir(self):
        item = self.list_kurulu.currentItem()
        if item and "AKTİF" not in item.text():
            self.cmd(["apt", "remove", "-y", item.text().split()[0]])
        else:
            QMessageBox.warning(self, "Hata", "Aktif kernel silinemez!")

    def cmd(self, c):
        subprocess.Popen(["pkexec"] + c)