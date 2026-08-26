import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import unittest
import numpy as np
import sympy as sp
from core import parsing, derivadas, raizes


class TestDerivadas(unittest.TestCase):
    def setUp(self):
        self.expr_str = "x**3 - 2*x - 5"
        self.expr, self.f = parsing.parse_funcao_1var(self.expr_str)
        # f'(x) = 3*x^2 - 2
        self.x_test = 2.0
        self.df_esperado = 3.0 * (self.x_test ** 2) - 2.0  # 10.0

    def test_derivada_simbolica(self):
        df, desc, expr_df = derivadas.construir_derivada(
            tipo="simbolica",
            expr_sympy=self.expr,
            f=self.f
        )
        self.assertIn("Simbólica", desc)
        self.assertIsNotNone(expr_df)
        self.assertAlmostEqual(df(self.x_test), self.df_esperado, places=7)

    def test_diferenca_central(self):
        df, desc, _ = derivadas.construir_derivada(
            tipo="central",
            f=self.f,
            h=1e-6
        )
        self.assertIn("Central", desc)
        self.assertAlmostEqual(df(self.x_test), self.df_esperado, places=5)

    def test_diferenca_progressiva(self):
        df, desc, _ = derivadas.construir_derivada(
            tipo="progressiva",
            f=self.f,
            h=1e-6
        )
        self.assertIn("Progressiva", desc)
        self.assertAlmostEqual(df(self.x_test), self.df_esperado, places=4)

    def test_diferenca_regressiva(self):
        df, desc, _ = derivadas.construir_derivada(
            tipo="regressiva",
            f=self.f,
            h=1e-6
        )
        self.assertIn("Regressiva", desc)
        self.assertAlmostEqual(df(self.x_test), self.df_esperado, places=4)

    def test_passo_complexo(self):
        df, desc, _ = derivadas.construir_derivada(
            tipo="complexa",
            expr_sympy=self.expr,
            h=1e-20
        )
        self.assertIn("Complex-Step", desc)
        self.assertAlmostEqual(df(self.x_test), self.df_esperado, places=10)

    def test_derivada_manual(self):
        df, desc, expr_df = derivadas.construir_derivada(
            tipo="manual",
            expressao_manual_str="3*x**2 - 2"
        )
        self.assertIn("Manual", desc)
        self.assertIsNotNone(expr_df)
        self.assertAlmostEqual(df(self.x_test), self.df_esperado, places=7)

    def test_erro_passo_invalido(self):
        with self.assertRaises(ValueError):
            derivadas.construir_derivada(tipo="central", f=self.f, h=-1e-5)

        with self.assertRaises(ValueError):
            derivadas.construir_derivada(tipo="complexa", expr_sympy=self.expr, h=0)

    def test_erro_manual_vazia(self):
        with self.assertRaises(ValueError):
            derivadas.construir_derivada(tipo="manual", expressao_manual_str="")


class TestNewtonRaphsonComDerivadas(unittest.TestCase):
    def setUp(self):
        # f(x) = x^2 - 2, raiz exata = sqrt(2) ≈ 1.41421356
        self.expr, self.f = parsing.parse_funcao_1var("x**2 - 2")
        self.raiz_exata = np.sqrt(2.0)
        self.x0 = 1.5

    def test_newton_simbolico(self):
        df, _, _ = derivadas.construir_derivada("simbolica", expr_sympy=self.expr)
        res = raizes.metodo_newton_raphson(self.f, df, self.x0, tol=1e-8)
        self.assertTrue(res["sucesso"])
        self.assertAlmostEqual(res["resultado"], self.raiz_exata, places=7)

    def test_newton_diferenca_central(self):
        df, _, _ = derivadas.construir_derivada("central", f=self.f, h=1e-6)
        res = raizes.metodo_newton_raphson(self.f, df, self.x0, tol=1e-8)
        self.assertTrue(res["sucesso"])
        self.assertAlmostEqual(res["resultado"], self.raiz_exata, places=7)

    def test_newton_passo_complexo(self):
        df, _, _ = derivadas.construir_derivada("complexa", expr_sympy=self.expr, h=1e-20)
        res = raizes.metodo_newton_raphson(self.f, df, self.x0, tol=1e-8)
        self.assertTrue(res["sucesso"])
        self.assertAlmostEqual(res["resultado"], self.raiz_exata, places=7)

    def test_newton_manual(self):
        df, _, _ = derivadas.construir_derivada("manual", expressao_manual_str="2*x")
        res = raizes.metodo_newton_raphson(self.f, df, self.x0, tol=1e-8)
        self.assertTrue(res["sucesso"])
        self.assertAlmostEqual(res["resultado"], self.raiz_exata, places=7)

    def test_metodo_secante(self):
        res = raizes.metodo_secante(self.f, x0=1.0, x1=2.0, tol=1e-8)
        self.assertTrue(res["sucesso"])
        self.assertAlmostEqual(res["resultado"], self.raiz_exata, places=7)


if __name__ == "__main__":
    unittest.main()
