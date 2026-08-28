def metodo_euler(f, t0, y0, tn, h):
    historico = []
    if h <= 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O passo h deve ser um número positivo."}
    if tn <= t0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O tempo final (tₙ) deve ser maior que o tempo inicial (t₀)."}

    n_passos = int(round((tn - t0) / h))
    pontos = [(float(t0), float(y0))]
    t, y = float(t0), float(y0)

    historico.append(f"{'i':>4} | {'tᵢ':>10} | {'yᵢ':>14} | {'f(tᵢ, yᵢ)':>16} | {'yᵢ₊₁ = yᵢ + h·f':>16}")

    try:
        for i in range(n_passos):
            fty = float(f(t, y))
            y_novo = y + h * fty
            t_novo = t + h
            historico.append(f"{i:>4} | {t:>10.4f} | {y:>14.8f} | {fty:>16.8f} | {y_novo:>16.8f}")
            t, y = t_novo, y_novo
            pontos.append((t, y))
    except ZeroDivisionError:
        return {"sucesso": False, "resultado": pontos, "historico": historico,
                "erro": f"Divisão por zero ao avaliar f(t, y) em t={t:.4f}, y={y:.6f}."}
    except Exception as exc:
        return {"sucesso": False, "resultado": pontos, "historico": historico,
                "erro": f"Erro ao avaliar f(t, y): {exc}"}

    historico.append(f"{'Fim':>4} | {f'tₙ = {tn:.4f}':>10} | {f'y(tₙ) = {y:.8f}':>14} | {'—':>16} | {'PVI Concluído':>16}")
    return {"sucesso": True, "resultado": pontos, "historico": historico, "erro": None}


def metodo_runge_kutta_2(f, t0, y0, tn, h):
    historico = []
    if h <= 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O passo h deve ser um número positivo."}
    if tn <= t0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O tempo final (tₙ) deve ser maior que o tempo inicial (t₀)."}

    n_passos = int(round((tn - t0) / h))
    pontos = [(float(t0), float(y0))]
    t, y = float(t0), float(y0)

    historico.append(f"{'i':>4} | {'tᵢ':>10} | {'yᵢ':>12} | {'k₁':>12} | {'k₂':>12} | {'yᵢ₊₁':>12}")

    try:
        for i in range(n_passos):
            k1 = float(f(t, y))
            k2 = float(f(t + h, y + h * k1))
            y_novo = y + (h / 2.0) * (k1 + k2)
            t_novo = t + h
            historico.append(f"{i:>4} | {t:>10.4f} | {y:>12.6f} | {k1:>12.6f} | {k2:>12.6f} | {y_novo:>12.6f}")
            t, y = t_novo, y_novo
            pontos.append((t, y))
    except Exception as exc:
        return {"sucesso": False, "resultado": pontos, "historico": historico,
                "erro": f"Erro ao avaliar f(t, y): {exc}"}

    historico.append(f"{'Fim':>4} | {f'tₙ = {tn:.4f}':>10} | {f'y(tₙ) = {y:.6f}':>12} | {'—':>12} | {'—':>12} | {'PVI Concluído':>12}")
    return {"sucesso": True, "resultado": pontos, "historico": historico, "erro": None}


def metodo_runge_kutta_4(f, t0, y0, tn, h):
    historico = []
    if h <= 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O passo h deve ser um número positivo."}
    if tn <= t0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O tempo final (tₙ) deve ser maior que o tempo inicial (t₀)."}

    n_passos = int(round((tn - t0) / h))
    pontos = [(float(t0), float(y0))]
    t, y = float(t0), float(y0)

    historico.append(f"{'i':>4} | {'tᵢ':>8} | {'yᵢ':>11} | {'k₁':>10} | {'k₂':>10} | {'k₃':>10} | {'k₄':>10} | {'yᵢ₊₁':>11}")

    try:
        for i in range(n_passos):
            k1 = float(f(t, y))
            k2 = float(f(t + h / 2.0, y + h * k1 / 2.0))
            k3 = float(f(t + h / 2.0, y + h * k2 / 2.0))
            k4 = float(f(t + h, y + h * k3))
            y_novo = y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
            t_novo = t + h
            historico.append(
                f"{i:>4} | {t:>8.3f} | {y:>11.6f} | {k1:>10.5f} | {k2:>10.5f} | {k3:>10.5f} | {k4:>10.5f} | {y_novo:>11.6f}"
            )
            t, y = t_novo, y_novo
            pontos.append((t, y))
    except Exception as exc:
        return {"sucesso": False, "resultado": pontos, "historico": historico,
                "erro": f"Erro ao avaliar f(t, y): {exc}"}

    historico.append(f"{'Fim':>4} | {f'tₙ={tn:.2f}':>8} | {f'{y:.6f}':>11} | {'—':>10} | {'—':>10} | {'—':>10} | {'—':>10} | {'PVI Concluído':>11}")
    return {"sucesso": True, "resultado": pontos, "historico": historico, "erro": None}
