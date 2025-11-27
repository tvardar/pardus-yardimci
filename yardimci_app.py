# yardimci_app.py

import sys
import os
import subprocess
import site
import traceback
import time

# Yol bulucu
def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def bagimliliklari_yukle():
    """
    İnternet yoksa 'bagimliliklar' klasöründeki yerel paketleri yüklemeye çalışır.
    PyInstaller ile derlenmiş (frozen) yapıda bu fonksiyon atlanır.
    """
    if getattr(sys, 'frozen', False): return
    
    base_dir = get_base_dir()
    deps = os.path.join(base_dir, "bagimliliklar")
    
    # Eğer klasör yoksa işlem yapma
    if not os.path.exists(deps): return
    
    # Python path'ine ekle
    site.addsitedir(deps)
    
    # Opsiyonel: Otomatik yükleme denemesi (Offline mod için --no-index)
    # Bu kısım sadece kaynak koddan çalışırken ve kütüphane eksikse devreye girer.
    try:
        import PyQt6
        import psutil
        import requests
    except ImportError:
        print("⚠️ Bazı kütüphaneler eksik, yerel 'bagimliliklar' klasöründen yükleniyor...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "--no-index", "--find-links", deps,
                "PyQt6", "PyQt6-WebEngine", "psutil", "requests",
                "--quiet", "--no-warn-script-location"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

def uygulamayi_baslat():
    # 1. WebEngine Ayarları (Crash Önleyici)
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --no-sandbox --disable-logging --ignore-certificate-errors"

    try:
        # --- KRİTİK DÜZELTME BAŞLANGICI ---
        # QApplication oluşturulmadan ÖNCE bu import yapılmalı yoksa "ImportError" verir.
        # Bu satır, OpenGL context paylaşımını QApplication oluşmadan ayarlar.
        from PyQt6.QtWebEngineWidgets import QWebEngineView
        # --- KRİTİK DÜZELTME BİTİŞİ ---

        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtNetwork import QLocalSocket
        from PyQt6.QtGui import QFont

        app = QApplication(sys.argv)
        app.setApplicationName("Pardus Yardımcı")
        app.setQuitOnLastWindowClosed(False)

        # --- TEK ÖRNEK (SINGLE INSTANCE) KONTROLÜ ---
        socket_name = "PardusYardimciInstance"
        socket = QLocalSocket()
        socket.connectToServer(socket_name)

        if socket.waitForConnected(500):
            # Eğer sunucuya (çalışan programa) bağlanırsa:
            print("Program zaten çalışıyor. Mevcut pencere öne getiriliyor...")
            # Çalışan programa "SHOW" sinyali gönder
            socket.write(b"SHOW")
            socket.waitForBytesWritten(1000)
            socket.disconnectFromServer()
            sys.exit(0) # Bu yeni örneği kapat
        
        # --- ANA PENCEREYİ BAŞLAT ---
        # import işlemini burada yapıyoruz ki hata olursa yakalayabilelim
        from ana_pencere import AnaPencere

        font = QFont("Sans Serif", 10)
        app.setFont(font)

        # Ana pencereyi başlat (Socket sunucusu orada kurulacak)
        p = AnaPencere(socket_name=socket_name)
        p.show()

        sys.exit(app.exec())

    except Exception as e:
        # Hatayı konsola bas
        print("\n" + "=" * 40)
        print("KRİTİK HATA OLUŞTU!")
        print(f"Hata Mesajı: {str(e)}")
        print("-" * 40)
        traceback.print_exc()
        print("=" * 40 + "\n")

        # Hatayı dosyaya da yaz
        try:
            home = os.path.expanduser("~")
            log_path = os.path.join(home, "pardus_yardimci_hata.log")
            with open(log_path, "w") as f:
                f.write(f"Zaman: {time.ctime()}\n")
                f.write(f"Hata: {str(e)}\n\n")
                traceback.print_exc(file=f)
            print(f"Hata raporu kaydedildi: {log_path}")
        except:
            pass
        sys.exit(1)

if __name__ == '__main__':
    bagimliliklari_yukle()
    uygulamayi_baslat()