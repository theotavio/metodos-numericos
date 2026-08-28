from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class BaseCalculationResponse(BaseModel):
    sucesso: bool
    resultado: Any = None
    historico: List[str] = Field(default_factory=list)
    erro: Optional[str] = None
    iteracoes: Optional[int] = None
    tempo_ms: float = 0.0
    kpis: List[Dict[str, Any]] = Field(default_factory=list)
    detalhes_matematicos: List[Dict[str, str]] = Field(default_factory=list)
    plot_data: Optional[Dict[str, Any]] = None
    etapas_gauss: Optional[List[Dict[str, Any]]] = None
    substituicao_passos: Optional[List[str]] = None
    dominancia_info: Optional[Dict[str, Any]] = None


class RaizesRequest(BaseModel):
    metodo: str = Field(..., description="bissecao, newton, secante, cordas, pegaso, iteracao_linear")
    funcao: str = Field(..., description="Expressão matemática da função f(x) ou φ(x)")
    tipo_derivada: Optional[str] = Field(default="simbolica", description="simbolica, central, progressiva, regressiva, complexa, manual")
    df_manual: Optional[str] = Field(default=None, description="Expressão analítica de f'(x) quando tipo_derivada='manual'")
    h_derivada: Optional[float] = Field(default=1e-6, description="Passo de diferenciação numérica")
    a: Optional[float] = Field(default=None, description="Limite inferior para métodos intervalares")
    b: Optional[float] = Field(default=None, description="Limite superior para métodos intervalares")
    x0: Optional[float] = Field(default=None, description="Estimativa inicial")
    x1: Optional[float] = Field(default=None, description="Segunda estimativa inicial (Secante)")
    tol: float = Field(default=1e-6, gt=0, description="Tolerância de convergência")
    max_iter: int = Field(default=100, gt=0, description="Número máximo de iterações")


class SistemasRequest(BaseModel):
    metodo: str = Field(..., description="gauss, gauss_seidel")
    A: List[List[float]] = Field(..., description="Matriz dos coeficientes n×n")
    b: List[float] = Field(..., description="Vetor de termos independentes de tamanho n")
    tol: Optional[float] = Field(default=1e-6, gt=0, description="Tolerância (Gauss-Seidel)")
    max_iter: Optional[int] = Field(default=100, gt=0, description="Máximo de iterações (Gauss-Seidel)")


class InterpolacaoRequest(BaseModel):
    metodo: str = Field(..., description="linear, quadratica, lagrange, newton_dd")
    pontos: List[Tuple[float, float]] = Field(..., description="Lista de pares (x, y)")
    x_alvo: float = Field(..., description="Ponto a interpolar x*")


class AjusteRequest(BaseModel):
    metodo: str = Field(..., description="simples, multiplo")
    pontos: Optional[List[Tuple[float, float]]] = None
    X: Optional[List[List[float]]] = None
    y: Optional[List[float]] = None


class IntegracaoRequest(BaseModel):
    metodo: str = Field(..., description="trapezios, simpson13, simpson38, gauss2p")
    funcao: str = Field(..., description="Expressão matemática da função f(x)")
    a: float = Field(..., description="Limite inferior de integração")
    b: float = Field(..., description="Limite superior de integração")
    n: Optional[int] = Field(default=10, description="Número de subintervalos")


class EdoRequest(BaseModel):
    metodo: str = Field(..., description="euler, rk2, rk4")
    funcao: str = Field(..., description="Expressão da derivada dy/dt = f(t, y)")
    t0: float = Field(..., description="Tempo inicial t0")
    y0: float = Field(..., description="Condição inicial y(t0)")
    tn: float = Field(..., description="Tempo final tn")
    h: float = Field(..., gt=0, description="Tamanho do passo h = Δt")
