import time
import numpy as np
from fastapi import APIRouter, HTTPException
from ..core import parsing, raizes, derivadas
from ..schemas import RaizesRequest, BaseCalculationResponse

router = APIRouter(prefix="/raizes", tags=["Raízes de Funções"])

PRESETS_RAIZES = {
    "Polinomial: x³ - x - 2 = 0 em [1, 2]": {
        "metodo": "bissecao",
        "funcao": "x**3 - x - 2",
        "a": 1.0,
        "b": 2.0,
        "tol": 1e-6,
        "max_iter": 100
    },
    "Newton-Raphson (Simbólica): x² - 2 = 0 (x₀ = 1.5)": {
        "metodo": "newton",
        "funcao": "x**2 - 2",
        "tipo_derivada": "simbolica",
        "x0": 1.5,
        "tol": 1e-8,
        "max_iter": 50
    },
    "Newton-Raphson (Dif. Finita Central): exp(-x) - x = 0 (x₀ = 0.5)": {
        "metodo": "newton",
        "funcao": "exp(-x) - x",
        "tipo_derivada": "central",
        "h_derivada": 1e-6,
        "x0": 0.5,
        "tol": 1e-8,
        "max_iter": 50
    },
    "Newton-Raphson (Passo Complexo): sin(x) - x/2 = 0 (x₀ = 2.0)": {
        "metodo": "newton",
        "funcao": "sin(x) - x/2",
        "tipo_derivada": "complexa",
        "h_derivada": 1e-20,
        "x0": 2.0,
        "tol": 1e-8,
        "max_iter": 50
    },
    "Newton-Raphson (Derivada Manual): x³ - 2x - 5 = 0 (x₀ = 2.0)": {
        "metodo": "newton",
        "funcao": "x**3 - 2*x - 5",
        "tipo_derivada": "manual",
        "df_manual": "3*x**2 - 2",
        "x0": 2.0,
        "tol": 1e-8,
        "max_iter": 50
    },
    "Método da Secante: x³ - x - 2 = 0 (x₀=1.0, x₁=2.0)": {
        "metodo": "secante",
        "funcao": "x**3 - x - 2",
        "x0": 1.0,
        "x1": 2.0,
        "tol": 1e-6,
        "max_iter": 100
    },
    "Transcendente: exp(-x) - x = 0 em [0, 1]": {
        "metodo": "cordas",
        "funcao": "exp(-x) - x",
        "a": 0.0,
        "b": 1.0,
        "tol": 1e-6,
        "max_iter": 100
    },
    "Trigonométrica: sin(x) - x/2 = 0 em [1, 2.5]": {
        "metodo": "pegaso",
        "funcao": "sin(x) - x/2",
        "a": 1.0,
        "b": 2.5,
        "tol": 1e-6,
        "max_iter": 100
    },
    "Ponto Fixo: φ(x) = (x+2)^(1/3) (x₀ = 1.5)": {
        "metodo": "iteracao_linear",
        "funcao": "(x+2)**(1/3)",
        "x0": 1.5,
        "tol": 1e-6,
        "max_iter": 50
    },
    "Engenharia: Deflexão de Viga: 2*x³ - 9*x² + 12*x - 4 = 0 em [1.5, 2.5]": {
        "metodo": "cordas",
        "funcao": "2*x**3 - 9*x**2 + 12*x - 4",
        "a": 1.5,
        "b": 2.5,
        "tol": 1e-6,
        "max_iter": 100
    },
    "Mecânica Orbital: Equação de Kepler: x - 0.2*sin(x) - 0.8 = 0 (x₀ = 0.8)": {
        "metodo": "newton",
        "funcao": "x - 0.2*sin(x) - 0.8",
        "tipo_derivada": "simbolica",
        "x0": 0.8,
        "tol": 1e-8,
        "max_iter": 50
    }
}


@router.get("/presets")
def get_presets():
    return PRESETS_RAIZES


@router.post("/calcular", response_model=BaseCalculationResponse)
def calcular_raizes(req: RaizesRequest):
    t_start = time.perf_counter()

    if not req.funcao or not req.funcao.strip():
        raise HTTPException(status_code=400, detail="O campo da função f(x) não pode estar vazio.")

    try:
        expr, f = parsing.parse_funcao_1var(req.funcao)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Erro ao interpretar a função: {exc}")

    metodo = req.metodo.lower().strip()
    resultado_dict = {}
    descricao_derivada = None

    if metodo == "bissecao":
        if req.a is None or req.b is None:
            raise HTTPException(status_code=400, detail="Informe os limites 'a' e 'b' para a Bisseção.")
        if req.a >= req.b:
            raise HTTPException(status_code=400, detail="O limite inferior (a) deve ser menor que o superior (b).")
        resultado_dict = raizes.metodo_bissecao(f, req.a, req.b, req.tol, req.max_iter)

    elif metodo == "newton":
        if req.x0 is None:
            raise HTTPException(status_code=400, detail="Informe a estimativa inicial 'x₀' para o método de Newton.")
        tipo_deriv = req.tipo_derivada or "simbolica"
        h_val = req.h_derivada if req.h_derivada and req.h_derivada > 0 else 1e-6

        df, desc_deriv, _ = derivadas.construir_derivada(
            tipo=tipo_deriv,
            f=f,
            expr_sympy=expr,
            variavel="x",
            h=h_val,
            expressao_manual_str=req.df_manual
        )
        descricao_derivada = desc_deriv
        resultado_dict = raizes.metodo_newton_raphson(f, df, req.x0, req.tol, req.max_iter)
        resultado_dict["historico"].insert(0, f"Método de Derivação: {desc_deriv}")

    elif metodo == "secante":
        if req.x0 is None or req.x1 is None:
            raise HTTPException(status_code=400, detail="Informe as estimativas iniciais 'x₀' e 'x₁' para a Secante.")
        resultado_dict = raizes.metodo_secante(f, req.x0, req.x1, req.tol, req.max_iter)

    elif metodo == "cordas":
        if req.a is None or req.b is None:
            raise HTTPException(status_code=400, detail="Informe os limites 'a' e 'b' para o Método das Cordas.")
        if req.a >= req.b:
            raise HTTPException(status_code=400, detail="O limite inferior (a) deve ser menor que o superior (b).")
        resultado_dict = raizes.metodo_cordas(f, req.a, req.b, req.tol, req.max_iter)

    elif metodo == "pegaso":
        if req.a is None or req.b is None:
            raise HTTPException(status_code=400, detail="Informe os limites 'a' e 'b' para o Método de Pégaso.")
        if req.a >= req.b:
            raise HTTPException(status_code=400, detail="O limite inferior (a) deve ser menor que o superior (b).")
        resultado_dict = raizes.metodo_pegaso(f, req.a, req.b, req.tol, req.max_iter)

    elif metodo == "iteracao_linear":
        if req.x0 is None:
            raise HTTPException(status_code=400, detail="Informe a estimativa inicial 'x₀' para a Iteração Linear.")
        resultado_dict = raizes.metodo_iteracao_linear(f, req.x0, req.tol, req.max_iter)

    else:
        raise HTTPException(status_code=400, detail=f"Método desconhecido: '{metodo}'.")

    tempo_ms = (time.perf_counter() - t_start) * 1000.0

    sucesso = resultado_dict.get("sucesso", False)
    root = resultado_dict.get("resultado")
    kpis = []
    detalhes_matematicos = []
    residuo = None

    if sucesso and root is not None:
        try:
            residuo = float(f(root))
        except Exception:
            residuo = 0.0

        kpis.append({"title": "Raiz Estimada x*", "value": f"{root:.8f}"})
        if residuo is not None:
            kpis.append({"title": "Resíduo |f(x*)|", "value": f"{abs(residuo):.2e}"})
        if "iteracoes" in resultado_dict:
            kpis.append({"title": "Iterações Realizadas (k)", "value": str(resultado_dict["iteracoes"])})
        if req.tol:
            kpis.append({"title": "Tolerância Definida (ε)", "value": f"{req.tol:g}"})

        if descricao_derivada:
            detalhes_matematicos.append({"label": "Derivada", "value": descricao_derivada})

    plot_data = None
    if sucesso and root is not None:
        pontos_ref = [p for p in [req.a, req.b, root, req.x0, req.x1] if p is not None]
        if pontos_ref:
            min_x, max_x = min(pontos_ref), max(pontos_ref)
            delta = max((max_x - min_x) * 0.4, 1.5)
            x_start, x_end = min_x - delta, max_x + delta
        else:
            x_start, x_end = -5.0, 5.0

        xs = np.linspace(x_start, x_end, 300)
        try:
            ys = [float(f(x)) for x in xs]
            ys_clean = np.nan_to_num(ys, nan=0.0, posinf=1e4, neginf=-1e4)
            p95 = float(np.percentile(np.abs(ys_clean), 95)) if len(ys_clean) > 0 else 10.0
            y_limit = max(p95 * 1.5, 5.0)
            ys_clamped = np.clip(ys_clean, -y_limit, y_limit).tolist()

            plot_data = {
                "xs": xs.tolist(),
                "ys": ys_clamped,
                "a": req.a,
                "b": req.b,
                "x0": req.x0,
                "root": root,
                "residuo": residuo,
                "metodo": metodo
            }
        except Exception:
            plot_data = None

    return BaseCalculationResponse(
        sucesso=sucesso,
        resultado=root,
        historico=resultado_dict.get("historico", []),
        erro=resultado_dict.get("erro"),
        iteracoes=resultado_dict.get("iteracoes"),
        tempo_ms=round(tempo_ms, 2),
        kpis=kpis,
        detalhes_matematicos=detalhes_matematicos,
        plot_data=plot_data
    )
