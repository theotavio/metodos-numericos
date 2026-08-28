from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .routes import raizes, sistemas, interpolacao, ajuste, integracao, edo, info

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Métodos Numéricos Computacionais API",
    description="Backend REST modular para resolução e visualização de problemas de Cálculo Numérico.",
    version="3.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(raizes.router, prefix="/api")
app.include_router(sistemas.router, prefix="/api")
app.include_router(interpolacao.router, prefix="/api")
app.include_router(ajuste.router, prefix="/api")
app.include_router(integracao.router, prefix="/api")
app.include_router(edo.router, prefix="/api")
app.include_router(info.router, prefix="/api")


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "Métodos Numéricos API",
        "version": "3.0.0"
    }


@app.get("/api/modulos")
def get_modulos():
    return [
        {
            "id": "raizes",
            "nome": "Raízes de Funções",
            "notacao": "f(x) = 0",
            "simbolo": "[ f(x) = 0 ]",
            "descricao": "Isolamento e refinamento de raízes de equações algébricas e transcendentes f(x) = 0",
            "metodos": [
                {"id": "bissecao", "nome": "Bisseção [ Intervalar ]"},
                {"id": "newton", "nome": "Newton-Raphson [ Tangente f'(x) ]"},
                {"id": "secante", "nome": "Método da Secante [ Quasi-Newton ]"},
                {"id": "cordas", "nome": "Método das Cordas [ Falsa Posição ]"},
                {"id": "pegaso", "nome": "Método de Pégaso [ Acelerado ]"},
                {"id": "iteracao_linear", "nome": "Iteração Linear [ Ponto Fixo x = φ(x) ]"}
            ]
        },
        {
            "id": "sistemas",
            "nome": "Sistemas Lineares",
            "notacao": "Ax = b",
            "simbolo": "[ Ax = b ]",
            "descricao": "Resolução direta e iterativa de sistemas de equações algébricas lineares Ax = b",
            "metodos": [
                {"id": "gauss", "nome": "Eliminação de Gauss [ Direto ]"},
                {"id": "gauss_seidel", "nome": "Gauss-Seidel [ Iterativo ]"}
            ]
        },
        {
            "id": "interpolacao",
            "nome": "Interpolação Numérica",
            "notacao": "P(x)",
            "simbolo": "[ P(x) ]",
            "descricao": "Construção de polinômios interpoladores P(x) e estimativa de valores intermediários",
            "metodos": [
                {"id": "linear", "nome": "Interpolação Linear [ 2 Pontos ]"},
                {"id": "quadratica", "nome": "Interpolação Quadrática [ 3 Pontos ]"},
                {"id": "lagrange", "nome": "Interpolação de Lagrange [ ∑ Lᵢ(x)yᵢ ]"},
                {"id": "newton_dd", "nome": "Diferenças Divididas de Newton [ f[x₀,...,xₖ] ]"}
            ]
        },
        {
            "id": "ajuste",
            "nome": "Ajuste de Curvas",
            "notacao": "ŷ = a₀ + a₁x",
            "simbolo": "[ ŷ = a₀ + a₁x ]",
            "descricao": "Regressão linear simples e múltipla pelo Método dos Mínimos Quadrados com coeficiente R²",
            "metodos": [
                {"id": "simples", "nome": "Ajuste Linear Simples [ ŷ = a₀ + a₁x ]"},
                {"id": "multiplo", "nome": "Ajuste Linear Múltiplo [ ŷ = β₀ + ∑ βⱼxⱼ ]"}
            ]
        },
        {
            "id": "integracao",
            "nome": "Integração Numérica",
            "notacao": "∫ f(x) dx",
            "simbolo": "[ ∫ₐᵇ f(x) dx ]",
            "descricao": "Aproximação de integrais definidas através de fórmulas de Newton-Cotes e Quadratura Gaussiana",
            "metodos": [
                {"id": "trapezios", "nome": "Regra dos Trapézios [ h/2 ]"},
                {"id": "simpson13", "nome": "Regra 1/3 de Simpson [ h/3 (n Par) ]"},
                {"id": "simpson38", "nome": "Regra 3/8 de Simpson [ 3h/8 (n Múltiplo de 3) ]"},
                {"id": "gauss2p", "nome": "Quadratura Gaussiana [ 2 Pontos de Legendre ]"}
            ]
        },
        {
            "id": "edo",
            "nome": "Equações Diferenciais",
            "notacao": "dy/dt = f(t, y)",
            "simbolo": "[ dy/dt = f(t, y) ]",
            "descricao": "Solução numérica de Problemas de Valor Inicial (PVI): dy/dt = f(t, y), com y(t₀) = y₀",
            "metodos": [
                {"id": "euler", "nome": "Método de Euler [ 1ª Ordem ]"},
                {"id": "rk2", "nome": "Runge-Kutta 2ª ordem [ Heun ]"},
                {"id": "rk4", "nome": "Runge-Kutta 4ª ordem [ RK4 Clássico ]"}
            ]
        }
    ]


if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(str(FRONTEND_DIR / "index.html"))

    @app.get("/{full_path:path}")
    async def serve_static_or_spa(full_path: str):
        file_path = FRONTEND_DIR / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(FRONTEND_DIR / "index.html"))
