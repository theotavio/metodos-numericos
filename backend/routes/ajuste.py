import time
import numpy as np
from fastapi import APIRouter, HTTPException
from ..core import ajuste_curvas
from ..schemas import AjusteRequest, BaseCalculationResponse

router = APIRouter(prefix="/ajuste", tags=["Ajuste de Curvas"])

PRESETS_AJUSTE = {
    "Regressão Simples: Dados de Laboratório": {
        "metodo": "simples",
        "pontos": [[1.0, 2.1], [2.0, 3.9], [3.0, 6.2], [4.0, 7.8], [5.0, 10.1]]
    },
    "Regressão Simples: Temperatura vs Resistência Elétrica": {
        "metodo": "simples",
        "pontos": [[20.0, 100.2], [30.0, 104.1], [40.0, 107.9], [50.0, 111.8], [60.0, 115.7]]
    },
    "Regressão Simples: Calibração de Sensor de Pressão": {
        "metodo": "simples",
        "pontos": [[10.0, 1.25], [20.0, 2.48], [30.0, 3.76], [40.0, 5.01], [50.0, 6.27]]
    },
    "Regressão Múltipla: 2 Variáveis Independentes": {
        "metodo": "multiplo",
        "n_obs": 5,
        "n_vars": 2,
        "dados": [
            [50.0, 1.0, 150.0],
            [70.0, 2.0, 210.0],
            [85.0, 3.0, 270.0],
            [110.0, 3.0, 340.0],
            [130.0, 4.0, 410.0]
        ]
    },
    "Regressão Múltipla: Consumo de Combustível (Massa e Potência)": {
        "metodo": "multiplo",
        "n_obs": 6,
        "n_vars": 2,
        "dados": [
            [1200.0, 110.0, 14.5],
            [1400.0, 130.0, 12.8],
            [1600.0, 150.0, 11.2],
            [1800.0, 180.0, 9.8],
            [2000.0, 220.0, 8.4],
            [2200.0, 250.0, 7.1]
        ]
    }
}


@router.get("/presets")
def get_presets():
    return PRESETS_AJUSTE


@router.post("/calcular", response_model=BaseCalculationResponse)
def calcular_ajuste(req: AjusteRequest):
    t_start = time.perf_counter()

    metodo = req.metodo.lower().strip()
    if metodo == "simples":
        if not req.pontos or len(req.pontos) < 2:
            raise HTTPException(status_code=400, detail="São necessários ao menos 2 pontos para regressão simples.")
        resultado_dict = ajuste_curvas.ajuste_linear_simples(req.pontos)
    elif metodo == "multiplo":
        if req.X is None or req.y is None:
            raise HTTPException(status_code=400, detail="Matriz X e vetor y são obrigatórios para regressão múltipla.")
        if len(req.X) != len(req.y):
            raise HTTPException(status_code=400, detail="Número de linhas de X deve ser igual ao tamanho de y.")
        resultado_dict = ajuste_curvas.ajuste_linear_multiplo(req.X, req.y)
    else:
        raise HTTPException(status_code=400, detail=f"Método desconhecido: '{metodo}'.")

    tempo_ms = (time.perf_counter() - t_start) * 1000.0

    sucesso = resultado_dict.get("sucesso", False)
    r = resultado_dict.get("resultado", {})
    kpis = []
    plot_data = None

    if sucesso and r:
        if metodo == "simples":
            a0, a1, r2 = r["a0"], r["a1"], r["r2"]
            kpis.append({"title": "Coeficiente R²", "value": f"{r2:.4f}", "subtitle": f"{r2*100:.1f}% explicado"})
            kpis.append({"title": "Intercepto (a₀)", "value": f"{a0:.4f}"})
            kpis.append({"title": "Inclinação (a₁)", "value": f"{a1:.4f}"})
            kpis.append({"title": "Nº de Pontos Amostrados (N)", "value": str(len(req.pontos))})

            xs = np.array([p[0] for p in req.pontos], dtype=float)
            ys = np.array([p[1] for p in req.pontos], dtype=float)
            min_x, max_x = float(np.min(xs)), float(np.max(xs))
            delta = max((max_x - min_x) * 0.15, 1.0)
            x_line = np.linspace(min_x - delta, max_x + delta, 100).tolist()
            y_line = [float(a0 + a1 * x) for x in x_line]
            y_pred = [float(a0 + a1 * x) for x in xs]

            residuals = []
            for xi, yi, ypi in zip(xs, ys, y_pred):
                residuals.append({"x": [float(xi), float(xi)], "y": [float(yi), float(ypi)]})

            plot_data = {
                "type": "simples",
                "xs_pts": xs.tolist(),
                "ys_pts": ys.tolist(),
                "x_line": x_line,
                "y_line": y_line,
                "residuals": residuals,
                "a0": a0,
                "a1": a1,
                "r2": r2
            }
        else:
            coefs = r.get("coeficientes", [])
            r2 = r.get("r2", 0.0)

            kpis.append({"title": "Coeficiente R²", "value": f"{r2:.4f}", "subtitle": f"{r2*100:.1f}% explicado"})
            kpis.append({"title": "Intercepto (β₀)", "value": f"{coefs[0]:.4f}"})
            kpis.append({"title": "Variáveis Independentes (k)", "value": str(len(coefs) - 1)})
            kpis.append({"title": "Observações (N)", "value": str(len(req.y))})

            X_arr = np.array(req.X, dtype=float)
            y_arr = np.array(req.y, dtype=float)
            Xb = np.hstack([np.ones((X_arr.shape[0], 1)), X_arr])
            y_pred = (Xb @ np.array(coefs)).tolist()

            min_v = float(min(np.min(y_arr), np.min(y_pred)))
            max_v = float(max(np.max(y_arr), np.max(y_pred)))
            delta = max((max_v - min_v) * 0.1, 1.0)
            ref_line_x = [min_v - delta, max_v + delta]
            ref_line_y = [min_v - delta, max_v + delta]

            plot_data = {
                "type": "multiplo",
                "y_true": y_arr.tolist(),
                "y_pred": y_pred,
                "ref_line_x": ref_line_x,
                "ref_line_y": ref_line_y,
                "r2": r2
            }

    return BaseCalculationResponse(
        sucesso=sucesso,
        resultado=r,
        historico=resultado_dict.get("historico", []),
        erro=resultado_dict.get("erro"),
        tempo_ms=round(tempo_ms, 2),
        kpis=kpis,
        plot_data=plot_data
    )
