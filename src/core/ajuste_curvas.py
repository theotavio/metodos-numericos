import numpy as np


def ajuste_linear_simples(pontos):
    historico = []
    n = len(pontos)
    if n < 2:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "São necessários pelo menos 2 pontos para o ajuste linear."}

    xs = np.array([p[0] for p in pontos], dtype=float)
    ys = np.array([p[1] for p in pontos], dtype=float)

    soma_x = np.sum(xs)
    soma_y = np.sum(ys)
    soma_xy = np.sum(xs * ys)
    soma_x2 = np.sum(xs**2)

    denom = n * soma_x2 - soma_x**2
    if denom == 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Divisão por zero: todos os valores de x são iguais."}

    a1 = (n * soma_xy - soma_x * soma_y) / denom
    a0 = (soma_y - a1 * soma_x) / n

    historico.append(f"Σx={soma_x:.6f}  Σy={soma_y:.6f}  Σxy={soma_xy:.6f}  Σx²={soma_x2:.6f}")
    historico.append(f"a1 = (nΣxy - ΣxΣy) / (nΣx² - (Σx)²) = {a1:.8f}")
    historico.append(f"a0 = (Σy - a1·Σx) / n = {a0:.8f}")
    historico.append(f"Reta ajustada: y = {a0:.6f} + {a1:.6f}x")

    y_pred = a0 + a1 * xs
    ss_res = np.sum((ys - y_pred) ** 2)
    ss_tot = np.sum((ys - np.mean(ys)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 1.0
    historico.append(f"R² = {r2:.6f}")

    return {"sucesso": True, "resultado": {"a0": a0, "a1": a1, "r2": r2},
            "historico": historico, "erro": None}


def ajuste_linear_multiplo(X, y):
    historico = []
    try:
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float)
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao interpretar dados: {exc}"}

    if X.shape[0] != y.shape[0]:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Número de linhas de X ({X.shape[0]}) difere do tamanho de y ({y.shape[0]})."}

    n, k = X.shape
    if n <= k:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"São necessárias mais observações ({n}) do que variáveis ({k}) para o ajuste."}

    Xb = np.hstack([np.ones((n, 1)), X])
    historico.append(f"Matriz de projeto (com coluna de 1s para o intercepto), dimensão {Xb.shape}")

    try:
        XtX = Xb.T @ Xb
        Xty = Xb.T @ y
        coef = np.linalg.solve(XtX, Xty)
    except np.linalg.LinAlgError:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Sistema normal singular: variáveis podem ser colineares."}

    historico.append("Sistema normal (XᵀX)β = Xᵀy resolvido.")
    historico.append("Coeficientes β0 (intercepto), β1, β2, ...:")
    historico.append("  ".join(f"{c:.6f}" for c in coef))

    y_pred = Xb @ coef
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 1.0
    historico.append(f"R² = {r2:.6f}")

    return {"sucesso": True, "resultado": {"coeficientes": coef.tolist(), "r2": r2},
            "historico": historico, "erro": None}