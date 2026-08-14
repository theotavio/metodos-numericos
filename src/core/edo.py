def metodo_euler(f, t0, y0, tn, h):
    historico = []
    if h <= 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O passo h deve ser um número positivo."}
    if tn <= t0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O tempo final (tn) deve ser maior que o tempo inicial (t0)."}

    n_passos = int(round((tn - t0) / h))
    pontos = [(t0, y0)]
    t, y = t0, y0

    historico.append(f"{'i':>4} | {'t_i':>12} | {'y_i':>14} | {'f(t_i,y_i)':>14} | {'y_(i+1)':>14}")
    try:
        for i in range(n_passos):
            fty = f(t, y)
            y_novo = y + h * fty
            t_novo = t + h
            historico.append(f"{i:>4} | {t:>12.6f} | {y:>14.8f} | {fty:>14.8f} | {y_novo:>14.8f}")
            t, y = t_novo, y_novo
            pontos.append((t, y))
    except ZeroDivisionError:
        return {"sucesso": False, "resultado": pontos, "historico": historico,
                "erro": f"Divisão por zero ao avaliar f(t, y) em t={t:.6f}, y={y:.6f}."}
    except Exception as exc:
        return {"sucesso": False, "resultado": pontos, "historico": historico,
                "erro": f"Erro ao avaliar f(t, y): {exc}"}

    historico.append(f"Valor final aproximado: y({tn}) ≈ {y:.8f}")
    return {"sucesso": True, "resultado": pontos, "historico": historico, "erro": None}


def metodo_runge_kutta_2(f, t0, y0, tn, h):
    historico = []
    if h <= 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O passo h deve ser um número positivo."}
    if tn <= t0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O tempo final (tn) deve ser maior que o tempo inicial (t0)."}

    n_passos = int(round((tn - t0) / h))
    pontos = [(t0, y0)]
    t, y = t0, y0

    historico.append(f"{'i':>4} | {'t_i':>10} | {'y_i':>12} | {'k1':>10} | {'k2':>10} | {'y_(i+1)':>12}")
    try:
        for i in range(n_passos):
            k1 = f(t, y)
            k2 = f(t + h, y + h * k1)
            y_novo = y + (h / 2.0) * (k1 + k2)
            t_novo = t + h
            historico.append(f"{i:>4} | {t:>10.5f} | {y:>12.6f} | {k1:>10.6f} | {k2:>10.6f} | {y_novo:>12.6f}")
            t, y = t_novo, y_novo
            pontos.append((t, y))
    except Exception as exc:
        return {"sucesso": False, "resultado": pontos, "historico": historico,
                "erro": f"Erro ao avaliar f(t, y): {exc}"}

    historico.append(f"Valor final aproximado: y({tn}) ≈ {y:.8f}")
    return {"sucesso": True, "resultado": pontos, "historico": historico, "erro": None}


def metodo_runge_kutta_4(f, t0, y0, tn, h):
    historico = []
    if h <= 0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O passo h deve ser um número positivo."}
    if tn <= t0:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "O tempo final (tn) deve ser maior que o tempo inicial (t0)."}

    n_passos = int(round((tn - t0) / h))
    pontos = [(t0, y0)]
    t, y = t0, y0

    historico.append(f"{'i':>4} | {'t_i':>10} | {'y_i':>12} | {'k1':>9} | {'k2':>9} | {'k3':>9} | {'k4':>9} | {'y_(i+1)':>12}")
    try:
        for i in range(n_passos):
            k1 = f(t, y)
            k2 = f(t + h / 2.0, y + h * k1 / 2.0)
            k3 = f(t + h / 2.0, y + h * k2 / 2.0)
            k4 = f(t + h, y + h * k3)
            y_novo = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
            t_novo = t + h
            historico.append(
                f"{i:>4} | {t:>10.5f} | {y:>12.6f} | {k1:>9.5f} | {k2:>9.5f} | {k3:>9.5f} | {k4:>9.5f} | {y_novo:>12.6f}"
            )
            t, y = t_novo, y_novo
            pontos.append((t, y))
    except Exception as exc:
        return {"sucesso": False, "resultado": pontos, "historico": historico,
                "erro": f"Erro ao avaliar f(t, y): {exc}"}

    historico.append(f"Valor final aproximado: y({tn}) ≈ {y:.8f}")
    return {"sucesso": True, "resultado": pontos, "historico": historico, "erro": None}