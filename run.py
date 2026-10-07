#!/usr/bin/env python3
"""
CyberGuard Universal Cross-Platform Launcher
Works on Windows, macOS, and Linux without any file path errors.
Automatically resolves project root, checks dependencies, and launches backend + frontend.
"""

import sys
import os
import subprocess
import signal
import time
from pathlib import Path

# Always resolve paths relative to this script's directory
PROJECT_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_ROOT
FRONTEND_DIR = PROJECT_ROOT / "frontend"

def print_banner():
    banner = r"""
  ==============================================================
   ___       _              ____                     _ 
  / __\   _ | |__   ___ _ _|  _ \ _   _  __ _ _ __ _| |
 / / | | | || '_ \ / _ \ '__| |_) | | | |/ _` | '__/ _` |
/ /__| |_| || |_) |  __/ |  |  __/| |_| | (_| | | | (_| |
\____/\__, ||_.__/ \___|_|  |_|    \__,_|\__,_|_|  \__,_|
      |___/                                               
       Multilingual AI Cyberbullying & Safety Platform
  ==============================================================
    """
    print(banner)
    print(f"[*] Project Root : {PROJECT_ROOT}")
    print(f"[*] Python       : {sys.version.split()[0]} ({sys.executable})")
    print(f"[*] OS Platform  : {sys.platform}\n")

def check_environment():
    """Verify Node.js and basic requirements."""
    # Check Python version
    if sys.version_info < (3, 9):
        print("[!] Warning: Python 3.9+ is recommended.")

    # Check Node.js
    try:
        node_res = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        print(f"[✓] Node.js detected: {node_res.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[!] ERROR: Node.js is not found in PATH.")
        print("    Please install Node.js 18+ from https://nodejs.org/")
        sys.exit(1)

    # Check frontend node_modules
    nm_dir = FRONTEND_DIR / "node_modules"
    if not nm_dir.exists():
        print("[*] Installing frontend dependencies (npm install)...")
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
        subprocess.run([npm_cmd, "install"], cwd=str(FRONTEND_DIR), check=True)
        print("[✓] Frontend dependencies installed successfully.\n")

def main():
    print_banner()
    check_environment()

    # Set environment variables for universal execution
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    env["APP_DIR"] = str(PROJECT_ROOT)

    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    py_exec = sys.executable

    print("\n" + "="*60)
    print(" [1/2] Starting CyberGuard FastAPI Backend on http://127.0.0.1:8000 ...")
    print(" [2/2] Starting CyberGuard Vite Frontend   on http://127.0.0.1:5173 ...")
    print("="*60)
    print("\nPortal Links:")
    print("  -> User / Safety Portal : http://127.0.0.1:5173")
    print("  -> Backend Swagger API  : http://127.0.0.1:8000/docs")
    print("\nDefault Credentials:")
    print("  -> Admin User : admin@cyberguard.ai  |  Password: AdminSecure2026!")
    print("  -> Analyst Demo : Click 'Analyst Demo' button on the login screen")
    print("\nPress Ctrl+C at any time to shut down both servers.\n")

    processes = []
    try:
        # Launch Backend
        backend_cmd = [
            py_exec, "-m", "uvicorn", "backend.app.main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload"
        ]
        p_backend = subprocess.Popen(backend_cmd, cwd=str(PROJECT_ROOT), env=env)
        processes.append(p_backend)

        # Allow backend to bind socket
        time.sleep(1.5)

        # Launch Frontend
        frontend_cmd = [npm_cmd, "run", "dev"]
        p_frontend = subprocess.Popen(frontend_cmd, cwd=str(FRONTEND_DIR), env=env)
        processes.append(p_frontend)

        # Open in default browser
        try:
            import webbrowser
            time.sleep(1.0)
            webbrowser.open("http://127.0.0.1:5173")
        except Exception:
            pass

        # Keep parent alive until interrupted
        while True:
            time.sleep(1)
            # Check if any died unexpectedly
            if p_backend.poll() is not None:
                print(f"[!] Backend process exited with code {p_backend.returncode}")
                break
            if p_frontend.poll() is not None:
                print(f"[!] Frontend process exited with code {p_frontend.returncode}")
                break

    except KeyboardInterrupt:
        print("\n[*] Shutting down CyberGuard servers...")
    finally:
        for p in processes:
            if p.poll() is None:
                try:
                    if sys.platform == "win32":
                        subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
                    else:
                        p.terminate()
                except Exception:
                    pass
        print("[✓] CyberGuard safely terminated. Have a great day!")

if __name__ == "__main__":
    main()
