def regra_trapezios(f, a, b, n):
    historico = []
    if n <= 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O número de subintervalos (n) deve ser um inteiro positivo."}
    if a == b:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Os limites de integração a e b não podem ser iguais."}

    try:
        h = (b - a) / n
        xs = [a + i * h for i in range(n + 1)]
        ys = [f(x) for x in xs]
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x): {exc}"}

    historico.append(f"h = (b - a) / n = {h:.6f}")
    historico.append(f"{'i':>4} | {'x_i':>12} | {'f(x_i)':>12}")
    for i, (x, y) in enumerate(zip(xs, ys)):
        historico.append(f"{i:>4} | {x:>12.6f} | {y:>12.6f}")

    soma_extremos = ys[0] + ys[-1]
    soma_internos = sum(ys[1:-1])
    integral = (h / 2.0) * (soma_extremos + 2 * soma_internos)

    historico.append(f"Integral ≈ (h/2)·[f(x0)+f(xn) + 2Σf(xi)] = {integral:.8f}")
    return {"sucesso": True, "resultado": integral, "historico": historico, "erro": None}


def regra_simpson_1_3(f, a, b, n):
    historico = []
    if n <= 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O número de subintervalos (n) deve ser um inteiro positivo."}
    if n % 2 != 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"A Regra 1/3 de Simpson exige n PAR. Foi informado n = {n}."}
    if a == b:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Os limites de integração a e b não podem ser iguais."}

    try:
        h = (b - a) / n
        xs = [a + i * h for i in range(n + 1)]
        ys = [f(x) for x in xs]
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x): {exc}"}

    historico.append(f"h = (b - a) / n = {h:.6f}")
    historico.append(f"{'i':>4} | {'x_i':>12} | {'f(x_i)':>12} | {'Peso':>6}")

    soma_impares = 0.0
    soma_pares = 0.0
    for i, (x, y) in enumerate(zip(xs, ys)):
        if i == 0 or i == n:
            peso = 1
        elif i % 2 != 0:
            peso = 4
            soma_impares += y
        else:
            peso = 2
            soma_pares += y
        historico.append(f"{i:>4} | {x:>12.6f} | {y:>12.6f} | {peso:>6}")

    integral = (h / 3.0) * (ys[0] + ys[-1] + 4 * soma_impares + 2 * soma_pares)
    historico.append(f"Integral ≈ (h/3)·[f(x0)+f(xn) + 4Σímpares + 2Σpares] = {integral:.8f}")

    return {"sucesso": True, "resultado": integral, "historico": historico, "erro": None}


def regra_simpson_3_8(f, a, b, n):
    historico = []
    if n <= 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O número de subintervalos (n) deve ser um inteiro positivo."}
    if n % 3 != 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"A Regra 3/8 de Simpson exige n múltiplo de 3. Foi informado n = {n}."}
    if a == b:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Os limites de integração a e b não podem ser iguais."}

    try:
        h = (b - a) / n
        xs = [a + i * h for i in range(n + 1)]
        ys = [f(x) for x in xs]
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x): {exc}"}

    historico.append(f"h = (b - a) / n = {h:.6f}")
    soma = ys[0] + ys[-1]
    for i in range(1, n):
        peso = 3 if i % 3 != 0 else 2
        soma += peso * ys[i]
        historico.append(f"{i:>4} | x={xs[i]:>10.6f} | f(x)={ys[i]:>10.6f} | peso={peso}")

    integral = (3 * h / 8.0) * soma
    historico.append(f"Integral ≈ (3h/8)·Σ(pesos·f(xi)) = {integral:.8f}")

    return {"sucesso": True, "resultado": integral, "historico": historico, "erro": None}


def quadratura_gaussiana_2p(f, a, b):
    historico = []
    if a == b:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Os limites de integração a e b não podem ser iguais."}

    c = (b - a) / 2.0
    d = (b + a) / 2.0
    raizes = [-0.5773502691896257, 0.5773502691896257]
    pesos = [1.0, 1.0]

    try:
        soma = 0.0
        for r, w in zip(raizes, pesos):
            x_real = c * r + d
            valor = f(x_real)
            soma += w * valor
            historico.append(f"x = {x_real:.8f}   f(x) = {valor:.8f}   peso = {w}")
        integral = c * soma
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x): {exc}"}

    historico.append(f"Integral ≈ c·Σ(wi·f(xi)), c=(b-a)/2 = {c:.6f}  =>  {integral:.8f}")
    return {"sucesso": True, "resultado": integral, "historico": historico, "erro": None}