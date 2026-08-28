import time
import numpy as np
from fastapi import APIRouter, HTTPException
from ..core import sistemas_lineares
from ..schemas import SistemasRequest, BaseCalculationResponse

router = APIRouter(prefix="/sistemas", tags=["Sistemas Lineares"])

SUBSCRIPTS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

def _sub(num: int) -> str:
    return str(num).translate(SUBSCRIPTS)

PRESETS_SISTEMAS = {
    "Sistema 2×2: Interseção de Retas (2x₁ + x₂ = 7, x₁ - x₂ = 2)": {
        "metodo": "gauss",
        "n": 2,
        "A": [[2.0, 1.0], [1.0, -1.0]],
        "b": [7.0, 2.0]
    },
    "Sistema 3×3: Eliminação de Gauss Clássica": {
        "metodo": "gauss",
        "n": 3,
        "A": [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]],
        "b": [8.0, -11.0, -3.0]
    },
    "Sistema 3×3: Gauss-Seidel Dominante": {
        "metodo": "gauss_seidel",
        "n": 3,
        "A": [[10.0, 2.0, 1.0], [1.0, 10.0, -1.0], [2.0, -2.0, 10.0]],
        "b": [14.0, 11.0, 26.0],
        "tol": 1e-6,
        "max_iter": 100
    },
    "Sistema 4×4: Treliça de Estruturas": {
        "metodo": "gauss",
        "n": 4,
        "A": [[4.0, -1.0, 0.0, 0.0], [-1.0, 4.0, -1.0, 0.0], [0.0, -1.0, 4.0, -1.0], [0.0, 0.0, -1.0, 3.0]],
        "b": [10.0, 10.0, 10.0, 10.0]
    },
    "Sistema 3×3: Circuito Elétrico (Leis de Kirchhoff)": {
        "metodo": "gauss",
        "n": 3,
        "A": [[15.0, -5.0, 0.0], [-5.0, 20.0, -10.0], [0.0, -10.0, 12.0]],
        "b": [50.0, 0.0, 0.0]
    }
}


@router.get("/presets")
def get_presets():
    return PRESETS_SISTEMAS


@router.post("/calcular", response_model=BaseCalculationResponse)
def calcular_sistemas(req: SistemasRequest):
    t_start = time.perf_counter()

    if not req.A or not req.b:
        raise HTTPException(status_code=400, detail="Matriz A e vetor b não podem estar vazios.")

    n = len(req.b)
    if any(len(row) != n for row in req.A) or len(req.A) != n:
        raise HTTPException(status_code=400, detail=f"Dimensões incompatíveis. A matriz A deve ser {n}×{n} para b de dimensão {n}.")

    metodo = req.metodo.lower().strip()
    if metodo == "gauss":
        resultado_dict = sistemas_lineares.eliminacao_gauss(req.A, req.b)
    elif metodo == "gauss_seidel":
        tol = req.tol if req.tol and req.tol > 0 else 1e-6
        max_iter = req.max_iter if req.max_iter and req.max_iter > 0 else 100
        resultado_dict = sistemas_lineares.gauss_seidel(req.A, req.b, tol=tol, max_iter=max_iter)
    else:
        raise HTTPException(status_code=400, detail=f"Método desconhecido: '{metodo}'.")

    tempo_ms = (time.perf_counter() - t_start) * 1000.0

    sucesso = resultado_dict.get("sucesso", False)
    sol = resultado_dict.get("resultado")
    kpis = []
    detalhes_matematicos = []

    if sucesso and sol is not None:
        for i, val in enumerate(sol[:8]):
            kpis.append({"title": f"Incógnita x{_sub(i+1)}", "value": f"{val:.6f}"})
        if "iteracoes" in resultado_dict:
            kpis.append({"title": "Iterações Realizadas (k)", "value": str(resultado_dict["iteracoes"])})
        kpis.append({"title": "Ordem do Sistema (n)", "value": str(n)})

        dom_info = resultado_dict.get("dominancia_info")
        if dom_info:
            status_str = "Satisfeito (Convergência Garantida)" if dom_info.get("estritamente_dominante") else "Não estritamente dominante"
            detalhes_matematicos.append({
                "label": "Critério de Sassenfeld / Linhas",
                "value": status_str
            })

    plot_data = None
    if sucesso and sol is not None:
        if n == 2:
            x_center = sol[0]
            xs = np.linspace(x_center - 8.0, x_center + 8.0, 100).tolist()
            lines = []
            for i in range(2):
                a1, a2 = req.A[i][0], req.A[i][1]
                bi = req.b[i]
                if abs(a2) > 1e-9:
                    ys = [float((bi - a1 * x) / a2) for x in xs]
                    lines.append({"eq": f"Eq. {i+1}: {a1:.2f}x₁ + {a2:.2f}x₂ = {bi:.2f}", "xs": xs, "ys": ys, "vertical": False})
                else:
                    x_vert = bi / a1
                    lines.append({"eq": f"Eq. {i+1}: x₁ = {x_vert:.2f}", "x_vert": x_vert, "vertical": True})
            plot_data = {
                "type": "2d_lines",
                "lines": lines,
                "sol": sol
            }
        else:
            erros = []
            for l in resultado_dict.get("historico", []):
                if "|" in l and not any(k in l for k in ["Iter", "Etapa", "AVISO", "Matriz"]):
                    partes = [p.strip() for p in l.split("|")]
                    if len(partes) >= 2:
                        try:
                            erros.append(float(partes[-1]))
                        except ValueError:
                            pass

            plot_data = {
                "type": "bars_and_convergence",
                "sol": sol,
                "labels": [f"x{_sub(i+1)}" for i in range(n)],
                "erros": erros if erros else None
            }

    return BaseCalculationResponse(
        sucesso=sucesso,
        resultado=sol,
        historico=resultado_dict.get("historico", []),
        erro=resultado_dict.get("erro"),
        iteracoes=resultado_dict.get("iteracoes"),
        tempo_ms=round(tempo_ms, 2),
        kpis=kpis,
        detalhes_matematicos=detalhes_matematicos,
        plot_data=plot_data,
        etapas_gauss=resultado_dict.get("etapas_gauss"),
        substituicao_passos=resultado_dict.get("substituicao_passos"),
        dominancia_info=resultado_dict.get("dominancia_info")
    )
