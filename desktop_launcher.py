from __future__ import annotations

import os
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

from streamlit.web import cli as streamlit_cli


APP_NAME = "MarketAgentPro"
DEFAULT_PORT = 8501


def bundled_path(*parts: str) -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS")).joinpath(*parts)
    return Path(__file__).resolve().parent.joinpath(*parts)


def runtime_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def find_free_port(start_port: int = DEFAULT_PORT, attempts: int = 20) -> int:
    for port in range(start_port, start_port + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port


def open_browser_later(url: str):
    time.sleep(2.0)
    webbrowser.open(url)


def main():
    app_path = bundled_path("app.py")
    work_dir = runtime_dir()
    os.chdir(work_dir)
    work_dir.joinpath("data").mkdir(parents=True, exist_ok=True)

    port = find_free_port()
    url = f"http://127.0.0.1:{port}"
    threading.Thread(target=open_browser_later, args=(url,), daemon=True).start()

    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.headless=true",
        f"--server.port={port}",
        "--server.address=127.0.0.1",
        "--browser.gatherUsageStats=false",
        "--global.developmentMode=false",
    ]
    sys.exit(streamlit_cli.main())


if __name__ == "__main__":
    main()
