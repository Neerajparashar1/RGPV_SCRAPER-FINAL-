@echo off
:: Shared helper used by run.bat and build.bat.
:: Locates the .venv1 virtual environment's Python interpreter.
:: Sets VENV1_PYTHON_FOUND=1 and PYTHON_EXE=.venv1\Scripts\python.exe if found,
:: otherwise sets VENV1_PYTHON_FOUND=0. Does not exit/pause - caller decides
:: what to do (run.bat falls back to global Python, build.bat requires venv1).
set "VENV1_PYTHON_FOUND=0"
set "PYTHON_EXE="
if exist ".venv1\Scripts\python.exe" (
    set "PYTHON_EXE=.venv1\Scripts\python.exe"
    set "VENV1_PYTHON_FOUND=1"
)
