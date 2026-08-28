import time
import numpy as np
from fastapi import APIRouter, HTTPException
from ..core import parsing, integracao
from ..schemas import IntegracaoRequest, BaseCalculationResponse

router = APIRouter(prefix="/integracao", tags=["Integração Numérica"])

PRESETS_INTEGRACAO = {
    "Parábola: ∫₀² x² dx (Exato: 8/3 ≈ 2.6667)": {
        "metodo": "simpson13",
        "funcao": "x**2",
        "a": 0.0,
        "b": 2.0,
        "n": 6
    },
    "Trigonométrica: ∫₀^π sin(x) dx (Exato: 2.0)": {
        "metodo": "trapezios",
        "funcao": "sin(x)",
        "a": 0.0,
        "b": 3.141592653589793,
        "n": 12
    },
    "Função Racional: ∫₁³ (1/x) dx (Exato: ln 3 ≈ 1.0986)": {
        "metodo": "simpson38",
        "funcao": "1/x",
        "a": 1.0,
        "b": 3.0,
        "n": 6
    },
    "Campânula Gaussiana: ∫₀¹ exp(-x²) dx (Exato: 0.7468)": {
        "metodo": "gauss2p",
        "funcao": "exp(-x**2)",
        "a": 0.0,
        "b": 1.0,
        "n": 2
    },
    "Mecânica: Trabalho de Força Variável ∫₁⁵ (2·x + 3/x) dx": {
        "metodo": "simpson13",
        "funcao": "2*x + 3/x",
        "a": 1.0,
        "b": 5.0,
        "n": 8
    },
    "Estatística: Distribuição Normal Padrão ∫₀² (1/sqrt(2*pi))·exp(-x²/2) dx": {
        "metodo": "simpson38",
        "funcao": "(1/sqrt(2*pi))*exp(-x**2/2)",
        "a": 0.0,
        "b": 2.0,
        "n": 12
    }
}


@router.get("/presets")
def get_presets():
    return PRESETS_INTEGRACAO


@router.post("/calcular", response_model=BaseCalculationResponse)
def calcular_integracao(req: IntegracaoRequest):
    t_start = time.perf_counter()

    if not req.funcao or not req.funcao.strip():
        raise HTTPException(status_code=400, detail="A função integranda f(x) não pode estar vazia.")
    if req.a == req.b:
        raise HTTPException(status_code=400, detail="Os limites de integração a e b não podem ser iguais.")

    try:
        _, f = parsing.parse_funcao_1var(req.funcao)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Erro ao interpretar a função: {exc}")

    metodo = req.metodo.lower().strip()
    n = req.n if req.n and req.n > 0 else 10

    if metodo == "trapezios":
        resultado_dict = integracao.regra_trapezios(f, req.a, req.b, n)
    elif metodo == "simpson13":
        if n % 2 != 0:
            raise HTTPException(status_code=400, detail=f"A Regra 1/3 de Simpson exige 'n' PAR. Foi informado n = {n}.")
        resultado_dict = integracao.regra_simpson_1_3(f, req.a, req.b, n)
    elif metodo == "simpson38":
        if n % 3 != 0:
            raise HTTPException(status_code=400, detail=f"A Regra 3/8 de Simpson exige 'n' MÚLTIPLO DE 3. Foi informado n = {n}.")
        resultado_dict = integracao.regra_simpson_3_8(f, req.a, req.b, n)
    elif metodo == "gauss2p":
        n = 2
        resultado_dict = integracao.quadratura_gaussiana_2p(f, req.a, req.b)
    else:
        raise HTTPException(status_code=400, detail=f"Método desconhecido: '{metodo}'.")

    tempo_ms = (time.perf_counter() - t_start) * 1000.0

    sucesso = resultado_dict.get("sucesso", False)
    integral_val = resultado_dict.get("resultado")
    kpis = []
    plot_data = None

    if sucesso and integral_val is not None:
        kpis.append({"title": "Valor da Integral ∫ₐᵇ f(x)dx", "value": f"{integral_val:.8f}"})
        kpis.append({"title": "Intervalo [a, b]", "value": f"[{req.a:.2f}, {req.b:.2f}]"})
        kpis.append({"title": "Subintervalos (n)", "value": str(n)})
        kpis.append({"title": "Espaçamento (h)", "value": f"{(req.b - req.a)/n:.4f}" if metodo != "gauss2p" else "Legendre 2P"})

        delta = max((req.b - req.a) * 0.25, 0.5)
        xs_curve = np.linspace(req.a - delta, req.b + delta, 300).tolist()
        try:
            ys_curve = [float(f(x)) for x in xs_curve]
            x_nodes = np.linspace(req.a, req.b, n + 1).tolist()
            y_nodes = [float(f(x)) for x in x_nodes]

            xs_area = np.linspace(req.a, req.b, 200).tolist()
            ys_area = [float(f(x)) for x in xs_area]

            plot_data = {
                "xs_curve": xs_curve,
                "ys_curve": ys_curve,
                "xs_area": xs_area,
                "ys_area": ys_area,
                "x_nodes": x_nodes,
                "y_nodes": y_nodes,
                "a": req.a,
                "b": req.b,
                "integral_val": integral_val,
                "metodo": metodo
            }
        except Exception:
            plot_data = None

    return BaseCalculationResponse(
        sucesso=sucesso,
        resultado=integral_val,
        historico=resultado_dict.get("historico", []),
        erro=resultado_dict.get("erro"),
        tempo_ms=round(tempo_ms, 2),
        kpis=kpis,
        plot_data=plot_data
    )
