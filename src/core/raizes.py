"""
Módulo de Métodos Numéricos para Encontrar Raízes de Funções de Uma Variável: f(x) = 0.
Implementa: Bisseção, Newton-Raphson, Secante (Quasi-Newton), Cordas (Falsa Posição), Pégaso (Acelerado) e Iteração Linear (Ponto Fixo).
"""


def metodo_bissecao(f, a, b, tol=1e-6, max_iter=100):
    historico = []
    try:
        fa, fb = f(a), f(b)
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x) nos extremos: {exc}"}

    if fa == 0:
        return {"sucesso": True, "resultado": a, "historico": ["f(a) = 0 -> raiz exata em a"], "erro": None, "iteracoes": 0}
    if fb == 0:
        return {"sucesso": True, "resultado": b, "historico": ["f(b) = 0 -> raiz exata em b"], "erro": None, "iteracoes": 0}
    if fa * fb > 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "f(a) e f(b) possuem o mesmo sinal. O método exige troca de sinal em [a, b]."}

    historico.append(f"{'Iter':>4} | {'a':>12} | {'b':>12} | {'xm':>12} | {'f(xm)':>12} | {'Erro':>12}")
    xm_anterior = a
    for i in range(1, max_iter + 1):
        xm = (a + b) / 2.0
        try:
            fxm = f(xm)
        except ZeroDivisionError:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Divisão por zero ao avaliar f({xm}) na iteração {i}."}
        except Exception as exc:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Erro ao avaliar f(x) na iteração {i}: {exc}"}

        erro_estimado = abs(xm - xm_anterior) if i > 1 else abs(b - a)
        historico.append(f"{i:>4} | {a:>12.6f} | {b:>12.6f} | {xm:>12.6f} | {fxm:>12.6f} | {erro_estimado:>12.6e}")

        if abs(fxm) < tol or (b - a) / 2.0 < tol:
            return {"sucesso": True, "resultado": xm, "historico": historico, "erro": None, "iteracoes": i}

        if fa * fxm < 0:
            b, fb = xm, fxm
        else:
            a, fa = xm, fxm
        xm_anterior = xm

    return {"sucesso": False, "resultado": xm, "historico": historico,
            "erro": f"Máximo de iterações ({max_iter}) atingido sem convergência para tolerância {tol}.",
            "iteracoes": max_iter}


def metodo_newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    historico = []
    x_atual = x0
    historico.append(f"{'Iter':>4} | {'x_n':>14} | {'f(x_n)':>14} | {'f_(x_n)':>14} | {'Erro':>12}")

    for i in range(1, max_iter + 1):
        try:
            fx = f(x_atual)
            dfx = df(x_atual)
        except Exception as exc:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Erro ao avaliar f(x) ou f'(x) na iteração {i}: {exc}"}

        if dfx == 0:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Derivada nula em x = {x_atual:.6f} na iteração {i}."}

        x_novo = x_atual - fx / dfx
        erro_estimado = abs(x_novo - x_atual)
        historico.append(f"{i:>4} | {x_atual:>14.8f} | {fx:>14.8f} | {dfx:>14.8f} | {erro_estimado:>12.6e}")

        if erro_estimado < tol:
            return {"sucesso": True, "resultado": x_novo, "historico": historico, "erro": None, "iteracoes": i}
        x_atual = x_novo

    return {"sucesso": False, "resultado": x_atual, "historico": historico,
            "erro": f"Máximo de iterações ({max_iter}) atingido sem convergência para tolerância {tol}.",
            "iteracoes": max_iter}


def metodo_secante(f, x0, x1, tol=1e-6, max_iter=100):
    """Método da Secante (Quasi-Newton aberto sem derivada explícita)."""
    historico = []
    if x0 == x1:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Os pontos iniciais x₀ e x₁ não podem ser iguais."}

    try:
        f0 = f(x0)
        f1 = f(x1)
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x) nos pontos iniciais: {exc}"}

    historico.append(f"{'Iter':>4} | {'x_k':>14} | {'f(x_k)':>14} | {'Erro':>12}")
    historico.append(f"{0:>4} | {x0:>14.8f} | {f0:>14.8f} | {'—':>12}")
    historico.append(f"{1:>4} | {x1:>14.8f} | {f1:>14.8f} | {abs(x1 - x0):>12.6e}")

    if abs(f1) < tol:
        return {"sucesso": True, "resultado": x1, "historico": historico, "erro": None, "iteracoes": 1}

    x_ant, f_ant = x0, f0
    x_at, f_at = x1, f1

    for i in range(2, max_iter + 1):
        delta_f = f_at - f_ant
        if delta_f == 0:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Divisão por zero: f(x_{i-1}) - f(x_{i-2}) = 0 na iteração {i}."}

        x_novo = x_at - f_at * (x_at - x_ant) / delta_f
        try:
            f_novo = f(x_novo)
        except Exception as exc:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Erro ao avaliar f(x) em x={x_novo}: {exc}"}

        erro_estimado = abs(x_novo - x_at)
        historico.append(f"{i:>4} | {x_novo:>14.8f} | {f_novo:>14.8f} | {erro_estimado:>12.6e}")

        if abs(f_novo) < tol or erro_estimado < tol:
            return {"sucesso": True, "resultado": x_novo, "historico": historico, "erro": None, "iteracoes": i}

        x_ant, f_ant = x_at, f_at
        x_at, f_at = x_novo, f_novo

    return {"sucesso": False, "resultado": x_at, "historico": historico,
            "erro": f"Máximo de iterações ({max_iter}) atingido sem convergência para tolerância {tol}.",
            "iteracoes": max_iter}


def metodo_cordas(f, a, b, tol=1e-6, max_iter=100):
    """Método das Cordas (Falsa Posição / Regula Falsi)."""
    historico = []
    try:
        fa, fb = f(a), f(b)
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x) nos extremos: {exc}"}

    if fa * fb > 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "f(a) e f(b) possuem o mesmo sinal. O método exige troca de sinal em [a, b]."}

    historico.append(f"{'Iter':>4} | {'a':>12} | {'b':>12} | {'x':>12} | {'f(x)':>12} | {'Erro':>12}")
    x_anterior = a
    for i in range(1, max_iter + 1):
        if fb - fa == 0:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Divisão por zero: f(b) - f(a) = 0 na iteração {i}."}

        x = b - fb * (b - a) / (fb - fa)
        try:
            fx = f(x)
        except Exception as exc:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Erro ao avaliar f(x) em x={x}: {exc}"}

        erro_estimado = abs(x - x_anterior)
        historico.append(f"{i:>4} | {a:>12.6f} | {b:>12.6f} | {x:>12.6f} | {fx:>12.6f} | {erro_estimado:>12.6e}")

        if abs(fx) < tol or erro_estimado < tol:
            return {"sucesso": True, "resultado": x, "historico": historico, "erro": None, "iteracoes": i}

        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx
        x_anterior = x

    return {"sucesso": False, "resultado": x, "historico": historico,
            "erro": f"Máximo de iterações ({max_iter}) atingido sem convergência para tolerância {tol}.",
            "iteracoes": max_iter}


def metodo_pegaso(f, a, b, tol=1e-6, max_iter=100):
    """Método de Pégaso (Dowell & Jarratt, 1971) - Aceleração com convergência de ordem 1.839."""
    historico = []
    try:
        fa, fb = f(a), f(b)
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x) nos extremos: {exc}"}

    if fa * fb > 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "f(a) e f(b) possuem o mesmo sinal. O método exige troca de sinal em [a, b]."}

    historico.append(f"{'Iter':>4} | {'a':>12} | {'b':>12} | {'x':>12} | {'f(x)':>12} | {'Erro':>12}")
    x_anterior = a
    for i in range(1, max_iter + 1):
        if fb - fa == 0:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Divisão por zero: f(b) - f(a) = 0 na iteração {i}."}

        x = b - fb * (b - a) / (fb - fa)
        try:
            fx = f(x)
        except Exception as exc:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Erro ao avaliar f(x) em x={x}: {exc}"}

        erro_estimado = abs(x - x_anterior)
        historico.append(f"{i:>4} | {a:>12.6f} | {b:>12.6f} | {x:>12.6f} | {fx:>12.6f} | {erro_estimado:>12.6e}")

        if abs(fx) < tol or erro_estimado < tol:
            return {"sucesso": True, "resultado": x, "historico": historico, "erro": None, "iteracoes": i}

        if fb * fx < 0:
            a, fa = b, fb
            b, fb = x, fx
        else:
            fa = fa * fb / (fb + fx)
            b, fb = x, fx
        x_anterior = x

    return {"sucesso": False, "resultado": x, "historico": historico,
            "erro": f"Máximo de iterações ({max_iter}) atingido sem convergência para tolerância {tol}.",
            "iteracoes": max_iter}


def metodo_iteracao_linear(phi, x0, tol=1e-6, max_iter=100):
    """Método do Ponto Fixo / Iteração Linear: x = phi(x)."""
    historico = []
    x_atual = x0
    historico.append(f"{'Iter':>4} | {'x_n':>16} | {'phi(x_n)':>16} | {'Erro':>12}")

    for i in range(1, max_iter + 1):
        try:
            x_novo = phi(x_atual)
        except Exception as exc:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Erro ao avaliar phi(x) na iteração {i}: {exc}"}

        erro_estimado = abs(x_novo - x_atual)
        historico.append(f"{i:>4} | {x_atual:>16.8f} | {x_novo:>16.8f} | {erro_estimado:>12.6e}")

        if erro_estimado < tol:
            return {"sucesso": True, "resultado": x_novo, "historico": historico, "erro": None, "iteracoes": i}

        if abs(x_novo) > 1e15 or erro_estimado != erro_estimado:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"A sequência diverge (|x| cresceu sem limite) na iteração {i}. "
                            f"Escolha outra função de iteração phi(x)."}
        x_atual = x_novo

    return {"sucesso": False, "resultado": x_atual, "historico": historico,
            "erro": f"Máximo de iterações ({max_iter}) atingido sem convergência para tolerância {tol}.",
            "iteracoes": max_iter}