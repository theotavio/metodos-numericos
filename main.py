import sys
import threading
import time
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import uvicorn


def abrir_navegador(url: str, delay: float = 1.0):
    def _abrir():
        time.sleep(delay)
        try:
            webbrowser.open(url)
        except Exception:
            pass
    threading.Thread(target=_abrir, daemon=True).start()


def main():
    host = "127.0.0.1"
    port = 8000
    url = f"http://{host}:{port}"
    abrir_navegador(url)
    uvicorn.run(
        "backend.app:app",
        host=host,
        port=port,
        log_level="error",
        reload=False
    )


if __name__ == "__main__":
    main()
