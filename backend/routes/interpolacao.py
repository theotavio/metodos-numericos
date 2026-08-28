import time
import numpy as np
from fastapi import APIRouter, HTTPException
from ..core import interpolacao
from ..schemas import InterpolacaoRequest, BaseCalculationResponse

router = APIRouter(prefix="/interpolacao", tags=["Interpolação Numérica"])

PRESETS_INTERPOLACAO = {
    "Polinômio Cúbico: 4 Pontos de Lagrange (x* = 1.5)": {
        "metodo": "lagrange",
        "pontos": [[0.0, 1.0], [1.0, 3.0], [2.0, 2.0], [3.0, 5.0]],
        "x_alvo": 1.5
    },
    "Interpolação Quadrática: Parábola (x* = 3.0)": {
        "metodo": "quadratica",
        "pontos": [[1.0, 2.0], [2.0, 5.0], [4.0, 17.0]],
        "x_alvo": 3.0
    },
    "Diferenças Divididas de Newton: Tabela (x* = 1.0)": {
        "metodo": "newton_dd",
        "pontos": [[-1.0, 4.0], [0.0, 1.0], [2.0, -1.0], [3.0, 2.0]],
        "x_alvo": 1.0
    },
    "Termodinâmica: Vapor d'Água (T* = 135.0 °C)": {
        "metodo": "lagrange",
        "pontos": [[100.0, 1.013], [120.0, 1.985], [140.0, 3.613], [160.0, 6.178]],
        "x_alvo": 135.0
    },
    "Aerodinâmica: Coeficiente de Sustentação (α* = 6.0°)": {
        "metodo": "newton_dd",
        "pontos": [[0.0, 0.12], [4.0, 0.52], [8.0, 0.91], [12.0, 1.25], [16.0, 1.48]],
        "x_alvo": 6.0
    },
    "Cinemática: Posição vs Tempo (t* = 5.0 s)": {
        "metodo": "linear",
        "pontos": [[0.0, 0.0], [2.0, 14.0], [4.0, 48.0], [6.0, 102.0], [8.0, 176.0]],
        "x_alvo": 5.0
    }
}


@router.get("/presets")
def get_presets():
    return PRESETS_INTERPOLACAO


@router.post("/calcular", response_model=BaseCalculationResponse)
def calcular_interpolacao(req: InterpolacaoRequest):
    t_start = time.perf_counter()

    if not req.pontos or len(req.pontos) < 2:
        raise HTTPException(status_code=400, detail="São necessários ao menos 2 nós para interpolação.")

    metodo = req.metodo.lower().strip()
    if metodo == "linear":
        resultado_dict = interpolacao.interpolacao_linear(req.pontos, req.x_alvo)
    elif metodo == "quadratica":
        if len(req.pontos) != 3:
            raise HTTPException(status_code=400, detail=f"A interpolação quadrática exige exatamente 3 pontos. Recebidos: {len(req.pontos)}.")
        resultado_dict = interpolacao.interpolacao_quadratica(req.pontos, req.x_alvo)
    elif metodo == "lagrange":
        resultado_dict = interpolacao.interpolacao_lagrange(req.pontos, req.x_alvo)
    elif metodo == "newton_dd":
        resultado_dict = interpolacao.diferencas_divididas_newton(req.pontos, req.x_alvo)
    else:
        raise HTTPException(status_code=400, detail=f"Método desconhecido: '{metodo}'.")

    tempo_ms = (time.perf_counter() - t_start) * 1000.0

    sucesso = resultado_dict.get("sucesso", False)
    val = resultado_dict.get("resultado")
    kpis = []

    if sucesso and val is not None:
        kpis.append({"title": "Ponto Alvo x*", "value": f"{req.x_alvo:.4f}"})
        kpis.append({"title": "Valor Interpolado P(x*)", "value": f"{val:.8f}"})
        kpis.append({"title": "Nº de Nós Amostrados (N)", "value": str(len(req.pontos))})

    plot_data = None
    if sucesso and val is not None:
        xs_known = [p[0] for p in req.pontos]
        ys_known = [p[1] for p in req.pontos]
        min_x, max_x = min(xs_known + [req.x_alvo]), max(xs_known + [req.x_alvo])
        delta = max((max_x - min_x) * 0.15, 0.5)

        x_dense = np.linspace(min_x - delta, max_x + delta, 200).tolist()
        try:
            poly = np.poly1d(np.polyfit(xs_known, ys_known, len(xs_known) - 1))
            y_dense = [float(poly(x)) for x in x_dense]
        except Exception:
            y_dense = np.interp(x_dense, xs_known, ys_known).tolist()

        plot_data = {
            "xs_known": xs_known,
            "ys_known": ys_known,
            "x_alvo": req.x_alvo,
            "y_alvo": val,
            "x_dense": x_dense,
            "y_dense": y_dense,
            "metodo": metodo
        }

    return BaseCalculationResponse(
        sucesso=sucesso,
        resultado=val,
        historico=resultado_dict.get("historico", []),
        erro=resultado_dict.get("erro"),
        tempo_ms=round(tempo_ms, 2),
        kpis=kpis,
        plot_data=plot_data
    )
