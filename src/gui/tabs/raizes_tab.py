import customtkinter as ctk
from gui.base_tab import AbaBase
from gui.widgets import CampoEntrada
from gui import theme
from core import parsing, raizes


class RaizesTab(AbaBase):
    def __init__(self, tab):
        self.metodos_disponiveis = {
            "Bisseção": "bissecao",
            "Newton-Raphson": "newton",
            "Método das Cordas": "cordas",
            "Método de Pégaso": "pegaso",
            "Iteração Linear": "iteracao_linear",
        }
        super().__init__(tab, "Raízes de Funções", "Isolamento e refinamento de raízes de equações algébricas e transcendentes")

    def _montar_formulario(self, nome_metodo):
        campos = {}

        if nome_metodo == "iteracao_linear":
            campos["funcao"] = CampoEntrada(self.frame_formulario, "phi(x) — forma x = phi(x)", "(x+2)**(1/3)")
        else:
            campos["funcao"] = CampoEntrada(self.frame_formulario, "f(x)", "x**3 - x - 2")
        campos["funcao"].pack(fill="x")

        if nome_metodo in ("bissecao", "cordas", "pegaso"):
            campos["a"] = CampoEntrada(self.frame_formulario, "Limite inferior (a)", "1")
            campos["a"].pack(fill="x")
            campos["b"] = CampoEntrada(self.frame_formulario, "Limite superior (b)", "2")
            campos["b"].pack(fill="x")
        else:
            campos["x0"] = CampoEntrada(self.frame_formulario, "Estimativa inicial (x0)", "1.5")
            campos["x0"].pack(fill="x")

        campos["tol"] = CampoEntrada(self.frame_formulario, "Tolerância", "1e-6")
        campos["tol"].pack(fill="x")
        campos["max_iter"] = CampoEntrada(self.frame_formulario, "Máx. iterações", "100")
        campos["max_iter"].pack(fill="x")

        if nome_metodo == "iteracao_linear":
            ctk.CTkLabel(
                self.frame_formulario,
                text="A convergência depende de |phi'(x)| < 1 próximo à raiz.",
                font=theme.FONT_LABEL_ITALICO, text_color=theme.COR_AVISO,
                wraplength=280, justify="left"
            ).pack(fill="x", pady=(4, 0))

        return campos

    def _executar(self, nome_metodo, campos):
        funcao_str = campos["funcao"].get()
        if not funcao_str:
            raise ValueError("O campo da função não pode estar vazio.")
        tol = campos["tol"].get_float("Tolerância")
        max_iter = campos["max_iter"].get_int("Máx. iterações")
        if tol <= 0:
            raise ValueError("A tolerância deve ser positiva.")
        if max_iter <= 0:
            raise ValueError("O máximo de iterações deve ser um inteiro positivo.")

        expr, f = parsing.parse_funcao_1var(funcao_str)

        if nome_metodo == "bissecao":
            a = campos["a"].get_float("Limite inferior (a)")
            b = campos["b"].get_float("Limite superior (b)")
            if a >= b:
                raise ValueError("O limite inferior deve ser menor que o superior.")
            return raizes.metodo_bissecao(f, a, b, tol, max_iter)

        if nome_metodo == "newton":
            x0 = campos["x0"].get_float("Estimativa inicial (x0)")
            expr_deriv, df = parsing.derivada_simbolica(expr)
            resultado = raizes.metodo_newton_raphson(f, df, x0, tol, max_iter)
            resultado["historico"].insert(0, f"f'(x) calculada simbolicamente = {expr_deriv}\n")
            return resultado

        if nome_metodo == "cordas":
            a = campos["a"].get_float("Limite inferior (a)")
            b = campos["b"].get_float("Limite superior (b)")
            if a >= b:
                raise ValueError("O limite inferior deve ser menor que o superior.")
            return raizes.metodo_cordas(f, a, b, tol, max_iter)

        if nome_metodo == "pegaso":
            a = campos["a"].get_float("Limite inferior (a)")
            b = campos["b"].get_float("Limite superior (b)")
            if a >= b:
                raise ValueError("O limite inferior deve ser menor que o superior.")
            return raizes.metodo_pegaso(f, a, b, tol, max_iter)

        x0 = campos["x0"].get_float("Estimativa inicial (x0)")
        return raizes.metodo_iteracao_linear(f, x0, tol, max_iter)

    def _formatar_resultado_final(self, resultado_dict):
        raiz = resultado_dict.get("resultado")
        return f"Raiz aproximada: x ≈ {raiz:.10f}"