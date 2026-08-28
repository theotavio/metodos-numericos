import time
import numpy as np
from fastapi import APIRouter, HTTPException
from ..core import parsing, edo
from ..schemas import EdoRequest, BaseCalculationResponse

router = APIRouter(prefix="/edo", tags=["Equações Diferenciais Ordinárias"])

PRESETS_EDO = {
    "PVI 1: dy/dt = y - t² + 1, y(0) = 0.5 em [0, 2]": {
        "metodo": "rk4",
        "funcao": "y - t**2 + 1",
        "t0": 0.0,
        "y0": 0.5,
        "tn": 2.0,
        "h": 0.2
    },
    "PVI 2 (Euler): dy/dt = -2*t*y, y(0) = 1 em [0, 1.5]": {
        "metodo": "euler",
        "funcao": "-2*t*y",
        "t0": 0.0,
        "y0": 1.0,
        "tn": 1.5,
        "h": 0.1
    },
    "PVI 3 (RK2 Heun): dy/dt = sin(t) - y, y(0) = 0 em [0, 5]": {
        "metodo": "rk2",
        "funcao": "sin(t) - y",
        "t0": 0.0,
        "y0": 0.0,
        "tn": 5.0,
        "h": 0.25
    },
    "PVI 4: Crescimento Logístico dy/dt = y*(1 - y/10)": {
        "metodo": "rk4",
        "funcao": "y*(1 - y/10)",
        "t0": 0.0,
        "y0": 1.0,
        "tn": 8.0,
        "h": 0.4
    },
    "PVI 5: Lei do Resfriamento de Newton dy/dt = -0.07*(y - 20)": {
        "metodo": "rk4",
        "funcao": "-0.07*(y - 20)",
        "t0": 0.0,
        "y0": 80.0,
        "tn": 60.0,
        "h": 3.0
    },
    "PVI 6: Circuito RC dy/dt = (10 - y)/2": {
        "metodo": "rk2",
        "funcao": "(10 - y)/2",
        "t0": 0.0,
        "y0": 0.0,
        "tn": 10.0,
        "h": 0.5
    }
}


@router.get("/presets")
def get_presets():
    return PRESETS_EDO


@router.post("/calcular", response_model=BaseCalculationResponse)
def calcular_edo(req: EdoRequest):
    t_start = time.perf_counter()

    if not req.funcao or not req.funcao.strip():
        raise HTTPException(status_code=400, detail="A equação diferencial dy/dt = f(t, y) não pode estar vazia.")
    if req.h <= 0:
        raise HTTPException(status_code=400, detail="O passo (h) deve ser estritamente positivo.")
    if req.tn <= req.t0:
        raise HTTPException(status_code=400, detail="O tempo final (tₙ) deve ser maior que o tempo inicial (t₀).")

    try:
        _, f = parsing.parse_funcao_2var(req.funcao)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Erro ao interpretar a função da EDO: {exc}")

    metodo = req.metodo.lower().strip()
    if metodo == "euler":
        resultado_dict = edo.metodo_euler(f, req.t0, req.y0, req.tn, req.h)
    elif metodo == "rk2":
        resultado_dict = edo.metodo_runge_kutta_2(f, req.t0, req.y0, req.tn, req.h)
    elif metodo == "rk4":
        resultado_dict = edo.metodo_runge_kutta_4(f, req.t0, req.y0, req.tn, req.h)
    else:
        raise HTTPException(status_code=400, detail=f"Método desconhecido: '{metodo}'.")

    tempo_ms = (time.perf_counter() - t_start) * 1000.0

    sucesso = resultado_dict.get("sucesso", False)
    pontos = resultado_dict.get("resultado", [])
    kpis = []
    plot_data = None

    if sucesso and pontos:
        t_final, y_final = pontos[-1]
        kpis.append({"title": "Valor Final Estimado y(tₙ)", "value": f"{y_final:.6f}"})
        kpis.append({"title": "Total de Passos (N)", "value": str(len(pontos) - 1)})
        kpis.append({"title": "Passo Temporal h (Δt)", "value": f"{req.h:.4f}"})
        kpis.append({"title": "Intervalo [t₀, tₙ]", "value": f"[{req.t0:.2f}, {req.tn:.2f}]"})

        ts = [p[0] for p in pontos]
        ys = [p[1] for p in pontos]
        min_t, max_t = min(ts), max(ts)
        min_y, max_y = min(ys), max(ys)
        dt = max((max_t - min_t) * 0.1, 0.2)
        dy = max((max_y - min_y) * 0.2, 1.0)

        grid_t = np.linspace(min_t - dt, max_t + dt, 16).tolist()
        grid_y = np.linspace(min_y - dy, max_y + dy, 14).tolist()

        vectors = []
        delta_t_step = (max_t - min_t + 2*dt) / 16.0
        delta_y_step = (max_y - min_y + 2*dy) / 14.0

        for t_val in grid_t:
            for y_val in grid_y:
                try:
                    slope = float(f(t_val, y_val))
                    if np.isfinite(slope):
                        mag = np.sqrt(1.0 + slope**2)
                        u = 0.45 * (1.0 / mag) * delta_t_step
                        v = 0.45 * (slope / mag) * delta_y_step
                        vectors.append({
                            "t0": t_val - u, "y0": y_val - v,
                            "t1": t_val + u, "y1": y_val + v
                        })
                except Exception:
                    pass

        plot_data = {
            "ts": ts,
            "ys": ys,
            "t0": req.t0,
            "y0": req.y0,
            "tn": req.tn,
            "vectors": vectors,
            "metodo": metodo
        }

    return BaseCalculationResponse(
        sucesso=sucesso,
        resultado=pontos,
        historico=resultado_dict.get("historico", []),
        erro=resultado_dict.get("erro"),
        tempo_ms=round(tempo_ms, 2),
        kpis=kpis,
        plot_data=plot_data
    )
