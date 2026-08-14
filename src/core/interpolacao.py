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
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"x = {x_alvo} está fora do intervalo dos pontos fornecidos."}

    if x1 - x0 == 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Dois pontos com o mesmo x foram fornecidos (divisão por zero)."}

    historico.append(f"Intervalo escolhido: [x0={x0}, x1={x1}]")
    historico.append(f"y0={y0}, y1={y1}")
    y_alvo = y0 + (y1 - y0) * (x_alvo - x0) / (x1 - x0)
    historico.append(f"y = y0 + (y1-y0)*(x-x0)/(x1-x0) = {y_alvo:.8f}")

    return {"sucesso": True, "resultado": y_alvo, "historico": historico, "erro": None}


def interpolacao_quadratica(pontos, x_alvo):
    historico = []
    if len(pontos) < 3:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "São necessários exatamente 3 pontos para interpolação quadrática."}

    (x0, y0), (x1, y1), (x2, y2) = pontos[0], pontos[1], pontos[2]
    A = np.array([
        [x0**2, x0, 1],
        [x1**2, x1, 1],
        [x2**2, x2, 1],
    ], dtype=float)
    b = np.array([y0, y1, y2], dtype=float)

    try:
        coef = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Sistema singular: verifique se os pontos possuem valores de x distintos."}

    a, bb, c = coef
    historico.append(f"Polinômio ajustado: p(x) = {a:.6f}x^2 + {bb:.6f}x + {c:.6f}")
    y_alvo = a * x_alvo**2 + bb * x_alvo + c
    historico.append(f"p({x_alvo}) = {y_alvo:.8f}")

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
                "erro": "Os valores de x devem ser distintos."}

    resultado = 0.0
    for i in range(n):
        xi, yi = pontos[i]
        termo = yi
        partes = []
        for j in range(n):
            if j != i:
                xj = pontos[j][0]
                if xi - xj == 0:
                    return {"sucesso": False, "resultado": None, "historico": historico,
                            "erro": "Dois pontos possuem o mesmo x (divisão por zero)."}
                termo *= (x_alvo - xj) / (xi - xj)
                partes.append(f"(x-{xj})/({xi}-{xj})")
        historico.append(f"L{i}(x) = " + " * ".join(partes) + f"  =>  termo = {termo:.8f}")
        resultado += termo

    historico.append(f"P({x_alvo}) = soma dos termos = {resultado:.8f}")
    return {"sucesso": True, "resultado": resultado, "historico": historico, "erro": None}


def diferencas_divididas_newton(pontos, x_alvo):
    historico = []
    n = len(pontos)
    if n < 2:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "São necessários pelo menos 2 pontos."}

    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]
    if len(set(xs)) != len(xs):
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Os valores de x devem ser distintos."}

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
    historico.append("Coeficientes f[x0], f[x0,x1], f[x0,x1,x2], ...:")
    historico.append("  ".join(f"{c:.6f}" for c in coeficientes))

    resultado = coeficientes[0]
    produto = 1.0
    for i in range(1, n):
        produto *= (x_alvo - xs[i - 1])
        resultado += coeficientes[i] * produto

    historico.append(f"P({x_alvo}) = {resultado:.8f}")
    return {"sucesso": True, "resultado": resultado, "historico": historico, "erro": None,
            "coeficientes": coeficientes}