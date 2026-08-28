def metodo_bissecao(f, a, b, tol=1e-6, max_iter=100):
    historico = []
    try:
        fa, fb = f(a), f(b)
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x) nos extremos: {exc}"}

    if fa == 0:
        return {"sucesso": True, "resultado": a, "historico": [f"{'k':>4} | {'a':>12} | {'b':>12} | {'xₘ = (a+b)/2':>16} | {'f(xₘ)':>14} | {'Sinal f(a)·f(xₘ)':>18} | {'Erro = |b-a|/2':>16}", f"{0:>4} | {a:>12.6f} | {b:>12.6f} | {a:>16.8f} | {0.0:>14.6e} | {'Raiz Exata':>18} | {0.0:>16.6e}"], "erro": None, "iteracoes": 0}
    if fb == 0:
        return {"sucesso": True, "resultado": b, "historico": [f"{'k':>4} | {'a':>12} | {'b':>12} | {'xₘ = (a+b)/2':>16} | {'f(xₘ)':>14} | {'Sinal f(a)·f(xₘ)':>18} | {'Erro = |b-a|/2':>16}", f"{0:>4} | {a:>12.6f} | {b:>12.6f} | {b:>16.8f} | {0.0:>14.6e} | {'Raiz Exata':>18} | {0.0:>16.6e}"], "erro": None, "iteracoes": 0}
    if fa * fb > 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "f(a) e f(b) possuem o mesmo sinal. O método da Bisseção exige troca de sinal no intervalo [a, b]."}

    historico.append(f"{'k':>4} | {'a':>12} | {'b':>12} | {'xₘ = (a+b)/2':>16} | {'f(xₘ)':>14} | {'Sinal f(a)·f(xₘ)':>18} | {'Erro = |b-a|/2':>16}")
    
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

        erro_estimado = (b - a) / 2.0
        sinal_prod = "< 0 (b ← xₘ)" if fa * fxm < 0 else "> 0 (a ← xₘ)"
        historico.append(f"{i:>4} | {a:>12.6f} | {b:>12.6f} | {xm:>16.8f} | {fxm:>14.6e} | {sinal_prod:>18} | {erro_estimado:>16.6e}")

        if abs(fxm) < tol or erro_estimado < tol:
            return {"sucesso": True, "resultado": xm, "historico": historico, "erro": None, "iteracoes": i}

        if fa * fxm < 0:
            b, fb = xm, fxm
        else:
            a, fa = xm, fxm

    return {"sucesso": False, "resultado": xm, "historico": historico,
            "erro": f"Máximo de iterações ({max_iter}) atingido sem convergência para tolerância {tol}.",
            "iteracoes": max_iter}


def metodo_newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    historico = []
    x_atual = x0
    historico.append(f"{'k':>4} | {'xₖ':>14} | {'f(xₖ)':>14} | {'f\'(xₖ)':>14} | {'Δx = -f/f\'':>14} | {'xₖ₊₁ = xₖ+Δx':>18} | {'Erro = |Δx|':>14}")

    for i in range(1, max_iter + 1):
        try:
            fx = f(x_atual)
            dfx = df(x_atual)
        except Exception as exc:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Erro ao avaliar f(x) ou f'(x) na iteração {i}: {exc}"}

        if dfx == 0:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Derivada nula f'({x_atual:.6f}) = 0 na iteração {i}. Divisão por zero evitada."}

        delta_x = -fx / dfx
        x_novo = x_atual + delta_x
        erro_estimado = abs(delta_x)
        historico.append(f"{i:>4} | {x_atual:>14.8f} | {fx:>14.6e} | {dfx:>14.6f} | {delta_x:>14.6e} | {x_novo:>18.8f} | {erro_estimado:>14.6e}")

        if erro_estimado < tol or abs(fx) < tol:
            return {"sucesso": True, "resultado": x_novo, "historico": historico, "erro": None, "iteracoes": i}
        x_atual = x_novo

    return {"sucesso": False, "resultado": x_atual, "historico": historico,
            "erro": f"Máximo de iterações ({max_iter}) atingido sem convergência para tolerância {tol}.",
            "iteracoes": max_iter}


def metodo_secante(f, x0, x1, tol=1e-6, max_iter=100):
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

    historico.append(f"{'k':>4} | {'xₖ₋₁':>14} | {'xₖ':>14} | {'f(xₖ₋₁)':>14} | {'f(xₖ)':>14} | {'xₖ₊₁':>16} | {'Erro = |xₖ₊₁ - xₖ|':>18}")

    x_ant, f_ant = x0, f0
    x_at, f_at = x1, f1

    for i in range(1, max_iter + 1):
        delta_f = f_at - f_ant
        if delta_f == 0:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Divisão por zero: f(xₖ) - f(xₖ₋₁) = 0 na iteração {i}."}

        x_novo = x_at - f_at * (x_at - x_ant) / delta_f
        try:
            f_novo = f(x_novo)
        except Exception as exc:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Erro ao avaliar f(x) em x={x_novo}: {exc}"}

        erro_estimado = abs(x_novo - x_at)
        historico.append(f"{i:>4} | {x_ant:>14.8f} | {x_at:>14.8f} | {f_ant:>14.6e} | {f_at:>14.6e} | {x_novo:>16.8f} | {erro_estimado:>18.6e}")

        if abs(f_novo) < tol or erro_estimado < tol:
            return {"sucesso": True, "resultado": x_novo, "historico": historico, "erro": None, "iteracoes": i}

        x_ant, f_ant = x_at, f_at
        x_at, f_at = x_novo, f_novo

    return {"sucesso": False, "resultado": x_at, "historico": historico,
            "erro": f"Máximo de iterações ({max_iter}) atingido sem convergência para tolerância {tol}.",
            "iteracoes": max_iter}


def metodo_cordas(f, a, b, tol=1e-6, max_iter=100):
    historico = []
    try:
        fa, fb = f(a), f(b)
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x) nos extremos: {exc}"}

    if fa * fb > 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "f(a) e f(b) possuem o mesmo sinal. O método exige troca de sinal no intervalo [a, b]."}

    historico.append(f"{'k':>4} | {'a':>12} | {'b':>12} | {'xₖ = b - f(b)·(b-a)/(f(b)-f(a))':>32} | {'f(xₖ)':>14} | {'Erro = |xₖ - xₖ₋₁|':>18}")
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
        historico.append(f"{i:>4} | {a:>12.6f} | {b:>12.6f} | {x:>32.8f} | {fx:>14.6e} | {erro_estimado:>18.6e}")

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
    historico = []
    try:
        fa, fb = f(a), f(b)
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao avaliar f(x) nos extremos: {exc}"}

    if fa * fb > 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "f(a) e f(b) possuem o mesmo sinal. O método exige troca de sinal no intervalo [a, b]."}

    historico.append(f"{'k':>4} | {'a':>12} | {'b':>12} | {'xₖ = b - f(b)·(b-a)/(f(b)-f(a))':>32} | {'f(xₖ)':>14} | {'Erro = |xₖ - xₖ₋₁|':>18}")
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
        historico.append(f"{i:>4} | {a:>12.6f} | {b:>12.6f} | {x:>32.8f} | {fx:>14.6e} | {erro_estimado:>18.6e}")

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
    historico = []
    x_atual = x0
    historico.append(f"{'k':>4} | {'xₖ':>16} | {'φ(xₖ) = xₖ₊₁':>20} | {'Erro = |xₖ₊₁ - xₖ|':>22}")

    for i in range(1, max_iter + 1):
        try:
            x_novo = phi(x_atual)
        except Exception as exc:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"Erro ao avaliar φ(x) na iteração {i}: {exc}"}

        erro_estimado = abs(x_novo - x_atual)
        historico.append(f"{i:>4} | {x_atual:>16.8f} | {x_novo:>20.8f} | {erro_estimado:>22.6e}")

        if erro_estimado < tol:
            return {"sucesso": True, "resultado": x_novo, "historico": historico, "erro": None, "iteracoes": i}

        if abs(x_novo) > 1e15 or erro_estimado != erro_estimado:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": f"A sequência diverge na iteração {i}. Escolha outra função de iteração φ(x)."}
        x_atual = x_novo

    return {"sucesso": False, "resultado": x_atual, "historico": historico,
            "erro": f"Máximo de iterações ({max_iter}) atingido sem convergência para tolerância {tol}.",
            "iteracoes": max_iter}
