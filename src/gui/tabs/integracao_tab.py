"""
Aba de Integração Numérica (PySide6).
Implementa Regra dos Trapézios, Simpson 1/3, Simpson 3/8 e Quadratura Gaussiana (2 pontos)
com visualização gráfica da área hachurada e partição dos subintervalos.
"""

from PySide6.QtWidgets import QLabel
from gui.base_tab import AbaBase
from gui.widgets import ModernInput, MetricCard
from gui import theme
from core import parsing, integracao


class IntegracaoTab(AbaBase):
    def __init__(self, parent=None):
        super().__init__(
            titulo="∫ Integração Numérica — [ ∫ₐᵇ f(x) dx ]",
            subtitulo="Aproximação de integrais definidas através de fórmulas de Newton-Cotes e Quadratura Gaussiana",
            parent=parent
        )
        self.metodos_disponiveis = {
            "Regra dos Trapézios [ h/2 ]": "trapezios",
            "Regra 1/3 de Simpson [ h/3 (n Par) ]": "simpson13",
            "Regra 3/8 de Simpson [ 3h/8 (n Múltiplo de 3) ]": "simpson38",
            "Quadratura Gaussiana [ 2 Pontos de Legendre ]": "gauss2p",
        }
        self.exemplos_disponiveis = {
            "Parábola: ∫₀² x² dx (Exato: 8/3 ≈ 2.6667)": {
                "metodo": "Regra 1/3 de Simpson [ h/3 (n Par) ]", "funcao": "x**2", "a": "0", "b": "2", "n": "6"
            },
            "Trigonométrica: ∫₀^π sin(x) dx (Exato: 2.0)": {
                "metodo": "Regra dos Trapézios [ h/2 ]", "funcao": "sin(x)", "a": "0", "b": "pi", "n": "12"
            },
            "Função Racional: ∫₁³ 1/x dx (Exato: ln 3 ≈ 1.0986)": {
                "metodo": "Regra 3/8 de Simpson [ 3h/8 (n Múltiplo de 3) ]", "funcao": "1/x", "a": "1", "b": "3", "n": "6"
            },
            "Campânula Gaussiana: ∫₀¹ exp(-x²) dx (Exato: 0.7468)": {
                "metodo": "Quadratura Gaussiana [ 2 Pontos de Legendre ]", "funcao": "exp(-x**2)", "a": "0", "b": "1"
            },
        }
        self.parsed_func = None
        self.setup_ui()

    def _montar_formulario(self, nome_metodo):
        campos = {}

        campos["funcao"] = ModernInput(
            "Função Integranda f(x)",
            default_value="x**2",
            placeholder="Ex: x**2, sin(x), exp(-x**2), 1/x",
            tooltip="Função em notação SymPy/Python"
        )
        self.layout_formulario.addWidget(campos["funcao"])

        campos["a"] = ModernInput("Limite Inferior de Integração (a)", "0", tooltip="Início do intervalo [a, b]")
        campos["b"] = ModernInput("Limite Superior de Integração (b)", "2", tooltip="Fim do intervalo [a, b]")
        self.layout_formulario.addWidget(campos["a"])
        self.layout_formulario.addWidget(campos["b"])

        if nome_metodo != "gauss2p":
            campos["n"] = ModernInput(
                "Número de Subintervalos (n)",
                default_value="10" if nome_metodo == "trapezios" else ("6" if nome_metodo in ("simpson13", "simpson38") else "4"),
                tooltip="Número de divisões do intervalo"
            )
            self.layout_formulario.addWidget(campos["n"])

        avisos = {
            "simpson13": "Nota: A Regra 1/3 de Simpson exige 'n' PAR.",
            "simpson38": "Nota: A Regra 3/8 de Simpson exige 'n' MÚLTIPLO DE 3.",
            "gauss2p": "Nota: A Quadratura Gaussiana avalia a função em 2 pontos de Legendre otimizados.",
        }
        if nome_metodo in avisos:
            lbl_aviso = QLabel(avisos[nome_metodo])
            lbl_aviso.setStyleSheet(f"color: {theme.get_current_theme()['warning']}; font-size: 11px; font-style: italic;")
            lbl_aviso.setWordWrap(True)
            self.layout_formulario.addWidget(lbl_aviso)

        return campos

    def _carregar_exemplo(self, ex):
        if "funcao" in self.campos_atuais and "funcao" in ex:
            self.campos_atuais["funcao"].set(ex["funcao"])
        if "a" in self.campos_atuais and "a" in ex:
            self.campos_atuais["a"].set(ex["a"])
        if "b" in self.campos_atuais and "b" in ex:
            self.campos_atuais["b"].set(ex["b"])
        if "n" in self.campos_atuais and "n" in ex:
            self.campos_atuais["n"].set(ex["n"])

    def _executar(self, nome_metodo, campos):
        funcao_str = campos["funcao"].get()
        if not funcao_str:
            raise ValueError("O campo da função integranda não pode estar vazio.")

        a = campos["a"].get_float("Limite inferior (a)")
        b = campos["b"].get_float("Limite superior (b)")
        _, f = parsing.parse_funcao_1var(funcao_str)
        self.parsed_func = f
        self.last_a = a
        self.last_b = b

        if nome_metodo == "gauss2p":
            self.last_n = 2
            return integracao.quadratura_gaussiana_2p(f, a, b)

        n = campos["n"].get_int("Número de subintervalos (n)")
        self.last_n = n

        if nome_metodo == "trapezios":
            return integracao.regra_trapezios(f, a, b, n)
        if nome_metodo == "simpson13":
            return integracao.regra_simpson_1_3(f, a, b, n)
        return integracao.regra_simpson_3_8(f, a, b, n)

    def _formatar_resultado_final(self, resultado_dict):
        res = resultado_dict.get("resultado")
        if res is None:
            return "Sem integral calculada."
        return f"Integral Definida Aproximada:\n  I = ∫[{self.last_a:.4f}, {self.last_b:.4f}] f(x) dx ≈ {res:.10f}"

    def _atualizar_kpis(self, resultado_dict):
        self._limpar_kpis()
        res = resultado_dict.get("resultado")
        if res is not None:
            self.layout_kpis.addWidget(MetricCard("Valor da Integral ∫", f"{res:.8f}"))
            self.layout_kpis.addWidget(MetricCard("Intervalo [a, b]", f"[{self.last_a:.2f}, {self.last_b:.2f}]"))
            if hasattr(self, "last_n"):
                self.layout_kpis.addWidget(MetricCard("Subintervalos (n)", str(self.last_n)))

    def _renderizar_grafico(self, resultado_dict):
        res = resultado_dict.get("resultado")
        if res is None or self.parsed_func is None:
            self.plot_canvas.clear()
            return

        nome_metodo = self.combo_metodo.currentText()
        self.plot_canvas.plot_integracao(
            f=self.parsed_func,
            a=self.last_a,
            b=self.last_b,
            n=self.last_n,
            method_name=nome_metodo,
            result_val=res
        )