"""
RGPV Result Scraper — EXE Launcher
===================================
Yeh file PyInstaller ka entry point hai.
Frozen EXE mode mein:
  - Correct template/resource paths set karta hai
  - Flask server background thread mein start karta hai
  - Microsoft Edge automatically open karta hai
  - CSV files EXE ke saath wali directory mein save karta hai
"""

import sys
import os
import threading
import time
import webbrowser

# ── Path helpers ─────────────────────────────────────────────────
def resource_path(relative: str) -> str:
    """Bundled resource ka absolute path deta hai (works in EXE + dev)."""
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS          # PyInstaller ka temp extraction folder
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative)

def exe_dir() -> str:
    """EXE ke saath wali directory — CSV yahan save honge."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# ── Environment variables set karo BEFORE importing app ──────────
os.environ['RGPV_TEMPLATE_FOLDER'] = resource_path('templates')
os.environ['RGPV_BASE_DIR']        = exe_dir()

# Selenium Manager binary — frozen EXE mein sys._MEIPASS ke andar hoga
# SE_MANAGER_PATH set karne se Selenium apna bundled binary use karta hai
# aur internet se download karne ki koshish nahi karta
if getattr(sys, 'frozen', False):
    _sm_path = resource_path(
        os.path.join('selenium', 'webdriver', 'common', 'windows', 'selenium-manager.exe')
    )
    if os.path.exists(_sm_path):
        os.environ['SE_MANAGER_PATH'] = _sm_path
        print(f'[LAUNCHER] Selenium Manager found: {_sm_path}')
    else:
        print(f'[LAUNCHER] WARNING: selenium-manager.exe not found at {_sm_path}')

# Working directory bhi EXE folder set karo (msedgedriver fallback ke liye)
os.chdir(exe_dir())

# ── App import ───────────────────────────────────────────────────
from app import app   # noqa: E402

PORT = 5001
HOST = '127.0.0.1'

# ── Preload ddddocr at startup (background) ───────────────────
def _preload_ocr():
    """EXE start hote hi AI OCR engine load karo aur result file mein likho."""
    log_file = os.path.join(exe_dir(), 'ocr_startup.log')
    try:
        import PIL.Image
        if not hasattr(PIL.Image, 'ANTIALIAS'):
            PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
        import ddddocr
        ocr = ddddocr.DdddOcr(show_ad=False)
        msg = f'[OK] AI Captcha Solver (ddddocr) loaded: {type(ocr)}'
        print(f'[LAUNCHER] {msg}', flush=True)
        with open(log_file, 'w') as f:
            f.write(msg + '\n')
    except Exception as e:
        msg = f'[FAIL] ddddocr load error: {e}'
        print(f'[LAUNCHER] {msg}', flush=True)
        with open(log_file, 'w') as f:
            f.write(msg + '\n')

# ── Browser opener ───────────────────────────────────────────────
def _open_browser():
    """Flask ke ready hone ka thoda intezaar karo, phir browser kholo."""
    time.sleep(2.0)
    url = f'http://{HOST}:{PORT}'
    print(f'[LAUNCHER] Opening browser at {url}')
    webbrowser.open(url)

# ── Main ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('=' * 55)
    print('  RGPV Result Scraper')
    print('=' * 55)
    print(f'[LAUNCHER] Results will be saved to: {exe_dir()}')
    print(f'[LAUNCHER] Starting Flask server on http://{HOST}:{PORT} ...')
    print('[LAUNCHER] Please wait, browser will open automatically...')
    print('[LAUNCHER] Close this window to stop the server.')
    print('=' * 55)

    # AI OCR engine preload (background — startup ko slow nahi karega)
    threading.Thread(target=_preload_ocr, daemon=True).start()

    # Browser ko background mein kholna
    browser_thread = threading.Thread(target=_open_browser, daemon=True)
    browser_thread.start()

    # Flask server (blocking — process yahan ruka rahega)
    app.run(
        debug=False,
        use_reloader=False,
        port=PORT,
        host=HOST,
        threaded=True,
    )
