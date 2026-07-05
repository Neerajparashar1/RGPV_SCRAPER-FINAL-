# -*- mode: python ; coding: utf-8 -*-
# =============================================================
#  RGPV Result Scraper — PyInstaller Build Spec
#  Generates: dist/RGPV_Scraper.exe  (single standalone file)
#  Requirements: .venv1 with all packages + PyInstaller 6.x
# =============================================================

from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_dynamic_libs,
    collect_submodules,
    collect_all,
)

import os
import selenium

# ── Dynamic path resolution for Selenium Manager ──
selenium_path = os.path.dirname(selenium.__file__)
selenium_manager_path = os.path.join(selenium_path, 'webdriver', 'common', 'windows', 'selenium-manager.exe')

# ── Collect ddddocr (AI captcha solver) — ONNX models + binaries ──
ddddocr_datas, ddddocr_binaries, ddddocr_hidden = collect_all('ddddocr')

# ── Collect onnxruntime (ddddocr ka engine) ───────────────────────
onnx_datas,    onnx_binaries,    onnx_hidden    = collect_all('onnxruntime')

# ── All hidden imports ────────────────────────────────────────────
hidden_imports = [
    # Flask + Werkzeug
    'flask', 'flask.templating', 'flask.json',
    'werkzeug', 'werkzeug.serving', 'werkzeug.exceptions',
    'werkzeug.routing', 'werkzeug.utils', 'werkzeug.datastructures',
    'jinja2', 'jinja2.ext', 'jinja2.loaders', 'jinja2.environment',
    'click',

    # Selenium
    'selenium',
    'selenium.webdriver',
    'selenium.webdriver.edge',
    'selenium.webdriver.edge.service',
    'selenium.webdriver.edge.options',
    'selenium.webdriver.edge.webdriver',
    'selenium.webdriver.common.by',
    'selenium.webdriver.common.keys',
    'selenium.webdriver.common.alert',
    'selenium.webdriver.common.action_chains',
    'selenium.webdriver.support',
    'selenium.webdriver.support.ui',
    'selenium.webdriver.support.expected_conditions',
    'selenium.webdriver.support.select',
    'selenium.common.exceptions',
    'selenium.webdriver.remote.webelement',
    'selenium.webdriver.remote.command',

    # webdriver_manager (Edge auto-download fallback)
    'webdriver_manager',
    'webdriver_manager.microsoft',
    'webdriver_manager.core',
    'webdriver_manager.core.manager',
    'webdriver_manager.core.driver',
    'webdriver_manager.core.download_manager',
    'webdriver_manager.core.env_manager',
    'webdriver_manager.core.config',
    'webdriver_manager.core.logger',
    'webdriver_manager.core.os_manager',
    'webdriver_manager.core.file_manager',
    'webdriver_manager.core.http',

    # HTTP / Networking
    'requests', 'requests.adapters', 'requests.auth',
    'urllib3', 'urllib3.util', 'urllib3.util.retry',
    'certifi', 'charset_normalizer', 'idna',

    # HTML parsing
    'bs4', 'bs4.builder', 'bs4.formatter', 'soupsieve',

    # Image / OCR
    'PIL', 'PIL.Image', 'PIL.ImageEnhance',
    'PIL.ImageFilter', 'PIL.ImageOps',
    'pytesseract',

    # AI models
    *ddddocr_hidden,
    *onnx_hidden,

    # Excel / CSV
    'openpyxl', 'openpyxl.styles', 'openpyxl.utils',
    'openpyxl.workbook', 'openpyxl.worksheet',
    'xlrd',

    # Standard lib (sometimes missed)
    'csv', 'io', 're', 'base64', 'threading',
    'webbrowser', 'packaging', 'packaging.version',
    'cryptography', 'OpenSSL',

    # Self-Healing engine — Windows Registry path detection & Edge options
    'winreg',
    'selenium.webdriver.edge.options',
    'selenium.webdriver.edge.webdriver',
    'requests.exceptions',
]

a = Analysis(
    ['app_launcher.py'],
    pathex=['.'],
    binaries=[
        *ddddocr_binaries,
        *onnx_binaries,
    ],
    datas=[
        # ── UI template ──────────────────────────────────────
        ('templates', 'templates'),

        # ── UI static assets (CSS/JS) ─────────────────────────
        ('static', 'static'),

        # ── Pre-bundled msedgedriver.exe for offline reliability ──────────
        ('msedgedriver.exe', '.'),

        # ── Selenium Manager binary (auto-downloads EdgeDriver) ───────────
        # Without this, Selenium cannot find/download msedgedriver in frozen EXE
        (selenium_manager_path, 'selenium/webdriver/common/windows'),

        # ── AI captcha solver models ─────────────────────────
        *ddddocr_datas,

        # ── ONNX runtime resources ───────────────────────────
        *onnx_datas,
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Exclude heavy unused packages to reduce EXE size
    excludes=[
        'tkinter', 'matplotlib', 'scipy', 'pandas',
        'pytest', 'IPython', 'notebook', 'jupyter',
        'django', 'sqlalchemy', 'tornado',
        'PyQt5', 'PyQt6', 'wx',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RGPV_Scraper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,          # UPX compression (size kam karne ke liye)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,      # Console window: server status dikhata hai
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico',  # Agar icon add karna ho to uncomment karo
)
