# yardimci_app.py
# TAMAMEN OFFLINE (İNTERNETSİZ) BAŞLATICI
# İnternet bağlantısı aramaz, sadece 'bagimliliklar' klasörünü kullanır.

import sys
import os
import subprocess
import site
import traceback


def bagimliliklari_yukle():
    """
    'bagimliliklar' klasöründeki .whl dosyalarını kullanarak
    gerekli kütüphaneleri İNTERNETSİZ olarak kurar.
    """
    # 1. Çalışma dizinini ve bağımlılık klasörünü bul
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS  # Exe/Binary ise
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Script ise

    deps_path = os.path.join(base_dir, "bagimliliklar")

    # 2. Klasör kontrolü
    if not os.path.exists(deps_path):
        print(f"UYARI: '{deps_path}' klasörü bulunamadı!")
        # Klasör yoksa bile sistemde kurulu kütüphanelerle çalışmayı dener
        return

    # 3. Geçici olarak Python yoluna ekle (Anlık import için)
    site.addsitedir(deps_path)

    # 4. OFFLINE KURULUM KOMUTU
    # --no-index: PyPI sunucularına (internete) asla bakma.
    # --find-links: Sadece ve sadece bizim verdiğimiz klasöre bak.
    print(">> Sistem kontrol ediliyor ve yerel paketler yükleniyor...")

    gerekli_paketler = [
        "PyQt6",
        "PyQt6-WebEngine",
        "psutil",
        "requests"
    ]

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--no-index",  # İNTERNET YOK
            "--find-links", deps_path,  # Sadece bu klasör
            *gerekli_paketler,  # Listeyi açarak ekle
            "--quiet",  # Sessiz mod
            "--no-warn-script-location"  # Uyarıları azalt
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(">> Bağımlılık kontrolleri tamamlandı.")
    except Exception:
        # Hata olursa (örn: yetki sorunu veya zaten kuruluysa) devam et
        print(">> Kurulum adımı geçildi (Zaten kurulu veya yetki yok).")
        pass


def uygulamayi_baslat():
    """
    Ana pencereyi başlatır ve kritik ayarları yapar.
    """
    # Harita bileşeni için kritik ayarlar (Linux/Pardus için şart)
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
    os.environ[
        "QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --no-sandbox --disable-logging --ignore-certificate-errors"

    try:
        # Kütüphaneleri içe aktarmayı dene
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QFont
        from ana_pencere import AnaPencere

        # Uygulamayı Oluştur
        app = QApplication(sys.argv)
        app.setApplicationName("Pardus Yardımcı")

        # Kapanma Ayarı: Pencere kapansa bile tepside çalışmaya devam etsin
        app.setQuitOnLastWindowClosed(False)

        # Font Ayarı
        font = QFont("Sans Serif", 10)
        app.setFont(font)

        # Pencereyi Göster
        pencere = AnaPencere()
        pencere.show()

        # Döngüyü Başlat
        sys.exit(app.exec())

    except ImportError as e:
        print("\n" + "!" * 50)
        print("KRİTİK HATA: Gerekli kütüphaneler bulunamadı!")
        print(f"Eksik Modül: {e}")
        print("Lütfen 'bagimliliklar' klasörünün programın yanında olduğundan emin olun.")
        print("!" * 50 + "\n")
        input("Kapatmak için Enter'a basın...")
        sys.exit(1)

    except Exception as e:
        print("\n" + "=" * 40)
        print("BEKLENMEYEN BİR HATA OLUŞTU!")
        print(f"Hata: {e}")
        print("-" * 40)
        traceback.print_exc()
        print("=" * 40 + "\n")
        input("Kapatmak için Enter'a basın...")
        sys.exit(1)


if __name__ == '__main__':
    bagimliliklari_yukle()
    uygulamayi_baslat()