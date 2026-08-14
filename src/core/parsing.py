import sympy as sp

_TRANSFORMS = sp.parsing.sympy_parser.standard_transformations + (
    sp.parsing.sympy_parser.implicit_multiplication_application,
)


def parse_funcao_1var(expressao_str, variavel="x"):
    try:
        simbolo = sp.symbols(variavel)
        expr = sp.parsing.sympy_parser.parse_expr(
            expressao_str, local_dict={variavel: simbolo}, transformations=_TRANSFORMS
        )
        func = sp.lambdify(simbolo, expr, modules=["numpy"])
        return expr, func
    except Exception as exc:
        raise ValueError(f"Não foi possível interpretar a função '{expressao_str}': {exc}")


def parse_funcao_2var(expressao_str, var1="t", var2="y"):
    try:
        s1, s2 = sp.symbols(f"{var1} {var2}")
        expr = sp.parsing.sympy_parser.parse_expr(
            expressao_str, local_dict={var1: s1, var2: s2}, transformations=_TRANSFORMS
        )
        func = sp.lambdify((s1, s2), expr, modules=["numpy"])
        return expr, func
    except Exception as exc:
        raise ValueError(f"Não foi possível interpretar a função '{expressao_str}': {exc}")


def derivada_simbolica(expr_sympy, variavel="x"):
    simbolo = sp.symbols(variavel)
    expr_deriv = sp.diff(expr_sympy, simbolo)
    func_deriv = sp.lambdify(simbolo, expr_deriv, modules=["numpy"])
    return expr_deriv, func_deriv