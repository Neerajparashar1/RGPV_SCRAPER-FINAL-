import os
import sys

# Wrap standard streams to prevent background console buffer writing failures on Windows
class SafeStream:
    def __init__(self, original_stream):
        self.stream = original_stream

    def write(self, data):
        try:
            if self.stream is not None:
                self.stream.write(data)
        except OSError as e:
            if e.errno in (9, 22, 32):  # Bad file descriptor, Invalid argument, Broken pipe
                pass
            else:
                raise
        except Exception:
            pass

    def flush(self):
        try:
            if self.stream is not None:
                self.stream.flush()
        except OSError as e:
            if e.errno in (9, 22, 32):
                pass
            else:
                raise
        except Exception:
            pass

    def __getattr__(self, name):
        if self.stream is None:
            raise AttributeError(f"'NoneType' object has no attribute '{name}'")
        return getattr(self.stream, name)

sys.stdout = SafeStream(sys.stdout)
sys.stderr = SafeStream(sys.stderr)

import base64
import time
import re
import csv
import io
import requests
from flask import Flask, render_template, request, jsonify, send_file
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoAlertPresentException, InvalidSessionIdException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait






def get_base_dir() -> str:
    """
    Returns the base directory for CSV storage.
    If running as a frozen EXE, uses the directory of the executable.
    Otherwise, uses the directory of the app.py file.
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.environ.get('RGPV_BASE_DIR', os.path.dirname(os.path.abspath(__file__)))


def get_edge_service() -> Service:
    """
    Returns a Selenium Service for Edge.
    Priority order:
      1. Bundled msedgedriver.exe inside EXE (sys._MEIPASS) — offline, instant
      2. msedgedriver.exe next to EXE — user-placed manual driver
      3. Selenium Manager auto-download (needs internet)
      4. WebDriver Manager fallback (needs internet)
    """
    # ── 1. Frozen EXE: use bundled msedgedriver.exe ────────────────────────
    if getattr(sys, 'frozen', False):
        bundled_driver = os.path.join(sys._MEIPASS, 'msedgedriver.exe')
        if os.path.exists(bundled_driver):
            print(f'[SYSTEM LOGGER] Using bundled msedgedriver from EXE bundle.')
            try:
                return Service(executable_path=bundled_driver)
            except Exception as e:
                print(f'[SYSTEM LOGGER] Bundled driver failed: {e}. Trying fallbacks...')

    # ── 2. msedgedriver.exe placed next to EXE (manual override) ──────────
    local_path = os.path.abspath('msedgedriver.exe')
    if os.path.exists(local_path):
        try:
            print(f'[SYSTEM LOGGER] Using local msedgedriver.exe from EXE directory.')
            return Service(executable_path=local_path)
        except Exception as local_err:
            print(f'[SYSTEM LOGGER] Local msedgedriver failed: {local_err}')

    # ── 3. Selenium Manager auto-detect (needs internet on first run) ──────
    try:
        return Service()
    except Exception as e:
        print(f'[SYSTEM LOGGER] Selenium Manager service initialization failed: {e}')

    # ── 4. Fallback: webdriver-manager auto-download ───────────────────────
    try:
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        return Service(EdgeChromiumDriverManager().install())
    except Exception as manager_err:
        print(f'[SYSTEM LOGGER] Webdriver manager fallback failed: {manager_err}')
        raise RuntimeError(
            'All Edge driver initialization methods failed completely.\n'
            'Please ensure Microsoft Edge is installed on your system.'
        )


def find_edge_binary():
    try:
        import winreg
        for hkey in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            try:
                with winreg.OpenKey(hkey, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe") as key:
                    path, _ = winreg.QueryValueEx(key, "")
                    if os.path.exists(path):
                        return path
            except:
                pass
    except ImportError:
        pass
    common_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe")
    ]
    for p in common_paths:
        if os.path.exists(p):
            return p
    return None


def check_driver_health():
    global driver, session_program
    if not driver:
        return False
    try:
        # Check if browser window is responsive
        _ = driver.title
        
        # Check if browser is on the correct results page or the program select page
        current_url = driver.current_url
        if "ProgramSelect.aspx" in current_url:
            return True
            
        if session_program == "MCA":
            if "MCArslt.aspx" not in current_url:
                print(f"[SYSTEM LOGGER] Driver URL check failed: current URL '{current_url}' does not contain 'MCArslt.aspx'. Triggering recovery...")
                return False
        else:
            if "BErslt.aspx" not in current_url:
                print(f"[SYSTEM LOGGER] Driver URL check failed: current URL '{current_url}' does not contain 'BErslt.aspx'. Triggering recovery...")
                return False
                
        return True
    except Exception as e:
        print(f"[SYSTEM LOGGER] Driver health check failed: {e}")
        return False


def reset_results_form(driver, session_program):
    """
    Resets the results form by finding and clicking the 'Reset' or 'Back' button,
    or falls back to a clean page load if not found.
    """
    print("[SYSTEM LOGGER] reset_results_form() called.")
    try:
        # Dismiss any active alert first
        dismiss_alerts_safely(driver)
        
        # 1. Try finding Reset button using common locators
        reset_locators = [
            (By.ID, "ctl00_ContentPlaceHolder1_btnReset"),
            (By.ID, "ctl00_ContentPlaceHolder1_btnreset"),
            (By.XPATH, "//input[@value='Reset']"),
            (By.XPATH, "//input[@value='reset']"),
            (By.XPATH, "//input[contains(@id, 'Reset')]"),
            (By.XPATH, "//input[contains(@id, 'reset')]"),
            (By.XPATH, "//button[contains(text(), 'Reset')]"),
            (By.XPATH, "//button[contains(text(), 'reset')]"),
            (By.XPATH, "//a[contains(text(), 'Reset')]"),
            (By.XPATH, "//a[contains(text(), 'reset')]"),
            # Also check for "Back" button or link as fallback
            (By.XPATH, "//a[contains(@href, 'ProgramSelect.aspx')]"),
            (By.XPATH, "//a[contains(text(), 'Back')]")
        ]
        
        clicked = False
        for by, value in reset_locators:
            try:
                elem = driver.find_element(by, value)
                if elem.is_displayed() and elem.is_enabled():
                    # Scroll into view and click
                    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                    time.sleep(0.1)
                    elem.click()
                    print(f"[SYSTEM LOGGER] Reset/Back button clicked successfully via {by}='{value}'")
                    clicked = True
                    break
            except Exception:
                pass
                
        if not clicked:
            print("[SYSTEM LOGGER] Reset button not found or not clickable. Executing JS reset fallback...")
            # Try to trigger the postback directly via JS
            try:
                driver.execute_script("if(window.__doPostBack) { __doPostBack('ctl00$ContentPlaceHolder1$btnReset',''); }")
                clicked = True
                print("[SYSTEM LOGGER] JS __doPostBack('ctl00$ContentPlaceHolder1$btnReset','') triggered.")
            except Exception as js_err:
                print(f"[SYSTEM LOGGER] JS postback reset failed: {js_err}")
                
        if not clicked:
            # Fallback to driver.get if reset button was completely missing or failed
            print("[SYSTEM LOGGER] No reset button available. Falling back to clean page reload...")
            url = "http://result.rgpv.ac.in/Result/MCArslt.aspx" if session_program == "MCA" else "http://result.rgpv.ac.in/Result/BErslt.aspx"
            driver.get(url)
            
        # Post-reset/reload checks: Wait for the main semester dropdown to be clickable again
        dismiss_alerts_safely(driver)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_drpSemester"))
        )
        print("[SYSTEM LOGGER] Form reset/reload state verified successfully. Waiting 0.8s for portal readiness...")
        time.sleep(0.8)
        
    except Exception as e:
        print(f"[SYSTEM LOGGER] Form reset/reload failed: {e}. Attempting recovery page reload...")
        try:
            url = "http://result.rgpv.ac.in/Result/MCArslt.aspx" if session_program == "MCA" else "http://result.rgpv.ac.in/Result/BErslt.aspx"
            driver.get(url)
            dismiss_alerts_safely(driver)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_drpSemester"))
            )
        except Exception as recovery_err:
            print(f"[SYSTEM LOGGER] Recovery page reload failed: {recovery_err}")
            raise recovery_err


def heal_browser_session():
    global driver, session_program, session_branch_id, session_sem, session_prefix, last_captcha_src
    last_captcha_src = None
    print("[SYSTEM LOGGER] Browser window closed or unresponsive. Initiating self-healing recovery...")
    try:
        if driver:
            try:
                driver.quit()
            except:
                pass
    except:
        pass

    try:
        service = get_edge_service()
        from selenium.webdriver.edge.options import Options as EdgeOptions
        options = EdgeOptions()
        edge_bin = find_edge_binary()
        if edge_bin:
            print(f"[SYSTEM LOGGER] Auto-detected Edge binary location during recovery: {edge_bin}")
            options.binary_location = edge_bin
        
        options.add_argument("--disable-gpu")
        
        new_driver = webdriver.Edge(service=service, options=options)
        new_driver.implicitly_wait(3)
        new_driver.maximize_window()
        new_driver.get("http://result.rgpv.ac.in/Result/ProgramSelect.aspx")
        dismiss_alerts_safely(new_driver)

        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        if session_program == "MCA":
            print("[SYSTEM LOGGER] MCA selected in self-healing. Clicking MCA program...")
            try:
                WebDriverWait(new_driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "radlstProgram_17"))
                ).click()
            except Exception:
                WebDriverWait(new_driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "radlstProgram_2"))
                ).click()
        else:
            print("[SYSTEM LOGGER] B.Tech selected in self-healing. Clicking B.Tech program...")
            WebDriverWait(new_driver, 10).until(
                EC.element_to_be_clickable((By.ID, "radlstProgram_1"))
            ).click()
            
        if session_program == "MCA":
            WebDriverWait(new_driver, 15).until(EC.url_contains("MCArslt.aspx"))
        else:
            WebDriverWait(new_driver, 15).until(EC.url_contains("BErslt.aspx"))
            
        time.sleep(1.0)
        dismiss_alerts_safely(new_driver)
        
        driver = new_driver
        print("[SYSTEM LOGGER] Browser self-healing recovery successful!")
        return True
    except Exception as recovery_err:
        print(f"[SYSTEM LOGGER] Browser self-healing recovery failed: {recovery_err}")
        return False



# When running as frozen EXE, template folder is inside sys._MEIPASS
_template_folder = os.environ.get('RGPV_TEMPLATE_FOLDER', 'templates')
app = Flask(__name__, template_folder=_template_folder)

# ── Force all errors to return JSON (never HTML) ──────────────
app.config['PROPAGATE_EXCEPTIONS'] = False

from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Return JSON for all HTTP errors (404, 413, 405, etc.) instead of HTML."""
    return jsonify({"ok": False, "error": f"{e.code} {e.name}: {e.description}"}), e.code

@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON for all unhandled Python exceptions instead of HTML."""
    if isinstance(e, HTTPException):
        return handle_http_exception(e)
    import traceback
    traceback.print_exc()
    return jsonify({"ok": False, "error": f"Server error: {str(e)}"}), 500

# ── Global driver state ──────────────────────────────────────
driver = None
session_sem = None
session_prefix = None
session_filename = None
session_subjects = []  # Pre-defined subjects to match against
session_wait_mode = "dynamic"
session_wait_value = 40
last_captcha_src = None
session_wait_baseline = 40
session_program = "BTech"
session_branch_id = None
dddd_ocr_engine = None
session_speed_mode = "normal"
session_submit_delay = 1.5
session_reset_delay = 0.5

SPEED_CONFIGS = {
    "slow": {
        "settle": 0.6,
        "roll_enter": 0.45,
        "captcha_enter": 0.6,
        "scroll": 0.3,
        "post_submit": 5.0
    },
    "normal": {
        "settle": 0.4,
        "roll_enter": 0.3,
        "captcha_enter": 0.4,
        "scroll": 0.2,
        "post_submit": 3.5
    },
    "fast": {
        "settle": 0.2,
        "roll_enter": 0.15,
        "captcha_enter": 0.2,
        "scroll": 0.1,
        "post_submit": 2.0
    },
    "turbo": {
        "settle": 0.1,
        "roll_enter": 0.08,
        "captcha_enter": 0.1,
        "scroll": 0.05,
        "post_submit": 0.8
    }
}


# ── Roll List Mode (Excel/CSV Upload) ─────────────────────────
session_roll_list = []        # Full roll numbers from uploaded sheet
session_roll_list_idx = 0     # Current index in roll list
session_mode = "range"        # "range" (manual) or "list" (excel upload)

def get_dddd_ocr():
    global dddd_ocr_engine
    if dddd_ocr_engine is None:
        try:
            import PIL.Image
            if not hasattr(PIL.Image, 'ANTIALIAS'):
                PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
            import ddddocr
            # Simple standard load — works in both normal Python and frozen EXE mode.
            # PyInstaller correctly sets __file__ for bundled packages, so ddddocr
            # finds its ONNX models at sys._MEIPASS/ddddocr/ automatically.
            dddd_ocr_engine = ddddocr.DdddOcr(show_ad=False)
            print("[SYSTEM LOGGER] Deep Learning AI Captcha Solver loaded successfully!")
        except Exception as e:
            print(f"[SYSTEM LOGGER] Deep Learning AI Captcha Solver load failed: {e}. Falling back to Tesseract.")
            dddd_ocr_engine = False
    return dddd_ocr_engine if dddd_ocr_engine else None


BRANCHES = {
    "1": {
        "name": "Data Science",
        "prefix": "0905CD",
        "file": "CD",
        "subjects": {
            "1": ["BT201[T]", "BT102[T]", "BT203[T]", "BT204[T]", "BT205[T]", "BT201[P]", "BT203[P]", "BT204[P]", "BT205[P]", "BT206[P]"],
            "2": ["BT201", "BT202", "BT203", "BT204", "BT205"],
            "3": ["CD301", "CD302", "CD303", "CD304", "CD305", "CD303[P]", "CD304[P]", "CD305[P]", "CD306[P]", "BT107[P]"],
            "4": ["CD401[T]", "CD402[T]", "CD403[T]", "CD404[T]", "CD405[T]", "CD402[P]", "CD403[P]", "CD404[P]", "CD405[P]", "CD406[P]"],
            "5": ["CD501", "CD502", "CD503", "CD504", "BT407[P]", "CD501[P]", "CD502[P]", "CD505[P]", "CD506[P]", "CD508[P]"],
            "6": ["CD601[T]", "CD602[T]", "CD603[T]", "CD604[T]", "CD601[P]", "CD602[P]", "CD605[P]", "CD606[P]", "CD608"],
            "7": ["CD701", "CD702", "CD703", "CD704", "CD705"],
            "8": ["CD801", "CD802", "CD803", "CD804", "CD805"]
        }
    },
    "2": {
        "name": "AIML",
        "prefix": "0905AL",
        "file": "AIML",
        "subjects": {
            "1": ["BT201[T]", "BT102[T]", "BT203[T]", "BT204[T]", "BT205[T]", "BT201[P]", "BT203[P]", "BT204[P]", "BT205[P]", "BT206[P]"],
            "2": ["BT201", "BT202", "BT203", "BT204", "BT205"],
            "3": ["AL301", "AL302", "AL303", "AL304", "AL305", "AL303[P]", "AL304[P]", "AL305[P]", "AL306[P]", "BT107[P]"],
            "4": ["AL401[T]", "AL402[T]", "AL403[T]", "AL404[T]", "AL405[T]", "AL402[P]", "AL403[P]", "AL404[P]", "AL405[P]", "AL406[P]"],
            "5": ["AL501", "AL502", "AL503", "AL504", "BT407[P]", "AL501[P]", "AL502[P]", "AL505[P]", "AL506[P]", "AL508[P]"],
            "6": ["AL601[T]", "AL602[T]", "AL603[T]", "AL604[T]", "AL601[P]", "AL602[P]", "AL605[P]", "AL606[P]", "AL608"],
            "7": ["AL701", "AL702", "AL703", "AL704", "AL705"],
            "8": ["AL801", "AL802", "AL803", "AL804", "AL805"]
        }
    },
    "3": {
        "name": "CS-Core",
        "prefix": "0905CS",
        "file": "CS",
        "subjects": {
            "1": ["BT101[T]", "BT102[T]", "BT103[T]", "BT104[T]", "BT105[T]", "BT101[P]", "BT103[P]", "BT104[P]", "BT105[P]", "BT106[P]", "BT108[P]"],
            "2": ["BT201", "BT202", "BT203", "BT204", "BT205"],
            "3": ["ES301", "CS302", "CS303", "CS304", "CS305", "CS303[P]", "CS304[P]", "CS305[P]", "CS306[P]", "BT107[P]"],
            "4": ["CS401[T]", "CS402[T]", "CS403[T]", "CS404[T]", "CS405[T]", "CS402[P]", "CS403[P]", "CS404[P]", "CS405[P]", "CS406[P]"],
            "5": ["CS501", "CS502", "CS503", "CS504", "BT407[P]", "CS501[P]", "CS502[P]", "CS505[P]", "CS506[P]", "CS508[P]"],
            "6": ["CS601[T]", "CS602[T]", "CS603[T]", "CS604[T]", "CS601[P]", "CS602[P]", "CS605[P]", "CS606[P]", "CS608"],
            "7": ["CS701", "CS702", "CS703", "CS704", "CS705"],
            "8": ["CS801", "CS802", "CS803", "CS804", "CS805"]
        }
    },
    "4": {
        "name": "IT (Regular)",
        "prefix": "0905IT",
        "file": "IT",
        "subjects": {
            "1": ["BT101[T]", "BT102[T]", "BT103[T]", "BT104[T]", "BT105[T]", "BT101[P]", "BT103[P]", "BT104[P]", "BT105[P]", "BT106[P]", "BT108[P]"],
            "2": ["BT201", "BT202", "BT203", "BT204", "BT205"],
            "3": ["ES301", "IT302", "IT303", "IT304", "IT305", "IT303[P]", "IT304[P]", "IT305[P]", "IT306[P]", "BT107[P]"],
            "4": ["IT401[T]", "IT402[T]", "IT403[T]", "IT404[T]", "IT405[T]", "IT402[P]", "IT403[P]", "IT404[P]", "IT405[P]", "IT406[P]"],
            "5": ["IT501", "IT502", "IT503", "IT504", "BT408[P]", "IT501[P]", "IT502[P]", "IT505[P]", "IT506[P]", "IT508[P]"],
            "6": ["IT601[T]", "IT602[T]", "IT603[T]", "IT604[T]", "IT601[P]", "IT602[P]", "IT605[P]", "IT606[P]", "IT608"],
            "7": ["IT701", "IT702", "IT703", "IT704", "IT705"],
            "8": ["IT801", "IT802", "IT803", "IT804", "IT805"]
        }
    },
    "5": {
        "name": "Cyber Security",
        "prefix": "0905CY",
        "file": "CY",
        "subjects": {
            "1": ["BT201[T]", "BT102[T]", "BT203[T]", "BT204[T]", "BT205[T]", "BT201[P]", "BT203[P]", "BT204[P]", "BT205[P]", "BT206[P]"],
            "2": ["BT201", "BT202", "BT203", "BT204", "BT205"],
            "3": ["CY301", "CY302", "CY303", "CY304", "CY305", "CY303[P]", "CY304[P]", "CY305[P]", "CY306[P]", "BT107[P]"],
            "4": ["CY401[T]", "CY402[T]", "CY403[T]", "CY404[T]", "CY405[T]", "CY402[P]", "CY403[P]", "CY404[P]", "CY405[P]", "CY406[P]"],
            "5": ["CY501", "CY502", "CY503", "CY504", "BT407[P]", "CY501[P]", "CY502[P]", "CY505[P]", "CY506[P]", "CY508[P]"],
            "6": ["CY601[T]", "CY602[T]", "CY603[T]", "CY604[T]", "CY601[P]", "CY602[P]", "CY605[P]", "CY606[P]", "CY608"],
            "7": ["CY701", "CY702", "CY703", "CY704", "CY705"],
            "8": ["CY801", "CY802", "CY803", "CY804", "CY805"]
        }
    },
    "6": {
        "name": "IOT",
        "prefix": "0905IO",
        "file": "IO",
        "subjects": {
            "1": ["BT201[T]", "BT102[T]", "BT203[T]", "BT204[T]", "BT205[T]", "BT201[P]", "BT203[P]", "BT204[P]", "BT205[P]", "BT206[P]"],
            "2": ["BT201", "BT202", "BT203", "BT204", "BT205"],
            "3": ["IO301", "IO302", "IO303", "IO304", "IO305", "IO303[P]", "IO304[P]", "IO305[P]", "IO306[P]", "BT107[P]"],
            "4": ["IO401[T]", "IO402[T]", "IO403[T]", "IO404[T]", "IO405[T]", "IO402[P]", "IO403[P]", "IO404[P]", "IO405[P]", "IO406[P]"],
            "5": ["IO501", "IO502", "IO503", "IO504", "BT407[P]", "IO501[P]", "IO502[P]", "IO505[P]", "IO506[P]", "IO508[P]"],
            "6": ["IO601[T]", "IO602[T]", "IO603[T]", "IO604[T]", "IO601[P]", "IO602[P]", "IO605[P]", "IO606[P]", "IO608"],
            "7": ["IO701", "IO702", "IO703", "IO704", "IO705"],
            "8": ["IO801", "IO802", "IO803", "IO804", "IO805"]
        }
    },
    "mca": {
        "name": "MCA",
        "prefix": "0905CA",
        "file": "MCA",
        "subjects": {
            "1": ["MCA101", "MCA102", "MCA103", "MCA104", "MCA105", "MCA101[P]", "MCA102[P]", "MCA103[P]", "MCA105[P]"],
            "2": ["MCA201", "MCA202", "MCA203", "MCA204", "MCA205", "MCA201[P]", "MCA202[P]", "MCA203[P]", "MCA205[P]"],
            "3": ["MCA301", "MCA302", "MCA303", "MCA304", "MCA305", "MCA301[P]", "MCA302[P]", "MCA303[P]", "MCA305[P]"],
            "4": ["MCA401", "MCA402", "MCA403", "MCA404", "MCA405", "MCA401[P]", "MCA402[P]", "MCA403[P]", "MCA405[P]"]
        }
    }
}


def dismiss_alerts_safely(driver_instance):
    """
    Dismisses all active JavaScript alert popups on the current page.
    """
    if not driver_instance:
        return
    for _ in range(5):
        try:
            alert = driver_instance.switch_to.alert
            alert_text = alert.text
            print(f"[SYSTEM LOGGER] Auto-dismissed blocking portal alert: '{alert_text}'")
            alert.accept()
            time.sleep(0.5)
        except Exception:
            break


# ── Start browser session ─────────────────────────────────────
@app.route("/api/start", methods=["POST"])
def start_session():
    global driver, session_sem, session_prefix, session_filename, session_subjects
    global session_roll_list, session_roll_list_idx, session_mode
    global session_wait_mode, session_wait_value, session_wait_baseline
    global session_program, session_branch_id, last_captcha_src, session_speed_mode, session_submit_delay, session_reset_delay

    last_captcha_src = None

    try:
        data = request.json
        if not data:
            return jsonify({"ok": False, "error": "Invalid JSON request payload"})
        program = data.get("program", "BTech").strip()
        branch_id = data.get("branch")
        sem = data.get("sem", "").strip()
        year = data.get("year", "").strip()
        custom_prefix = data.get("custom_prefix", "").strip()
        
        # Read user-configured wait parameters
        session_wait_mode = data.get("wait_mode", "dynamic").strip().lower()
        session_wait_value = float(data.get("wait_value", 25.0))
        session_speed_mode = data.get("speed_mode", "normal").strip().lower()
        if session_speed_mode not in SPEED_CONFIGS:
            session_speed_mode = "normal"
        session_submit_delay = float(data.get("submit_delay", 1.5))
        session_reset_delay = float(data.get("reset_delay", 0.5))


        # ── Roll List Mode (from Excel upload) ────────────────
        roll_list = data.get("roll_list", None)  # Full roll numbers list
        if roll_list and isinstance(roll_list, list) and len(roll_list) > 0:
            session_mode = "list"
            session_roll_list = [str(r).strip().upper() for r in roll_list if str(r).strip()]
            session_roll_list_idx = 0
            # Detect prefix from the first roll number if not manually provided
            if not custom_prefix and session_roll_list:
                first_roll = session_roll_list[0]
                m = re.match(r'^([0-9]{4}[A-Z]{2,4}[0-9]{2})(?:[0-9]{3,4}|3D[0-9]{2})$', first_roll)
                if m:
                    custom_prefix = m.group(1)
        else:
            session_mode = "range"
            session_roll_list = []
            session_roll_list_idx = 0

        if branch_id not in BRANCHES:
            return jsonify({"ok": False, "error": "Invalid branch"})
        if not sem:
            return jsonify({"ok": False, "error": "Semester is required"})

        session_sem = sem
        session_program = program
        session_branch_id = branch_id
        session_wait_baseline = session_wait_value
        base_prefix = BRANCHES[branch_id]["prefix"]

        # Use manual custom prefix, selected admission year, or guess dynamically based on standard progression
        if custom_prefix:
            session_prefix = custom_prefix.upper()
        elif year:
            session_prefix = base_prefix + year
        else:
            try:
                sem_num = int(sem)
                # Standard guess (Even Sem in 2026): Sem 2 -> 25, Sem 4 -> 24, Sem 6 -> 23, Sem 8 -> 22
                guessed_year = 26 - (sem_num + 1) // 2
                session_prefix = base_prefix + f"{guessed_year:02d}"
            except Exception:
                session_prefix = base_prefix + "24"

        # Construct and sanitize safe absolute filename
        raw_filename = f'{BRANCHES[branch_id]["file"]}_sem{sem}_results.csv'
        clean_filename = raw_filename.strip().replace("\r", "").replace("\n", "")
        clean_filename = re.sub(r'[\\/*?:"<>|]', "", clean_filename)
        
        # Use EXE directory for CSV output when running as frozen binary
        base_dir = get_base_dir()
        
        # Map branch to folder name:
        # - CS-Core (Branch 3) -> CS_Core
        # - IT (Branch 4) -> IT
        # - AIML (Branch 2), CD (Branch 1), CY (Branch 5), IOT (Branch 6) -> CS_Emerging
        # - MCA (Branch 'mca') -> MCA
        folder_name = ""
        if branch_id == "3":
            folder_name = "CS_Core"
        elif branch_id == "4":
            folder_name = "IT"
        elif branch_id in ["1", "2", "5", "6"]:
            folder_name = "CS_Emerging"
        elif branch_id == "mca":
            folder_name = "MCA"
            
        if folder_name:
            folder_path = os.path.join(base_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            session_filename = os.path.abspath(os.path.join(folder_path, clean_filename))
        else:
            session_filename = os.path.abspath(os.path.join(base_dir, clean_filename))

        # Fetch pre-defined subjects for this branch and semester
        raw_session_subs = BRANCHES[branch_id].get("subjects", {}).get(sem, [])
        session_subjects = []
        for s in raw_session_subs:
            s_upper = s.upper()
            base = re.sub(r'[\(\[\{][PT][\)\]\}]', '', s).strip()
            if "[P]" in s_upper or "(P)" in s_upper or s_upper.endswith("P"):
                session_subjects.append(base + "[P]")
            else:
                session_subjects.append(base + "[T]")


        # ── LIST MODE (Excel Upload): Dynamic Subject Detection ────────────────
        # When processing roll numbers from an uploaded Excel sheet, we do NOT
        # use pre-defined subject lists. Instead, subjects are identified
        # dynamically from each student's result page on the portal.
        # This correctly handles:
        #   - Branch-changed students (old roll number, new branch subjects)
        #   - Mixed-branch Excel sheets
        #   - Any student whose subjects differ from the session branch
        if session_mode == "list":
            session_subjects = []
            print("[SYSTEM LOGGER] List mode: subjects will be detected dynamically from portal results.")

        # Create or dynamically upgrade CSV with structured subject columns
        if not os.path.exists(session_filename):
            header_row = ["Roll Number", "Name"] + session_subjects + ["SGPA", "CGPA", "Result"]
            try:
                with open(session_filename, "w", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerow(header_row)
            except PermissionError:
                return jsonify({"ok": False, "error": f"Permission denied creating '{clean_filename}'. Please close the CSV file if it is open in Excel or another program."})
            except Exception as file_err:
                print(f"[SYSTEM LOGGER] File create failed for '{session_filename}': {file_err}")
                import traceback
                traceback.print_exc()
                return jsonify({"ok": False, "error": f"Failed to create CSV file. Error: {file_err}"})
        else:
            try:
                with open(session_filename, "r", newline="", encoding="utf-8") as f:
                    reader = list(csv.reader(f))
                if reader:
                    existing_header = reader[0]
                    expected_header = ["Roll Number", "Name"] + session_subjects + ["SGPA", "CGPA", "Result"]
                    if existing_header != expected_header:
                        print(f"[SYSTEM LOGGER] Upgrading existing CSV header in '{session_filename}' to match current subject list.")
                        upgraded_rows = [expected_header]
                        for row in reader[1:]:
                            if len(row) < len(expected_header):
                                padded_row = row + [""] * (len(expected_header) - len(row))
                                upgraded_rows.append(padded_row)
                            else:
                                upgraded_rows.append(row[:len(expected_header)])
                        with open(session_filename, "w", newline="", encoding="utf-8") as f:
                            csv.writer(f).writerows(upgraded_rows)
            except PermissionError:
                return jsonify({"ok": False, "error": f"Permission denied accessing '{clean_filename}'. Please close the CSV file if it is open in Excel or another program."})
            except Exception as file_err:
                print(f"[SYSTEM LOGGER] CSV upgrade failed for '{session_filename}': {file_err}")

        if driver:
            try:
                driver.quit()
            except:
                pass

        try:
            service = get_edge_service()
            from selenium.webdriver.edge.options import Options as EdgeOptions
            options = EdgeOptions()
            edge_bin = find_edge_binary()
            if edge_bin:
                print(f"[SYSTEM LOGGER] Auto-detected Edge binary location: {edge_bin}")
                options.binary_location = edge_bin
            new_driver = webdriver.Edge(service=service, options=options)
        except Exception as e:
            print(f"[SYSTEM LOGGER] Primary Edge driver start failed: {e}. Attempting self-healing driver repair...")
            local_path = os.path.abspath("msedgedriver.exe")
            if os.path.exists(local_path):
                try:
                    # Rename the outdated local driver to prevent future conflicts
                    backup_path = os.path.abspath("msedgedriver_old.exe")
                    if os.path.exists(backup_path):
                        os.remove(backup_path)
                    os.rename(local_path, backup_path)
                    print("[SYSTEM LOGGER] Outdated msedgedriver.exe moved out of the way successfully!")
                except Exception as file_err:
                    print(f"[SYSTEM LOGGER] Failed to move local driver: {file_err}")

            try:
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                fallback_service = Service(executable_path=EdgeChromiumDriverManager().install())
                from selenium.webdriver.edge.options import Options as EdgeOptions
                options = EdgeOptions()
                edge_bin = find_edge_binary()
                if edge_bin:
                    options.binary_location = edge_bin
                new_driver = webdriver.Edge(service=fallback_service, options=options)
            except Exception as inner_e:
                err_msg = (
                    f"Edge driver initialization failed completely.\n"
                    f"Primary method error: {e}\n"
                    f"Fallback method error: {inner_e}\n\n"
                    "Please make sure Microsoft Edge is installed. Outdated driver was moved, but auto-download failed."
                )
                return jsonify({"ok": False, "error": err_msg})

        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        new_driver.implicitly_wait(3)
        new_driver.maximize_window()
        new_driver.get("http://result.rgpv.ac.in/Result/ProgramSelect.aspx")
        
        # Check and dismiss any alert on load
        dismiss_alerts_safely(new_driver)

        # Select and click correct program radio option dynamically
        if program == "MCA":
            print("[SYSTEM LOGGER] MCA selected. Clicktargeting MCA (2-Year) program...")
            try:
                # Primary choice: M.C.A. (2-Year) - radlstProgram_17
                WebDriverWait(new_driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "radlstProgram_17"))
                ).click()
            except Exception as e:
                print(f"[SYSTEM LOGGER] Primary MCA (2-Year) click failed: {e}. Falling back to standard M.C.A. (radlstProgram_2)...")
                WebDriverWait(new_driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "radlstProgram_2"))
                ).click()
        else:
            print("[SYSTEM LOGGER] B.Tech selected. Clicktargeting B.Tech...")
            WebDriverWait(new_driver, 10).until(
                EC.element_to_be_clickable((By.ID, "radlstProgram_1"))
            ).click()
        
        # Wait up to 10 seconds for the page to redirect to correct grading results form
        print("[SYSTEM LOGGER] Waiting for redirection to correct results page...")
        if program == "MCA":
            WebDriverWait(new_driver, 15).until(
                EC.url_contains("MCArslt.aspx")
            )
        else:
            WebDriverWait(new_driver, 15).until(
                EC.url_contains("BErslt.aspx")
            )
        print("[SYSTEM LOGGER] Redirection successful!")
        time.sleep(1.0)
        
        # Check and dismiss any alert on redirect
        dismiss_alerts_safely(new_driver)

        globals()["driver"] = new_driver
        return jsonify({
            "ok": True,
            "prefix": session_prefix,
            "message": f"Browser started for {BRANCHES[branch_id]['name']} sem {sem} with prefix {session_prefix}"
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"ok": False, "error": f"Start session failed: {e}"})


# ── Get captcha image as base64 ───────────────────────────────
@app.route("/api/captcha", methods=["GET"])
def get_captcha():
    global driver, session_wait_value, last_captcha_src
    if not check_driver_health():
        success = heal_browser_session()
        if not success:
            return jsonify({"ok": False, "error": "Browser window was closed and self-healing recovery failed. Please check Edge browser installation."})

    try:
        roll = request.args.get("roll", "").strip()
        full_roll_mode = request.args.get("full", "0") == "1"  # full=1 means roll is already the complete roll number
        if not roll:
            return jsonify({"ok": False, "error": "Roll suffix is required"})

        if full_roll_mode:
            roll_number = roll  # Already full roll number from Excel list
        else:
            roll_upper = roll.upper()
            if session_prefix and (roll_upper.startswith(session_prefix.upper()) or re.match(r'^[0-9]{4}[A-Z]{2,4}[0-9]{2}(?:[0-9]{3,4}|3D[0-9]{2})$', roll_upper)):
                roll_number = roll_upper
            else:
                roll_number = session_prefix + roll

        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            print(f"[SYSTEM LOGGER] Waiting for drpSemester to load for roll {roll_number}...")
            
            # Dismiss any blocking alerts first
            dismiss_alerts_safely(driver)

            # If on ProgramSelect.aspx, click B.Tech or MCA program first to get to results form
            current_url = driver.current_url
            if "ProgramSelect.aspx" in current_url:
                print(f"[SYSTEM LOGGER] Browser is on ProgramSelect.aspx. Clicking program '{session_program}'...")
                if session_program == "MCA":
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, "radlstProgram_17"))
                        ).click()
                    except Exception:
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, "radlstProgram_2"))
                        ).click()
                else:
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "radlstProgram_1"))
                    ).click()
                
                # Wait for redirection to complete
                target_contains = "MCArslt.aspx" if session_program == "MCA" else "BErslt.aspx"
                WebDriverWait(driver, 10).until(EC.url_contains(target_contains))
                time.sleep(1.0)
                dismiss_alerts_safely(driver)

            try:
                # Primary method: Standard Selenium interaction using precise By.ID selectors
                dropdown_element = WebDriverWait(driver, 12.0).until(
                    EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_drpSemester"))
                )
                
                # Only select the semester dropdown if not already correct
                current_sem = Select(dropdown_element).first_selected_option.get_attribute("value")
                if current_sem != session_sem:
                    Select(dropdown_element).select_by_value(session_sem)
                    print(f"[SYSTEM LOGGER] Selected semester {session_sem}.")
                    time.sleep(SPEED_CONFIGS.get(session_speed_mode, SPEED_CONFIGS["normal"])["settle"])
                else:
                    print("[SYSTEM LOGGER] Semester already correct (no change triggered).")

                # Wait for the roll number input to be clickable
                roll_field = WebDriverWait(driver, 8.0).until(
                    EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_txtrollno"))
                )
                current_roll = roll_field.get_attribute("value")
                if current_roll != roll_number:
                    driver.execute_script(
                        "var f = document.getElementById('ctl00_ContentPlaceHolder1_txtrollno');"
                        "if(f) {"
                        "    f.value = arguments[0];"
                        "    f.dispatchEvent(new Event('input'));"
                        "    f.dispatchEvent(new Event('change'));"
                        "}",
                        roll_number
                    )
                    print(f"[SYSTEM LOGGER] Entered roll number instantly via JS: {roll_number}")
                    time.sleep(SPEED_CONFIGS.get(session_speed_mode, SPEED_CONFIGS["normal"])["roll_enter"])
                else:
                    print("[SYSTEM LOGGER] Roll number already correct (no change triggered).")
                print("[SYSTEM LOGGER] Standard form fill succeeded!")
            except Exception as selenium_err:
                print(f"[SYSTEM LOGGER] Standard form fill failed: {selenium_err}. Attempting Javascript-based fallback...")
                
                # Fallback method: Direct JavaScript injection (100% bulletproof & guarded)
                success = driver.execute_script(
                    "var drp = document.getElementById('ctl00_ContentPlaceHolder1_drpSemester');"
                    "var txt = document.getElementById('ctl00_ContentPlaceHolder1_txtrollno');"
                    "if (drp && txt) {"
                    "  if (drp.value !== arguments[0]) {"
                    "    drp.value = arguments[0]; drp.dispatchEvent(new Event('change'));"
                    "  }"
                    "  if (txt.value !== arguments[1]) {"
                    "    txt.value = arguments[1]; txt.dispatchEvent(new Event('input')); txt.dispatchEvent(new Event('change'));"
                    "  }"
                    "  return true;"
                    "}"
                    "return false;",
                    session_sem, roll_number
                )
                if not success:
                    raise Exception(f"Form elements (drpSemester or txtrollno) not found in DOM. Standard error: {selenium_err}")
                time.sleep(SPEED_CONFIGS.get(session_speed_mode, SPEED_CONFIGS["normal"])["settle"] + 0.1)
                print("[SYSTEM LOGGER] Javascript fallback form fill executed successfully!")

        except TimeoutException as time_err:
            print(f"[SYSTEM LOGGER] Form fill timed out. Scaling up wait delay due to server lag.")
            if session_wait_value < 45.0:
                session_wait_value = min(45.0, session_wait_value + 5.0)
                print(f"[SYSTEM LOGGER] Dynamic Delay Scaling: Increased wait value to {session_wait_value}s")
            return jsonify({"ok": False, "error": f"Portal page load timed out. Delay scaled to {session_wait_value}s. Try again."})
        except Exception as e:
            print(f"[SYSTEM LOGGER] Form fill error: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"ok": False, "error": f"Form fill error: {e}. Please check if the portal page has fully loaded."})

        # ── CAPTCHA IMAGE: Selenium element screenshot (fastest + always GUID-sync) ──
        # Directly captures the captcha element from the live browser memory.
        # No extra HTTP request, no cookie sync, no GUID mismatch possible.
        img_bytes = None
        captcha_url = "[element-screenshot]"  # for logging only
        try:
            # Locate the captcha element
            captcha_elem = WebDriverWait(driver, 8).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@id='ctl00_ContentPlaceHolder1_pnlCaptcha']//img"))
            )
            
            # Wait for captcha src to update (prevents capturing the old stale captcha during retries/resets)
            if last_captcha_src:
                try:
                    # 1. Wait until src attribute changes
                    WebDriverWait(driver, 5).until(
                        lambda d: d.find_element(By.XPATH, "//div[@id='ctl00_ContentPlaceHolder1_pnlCaptcha']//img").get_attribute("src") != last_captcha_src
                    )
                    # 2. Wait until new image is fully loaded & rendered by browser
                    WebDriverWait(driver, 5).until(
                        lambda d: d.execute_script(
                            "var img = document.querySelector(\"#ctl00_ContentPlaceHolder1_pnlCaptcha img\");"
                            "return img && img.complete && img.naturalWidth > 0;"
                        )
                    )
                    # Tiny sleep to allow browser render engine to draw pixels
                    time.sleep(0.15)
                    # Re-locate to ensure we capture the updated DOM element
                    captcha_elem = driver.find_element(By.XPATH, "//div[@id='ctl00_ContentPlaceHolder1_pnlCaptcha']//img")
                    print("[SYSTEM LOGGER] Stale captcha check: captcha src updated and fully loaded in browser.")
                except Exception as wait_err:
                    print(f"[SYSTEM LOGGER] Stale captcha check: wait for new captcha load timed out: {wait_err}")

            # Save the new captcha src
            try:
                last_captcha_src = captcha_elem.get_attribute("src")
                print(f"[SYSTEM LOGGER] Current Captcha URL saved: {last_captcha_src}")
            except Exception as src_err:
                print(f"[SYSTEM LOGGER] Failed to read captcha src: {src_err}")

            img_bytes = captcha_elem.screenshot_as_png
            print(f"[SYSTEM LOGGER] Captcha captured via element screenshot ({len(img_bytes)} bytes)")
        except Exception as ss_err:
            print(f"[SYSTEM LOGGER] Element screenshot failed: {ss_err}. Falling back to requests.get...")

        # Fallback: download via requests (old method) if screenshot failed
        if not img_bytes:
            captcha_url = None
            try:
                live_img = driver.find_element(By.XPATH, "//div[@id='ctl00_ContentPlaceHolder1_pnlCaptcha']//img")
                live_src = live_img.get_attribute("src")
                if live_src:
                    captcha_url = live_src if live_src.startswith("http") else "http://result.rgpv.ac.in/Result/" + live_src.lstrip("/")
            except Exception:
                pass
            if not captcha_url:
                soup = BeautifulSoup(driver.page_source, "html.parser")
                pnl = soup.find(id="ctl00_ContentPlaceHolder1_pnlCaptcha")
                img_tag = pnl.find("img") if pnl else None
                if img_tag and img_tag.get("src"):
                    captcha_url = "http://result.rgpv.ac.in/Result/" + img_tag["src"]
            if not captcha_url:
                return jsonify({"ok": False, "error": "Captcha not found on page"})
            cookies = {c["name"]: c["value"] for c in driver.get_cookies()}
            headers = {"User-Agent": "Mozilla/5.0", "Referer": "http://result.rgpv.ac.in/Result/BErslt.aspx"}
            for attempt in range(1, 4):
                try:
                    r = requests.get(captcha_url, cookies=cookies, headers=headers, timeout=10)
                    if r.status_code == 200:
                        img_bytes = r.content
                        break
                    print(f"[SYSTEM LOGGER] Captcha download attempt {attempt} returned HTTP {r.status_code}")
                except Exception as net_err:
                    print(f"[SYSTEM LOGGER] Captcha download attempt {attempt} failed: {net_err}")
                    if attempt == 3:
                        return jsonify({"ok": False, "error": f"Captcha download failed: {net_err}"})
                    time.sleep(2.0)

        if not img_bytes:
            return jsonify({"ok": False, "error": "Captcha image could not be obtained"})

        img_b64 = base64.b64encode(img_bytes).decode("utf-8")

        # ── OCR CAPTCHA SOLVING ─────────────────────────────────────
        captcha_text = ""
        ocr_error = None
        ocr_error_msg = None
        solver_used = "none"

        # Level 1: Deep Learning OCR Engine (ddddocr)
        # Simple single-pass on raw img_bytes (optimal for ddddocr's trained model resolution)
        try:
            dl_ocr = get_dddd_ocr()
            if dl_ocr:
                raw_prediction = dl_ocr.classification(img_bytes)
                captcha_text = re.sub(r'[^A-Z0-9]', '', raw_prediction.upper()).strip()
                if captcha_text:
                    solver_used = "deep_learning"
                    print(f"[SYSTEM LOGGER] Deep Learning AI Solved Captcha (Raw Mode): '{captcha_text}'")
        except Exception as dl_err:
            print(f"[SYSTEM LOGGER] Deep Learning AI Solver failed: {dl_err}. Falling back to Tesseract.")



        # Level 2: Tesseract OCR Fallback
        if not captcha_text:
            try:
                from PIL import Image
                import io
                import pytesseract

                # Dynamically locate Tesseract executable on Windows if default call fails
                tesseract_paths = [
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                ]
                local_appdata = os.environ.get("LOCALAPPDATA")
                if local_appdata:
                    tesseract_paths.append(os.path.join(local_appdata, "Programs", "Tesseract-OCR", "tesseract.exe"))
                    tesseract_paths.append(os.path.join(local_appdata, "Tesseract-OCR", "tesseract.exe"))

                tesseract_found = False
                try:
                    pytesseract.get_tesseract_version()
                    tesseract_found = True
                except Exception:
                    # Tesseract not found on default PATH, search fallback paths
                    for p in tesseract_paths:
                        if os.path.exists(p):
                            pytesseract.pytesseract.tesseract_cmd = p
                            tesseract_found = True
                            print(f"[SYSTEM LOGGER] Dynamic fallback: set tesseract path to '{p}'")
                            break

                if not tesseract_found:
                    ocr_error = "tesseract_not_installed"
                    ocr_error_msg = (
                        "Deep Learning AI engine could not load, AND Tesseract OCR engine was not found on your system.\n"
                        "Please install Tesseract OCR on your Windows machine:\n"
                        "1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki\n"
                        "2. Install it in the default directory: C:\\Program Files\\Tesseract-OCR\n"
                        "3. Restart this application."
                    )
                    solver_used = "manual"
                    print(f"[SYSTEM LOGGER] {ocr_error_msg}")
                else:
                    # Read image from bytes
                    img = Image.open(io.BytesIO(img_bytes))

                    # Preprocessing: convert to grayscale
                    img_gray = img.convert('L')

                    # Enhance contrast to clearly separate characters from background noise lines (Optimal: 1.5x)
                    from PIL import ImageEnhance
                    enhancer = ImageEnhance.Contrast(img_gray)
                    img_contrast = enhancer.enhance(1.5)

                    # Resize image (upscale by 3x) for optimal character stroke density (Optimal: 3x)
                    img_resized = img_contrast.resize((img_contrast.width * 3, img_contrast.height * 3), Image.Resampling.LANCZOS)

                    # Apply a binary threshold to remove background noise (Optimal: 150)
                    img_bin = img_resized.point(lambda p: 255 if p > 150 else 0)

                    # Run pytesseract OCR
                    custom_config = '--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                    raw_text = pytesseract.image_to_string(img_bin, config=custom_config)

                    # Extract alphanumeric uppercase characters only and strip whitespace
                    captcha_text = re.sub(r'[^A-Z0-9]', '', raw_text.upper()).strip()
                    solver_used = "tesseract"
                    print(f"[SYSTEM LOGGER] Tesseract OCR Solved Captcha: '{captcha_text}'")

            except ImportError as imp_err:
                ocr_error = "missing_dependencies"
                ocr_error_msg = (
                    f"Both Deep Learning and Tesseract failed. Missing Python dependencies: {imp_err}\n"
                    "Please make sure you are running the application using 'run.bat' "
                    "(which launches inside the pre-configured virtual environment '.venv1').\n"
                    "Or manually run in your terminal: pip install pytesseract Pillow"
                )
                solver_used = "manual"
                print(f"[SYSTEM LOGGER] {ocr_error_msg}")
            except Exception as ocr_err:
                ocr_error = "ocr_failed"
                ocr_error_msg = f"OCR solver failed internally: {ocr_err}"
                solver_used = "manual"
                print(f"[SYSTEM LOGGER] {ocr_error_msg}")

        return jsonify({
            "ok": True,
            "image": f"data:image/jpeg;base64,{img_b64}",
            "captcha_text": captcha_text,
            "ocr_error": ocr_error,
            "ocr_error_msg": ocr_error_msg,
            "solver_used": solver_used
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"ok": False, "error": f"Captcha extraction failed: {e}"})


# ── Submit captcha + fetch result ─────────────────────────────
@app.route("/api/submit", methods=["POST"])
def submit():
    global session_subjects, driver, session_wait_value, last_captcha_src
    if not check_driver_health():
        success = heal_browser_session()
        if not success:
            return jsonify({"ok": False, "error": "Browser window was closed and self-healing recovery failed. Please check Edge browser installation."})
        # If healed during submit, the captcha image has changed on the new browser.
        # Return a special status to let frontend know it must fetch and solve a new captcha.
        return jsonify({"ok": True, "status": "browser_recovered", "message": "Browser session recovered. Re-solving captcha..."})

    old_captcha_elem = None
    try:
        data = request.json
        if not data:
            return jsonify({"ok": False, "error": "Invalid JSON request payload"})
        roll = str(data.get("roll", "")).strip()
        captcha = str(data.get("captcha", "")).strip()
        full_roll_mode = bool(data.get("full_roll", False))  # True when roll is already full roll number

        if not roll:
            return jsonify({"ok": False, "error": "Roll suffix is required"})
        if not captcha:
            return jsonify({"ok": False, "error": "Captcha is required"})

        print(f"[SYSTEM LOGGER] submit() called: roll='{roll}', captcha='{captcha}', full_roll_mode={full_roll_mode}")
        print(f"[SYSTEM LOGGER] Session variables: prefix='{session_prefix}', filename='{session_filename}', sem='{session_sem}'")

        if full_roll_mode:
            roll_number = roll.upper()  # Already full roll number (from Excel list mode)
        else:
            if not session_prefix:
                return jsonify({"ok": False, "error": "Session prefix is not initialized. Please restart the session."})
            roll_upper = roll.upper()
            if roll_upper.startswith(session_prefix.upper()) or re.match(r'^[0-9]{4}[A-Z]{2,4}[0-9]{2}(?:[0-9]{3,4}|3D[0-9]{2})$', roll_upper):
                roll_number = roll_upper
            else:
                roll_number = session_prefix + roll

        if not session_filename:
            return jsonify({"ok": False, "error": "Session filename is not initialized. Please restart the session."})

        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            # Dismiss any blocking alerts first
            dismiss_alerts_safely(driver)

            try:
                # Capture reference to the current captcha element before submitting
                try:
                    old_captcha_elem = driver.find_element(By.XPATH, "//div[@id='ctl00_ContentPlaceHolder1_pnlCaptcha']//img")
                except Exception:
                    old_captcha_elem = None

                # NOTE: Do NOT re-touch drpSemester or txtrollno here — not even via JS property-set.
                # get_captcha() already set both fields correctly before the captcha image was captured.
                # Any write to either field — even setting .value without dispatchEvent — risks
                # triggering RGPV's portal JS, which silently refreshes the captcha and invalidates
                # the already-solved text. roll_number is still used below for CSV/matching purposes.

                # Guard: abort if the portal already invalidated our captcha (src changed since get_captcha).
                try:
                    current_img_src = driver.execute_script(
                        "var img = document.querySelector('#ctl00_ContentPlaceHolder1_pnlCaptcha img');"
                        "return img ? img.src : '';"
                    )
                    if last_captcha_src and current_img_src and current_img_src != last_captcha_src:
                        print(f"[SYSTEM LOGGER] Captcha src changed before submit — aborting. old='{last_captcha_src}' new='{current_img_src}'")
                        return jsonify({"ok": True, "status": "captcha_expired", "message": "Captcha image changed before submission. Re-solving..."})
                except Exception as src_err:
                    print(f"[SYSTEM LOGGER] Could not verify captcha src: {src_err}")

                # Fill captcha text box (safe — captcha field events do NOT trigger captcha refresh)
                captcha_box = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_TextBox1"))
                )
                captcha_box.clear()
                captcha_box.send_keys(captcha)
                print(f"[SYSTEM LOGGER] Captcha entered. Waiting {session_submit_delay}s before clicking View Result...")
                time.sleep(session_submit_delay)

                # Click View Result button directly
                # Direct click() doesn't fire hover/mousemove events, preventing RGPV from auto-refreshing the captcha.
                try:
                    submit_btn = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btnviewresult"))
                    )
                    # Scroll button into view to prevent click interception
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                    time.sleep(SPEED_CONFIGS.get(session_speed_mode, SPEED_CONFIGS["normal"])["scroll"])
                    
                    try:
                        # Try submitting using ENTER key as it mimics human submission
                        submit_btn.send_keys(Keys.ENTER)
                        print("[SYSTEM LOGGER] View Result submitted via ENTER key.")
                    except Exception:
                        submit_btn.click()
                        print("[SYSTEM LOGGER] View Result clicked directly.")
                except Exception as click_err:
                    print(f"[SYSTEM LOGGER] Direct click failed: {click_err}. Falling back to __doPostBack...")
                    driver.execute_script("__doPostBack('ctl00$ContentPlaceHolder1$btnviewresult','')")

                print("[SYSTEM LOGGER] Standard submit succeeded!")
            except Exception as selenium_err:
                print(f"[SYSTEM LOGGER] Standard submit failed: {selenium_err}. Attempting Javascript-based fallback...")

                # Fallback method: set ONLY the captcha text box via JS — do NOT re-touch semester or
                # roll number fields here. Dispatching events on those fields triggers RGPV's silent
                # captcha refresh. get_captcha() already filled them correctly.
                driver.execute_script(
                    "var box = document.getElementById('ctl00_ContentPlaceHolder1_TextBox1');"
                    "if(box) { box.value = arguments[0]; }",
                    captcha
                )
                print(f"[SYSTEM LOGGER] Captcha entered via JS fallback. Waiting {session_submit_delay}s before clicking View Result...")
                time.sleep(session_submit_delay)
                driver.execute_script(
                    "var btn = document.getElementById('ctl00_ContentPlaceHolder1_btnviewresult');"
                    "if(btn) { btn.click(); }"
                )
                print("[SYSTEM LOGGER] Javascript fallback submit executed successfully!")

            # Wait dynamic seconds for RGPV server processing/rendering
            post_submit_delay = SPEED_CONFIGS.get(session_speed_mode, SPEED_CONFIGS["normal"])["post_submit"]
            print(f"[SYSTEM LOGGER] Submission complete. Waiting {post_submit_delay} seconds...")
            time.sleep(post_submit_delay)

            # Wait for portal response dynamically or statically
            if session_wait_mode == "static":
                print(f"[SYSTEM LOGGER] Using Static Wait. Sleeping for {session_wait_value} seconds...")
                time.sleep(session_wait_value)
            else:
                print(f"[SYSTEM LOGGER] Using Smart Dynamic Wait. Max timeout: {session_wait_value} seconds...")
                from selenium.webdriver.support.ui import WebDriverWait
                
                def portal_response_received(d):
                    try:
                        # 1. Check if alert is present
                        try:
                            alert = d.switch_to.alert
                            if alert.text:
                                return True
                        except NoAlertPresentException:
                            pass
                        
                        # 2. Check if result table is present
                        try:
                            tbl = d.find_element(By.ID, "ctl00_ContentPlaceHolder1_GrdResult")
                            if tbl.is_displayed():
                                return True
                        except Exception:
                            pass
                            
                        try:
                            lbl = d.find_element(By.ID, "ctl00_ContentPlaceHolder1_lblRollNoGrading")
                            if lbl.is_displayed():
                                return True
                        except Exception:
                            pass
                            
                        # 3. Check if page contains "not found" or "wrong captcha" indicators
                        # Avoid calling d.page_source (which transfers megabytes of ViewState and blocks Edge) inside the poll loop.
                        # Instead, check the fast body.text fallback.
                        try:
                            body_text = d.find_element(By.TAG_NAME, "body").text.lower()
                            if "not found" in body_text or "wrong captcha" in body_text:
                                return True
                        except Exception:
                            pass
                    except Exception as driver_err:
                        name = type(driver_err).__name__
                        if "NoSuchWindow" in name or "InvalidSessionId" in name or "WebDriverException" in name:
                            raise driver_err
                    return False
                
                start_wait = time.time()
                try:
                    WebDriverWait(driver, session_wait_value).until(portal_response_received)
                    elapsed = time.time() - start_wait
                    # If it loaded very quickly, gradually scale down towards baseline
                    if elapsed < 3.5 and session_wait_value > session_wait_baseline:
                        session_wait_value = max(session_wait_baseline, session_wait_value - 1.0)
                        print(f"[SYSTEM LOGGER] Dynamic Delay Scaling: Decreased wait value to {session_wait_value}s")
                except TimeoutException:
                    print(f"[SYSTEM LOGGER] Smart wait timeout ({session_wait_value}s) reached.")
                    try:
                        diag_path = os.path.join(r"C:\Users\Hp\.gemini\antigravity\brain\a2dfe04c-7012-4fb9-ae6a-32e12c1e1c64", "timeout_screenshot.png")
                        driver.save_screenshot(diag_path)
                        print(f"[SYSTEM LOGGER] Diagnostic screenshot saved to {diag_path}")
                        print(f"[SYSTEM LOGGER] Diagnostic page source snippet:\n{driver.page_source[:3000]}")
                    except Exception as diag_err:
                        print(f"[SYSTEM LOGGER] Diagnostic capture failed: {diag_err}")

                    # ── TIMEOUT RECOVERY: Check page source BEFORE aborting ──────
                    # RGPV server is slow — result may have loaded but not matched our wait conditions
                    try:
                        current_src = driver.page_source
                        if "Total Credit" in current_src or "SGPA" in current_src or "lblRollNoGrading" in current_src:
                            print("[SYSTEM LOGGER] Timeout recovery: Result data found in page source! Proceeding with parse.")
                            # Don't abort — let the code below parse it naturally
                            # Skip the refresh/abort steps
                        else:
                            print("[SYSTEM LOGGER] Aborting pending request (no result data found)...")
                            # Abort any pending postback / page load in the browser to prevent late page updates
                            try:
                                driver.execute_script("window.stop();")
                            except Exception:
                                pass
                            # Refresh page to return to a clean GET state
                            try:
                                driver.refresh()
                                dismiss_alerts_safely(driver)
                                WebDriverWait(driver, 8).until(
                                    lambda d: d.execute_script("return document.readyState") == "complete"
                                )
                                WebDriverWait(driver, 8).until(
                                    EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_drpSemester"))
                                )
                                print("[SYSTEM LOGGER] Browser request aborted and page successfully refreshed.")
                            except Exception as refresh_err:
                                print(f"[SYSTEM LOGGER] Failed to refresh browser after abort: {refresh_err}")

                            # Dynamic Delay Scaling: increase wait limit by 5 seconds (up to 60s)
                            if session_wait_value < 60.0:
                                session_wait_value = min(60.0, session_wait_value + 5.0)
                                print(f"[SYSTEM LOGGER] Dynamic Delay Scaling: Increased wait value to {session_wait_value}s due to portal slowdown.")
                            
                            # Return immediately from route to prevent fall-through desyncs
                            return jsonify({
                                "ok": True,
                                "status": "wrong_captcha",
                                "message": "Portal lag detected. Session reset and retrying..."
                            })
                    except Exception as src_check_err:
                        print(f"[SYSTEM LOGGER] Timeout recovery check failed: {src_check_err}")

                    # Dynamic Delay Scaling (if we didn't return, i.e. success data was found)
                    if session_wait_value < 60.0:
                        session_wait_value = min(60.0, session_wait_value + 5.0)
                        print(f"[SYSTEM LOGGER] Dynamic Delay Scaling: Increased wait value to {session_wait_value}s due to portal slowdown.")


        except Exception as e:
            return jsonify({"ok": False, "error": f"Submit error: {e}"})

        alerttext = ""
        try:
            alert = Alert(driver)
            alerttext = alert.text
            alert.accept()
            print(f"[SYSTEM LOGGER] Dismissed submit alert: '{alerttext}'")
            # Save the old captcha src so that the next /api/captcha call knows to wait for it to change
            if old_captcha_elem:
                try:
                    last_captcha_src = old_captcha_elem.get_attribute("src")
                except Exception:
                    pass
        except (NoAlertPresentException, InvalidSessionIdException):
            pass

        page_source = driver.page_source

        # ── CASE 1: SUCCESS ───────────────────────────────────────
        if "Total Credit" in page_source or "SGPA" in page_source:
            soup = BeautifulSoup(page_source, "html.parser")

            try:
                rollno = soup.find("span", id="ctl00_ContentPlaceHolder1_lblRollNoGrading").get_text().strip()
                name = soup.find("span", id="ctl00_ContentPlaceHolder1_lblNameGrading").get_text().strip()
                sgpa = soup.find("span", id="ctl00_ContentPlaceHolder1_lblSGPA").get_text().strip()
                cgpa = soup.find("span", id="ctl00_ContentPlaceHolder1_lblcgpa").get_text().strip()
                result = soup.find("span", id="ctl00_ContentPlaceHolder1_lblResultNewGrading").get_text().strip()
            except AttributeError:
                # Fallback wrapper if spans can't be fetched due to partial page updates
                return jsonify({"ok": True, "status": "wrong_captcha", "message": "Portal lag detected. Retrying..."})

            # ── UNIVERSAL GLOBAL TABLE PARSER ──
            extracted_grades = {}

            # Strategy A: Target explicit component ID
            grades_table = soup.find("table", id="ctl00_ContentPlaceHolder1_GrdResult")

            # Strategy B: Fallback to scanning all available markup tables if explicit ID fails
            if not grades_table:
                all_tables = soup.find_all("table")
                for t in all_tables:
                    if "Subject" in t.get_text() or "Grade" in t.get_text():
                        grades_table = t
                        break

            if grades_table:
                rows = grades_table.find_all("tr")
                for row in rows:
                    cols = [td.get_text(strip=True) for td in row.find_all("td")]

                    if len(cols) >= 3:
                        sub_code = ""
                        grade = ""

                        for col_text in cols:
                            col_clean = col_text.strip().upper()

                            # Pinpoint subject code substring entry patterns using a strict regex
                            if re.match(r'^[A-Z]{2,6}-?\d{3,4}', col_clean) and not any(
                                    g in col_clean for g in ["PASS", "FAIL", "TOTAL", "SGPA", "CGPA"]):
                                sub_code = col_clean

                            # Match grading score boundaries (including standard, special codes, grace grades, and absent formats like F (ABS))
                            elif re.match(r'^(O|A\+|A|B\+|B|C\+|C|D|F|ABS|ABSENT|W|I|P)#*(\s*[\(\[\{]ABS[\)\]\}])?$', col_clean):
                                grade = col_clean

                        # Skip subjects marked as [N] / (N) - Not Applicable to this student
                        # Also checks if subject code contains " - N" or ends with "-N"
                        sub_has_N = bool(re.search(r'[\(\[\{]N[\)\]\}]|\bN\b|-N$', sub_code, re.IGNORECASE)) if sub_code else False

                        if sub_code and grade and not sub_has_N:
                            # Split by brackets/parentheses to extract clean subject key
                            clean_key = sub_code
                            for separator in ["(", "[", "{"]:
                                if separator in clean_key:
                                    clean_key = clean_key.split(separator)[0]
                            clean_key = clean_key.strip()

                            # Detect practical components using robust indicator checks
                            sub_upper = sub_code.upper()
                            is_practical = any(p in sub_upper for p in ["(P)", "[P]", "(P}", "[P}", "(PR)", "[PR]"]) or sub_upper.endswith("P") or sub_upper.endswith("PR")

                            # Store in extracted_grades
                            if is_practical:
                                extracted_grades[clean_key + "[P]"] = grade
                                extracted_grades[sub_code + "[P]"] = grade
                                clean_p_key = re.sub(r'[\(\[\{]P[\)\]\}]', '', clean_key).strip()
                                extracted_grades[clean_p_key + "[P]"] = grade
                            else:
                                extracted_grades[clean_key] = grade
                                extracted_grades[sub_code] = grade

            # Print layout mapping
            print(f"\n[SYSTEM LOGGER] MAP RESULT FOR {rollno} -> {extracted_grades}\n")

            # Post-extraction: remove [N] subjects (Not Applicable)
            _N_PAT = re.compile(r'[\(\[\{]N[\)\]\}]|\bN\b|-N$', re.IGNORECASE)
            extracted_grades = {
                code: grd for code, grd in extracted_grades.items()
                if not _N_PAT.search(code) and grd.upper() not in ('N', '[N]', '(N)')
            }

            # Fallback if empty
            if not extracted_grades:
                print("[WARNING] Extraction dictionary was empty. Checking backup markup data...")

            # --- DYNAMIC CSV HEADER EXPANSION FOR MIXED BRANCHES / BRANCH CHANGES ---
            unmatched_portal_subs = []
            for portal_code, portal_grade in extracted_grades.items():
                portal_clean = portal_code.replace("-", "").replace(" ", "").strip().upper()
                portal_is_practical = "[P]" in portal_clean or "(P)" in portal_clean or portal_clean.endswith("P")
                p_sub_base = re.sub(r'[\(\[\{][PT][\)\]\}]', '', portal_clean).strip()
                
                # Check if this portal_code matches any target_sub in session_subjects
                matched = False
                for target_sub in session_subjects:
                    target_clean = target_sub.replace("-", "").replace(" ", "").strip().upper()
                    target_is_practical = "[P]" in target_clean or target_clean.endswith("P")
                    t_sub_base = re.sub(r'[\(\[\{][PT][\)\]\}]', '', target_clean).strip()
                    
                    if target_is_practical == portal_is_practical:
                        if t_sub_base in p_sub_base or p_sub_base in t_sub_base:
                            matched = True
                            break
                if not matched:
                    if p_sub_base and not any(g in p_sub_base for g in ["PASS", "FAIL", "TOTAL", "SGPA", "CGPA"]):
                        clean_new_sub = p_sub_base + "[P]" if portal_is_practical else p_sub_base + "[T]"
                        if clean_new_sub not in unmatched_portal_subs and clean_new_sub not in session_subjects:
                            unmatched_portal_subs.append(clean_new_sub)


            if unmatched_portal_subs:
                print(f"[SYSTEM LOGGER] New subjects detected on portal: {unmatched_portal_subs}. Expanding CSV headers...")
                for new_sub in unmatched_portal_subs:
                    if new_sub not in session_subjects:
                        session_subjects.append(new_sub)
                
                # Order subjects: Theory first, Practical second
                def is_pract(s: str) -> bool:
                    s_upper = s.upper()
                    return "[P]" in s_upper or "(P)" in s_upper or s_upper.endswith("P")
                theory_subs = [s for s in session_subjects if not is_pract(s)]
                practical_subs = [s for s in session_subjects if is_pract(s)]
                session_subjects = theory_subs + practical_subs
                
                if os.path.exists(session_filename):
                    try:
                        with open(session_filename, "r", newline="", encoding="utf-8") as f:
                            reader = csv.reader(f)
                            file_data = list(reader)
                        if file_data:
                            existing_header = file_data[0]
                            expected_header = ["Roll Number", "Name"] + session_subjects + ["SGPA", "CGPA", "Result"]
                            if existing_header != expected_header:
                                upgraded_rows = [expected_header]
                                for row in file_data[1:]:
                                    new_row = [""] * len(expected_header)
                                    for i, col_name in enumerate(existing_header):
                                        if col_name in expected_header:
                                            new_idx = expected_header.index(col_name)
                                            if i < len(row):
                                                new_row[new_idx] = row[i]
                                    upgraded_rows.append(new_row)
                                with open(session_filename, "w", newline="", encoding="utf-8") as f:
                                    csv.writer(f).writerows(upgraded_rows)
                    except Exception as file_err:
                        print(f"[SYSTEM LOGGER] Dynamic CSV header expansion failed: {file_err}")

            # Align structural values for matching columns inside generated CSV output file
            grade_values = []
            for target_sub in session_subjects:
                best_portal_code = None
                best_portal_grade = ""
                target_clean = target_sub.replace("-", "").replace(" ", "").strip().upper()
                
                # Check if target column is practical
                target_is_practical = "[P]" in target_clean or target_clean.endswith("P")
                
                for portal_code, portal_grade in extracted_grades.items():
                    portal_clean = portal_code.replace("-", "").replace(" ", "").strip().upper()
                    
                    # Check if portal code is practical
                    portal_is_practical = "[P]" in portal_clean or "(P)" in portal_clean or portal_clean.endswith("P")
                    
                    if target_is_practical == portal_is_practical:
                         t_sub_base = re.sub(r'[\(\[\{][PT][\)\]\}]', '', target_clean).strip()
                         p_sub_base = re.sub(r'[\(\[\{][PT][\)\]\}]', '', portal_clean).strip()
                         
                         if t_sub_base in p_sub_base or p_sub_base in t_sub_base:
                             best_portal_code = portal_code
                             best_portal_grade = portal_grade
                             break
                grade_values.append(best_portal_grade)

            # Check if roll number already exists in CSV to prevent duplicate rows
            row_exists = False
            rows = []
            headers = []
            if os.path.exists(session_filename):
                try:
                    with open(session_filename, "r", newline="", encoding="utf-8") as f:
                        reader = csv.reader(f)
                        file_data = list(reader)
                        if file_data:
                            headers = file_data[0]
                            # Find index of Roll Number column
                            roll_idx = 0 if "Roll Number" in headers else -1
                            if roll_idx != -1:
                                for r in file_data[1:]:
                                    if r and len(r) > roll_idx and r[roll_idx].strip().upper() == rollno.strip().upper():
                                        row_exists = True
                                        # Update row content with fresh scraped data
                                        rows.append([rollno, name] + grade_values + [sgpa, cgpa, result])
                                    else:
                                        rows.append(r)
                            else:
                                rows = file_data[1:]
                except Exception as file_read_err:
                    print(f"[SYSTEM LOGGER] Duplicate check failed: {file_read_err}")

            if row_exists:
                # Rewrite entire file with updated data row
                try:
                    with open(session_filename, "w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(headers)
                        writer.writerows(rows)
                except PermissionError:
                    return jsonify({
                        "ok": False,
                        "error": f"Permission denied writing to '{session_filename}'. Please close the CSV file if it is open in Excel or another program, then try submitting again."
                    })
                except Exception as file_err:
                    print(f"[SYSTEM LOGGER] File update failed for '{session_filename}': {file_err}")
                    import traceback
                    traceback.print_exc()
                    return jsonify({
                        "ok": False,
                        "error": f"Failed to update CSV file. Error: {file_err}"
                    })
            else:
                # Standard append if roll number is new
                try:
                    with open(session_filename, "a", newline="", encoding="utf-8") as f:
                        csv.writer(f).writerow([rollno, name] + grade_values + [sgpa, cgpa, result])
                except PermissionError:
                    return jsonify({
                        "ok": False,
                        "error": f"Permission denied writing to '{session_filename}'. Please close the CSV file if it is open in Excel or another program, then try submitting again."
                    })
                except Exception as file_err:
                    print(f"[SYSTEM LOGGER] File append failed for '{session_filename}': {file_err}")
                    import traceback
                    traceback.print_exc()
                    return jsonify({
                        "ok": False,
                        "error": f"Failed to append to CSV file. Error: {file_err}"
                    })

            try:
                print(f"[SYSTEM LOGGER] Result resolved. Waiting {session_reset_delay}s before resetting...")
                time.sleep(session_reset_delay)
                reset_results_form(driver, session_program)
                print("[SYSTEM LOGGER] Form reset complete (Success case).")
            except Exception as reset_err:
                print(f"[SYSTEM LOGGER] Form reset failed: {reset_err}")

            return jsonify({
                "ok": True,
                "status": "success",
                "data": {
                    "roll": rollno,
                    "name": name,
                    "sgpa": sgpa,
                    "cgpa": cgpa,
                    "result": result,
                    "subjects": extracted_grades,
                },
            })

        # ── CASE 2: NOT FOUND ─────────────────────────────────────
        elif "Result" in alerttext or "not found" in page_source.lower():
            try:
                print(f"[SYSTEM LOGGER] Student not found. Waiting {session_reset_delay}s before resetting...")
                time.sleep(session_reset_delay)
                reset_results_form(driver, session_program)
                print("[SYSTEM LOGGER] Form reset complete (Not Found case).")
            except Exception as reset_err:
                print(f"[SYSTEM LOGGER] Form reset failed: {reset_err}")
            return jsonify({
                "ok": True,
                "status": "not_found",
                "message": f"Roll {roll_number} not found on portal",
            })

        # ── CASE 3: WRONG CAPTCHA ─────────────────────────────────
        else:
            try:
                print(f"[SYSTEM LOGGER] Wrong captcha. Waiting {session_reset_delay}s before resetting...")
                time.sleep(session_reset_delay)
                reset_results_form(driver, session_program)
                print("[SYSTEM LOGGER] Form reset complete (Wrong Captcha case).")
            except Exception as e:
                pass
            return jsonify({
                "ok": True,
                "status": "wrong_captcha",
                "message": "Wrong captcha — please try again",
            })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"ok": False, "error": f"Submit result failed: {e}"})


# ── Download CSV ──────────────────────────────────────────────
@app.route("/api/download")
def download_csv():
    try:
        if session_filename and os.path.exists(session_filename):
            return send_file(session_filename, as_attachment=True)
        return jsonify({"ok": False, "error": "No result file found. Run a session first."})
    except Exception as e:
        return jsonify({"ok": False, "error": f"Download failed: {e}"})


# ── Parse Uploaded Roll Number Sheet (Excel / CSV) ────────────
@app.route("/api/parse_rollsheet", methods=["POST"])
def parse_rollsheet():
    """
    Accepts a multipart file upload (.xlsx or .csv).
    Scans all cells for RGPV roll number patterns.
    Returns detected roll numbers, prefix, and branch info.
    """
    try:
        if "file" not in request.files:
            return jsonify({"ok": False, "error": "No file uploaded. Please select an Excel or CSV file."})

        uploaded_file = request.files["file"]
        filename = uploaded_file.filename.lower()

        if not (filename.endswith(".xlsx") or filename.endswith(".xls") or filename.endswith(".csv")):
            return jsonify({"ok": False, "error": "Unsupported file format. Please upload a .xlsx or .csv file."})

        # RGPV roll number pattern:
        # 4-digit institution code + 2-4 uppercase letters (branch) + exactly 2-digit year + 3-4 digit sequence
        # Year is ALWAYS 2 digits (e.g. 24 for 2024). Using [0-9]{2,4} caused greedy over-matching.
        ROLL_PATTERN = re.compile(r'(?<!\w)([0-9]{4}[A-Z]{2,4}[0-9]{2}(?:[0-9]{3,4}|3D[0-9]{2}))(?!\w)', re.IGNORECASE)

        roll_numbers = set()
        file_bytes = uploaded_file.read()

        if filename.endswith(".csv"):
            # Parse CSV (UTF-8 with BOM support)
            content = file_bytes.decode("utf-8-sig", errors="replace")
            reader = csv.reader(io.StringIO(content))
            for row in reader:
                for cell in row:
                    cell_clean = str(cell).strip().upper()
                    matches = ROLL_PATTERN.findall(cell_clean)
                    for m in matches:
                        roll_numbers.add(m.upper())

        elif filename.endswith(".xlsx"):
            # Parse modern Excel (.xlsx) using openpyxl
            try:
                import openpyxl
                wb = openpyxl.load_workbook(io.BytesIO(file_bytes), read_only=True, data_only=True)
                for sheet in wb.worksheets:
                    for row in sheet.iter_rows(values_only=True):
                        for cell in row:
                            if cell is None:
                                continue
                            cell_str = str(cell).strip().upper()
                            matches = ROLL_PATTERN.findall(cell_str)
                            for m in matches:
                                roll_numbers.add(m.upper())
                wb.close()
            except Exception as xlsx_err:
                print(f"[SYSTEM LOGGER] openpyxl failed to parse .xlsx: {xlsx_err}")
                return jsonify({"ok": False, "error": f"Failed to read .xlsx file: {xlsx_err}. Make sure the file is a valid Excel 2007+ (.xlsx) file."})

        elif filename.endswith(".xls"):
            # Parse old Excel (.xls) using xlrd
            try:
                import xlrd
                wb_xls = xlrd.open_workbook(file_contents=file_bytes)
                for sheet in wb_xls.sheets():
                    for row_idx in range(sheet.nrows):
                        for col_idx in range(sheet.ncols):
                            cell_val = sheet.cell_value(row_idx, col_idx)
                            cell_str = str(cell_val).strip().upper()
                            matches = ROLL_PATTERN.findall(cell_str)
                            for m in matches:
                                roll_numbers.add(m.upper())
            except ImportError:
                return jsonify({
                    "ok": False,
                    "error": (
                        "Old .xls format requires the 'xlrd' package which is not installed.\n"
                        "Quick Fix: Open your .xls file in Excel and save it as .xlsx (Excel Workbook),\n"
                        "then upload the .xlsx file instead."
                    )
                })
            except Exception as xls_err:
                print(f"[SYSTEM LOGGER] xlrd failed to parse .xls: {xls_err}")
                return jsonify({
                    "ok": False,
                    "error": (
                        f"Failed to read .xls file: {xls_err}\n"
                        "Try saving the file as .xlsx (Excel Workbook) and uploading again."
                    )
                })

        if not roll_numbers:
            return jsonify({
                "ok": False,
                "error": "No valid roll numbers found in the file. Make sure roll numbers follow the format like: 0905CS241001"
            })

        # Sort roll numbers
        sorted_rolls = sorted(list(roll_numbers))

        # ── Branch / Program Auto-Detection from first roll ──────
        # Prefix map: branch code (letters portion) → branch_id and program
        BRANCH_CODE_MAP = {
            "CS": {"branch_id": "3", "program": "BTech", "name": "CS-Core"},
            "CD": {"branch_id": "1", "program": "BTech", "name": "Data Science"},
            "AL": {"branch_id": "2", "program": "BTech", "name": "AIML"},
            "IT": {"branch_id": "4", "program": "BTech", "name": "IT (Regular)"},
            "CY": {"branch_id": "5", "program": "BTech", "name": "Cyber Security"},
            "IO": {"branch_id": "6", "program": "BTech", "name": "IOT"},
            "CA": {"branch_id": "mca", "program": "MCA",   "name": "MCA"},
        }

        detected_prefix = ""
        detected_branch_id = ""
        detected_program = "BTech"
        detected_branch_name = ""
        detected_year = ""

        first_roll = sorted_rolls[0]
        # Pattern: 4digit + 2-4letter + 2digit(year) + 3-4digit(seq)
        m = re.match(r'^([0-9]{4})([A-Z]{2,4})([0-9]{2})(?:[0-9]{3,4}|3D[0-9]{2})$', first_roll)
        if m:
            inst_code = m.group(1)
            branch_code = m.group(2)
            year_code = m.group(3)
            detected_prefix = inst_code + branch_code + year_code
            detected_year = year_code
            if branch_code in BRANCH_CODE_MAP:
                info = BRANCH_CODE_MAP[branch_code]
                detected_branch_id = info["branch_id"]
                detected_program = info["program"]
                detected_branch_name = info["name"]

        print(f"[SYSTEM LOGGER] Roll sheet parsed: {len(sorted_rolls)} rolls found. Prefix='{detected_prefix}', Branch='{detected_branch_name}'")

        return jsonify({
            "ok": True,
            "rolls": sorted_rolls,
            "count": len(sorted_rolls),
            "detected_prefix": detected_prefix,
            "detected_year": detected_year,
            "detected_branch_id": detected_branch_id,
            "detected_program": detected_program,
            "detected_branch_name": detected_branch_name,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"ok": False, "error": f"File parsing failed: {e}"})


# ── List Previous CSV Files (Recursive Scan of Folders) ────────
@app.route("/api/previous_files", methods=["GET"])
def previous_files():
    try:
        base_dir = get_base_dir()
        files = []
        folders = ["", "CS_Core", "IT", "CS_Emerging", "MCA"]
        for folder in folders:
            folder_path = os.path.join(base_dir, folder)
            if not os.path.exists(folder_path):
                continue
            for f in os.listdir(folder_path):
                if f.endswith(".csv"):
                    if "results" in f or "result" in f:
                        filepath = os.path.join(folder_path, f)
                        if os.path.isfile(filepath):
                            stat = os.stat(filepath)
                            mtime = stat.st_mtime
                            size = stat.st_size
                            
                            size_str = f"{size / 1024:.1f} KB" if size >= 1024 else f"{size} Bytes"
                            mtime_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(mtime))
                            
                            files.append({
                                "name": f,
                                "folder": folder if folder else "Root",
                                "size": size_str,
                                "mtime": mtime_str,
                                "raw_mtime": mtime
                            })
        # Sort by newest first
        files.sort(key=lambda x: x["raw_mtime"], reverse=True)
        return jsonify({"ok": True, "files": files})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


# Helper to find a CSV file inside root or designated folders safely
def find_csv_file(filename, folder=None):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    if not filename.endswith(".csv"):
        return None
    base_dir = os.environ.get('RGPV_BASE_DIR', os.path.dirname(os.path.abspath(__file__)))
    
    if folder and folder != "Root":
        folder_sanitized = re.sub(r'[\\/*?:"<>|]', "", folder)
        filepath = os.path.abspath(os.path.join(base_dir, folder_sanitized, filename))
        if filepath.startswith(base_dir) and os.path.exists(filepath):
            return filepath
            
    folders = ["", "CS_Core", "IT", "CS_Emerging", "MCA"]
    for f in folders:
        filepath = os.path.abspath(os.path.join(base_dir, f, filename))
        if filepath.startswith(base_dir) and os.path.exists(filepath):
            return filepath
    return None


# ── Download Specific CSV File ────────────────────────────────
@app.route("/api/download_file/<filename>", methods=["GET"])
def download_specific_file(filename):
    try:
        folder = request.args.get("folder", "").strip()
        filepath = find_csv_file(filename, folder)
        if filepath and os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        return jsonify({"ok": False, "error": f"File '{filename}' not found."}), 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


# ── Get Parsed CSV Data as JSON ────────────────────────────────
@app.route("/api/get_csv_data/<filename>", methods=["GET"])
def get_csv_data(filename):
    try:
        folder = request.args.get("folder", "").strip()
        filepath = find_csv_file(filename, folder)
        if not filepath or not os.path.exists(filepath):
            return jsonify({"ok": False, "error": f"File '{filename}' not found."}), 404
            
        headers = []
        rows = []
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            file_data = list(reader)
            if file_data:
                headers = file_data[0]
                rows = file_data[1:]
                
        return jsonify({"ok": True, "headers": headers, "rows": rows})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


@app.route("/api/update_wait", methods=["POST"])
def update_wait():
    global session_wait_value, session_wait_mode, session_speed_mode, session_submit_delay, session_reset_delay
    try:
        data = request.json
        if data:
            if "wait_value" in data:
                session_wait_value = float(data["wait_value"])
            if "wait_mode" in data:
                session_wait_mode = str(data["wait_mode"])
            if "speed_mode" in data:
                val = str(data["speed_mode"]).strip().lower()
                if val in SPEED_CONFIGS:
                    session_speed_mode = val
            if "submit_delay" in data:
                session_submit_delay = float(data["submit_delay"])
            if "reset_delay" in data:
                session_reset_delay = float(data["reset_delay"])
            return jsonify({
                "ok": True,
                "wait_value": session_wait_value,
                "wait_mode": session_wait_mode,
                "speed_mode": session_speed_mode,
                "submit_delay": session_submit_delay,
                "reset_delay": session_reset_delay
            })
        return jsonify({"ok": False, "error": "No data provided"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


# ── Stop session ──────────────────────────────────────────────
@app.route("/api/stop", methods=["POST"])
def stop_session():
    global driver
    try:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
            driver = None
        return jsonify({"ok": True, "message": "Browser session closed"})
    except Exception as e:
        return jsonify({"ok": False, "error": f"Stop session failed: {e}"})


# ── Serve main UI ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# Disable caching to ensure that frontend updates take effect immediately in user's browser
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, port=5001)