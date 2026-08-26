"""
Módulo de Cálculo e Construção de Derivadas para Métodos Numéricos.
Suporta:
  - Derivada Simbólica (Analítica exata via SymPy)
  - Diferenças Finitas Centrais [ O(h²) ]
  - Diferenças Finitas Progressivas [ O(h) ]
  - Diferenças Finitas Regressivas [ O(h) ]
  - Diferenciação por Passo Complexo (Complex-Step Derivative Approximation)
  - Derivada Manual (Expressão algébrica fornecida pelo usuário)
"""

import sympy as sp
import numpy as np
from core import parsing


TIPOS_DERIVADAS = {
    "Simbólica [ SymPy / Analítica ]": "simbolica",
    "Diferença Finita Central [ O(h²) ]": "central",
    "Diferença Finita Progressiva [ O(h) ]": "progressiva",
    "Diferença Finita Regressiva [ O(h) ]": "regressiva",
    "Passo Complexo [ Complex-Step ]": "complexa",
    "Manual [ Expressão de f'(x) ]": "manual",
}


def construir_derivada(
    tipo="simbolica",
    f=None,
    expr_sympy=None,
    variavel="x",
    h=1e-6,
    expressao_manual_str=None
):
    """
    Constrói e retorna uma tupla (df_func, descricao_str, expr_deriv_sympy_ou_none).

    Parâmetros:
      - tipo: 'simbolica', 'central', 'progressiva', 'regressiva', 'complexa', 'manual'
      - f: função callable f(x) -> float (usada nas diferenças finitas)
      - expr_sympy: expressão SymPy de f(x) (usada em simbólica e passo complexo)
      - variavel: nome da variável independente (padrão 'x')
      - h: passo de diferenciação (para diferenças finitas e passo complexo)
      - expressao_manual_str: string contendo a fórmula de f'(x) caso tipo='manual'

    Retorna:
      - df_func: callable df(x) -> float
      - descricao_str: texto descritivo do método de derivação configurado
      - expr_deriv: expressão SymPy de f'(x) se calculada simbolicamente ou manualmente, caso contrário None
    """
    tipo = str(tipo).lower().strip()

    if tipo == "simbolica":
        if expr_sympy is None:
            raise ValueError("Expressão SymPy necessária para calcular derivada simbólica.")
        simbolo = sp.symbols(variavel)
        expr_deriv = sp.diff(expr_sympy, simbolo)
        df_func = sp.lambdify(simbolo, expr_deriv, modules=["numpy"])
        descricao = f"Derivada Simbólica (Analítica Exata): f'({variavel}) = {expr_deriv}"
        return df_func, descricao, expr_deriv

    elif tipo == "central":
        if f is None:
            raise ValueError("Função f(x) necessária para calcular diferença finita central.")
        h_val = float(h)
        if h_val <= 0:
            raise ValueError("O passo de diferenciação h deve ser estritamente positivo (h > 0).")

        def df_central(x):
            try:
                x_f = float(x)
                return float((f(x_f + h_val) - f(x_f - h_val)) / (2.0 * h_val))
            except Exception as exc:
                raise ValueError(f"Erro ao calcular derivada por diferença central em x={x}: {exc}")

        descricao = f"Diferença Finita Central [ O(h²) ] com passo h = {h_val:g}"
        return df_central, descricao, None

    elif tipo == "progressiva":
        if f is None:
            raise ValueError("Função f(x) necessária para calcular diferença finita progressiva.")
        h_val = float(h)
        if h_val <= 0:
            raise ValueError("O passo de diferenciação h deve ser estritamente positivo (h > 0).")

        def df_prog(x):
            try:
                x_f = float(x)
                return float((f(x_f + h_val) - f(x_f)) / h_val)
            except Exception as exc:
                raise ValueError(f"Erro ao calcular derivada por diferença progressiva em x={x}: {exc}")

        descricao = f"Diferença Finita Progressiva [ O(h) ] com passo h = {h_val:g}"
        return df_prog, descricao, None

    elif tipo == "regressiva":
        if f is None:
            raise ValueError("Função f(x) necessária para calcular diferença finita regressiva.")
        h_val = float(h)
        if h_val <= 0:
            raise ValueError("O passo de diferenciação h deve ser estritamente positivo (h > 0).")

        def df_reg(x):
            try:
                x_f = float(x)
                return float((f(x_f) - f(x_f - h_val)) / h_val)
            except Exception as exc:
                raise ValueError(f"Erro ao calcular derivada por diferença regressiva em x={x}: {exc}")

        descricao = f"Diferença Finita Regressiva [ O(h) ] com passo h = {h_val:g}"
        return df_reg, descricao, None

    elif tipo == "complexa":
        if expr_sympy is None and f is None:
            raise ValueError("Expressão ou função necessária para diferenciação por passo complexo.")
        h_val = float(h)
        if h_val <= 0:
            raise ValueError("O passo h para diferenciação por passo complexo deve ser positivo (h > 0).")

        if expr_sympy is not None:
            simbolo = sp.symbols(variavel)
            func_complex = sp.lambdify(simbolo, expr_sympy, modules=["numpy", "cmath"])
        else:
            func_complex = f

        def df_complex(x):
            try:
                z = complex(float(x), h_val)
                fz = func_complex(z)
                if isinstance(fz, (complex, np.complex128, np.complex64)):
                    return float(fz.imag / h_val)
                elif hasattr(fz, "imag"):
                    return float(fz.imag / h_val)
                return 0.0
            except Exception as exc:
                raise ValueError(f"Erro ao calcular derivada por passo complexo em x={x}: {exc}")

        descricao = f"Diferenciação por Passo Complexo (Complex-Step) com h = {h_val:g}"
        return df_complex, descricao, None

    elif tipo == "manual":
        if not expressao_manual_str or not str(expressao_manual_str).strip():
            raise ValueError("Para a opção de derivada manual, digite a expressão de f'(x).")
        expr_manual, df_manual = parsing.parse_funcao_1var(expressao_manual_str, variavel=variavel)
        descricao = f"Derivada Informada Manualmente: f'({variavel}) = {expr_manual}"
        return df_manual, descricao, expr_manual

    else:
        raise ValueError(f"Tipo de derivada desconhecido: '{tipo}'. Tipos válidos: {list(TIPOS_DERIVADAS.values())}")
