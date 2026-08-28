import numpy as np


def interpolacao_linear(pontos, x_alvo):
    historico = []
    if len(pontos) < 2:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "São necessários pelo menos 2 pontos para interpolação linear."}

    pontos = sorted(pontos, key=lambda p: p[0])
    x0 = y0 = x1 = y1 = None
    for i in range(len(pontos) - 1):
        if pontos[i][0] <= x_alvo <= pontos[i + 1][0]:
            x0, y0 = pontos[i]
            x1, y1 = pontos[i + 1]
            break

    if x0 is None:
        if x_alvo < pontos[0][0]:
            x0, y0 = pontos[0]
            x1, y1 = pontos[1]
        else:
            x0, y0 = pontos[-2]
            x1, y1 = pontos[-1]

    if x1 - x0 == 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Dois nós com o mesmo valor de x fornecidos (divisão por zero)."}

    historico.append(f"{'Etapa':>6} | {'Subintervalo [x₀, x₁]':>24} | {'Fórmula / Avaliação':<40}")
    historico.append(f"{'1':>6} | {f'[{x0:.4f}, {x1:.4f}]':>24} | {'P(x) = y₀ + (y₁ - y₀)·(x - x₀)/(x₁ - x₀)':<40}")
    
    y_alvo = y0 + (y1 - y0) * (x_alvo - x0) / (x1 - x0)
    historico.append(f"{'2':>6} | {f'x* = {x_alvo:.4f}':>24} | {f'P({x_alvo:.4f}) = {y_alvo:.8f}':<40}")

    return {"sucesso": True, "resultado": y_alvo, "historico": historico, "erro": None}


def interpolacao_quadratica(pontos, x_alvo):
    historico = []
    if len(pontos) != 3:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "A interpolação quadrática exige exatamente 3 pontos com valores de x distintos."}

    (x0, y0), (x1, y1), (x2, y2) = pontos[0], pontos[1], pontos[2]
    A = np.array([
        [x0**2, x0, 1.0],
        [x1**2, x1, 1.0],
        [x2**2, x2, 1.0],
    ], dtype=float)
    b = np.array([y0, y1, y2], dtype=float)

    try:
        coef = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Sistema singular: verifique se os 3 pontos possuem valores de x distintos."}

    a, bb, c = coef
    y_alvo = float(a * x_alvo**2 + bb * x_alvo + c)

    historico.append(f"{'i':>4} | {'Nó xᵢ':>12} | {'Valor yᵢ':>12} | {'Equação do Sistema a·xᵢ² + b·xᵢ + c = yᵢ':<45}")
    historico.append(f"{1:>4} | {x0:>12.4f} | {y0:>12.4f} | {f'{x0**2:.2f}a + {x0:.2f}b + c = {y0:.4f}':<45}")
    historico.append(f"{2:>4} | {x1:>12.4f} | {y1:>12.4f} | {f'{x1**2:.2f}a + {x1:.2f}b + c = {y1:.4f}':<45}")
    historico.append(f"{3:>4} | {x2:>12.4f} | {y2:>12.4f} | {f'{x2**2:.2f}a + {x2:.2f}b + c = {y2:.4f}':<45}")
    historico.append(f"{'Pol':>4} | {'Polinômio':>12} | {f'P(x*)':>12} | {f'P(x) = {a:.4f}x² + ({bb:.4f})x + ({c:.4f})  ->  P({x_alvo}) = {y_alvo:.6f}':<45}")

    return {"sucesso": True, "resultado": y_alvo, "historico": historico, "erro": None,
            "coeficientes": coef.tolist()}


def interpolacao_lagrange(pontos, x_alvo):
    historico = []
    n = len(pontos)
    if n < 2:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "São necessários pelo menos 2 pontos para interpolação de Lagrange."}

    xs = [p[0] for p in pontos]
    if len(set(xs)) != len(xs):
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Todos os valores de x devem ser estritamente distintos."}

    historico.append(f"{'i':>4} | {'Nó xᵢ':>12} | {'Valor yᵢ':>12} | {'Polinômio Base Lᵢ(x*)':>22} | {'Termo Lᵢ(x*)·yᵢ':>18}")
    
    resultado = 0.0
    for i in range(n):
        xi, yi = pontos[i]
        termo_L = 1.0
        for j in range(n):
            if j != i:
                xj = pontos[j][0]
                termo_L *= (x_alvo - xj) / (xi - xj)
        termo_total = yi * termo_L
        resultado += termo_total
        historico.append(f"{i+1:>4} | {xi:>12.4f} | {yi:>12.4f} | {termo_L:>22.8f} | {termo_total:>18.8f}")

    historico.append(f"{'∑':>4} | {'x* = ' + str(x_alvo):>12} | {'—':>12} | {'P(x*) = ∑ Lᵢ(x*)·yᵢ':>22} | {resultado:>18.8f}")
    return {"sucesso": True, "resultado": resultado, "historico": historico, "erro": None}


def diferencas_divididas_newton(pontos, x_alvo):
    historico = []
    n = len(pontos)
    if n < 2:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "São necessários pelo menos 2 pontos para a forma de Newton."}

    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]
    if len(set(xs)) != len(xs):
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Todos os valores de x devem ser distintos."}

    tabela = [ys[:]]
    for nivel in range(1, n):
        coluna_anterior = tabela[nivel - 1]
        nova_coluna = []
        for i in range(n - nivel):
            denom = xs[i + nivel] - xs[i]
            if denom == 0:
                return {"sucesso": False, "resultado": None, "historico": historico,
                        "erro": "Divisão por zero na tabela de diferenças divididas."}
            valor = (coluna_anterior[i + 1] - coluna_anterior[i]) / denom
            nova_coluna.append(valor)
        tabela.append(nova_coluna)

    coeficientes = [tabela[i][0] for i in range(n)]

    historico.append(f"{'i':>4} | {'Nó xᵢ':>12} | {'Ordem 0 f[xᵢ]':>16} | {'Coeficiente f[x₀...xᵢ]':>24}")
    for i in range(n):
        historico.append(f"{i:>4} | {xs[i]:>12.4f} | {ys[i]:>16.6f} | {coeficientes[i]:>24.8f}")

    resultado = coeficientes[0]
    produto = 1.0
    for i in range(1, n):
        produto *= (x_alvo - xs[i - 1])
        resultado += coeficientes[i] * produto

    historico.append(f"{'Fim':>4} | {f'x* = {x_alvo:.4f}':>12} | {'Resultado P(x*)':>16} | {resultado:>24.8f}")
    return {"sucesso": True, "resultado": resultado, "historico": historico, "erro": None,
            "coeficientes": coeficientes}
