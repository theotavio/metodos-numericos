"""
Aba de Interpolação Numérica (PySide6).
Implementa Interpolação Linear, Quadrática, Lagrange e Newton (Diferenças Divididas)
com tabela dinâmica de pontos e curva polinomial interativa contínua.
"""

from PySide6.QtWidgets import QLabel
from gui.base_tab import AbaBase
from gui.widgets import ModernInput, DynamicPointsWidget, MetricCard
from gui import theme
from core import interpolacao


class InterpolacaoTab(AbaBase):
    def __init__(self, parent=None):
        super().__init__(
            titulo="📈 Interpolação Numérica — [ P(x) ]",
            subtitulo="Construção de polinômios interpoladores P(x) e estimativa de valores intermediários",
            parent=parent
        )
        self.metodos_disponiveis = {
            "Interpolação Linear [ 2 Pontos ]": "linear",
            "Interpolação Quadrática [ 3 Pontos ]": "quadratica",
            "Interpolação de Lagrange [ ∑ Lᵢ(x)yᵢ ]": "lagrange",
            "Diferenças Divididas de Newton [ f[x₀,...,xₖ] ]": "newton_dd",
        }
        self.exemplos_disponiveis = {
            "Polinômio Cúbico: 4 Pontos de Lagrange": {
                "metodo": "Interpolação de Lagrange [ ∑ Lᵢ(x)yᵢ ]",
                "pontos": [(0, 1), (1, 3), (2, 2), (3, 5)],
                "x_alvo": "1.5"
            },
            "Interpolação Quadrática: Parábola (3 Pontos)": {
                "metodo": "Interpolação Quadrática [ 3 Pontos ]",
                "pontos": [(1, 2), (2, 5), (4, 17)],
                "x_alvo": "3.0"
            },
            "Diferenças Divididas de Newton: Tabela Dividida": {
                "metodo": "Diferenças Divididas de Newton [ f[x₀,...,xₖ] ]",
                "pontos": [(-1, 4), (0, 1), (2, -1), (3, 2)],
                "x_alvo": "1.0"
            },
            "Termodinâmica: Vapor d'Água (P vs T)": {
                "metodo": "Interpolação de Lagrange [ ∑ Lᵢ(x)yᵢ ]",
                "pontos": [(100, 1.013), (120, 1.985), (140, 3.613), (160, 6.178)],
                "x_alvo": "135.0"
            }
        }
        self.points_widget = None
        self.last_points = []
        self.last_x_alvo = 0.0
        self.setup_ui()

    def _montar_formulario(self, nome_metodo):
        campos = {}

        lbl_tabela = QLabel("Tabela de Pontos Amostrados (xᵢ, yᵢ):")
        lbl_tabela.setStyleSheet("font-size: 12px; font-weight: 500;")
        self.layout_formulario.addWidget(lbl_tabela)

        padrao_pontos = [(1, 2), (2, 5), (4, 17)] if nome_metodo == "quadratica" else [(0, 1), (1, 3), (2, 2), (3, 5)]
        self.points_widget = DynamicPointsWidget(default_points=padrao_pontos)
        self.layout_formulario.addWidget(self.points_widget)

        campos["x_alvo"] = ModernInput(
            "Ponto de Interpolação Alvo (x*)",
            default_value="1.5",
            tooltip="Ponto intermediário onde deseja calcular y* = P(x*)"
        )
        self.layout_formulario.addWidget(campos["x_alvo"])

        if nome_metodo == "quadratica":
            lbl_aviso = QLabel("Nota: A interpolação quadrática exige exatamente 3 pontos com valores de x distintos.")
            lbl_aviso.setStyleSheet(f"color: {theme.get_current_theme()['warning']}; font-size: 11px; font-style: italic;")
            lbl_aviso.setWordWrap(True)
            self.layout_formulario.addWidget(lbl_aviso)

        return campos

    def _carregar_exemplo(self, ex):
        if self.points_widget and "pontos" in ex:
            self.points_widget.set_points(ex["pontos"])
        if "x_alvo" in self.campos_atuais and "x_alvo" in ex:
            self.campos_atuais["x_alvo"].set(ex["x_alvo"])

    def _executar(self, nome_metodo, campos):
        pontos = self.points_widget.get_points()
        x_alvo = campos["x_alvo"].get_float("Valor de x a interpolar")
        
        self.last_points = pontos
        self.last_x_alvo = x_alvo

        if nome_metodo == "linear":
            return interpolacao.interpolacao_linear(pontos, x_alvo)
        if nome_metodo == "quadratica":
            if len(pontos) != 3:
                raise ValueError(f"A interpolação quadrática exige exatamente 3 pontos. Tabela possui {len(pontos)}.")
            return interpolacao.interpolacao_quadratica(pontos, x_alvo)
        if nome_metodo == "lagrange":
            return interpolacao.interpolacao_lagrange(pontos, x_alvo)
        return interpolacao.diferencas_divididas_newton(pontos, x_alvo)

    def _formatar_resultado_final(self, resultado_dict):
        valor = resultado_dict.get("resultado")
        if valor is None:
            return "Sem valor interpolado."
        return f"Valor Interpolado:\n  P({self.last_x_alvo:.4f}) ≈ {valor:.8f}"

    def _atualizar_kpis(self, resultado_dict):
        self._limpar_kpis()
        valor = resultado_dict.get("resultado")
        if valor is not None:
            self.layout_kpis.addWidget(MetricCard("Ponto x*", f"{self.last_x_alvo:.4f}"))
            self.layout_kpis.addWidget(MetricCard("Valor P(x*)", f"{valor:.8f}"))
            self.layout_kpis.addWidget(MetricCard("Nº de Pontos (N)", str(len(self.last_points))))

    def _renderizar_grafico(self, resultado_dict):
        valor = resultado_dict.get("resultado")
        if valor is None or not self.last_points:
            self.plot_canvas.clear()
            return

        nome_metodo = self.combo_metodo.currentText()
        self.plot_canvas.plot_interpolacao(
            pontos=self.last_points,
            x_alvo=self.last_x_alvo,
            y_alvo=valor,
            poly_coeffs=resultado_dict.get("coeficientes"),
            method_name=nome_metodo
        )