# RGPV Result Scraper

A local desktop tool that automates bulk-downloading student exam results from the [RGPV](http://result.rgpv.ac.in/result/BErslt.aspx) result portal. It runs a small Flask web app in your browser, drives Microsoft Edge via Selenium to fetch each result page, solves the captcha automatically (AI OCR with a Tesseract fallback), and saves everything to CSV as it goes.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Building the standalone EXE](#building-the-standalone-exe)
- [Project Layout](#project-layout)
- [Notes](#notes)
- [License](#license)

## Features

- **Web UI**: A single-page app (`templates/index.html`) served locally — pick a branch and semester, start a session, and watch results stream in.
- **Automated captcha solving**: Tries an AI OCR model (`ddddocr`) first, falls back to Tesseract OCR, and allows manual entry if both fail.
- **Bulk scraping**: Iterates roll numbers automatically, handles "not found" / "wrong captcha" cases, and recovers from slow-loading pages.
- **Roll-sheet upload**: Upload an Excel/CSV of roll numbers (`/api/parse_rollsheet`) instead of relying on sequential numbering.
- **CSV export**: Results are saved incrementally to CSV, with support for resuming/updating previously-saved files and downloading them from the browser.
- **Auto-healing browser session**: Detects a crashed/closed Edge session and recovers without losing progress.

## Prerequisites

- Windows (this project targets Microsoft Edge + `msedgedriver.exe`; other OSes are not tested)
- Python 3.10+
- Microsoft Edge installed
- (Optional) [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed if you want the OCR fallback to work — `setup.bat` can install this for you

## Getting Started

1. Clone the repository:

   ```shell
   git clone https://github.com/Neerajparashar1/RGPV_SCRAPER-FINAL-.git
   cd RGPV_SCRAPER-FINAL-
   ```

2. Run the setup script — it creates a virtual environment and installs dependencies:

   ```shell
   setup.bat
   ```

   Or, to set up manually:

   ```shell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

1. Start the app:

   ```shell
   run.bat
   ```

   Or manually, with the virtual environment activated:

   ```shell
   python app.py
   ```

2. Open `http://127.0.0.1:5001` in your browser (opens automatically when using the packaged EXE).
3. Select a branch and semester, start a session, and let it solve captchas and scrape results automatically.
4. Download the resulting CSV from the "Previous Files" panel once scraping finishes.

## Building the standalone EXE

The project ships with a PyInstaller spec (`build_exe.spec`) and `build.bat` to package the app (including `app_launcher.py`, the bundled `msedgedriver.exe`, and OCR models) into a single Windows executable:

```shell
build.bat
```

The output EXE is written to `dist/`.

## Project Layout

- `app.py` — Flask app: routes, Selenium/browser management, captcha solving, scraping, and CSV I/O.
- `app_launcher.py` — Entry point used by the packaged EXE (sets up paths, preloads OCR, opens the browser, then runs `app.py`'s Flask app).
- `templates/index.html` — the web UI.
- `build_exe.spec`, `build.bat` — PyInstaller packaging.
- `setup.bat`, `run.bat` — local dev environment setup and run scripts.
- `msedgedriver.exe` — bundled Edge WebDriver used as a fallback if Selenium Manager can't resolve one automatically.

Scraped result CSVs (e.g. per-branch folders) are written into the working directory at runtime and are not tracked in this repository — see `.gitignore`.

## Notes

- The RGPV result portal's structure can change over time; if scraping stops working, the HTML selectors/XPaths in `app.py` may need updating.
- This tool is intended for personal/academic use to retrieve results in bulk faster than the manual portal UI allows.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
