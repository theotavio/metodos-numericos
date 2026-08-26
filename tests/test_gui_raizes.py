import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# Configura Qt offscreen para testes de interface headless
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import unittest
from PySide6.QtWidgets import QApplication
from gui.tabs.raizes_tab import RaizesTab


app = QApplication.instance() or QApplication(sys.argv)


class TestGuiRaizesTab(unittest.TestCase):
    def setUp(self):
        self.tab = RaizesTab()

    def test_metodo_newton_simbolica(self):
        self.tab.combo_metodo.setCurrentText("Newton-Raphson [ Tangente f'(x) ]")
        campos = self.tab.campos_atuais
        self.assertIn("tipo_derivada", campos)
        campos["funcao"].set("x**2 - 2")
        campos["tipo_derivada"].set("simbolica")
        campos["x0"].set("1.5")
        campos["tol"].set("1e-6")

        resultado = self.tab._executar("newton", campos)
        self.assertTrue(resultado["sucesso"])
        self.assertAlmostEqual(resultado["resultado"], 1.41421356, places=5)
        self.assertIn("Simbólica", resultado["descricao_derivada"])

    def test_metodo_newton_diferenca_central(self):
        self.tab.combo_metodo.setCurrentText("Newton-Raphson [ Tangente f'(x) ]")
        campos = self.tab.campos_atuais
        campos["funcao"].set("x**2 - 2")
        campos["tipo_derivada"].set("central")
        campos["h_derivada"].set("1e-5")
        campos["x0"].set("1.5")
        campos["tol"].set("1e-6")

        resultado = self.tab._executar("newton", campos)
        self.assertTrue(resultado["sucesso"])
        self.assertAlmostEqual(resultado["resultado"], 1.41421356, places=5)
        self.assertIn("Central", resultado["descricao_derivada"])

    def test_metodo_newton_passo_complexo(self):
        self.tab.combo_metodo.setCurrentText("Newton-Raphson [ Tangente f'(x) ]")
        campos = self.tab.campos_atuais
        campos["funcao"].set("sin(x) - x/2")
        campos["tipo_derivada"].set("complexa")
        campos["h_derivada"].set("1e-20")
        campos["x0"].set("2.0")
        campos["tol"].set("1e-6")

        resultado = self.tab._executar("newton", campos)
        self.assertTrue(resultado["sucesso"])
        self.assertAlmostEqual(resultado["resultado"], 1.895494, places=5)
        self.assertIn("Complex-Step", resultado["descricao_derivada"])

    def test_metodo_newton_manual(self):
        self.tab.combo_metodo.setCurrentText("Newton-Raphson [ Tangente f'(x) ]")
        campos = self.tab.campos_atuais
        campos["funcao"].set("x**3 - 2*x - 5")
        campos["tipo_derivada"].set("manual")
        campos["df_manual"].set("3*x**2 - 2")
        campos["x0"].set("2.0")
        campos["tol"].set("1e-6")

        resultado = self.tab._executar("newton", campos)
        self.assertTrue(resultado["sucesso"])
        self.assertAlmostEqual(resultado["resultado"], 2.09455148, places=5)
        self.assertIn("Manual", resultado["descricao_derivada"])

    def test_metodo_secante_gui(self):
        self.tab.combo_metodo.setCurrentText("Método da Secante [ Quasi-Newton ]")
        campos = self.tab.campos_atuais
        self.assertIn("x0", campos)
        self.assertIn("x1", campos)
        campos["funcao"].set("x**2 - 2")
        campos["x0"].set("1.0")
        campos["x1"].set("2.0")
        campos["tol"].set("1e-6")

        resultado = self.tab._executar("secante", campos)
        self.assertTrue(resultado["sucesso"])
        self.assertAlmostEqual(resultado["resultado"], 1.41421356, places=5)


if __name__ == "__main__":
    unittest.main()
