import numpy as np


def ajuste_linear_simples(pontos):
    historico = []
    n = len(pontos)
    if n < 2:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "São necessários pelo menos 2 pontos para o ajuste linear simples."}

    xs = np.array([p[0] for p in pontos], dtype=float)
    ys = np.array([p[1] for p in pontos], dtype=float)

    soma_x = float(np.sum(xs))
    soma_y = float(np.sum(ys))
    soma_xy = float(np.sum(xs * ys))
    soma_x2 = float(np.sum(xs**2))

    denom = n * soma_x2 - soma_x**2
    if denom == 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Divisão por zero: todos os valores de x são idênticos."}

    a1 = (n * soma_xy - soma_x * soma_y) / denom
    a0 = (soma_y - a1 * soma_x) / n

    y_pred = a0 + a1 * xs
    residuos = ys - y_pred
    ss_res = float(np.sum(residuos**2))
    ss_tot = float(np.sum((ys - np.mean(ys)) ** 2))
    r2 = float(1 - ss_res / ss_tot if ss_tot != 0 else 1.0)

    historico.append(f"{'i':>4} | {'xᵢ':>10} | {'yᵢ':>10} | {'xᵢ·yᵢ':>12} | {'xᵢ²':>12} | {'ŷᵢ':>10} | {'Resíduo eᵢ':>12}")
    for i in range(n):
        historico.append(f"{i+1:>4} | {xs[i]:>10.4f} | {ys[i]:>10.4f} | {xs[i]*ys[i]:>12.4f} | {xs[i]**2:>12.4f} | {y_pred[i]:>10.4f} | {residuos[i]:>12.4e}")

    historico.append(f"{'∑':>4} | {soma_x:>10.4f} | {soma_y:>10.4f} | {soma_xy:>12.4f} | {soma_x2:>12.4f} | {'R² = ' + f'{r2:.4f}':>10} | {ss_res:>12.4e}")
    return {"sucesso": True, "resultado": {"a0": a0, "a1": a1, "r2": r2},
            "historico": historico, "erro": None}


def ajuste_linear_multiplo(X, y):
    historico = []
    try:
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float)
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao interpretar dados numéricos: {exc}"}

    if X.shape[0] != y.shape[0]:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Número de linhas de X ({X.shape[0]}) difere do tamanho de y ({y.shape[0]})."}

    n, k = X.shape
    if n <= k:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"São necessárias mais observações ({n}) do que variáveis ({k}) para o ajuste."}

    Xb = np.hstack([np.ones((n, 1)), X])

    try:
        XtX = Xb.T @ Xb
        Xty = Xb.T @ y
        coef = np.linalg.solve(XtX, Xty)
    except np.linalg.LinAlgError:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Sistema normal singular: variáveis explicativas colineares."}

    y_pred = Xb @ coef
    residuos = y - y_pred
    ss_res = float(np.sum(residuos**2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = float(1 - ss_res / ss_tot if ss_tot != 0 else 1.0)

    historico.append(f"{'Obs.':>5} | {'y Real':>12} | {'ŷ Estimado':>12} | {'Resíduo eᵢ':>14} | {'eᵢ²':>14}")
    for i in range(n):
        historico.append(f"{i+1:>5} | {y[i]:>12.4f} | {y_pred[i]:>12.4f} | {residuos[i]:>14.4e} | {residuos[i]**2:>14.4e}")

    historico.append(f"{'∑':>5} | {np.sum(y):>12.4f} | {np.sum(y_pred):>12.4f} | {np.sum(residuos):>14.4e} | {ss_res:>14.4e}")
    return {"sucesso": True, "resultado": {"coeficientes": coef.tolist(), "r2": r2},
            "historico": historico, "erro": None}
