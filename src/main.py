"""
Ponto de entrada principal da aplicação Métodos Numéricos Computacionais.
Inicializa a aplicação com PySide6 (Qt 6) e tema moderno.
"""

import sys
from pathlib import Path

# Adiciona o diretório 'src' ao sys.path para garantir resolução consistente de módulos
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from PySide6.QtWidgets import QApplication
from gui.app import App


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = App()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()