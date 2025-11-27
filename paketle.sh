#!/bin/bash

# Hata oluşursa işlemi durdur
set -e

APP_NAME="pardus-yardimci"
VERSION="1.0"
ARCH="amd64"
MAINTAINER="Tarik Vardar <tarikvardar@gmail.com>"
DESCRIPTION="Pardus Sistem Yonetim, Bakim ve Kontrol Araci"
BUILD_DIR="build_deb"
OUTPUT_DEB="${APP_NAME}_${VERSION}_${ARCH}.deb"

echo "🚀 Paketleme işlemi başlatılıyor..."

# 1. Temizlik
echo "🧹 Eski dosyalar temizleniyor..."
rm -rf build dist $BUILD_DIR *.deb

# 2. PyInstaller ile Derleme
echo "📦 PyInstaller ile derleniyor (Bu işlem biraz sürebilir)..."
if [ -f "PardusYardimci.spec" ]; then
    pyinstaller PardusYardimci.spec --clean --noconfirm
else
    echo "❌ HATA: PardusYardimci.spec dosyası bulunamadı!"
    exit 1
fi

# 3. Klasör Yapısını Oluştur
echo "📂 Dizin yapısı oluşturuluyor..."
mkdir -p $BUILD_DIR/DEBIAN
mkdir -p $BUILD_DIR/opt/$APP_NAME
mkdir -p $BUILD_DIR/usr/bin
mkdir -p $BUILD_DIR/usr/share/applications
mkdir -p $BUILD_DIR/usr/share/icons/hicolor/256x256/apps

# 4. Dosyaları Kopyala (/opt altına)
echo "📂 Uygulama dosyaları kopyalanıyor..."
cp -r dist/PardusYardimci/* $BUILD_DIR/opt/$APP_NAME/

# 5. İKONLARI AYARLA
echo "🖼️  Menü ikonları yerleştiriliyor..."
if [ -f "icons/yardimci-logo.png" ]; then
    # Menü için standart konuma kopyala
    cp icons/yardimci-logo.png $BUILD_DIR/usr/share/icons/hicolor/256x256/apps/$APP_NAME.png
    # Garanti olsun diye uygulama içine de kopyala
    mkdir -p $BUILD_DIR/opt/$APP_NAME/icons
    cp icons/yardimci-logo.png $BUILD_DIR/opt/$APP_NAME/icons/
else
    echo "⚠️ UYARI: 'icons/yardimci-logo.png' bulunamadı! İkonlar eksik çıkabilir."
fi

# 6. Başlatıcı Script Oluştur (/usr/bin/pardus-yardimci)
echo "🔧 Başlatıcı script oluşturuluyor..."
cat > $BUILD_DIR/usr/bin/$APP_NAME << EOF
#!/bin/bash
cd /opt/$APP_NAME
./PardusYardimci "\$@"
EOF
chmod 755 $BUILD_DIR/usr/bin/$APP_NAME

# 7. .desktop Dosyası Oluştur (KATEGORİLER GÜNCELLENDİ)
# Categories satırına 'Utility', 'Settings' ve 'System' ekleyerek her yerde görünmesini sağlıyoruz.
# X-Pardus-Apps ibaresi, eğer Pardus'ta özel bir filtre varsa oraya da düşmesini sağlar.
echo "🖥️  Desktop dosyası oluşturuluyor..."
cat > $BUILD_DIR/usr/share/applications/$APP_NAME.desktop << EOF
[Desktop Entry]
Name=Pardus Yardımcı
Comment=Sistem Bakım, Hız Testi ve Yönetim Aracı
Exec=/usr/bin/$APP_NAME
Icon=$APP_NAME
Terminal=false
Type=Application
Categories=System;Settings;Utility;X-Pardus-Apps;GTK;
Keywords=system;clean;update;manager;pardus;speedtest;
StartupNotify=true
StartupWMClass=Pardus Yardımcı
EOF

# 8. DEBIAN/control Dosyası Oluştur
echo "⚙️  Control dosyası oluşturuluyor..."
cat > $BUILD_DIR/DEBIAN/control << EOF
Package: $APP_NAME
Version: $VERSION
Architecture: $ARCH
Maintainer: $MAINTAINER
Depends: libc6, libgl1, policykit-1, network-manager, ufw, libxcb-cursor0
Section: utils
Priority: optional
Description: $DESCRIPTION
 Pardus ve Debian tabanlı sistemler için geliştirilmiş;
 sistem izleme, temizlik, güncelleme, hız testi ve yönetim aracı.
 Tamamen çevrimdışı çalışabilir.
EOF

# 9. İzinleri Ayarla
echo "🔒 İzinler ayarlanıyor..."
chmod 755 -R $BUILD_DIR/opt/$APP_NAME
chmod 755 $BUILD_DIR/DEBIAN/control
chmod 644 $BUILD_DIR/usr/share/applications/$APP_NAME.desktop

# 10. DEB Paketini Oluştur
echo "📦 .deb paketi sıkıştırılıyor..."
dpkg-deb --build $BUILD_DIR $OUTPUT_DEB

# Geçici klasörü sil
rm -rf $BUILD_DIR

echo ""
echo "✅ İŞLEM BAŞARIYLA TAMAMLANDI!"
echo "✨ Paket dosyanız hazır: $OUTPUT_DEB"
echo "👉 Kurulum için: sudo dpkg -i $OUTPUT_DEB"