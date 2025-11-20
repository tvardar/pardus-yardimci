# gorsel_araclar.py
# GÜNCELLEME: 'Ayarlar' (Dişli) ikonu eklendi.

import platform
import psutil
import requests
import subprocess
import time
import os
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QRectF, QSize, QByteArray
from PyQt6.QtGui import QFont, QColor, QPen, QPainter, QPixmap
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtSvg import QSvgRenderer


# --- GÖRSEL BİLEŞENLER (Aynen Kalıyor) ---
class GostergeWidget(QWidget):
    def sizeHint(self): return QSize(150, 150)

    def __init__(self, parent=None, baslik="Kullanım"):
        super().__init__(parent)
        self.setMinimumSize(150, 150)
        self.deger = 0;
        self.max_deger = 100;
        self.baslik = baslik

    def degeri_ayarla(self, deger):
        self.deger = deger;
        self.update()

    def paintEvent(self, event):
        p = QPainter(self);
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect();
        s = min(r.width(), r.height())
        mx, my = r.width() / 2, r.height() / 2
        rad = s / 2 - 10
        rect = QRectF(mx - rad, my - rad, rad * 2, rad * 2)
        p.setPen(QPen(QColor("#404040"), 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawArc(rect, int(45 * 16), int(-270 * 16))
        angle = int(270 * (self.deger / self.max_deger))
        p.setPen(QPen(QColor("#60A549"), 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawArc(rect, int(45 * 16), int(-angle * 16))
        p.setPen(QColor("white"));
        p.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        p.drawText(QRectF(mx - 50, my - 20, 100, 40), Qt.AlignmentFlag.AlignCenter, f"{int(self.deger)}%")
        p.setFont(QFont("Arial", 10))
        p.drawText(QRectF(mx - 50, my + rad - 25, 100, 20), Qt.AlignmentFlag.AlignCenter, self.baslik)


class HaritaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.harita = QWebEngineView()
        s = self.harita.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        self.layout.addWidget(self.harita)
        self.setMinimumSize(300, 200)
        self.html_sablon = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" /><style>body {{ margin: 0; background: #222; }} #map {{ height: 100vh; width: 100%; }}</style></head><body><div id="map"></div><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script><script>window.onload = function() {{ if (typeof L === 'undefined') {{ document.body.innerHTML = "<h3 style='color:white;text-align:center;margin-top:50px;font-family:sans-serif'>Harita Yüklenemedi</h3>"; return; }} try {{ var map = L.map('map').setView([{lat}, {lon}], 13); L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 19, attribution: 'OSM' }}).addTo(map); L.marker([{lat}, {lon}]).addTo(map); }} catch(e) {{ console.log(e); }} }};</script></body></html>"""
        self.konumu_guncelle(39.9334, 32.8597)

    def konumu_guncelle(self, lat, lon):
        self.harita.setHtml(self.html_sablon.format(lat=lat, lon=lon))


class SvgIkonOlusturucu:
    @staticmethod
    def get_pixmap(svg_data, boyut=24):
        r = QSvgRenderer(QByteArray(svg_data.encode()));
        p = QPixmap(boyut, boyut);
        p.fill(Qt.GlobalColor.transparent);
        pt = QPainter(p);
        r.render(pt);
        pt.end()
        return p

    @staticmethod
    def termometre_getir(renk="#ff5555", boyut=24):
        return SvgIkonOlusturucu.get_pixmap(
            f"""<svg viewBox="0 0 24 24" fill="none"><path d="M12 2C10.34 2 9 3.34 9 5V13.09C7.83 13.94 7.13 15.33 7.13 16.87C7.13 19.7 9.3 22 12 22C14.7 22 16.87 19.7 16.87 16.87C16.87 15.33 16.17 13.94 15 13.09V5C15 3.34 13.66 2 12 2Z" stroke="{renk}" stroke-width="2"/><path d="M12 12V6" stroke="{renk}" stroke-width="2"/><circle cx="12" cy="17" r="2" fill="{renk}"/></svg>""",
            boyut)

    @staticmethod
    def indir_ikonu(renk="#33AADD", boyut=24):
        return SvgIkonOlusturucu.get_pixmap(
            f"""<svg viewBox="0 0 24 24" fill="none" stroke="{renk}" stroke-width="2"><path d="M12 5V19M12 19L5 12M12 19L19 12"/></svg>""",
            boyut)

    @staticmethod
    def yukle_ikonu(renk="#e67e22", boyut=24):
        return SvgIkonOlusturucu.get_pixmap(
            f"""<svg viewBox="0 0 24 24" fill="none" stroke="{renk}" stroke-width="2"><path d="M12 19V5M12 5L5 12M12 5L19 12"/></svg>""",
            boyut)

    @staticmethod
    def anahtar_ikonu(renk="#aaaaaa", boyut=20):
        return SvgIkonOlusturucu.get_pixmap(
            f"""<svg viewBox="0 0 24 24" fill="{renk}"><path d="M12.65 10C11.83 7.67 9.61 6 7 6c-3.31 0-6 2.69-6 6s2.69 6 6 6c2.61 0 4.83-1.67 5.65-4H17v4h4v-4h2v-4H12.65zM7 14c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/></svg>""",
            boyut)

    # YENİ: AYARLAR (DİŞLİ) İKONU
    @staticmethod
    def ayarlar_ikonu(renk="#E0E0E0", boyut=24):
        return SvgIkonOlusturucu.get_pixmap(
            f"""<svg viewBox="0 0 24 24" fill="{renk}"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58a.49.49 0 0 0 .12-.61l-1.92-3.32a.488.488 0 0 0-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54a.484.484 0 0 0-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58a.49.49 0 0 0-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>""",
            boyut)


# --- THREAD ---
class BilgiIsleyicisi(QThread):
    bilgi_guncelle_sinyal = pyqtSignal(dict)

    def __init__(self):
        super().__init__(); self.cached_konum = None

    def konum_bul(self):
        try:
            j = requests.get('http://ip-api.com/json', timeout=5).json()
            return {"ip": j.get("query", "N/A"), "lat": j.get("lat", 0), "lon": j.get("lon", 0),
                    "org": j.get("isp", "Bilinmiyor"), "sehir": j.get("city", "Bilinmiyor"),
                    "ulke": j.get("countryCode", "")}
        except:
            pass
        try:
            j = requests.get('https://ipinfo.io/json', timeout=5, verify=False).json()
            loc = j.get("loc", "0,0").split(',')
            return {"ip": j.get("ip", "N/A"), "lat": float(loc[0]), "lon": float(loc[1]),
                    "org": j.get("org", "Bilinmiyor"), "sehir": j.get("city", "Bilinmiyor"),
                    "ulke": j.get("country", "")}
        except:
            return {"ip": "N/A", "lat": 0, "lon": 0, "org": "Veri Yok"}

    def bayt_cevir(self, b):
        return f"{b / 1048576:.1f} MB"

    def get_gpu_model(self):
        try:
            out = subprocess.check_output("lspci -mm | grep -i 'VGA\\|3D'", shell=True, text=True,
                                          stderr=subprocess.DEVNULL).strip()
            parts = out.split('"')
            if len(parts) > 3: return parts[3] + " " + parts[5]
            return "Standart VGA"
        except:
            return "Dahili / Bilinmiyor"

    def get_disk_models(self):
        models = {}
        try:
            out = subprocess.check_output(["lsblk", "-d", "-n", "-o", "NAME,MODEL"], text=True,
                                          stderr=subprocess.DEVNULL)
            for line in out.splitlines():
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2: models[parts[0]] = parts[1]
        except:
            pass
        return models

    def get_battery(self):
        try:
            batt = psutil.sensors_battery()
            if batt: return {"percent": batt.percent, "plugged": batt.power_plugged, "secsleft": batt.secsleft}
        except:
            pass
        return {"percent": 0, "plugged": True, "secsleft": -1, "status_yok": True}

    def get_temp(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                return int(f.read().strip()) / 1000.0
        except:
            pass
        try:
            t = psutil.sensors_temperatures()
            for k in t: return t[k][0].current
        except:
            return 0

    def run(self):
        while True:
            try:
                if not self.cached_konum or self.cached_konum.get("ip") == "N/A": self.cached_konum = self.konum_bul()
                c_pct = psutil.cpu_percent(percpu=True);
                ram = psutil.virtual_memory();
                net = psutil.net_io_counters()
                disk_models = self.get_disk_models()
                disk = []
                for p in psutil.disk_partitions():
                    try:
                        u = psutil.disk_usage(p.mountpoint)
                        dev_name = p.device.split('/')[-1]
                        match = re.match(r'([a-z]+|nvme[0-9]+n[0-9]+)', dev_name)
                        parent_dev = match.group(0) if match else dev_name
                        model = disk_models.get(parent_dev, "Disk")
                        disk.append({"aygit": p.device, "baglanti_noktasi": p.mountpoint, "yuzde": u.percent,
                                     "kullanilan": f"{u.used >> 30}G", "toplam": f"{u.total >> 30}G", "model": model})
                    except:
                        pass

                ssid = "Kablolu / Bilinmiyor"
                try:
                    out = subprocess.check_output("nmcli -t -f NAME connection show --active", shell=True, text=True,
                                                  stderr=subprocess.DEVNULL).strip()
                    if out:
                        ssid = out.split('\n')[0]
                    else:
                        ssid = subprocess.check_output("iwgetid -r", shell=True, text=True,
                                                       stderr=subprocess.DEVNULL).strip()
                except:
                    pass

                net_if = "Bilinmiyor"
                stats = psutil.net_if_stats()
                for i, d in stats.items():
                    if d.isup and i != 'lo': net_if = i; break

                self.bilgi_guncelle_sinyal.emit({
                    "cpu_yuzde": c_pct, "toplam_cpu_yuzde": sum(c_pct) / len(c_pct) if c_pct else 0,
                    "ram_yuzde": ram.percent, "ram_toplam": f"{ram.total >> 30} GB",
                    "ag_gonderilen": self.bayt_cevir(net.bytes_sent), "ag_alinan": self.bayt_cevir(net.bytes_recv),
                    "disk_bolumleri": disk, "konum_bilgisi": self.cached_konum,
                    "ag_ssid": ssid, "ag_arayuz": net_if, "cpu_sicaklik": self.get_temp(),
                    "dagitim_detay": self.get_distro(), "islemci_model": self.get_cpu_name(),
                    "ekran_karti_model": self.get_gpu_model(),
                    "batarya": self.get_battery()
                })
            except Exception as e:
                print(e)
            time.sleep(2)

    def get_distro(self):
        try:
            return subprocess.check_output(['lsb_release', '-ds'], text=True).strip()
        except:
            return platform.platform()

    def get_cpu_name(self):
        try:
            return [l.split(":")[1].strip() for l in open("/proc/cpuinfo") if "model name" in l][0]
        except:
            return "Bilinmiyor"