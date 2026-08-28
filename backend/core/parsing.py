import sympy as sp

_TRANSFORMS = sp.parsing.sympy_parser.standard_transformations + (
    sp.parsing.sympy_parser.implicit_multiplication_application,
)

_CONSTANTES = {"e": sp.E, "pi": sp.pi, "E": sp.E, "I": sp.I, "oo": sp.oo}


def _dicionario_local(*variaveis):
    dic = dict(_CONSTANTES)
    for v in variaveis:
        dic.pop(v, None)
        dic[v] = sp.symbols(v)
    return dic


def parse_funcao_1var(expressao_str, variavel="x"):
    try:
        dic = _dicionario_local(variavel)
        expr = sp.parsing.sympy_parser.parse_expr(
            expressao_str, local_dict=dic, transformations=_TRANSFORMS
        )
        func = sp.lambdify(dic[variavel], expr, modules=["numpy"])
        return expr, func
    except Exception as exc:
        raise ValueError(f"Não foi possível interpretar a função '{expressao_str}': {exc}")


def parse_funcao_2var(expressao_str, var1="t", var2="y"):
    try:
        dic = _dicionario_local(var1, var2)
        expr = sp.parsing.sympy_parser.parse_expr(
            expressao_str, local_dict=dic, transformations=_TRANSFORMS
        )
        func = sp.lambdify((dic[var1], dic[var2]), expr, modules=["numpy"])
        return expr, func
    except Exception as exc:
        raise ValueError(f"Não foi possível interpretar a função '{expressao_str}': {exc}")


def derivada_simbolica(expr_sympy, variavel="x"):
    simbolo = sp.symbols(variavel)
    expr_deriv = sp.diff(expr_sympy, simbolo)
    func_deriv = sp.lambdify(simbolo, expr_deriv, modules=["numpy"])
    return expr_deriv, func_deriv
