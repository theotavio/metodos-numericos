def regra_trapezios(f, a, b, n):
    historico = []
    if n <= 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O número de subintervalos (n) deve ser um inteiro positivo."}
    if a == b:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Os limites de integração a e b não podem ser iguais."}

    try:
        h = (b - a) / float(n)
        xs = [a + i * h for i in range(n + 1)]
        ys = [float(f(x)) for x in xs]
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x): {exc}"}

    historico.append(f"{'i':>4} | {'Nó xᵢ':>12} | {'f(xᵢ)':>14} | {'Peso wᵢ':>10} | {'Parcela wᵢ·f(xᵢ)':>18}")

    soma_ponderada = 0.0
    for i, (x, y) in enumerate(zip(xs, ys)):
        peso = 1 if (i == 0 or i == n) else 2
        parcela = peso * y
        soma_ponderada += parcela
        historico.append(f"{i:>4} | {x:>12.6f} | {y:>14.6f} | {peso:>10} | {parcela:>18.6f}")

    integral = (h / 2.0) * soma_ponderada
    historico.append(f"{'∑':>4} | {'h = ' + f'{h:.4f}':>12} | {'—':>14} | {'I ≈ (h/2)·∑':>10} | {integral:>18.8f}")
    return {"sucesso": True, "resultado": integral, "historico": historico, "erro": None}


def regra_simpson_1_3(f, a, b, n):
    historico = []
    if n <= 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O número de subintervalos (n) deve ser um inteiro positivo."}
    if n % 2 != 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"A Regra 1/3 de Simpson exige 'n' PAR. Foi informado n = {n}."}
    if a == b:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Os limites de integração a e b não podem ser iguais."}

    try:
        h = (b - a) / float(n)
        xs = [a + i * h for i in range(n + 1)]
        ys = [float(f(x)) for x in xs]
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x): {exc}"}

    historico.append(f"{'i':>4} | {'Nó xᵢ':>12} | {'f(xᵢ)':>14} | {'Peso wᵢ':>10} | {'Parcela wᵢ·f(xᵢ)':>18}")

    soma_ponderada = 0.0
    for i, (x, y) in enumerate(zip(xs, ys)):
        if i == 0 or i == n:
            peso = 1
        elif i % 2 != 0:
            peso = 4
        else:
            peso = 2
        parcela = peso * y
        soma_ponderada += parcela
        historico.append(f"{i:>4} | {x:>12.6f} | {y:>14.6f} | {peso:>10} | {parcela:>18.6f}")

    integral = (h / 3.0) * soma_ponderada
    historico.append(f"{'∑':>4} | {'h = ' + f'{h:.4f}':>12} | {'—':>14} | {'I ≈ (h/3)·∑':>10} | {integral:>18.8f}")
    return {"sucesso": True, "resultado": integral, "historico": historico, "erro": None}


def regra_simpson_3_8(f, a, b, n):
    historico = []
    if n <= 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O número de subintervalos (n) deve ser um inteiro positivo."}
    if n % 3 != 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"A Regra 3/8 de Simpson exige 'n' MÚLTIPLO DE 3. Foi informado n = {n}."}
    if a == b:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Os limites de integração a e b não podem ser iguais."}

    try:
        h = (b - a) / float(n)
        xs = [a + i * h for i in range(n + 1)]
        ys = [float(f(x)) for x in xs]
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x): {exc}"}

    historico.append(f"{'i':>4} | {'Nó xᵢ':>12} | {'f(xᵢ)':>14} | {'Peso wᵢ':>10} | {'Parcela wᵢ·f(xᵢ)':>18}")

    soma_ponderada = 0.0
    for i, (x, y) in enumerate(zip(xs, ys)):
        if i == 0 or i == n:
            peso = 1
        elif i % 3 == 0:
            peso = 2
        else:
            peso = 3
        parcela = peso * y
        soma_ponderada += parcela
        historico.append(f"{i:>4} | {x:>12.6f} | {y:>14.6f} | {peso:>10} | {parcela:>18.6f}")

    integral = (3.0 * h / 8.0) * soma_ponderada
    historico.append(f"{'∑':>4} | {'h = ' + f'{h:.4f}':>12} | {'—':>14} | {'I ≈ (3h/8)·∑':>10} | {integral:>18.8f}")
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

    historico.append(f"{'i':>4} | {'Ponto tᵢ':>12} | {'Abscissa xᵢ':>16} | {'f(xᵢ)':>16} | {'Peso wᵢ':>10} | {'Parcela wᵢ·f(xᵢ)':>18}")

    try:
        soma = 0.0
        for idx, (r, w) in enumerate(zip(raizes, pesos)):
            x_real = c * r + d
            valor = float(f(x_real))
            parcela = w * valor
            soma += parcela
            historico.append(f"{idx+1:>4} | {r:>12.6f} | {x_real:>16.8f} | {valor:>16.8f} | {w:>10.1f} | {parcela:>18.8f}")
        integral = c * soma
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x): {exc}"}

    historico.append(f"{'∑':>4} | {'c = ' + f'{c:.4f}':>12} | {'—':>16} | {'—':>16} | {'I ≈ c·∑':>10} | {integral:>18.8f}")
    return {"sucesso": True, "resultado": integral, "historico": historico, "erro": None}
