import customtkinter as ctk
from gui.base_tab import AbaBase
from gui.widgets import CampoEntrada
from gui import theme
from core import parsing
from core import integracao


class IntegracaoTab(AbaBase):
    def __init__(self, tab):
        self.metodos_disponiveis = {
            "Regra dos Trapézios": "trapezios",
            "Regra 1/3 de Simpson": "simpson13",
            "Regra 3/8 de Simpson": "simpson38",
            "Quadratura Gaussiana (2 pontos)": "gauss2p",
        }
        super().__init__(tab, "Integração Numérica", "Aproximação de integrais definidas")

    def _montar_formulario(self, nome_metodo):
        campos = {}
        campos["funcao"] = CampoEntrada(self.frame_formulario, "f(x)", "x**2")
        campos["funcao"].pack(fill="x")
        campos["a"] = CampoEntrada(self.frame_formulario, "Limite inferior (a)", "0")
        campos["a"].pack(fill="x")
        campos["b"] = CampoEntrada(self.frame_formulario, "Limite superior (b)", "2")
        campos["b"].pack(fill="x")

        if nome_metodo != "gauss2p":
            campos["n"] = CampoEntrada(self.frame_formulario, "Número de subintervalos (n)", "10")
            campos["n"].pack(fill="x")

        avisos = {
            "simpson13": "n deve ser PAR para a Regra 1/3 de Simpson.",
            "simpson38": "n deve ser MÚLTIPLO DE 3 para a Regra 3/8 de Simpson.",
        }
        if nome_metodo in avisos:
            ctk.CTkLabel(
                self.frame_formulario, text=avisos[nome_metodo],
                font=theme.FONT_LABEL_ITALICO, text_color=theme.COR_AVISO,
                wraplength=280, justify="left"
            ).pack(fill="x", pady=(4, 0))

        return campos

    def _executar(self, nome_metodo, campos):
        funcao_str = campos["funcao"].get()
        if not funcao_str:
            raise ValueError("O campo da função não pode estar vazio.")
        a = campos["a"].get_float("Limite inferior (a)")
        b = campos["b"].get_float("Limite superior (b)")
        _, f = parsing.parse_funcao_1var(funcao_str)

        if nome_metodo == "gauss2p":
            return integracao.quadratura_gaussiana_2p(f, a, b)

        n = campos["n"].get_int("Número de subintervalos (n)")
        if nome_metodo == "trapezios":
            return integracao.regra_trapezios(f, a, b, n)
        if nome_metodo == "simpson13":
            return integracao.regra_simpson_1_3(f, a, b, n)
        return integracao.regra_simpson_3_8(f, a, b, n)

    def _formatar_resultado_final(self, resultado_dict):
        return f"Integral aproximada: {resultado_dict.get('resultado'):.10f}"