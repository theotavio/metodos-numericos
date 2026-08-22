"""
Aba de Equações Diferenciais Ordinárias (PySide6).
Implementa Método de Euler, Runge-Kutta de 2ª ordem e Runge-Kutta de 4ª ordem
com gráfico de trajetória da solução e campo de direções (slope field) no plano de fase.
"""

from gui.base_tab import AbaBase
from gui.widgets import ModernInput, MetricCard
from core import parsing, edo


class EdoTab(AbaBase):
    def __init__(self, parent=None):
        super().__init__(
            titulo="🌀 Equações Diferenciais — [ dy/dt = f(t, y) ]",
            subtitulo="Solução numérica de Problemas de Valor Inicial (PVI): dy/dt = f(t, y), com y(t₀) = y₀",
            parent=parent
        )
        self.metodos_disponiveis = {
            "Método de Euler [ 1ª Ordem ]": "euler",
            "Runge-Kutta 2ª ordem [ Heun ]": "rk2",
            "Runge-Kutta 4ª ordem [ RK4 Clássico ]": "rk4",
        }
        self.exemplos_disponiveis = {
            "PVI 1: dy/dt = y - t² + 1, y(0) = 0.5 em [0, 2]": {
                "metodo": "Runge-Kutta 4ª ordem [ RK4 Clássico ]", "funcao": "y - t**2 + 1", "t0": "0", "y0": "0.5", "tn": "2", "h": "0.2"
            },
            "PVI 2 (Euler): dy/dt = -2*t*y, y(0) = 1 em [0, 1.5]": {
                "metodo": "Método de Euler [ 1ª Ordem ]", "funcao": "-2*t*y", "t0": "0", "y0": "1.0", "tn": "1.5", "h": "0.1"
            },
            "PVI 3 (RK2): dy/dt = sin(t) - y, y(0) = 0 em [0, 5]": {
                "metodo": "Runge-Kutta 2ª ordem [ Heun ]", "funcao": "sin(t) - y", "t0": "0", "y0": "0", "tn": "5", "h": "0.25"
            },
            "PVI 4: Crescimento Logístico dy/dt = y*(1 - y/10)": {
                "metodo": "Runge-Kutta 4ª ordem [ RK4 Clássico ]", "funcao": "y*(1 - y/10)", "t0": "0", "y0": "1.0", "tn": "8", "h": "0.4"
            },
        }
        self.parsed_func = None
        self.setup_ui()

    def _montar_formulario(self, nome_metodo):
        campos = {}

        campos["funcao"] = ModernInput(
            "Equação Diferencial dy/dt = f(t, y)",
            default_value="y - t**2 + 1",
            placeholder="Ex: y - t**2 + 1, -2*t*y, sin(t) - y",
            tooltip="Expressão em função das variáveis t (tempo) e y (estado)"
        )
        self.layout_formulario.addWidget(campos["funcao"])

        campos["t0"] = ModernInput("Tempo Inicial (t₀)", "0", tooltip="Ponto de partida temporal")
        campos["y0"] = ModernInput("Condição Inicial y(t₀)", "0.5", tooltip="Valor de y no instante t₀")
        campos["tn"] = ModernInput("Tempo Final (tₙ)", "2", tooltip="Ponto final temporal de integração")
        campos["h"] = ModernInput("Tamanho do Passo (h = Δt)", "0.2", tooltip="Incremento temporal entre passos sucessivos")

        self.layout_formulario.addWidget(campos["t0"])
        self.layout_formulario.addWidget(campos["y0"])
        self.layout_formulario.addWidget(campos["tn"])
        self.layout_formulario.addWidget(campos["h"])

        return campos

    def _carregar_exemplo(self, ex):
        if "funcao" in self.campos_atuais and "funcao" in ex:
            self.campos_atuais["funcao"].set(ex["funcao"])
        if "t0" in self.campos_atuais and "t0" in ex:
            self.campos_atuais["t0"].set(ex["t0"])
        if "y0" in self.campos_atuais and "y0" in ex:
            self.campos_atuais["y0"].set(ex["y0"])
        if "tn" in self.campos_atuais and "tn" in ex:
            self.campos_atuais["tn"].set(ex["tn"])
        if "h" in self.campos_atuais and "h" in ex:
            self.campos_atuais["h"].set(ex["h"])

    def _executar(self, nome_metodo, campos):
        funcao_str = campos["funcao"].get()
        if not funcao_str:
            raise ValueError("O campo da função f(t, y) não pode estar vazio.")

        t0 = campos["t0"].get_float("Tempo inicial (t0)")
        y0 = campos["y0"].get_float("Valor inicial (y0)")
        tn = campos["tn"].get_float("Tempo final (tn)")
        h = campos["h"].get_float("Passo (h)")

        if h <= 0:
            raise ValueError("O passo (h) deve ser estritamente positivo.")
        if tn <= t0:
            raise ValueError("O tempo final (tn) deve ser estritamente maior que o tempo inicial (t0).")

        _, f = parsing.parse_funcao_2var(funcao_str)
        self.parsed_func = f
        self.last_t0 = t0
        self.last_y0 = y0
        self.last_tn = tn
        self.last_h = h

        if nome_metodo == "euler":
            return edo.metodo_euler(f, t0, y0, tn, h)
        if nome_metodo == "rk2":
            return edo.metodo_runge_kutta_2(f, t0, y0, tn, h)
        return edo.metodo_runge_kutta_4(f, t0, y0, tn, h)

    def _formatar_resultado_final(self, resultado_dict):
        pontos = resultado_dict.get("resultado", [])
        if not pontos:
            return "Sem pontos calculados."
        
        t_final, y_final = pontos[-1]
        linhas = [
            f"Valor Final Estimado do PVI:",
            f"  y({t_final:.4f}) ≈ {y_final:.8f}",
            f"\nTotal de Passos Discretos: {len(pontos) - 1}",
            f"Tamanho do Passo (h = Δt): {self.last_h:.4f}",
            "\nÚltimos 3 pontos calculados:",
        ]
        for t, y in pontos[-3:]:
            linhas.append(f"  t = {t:.4f}  ──>  y = {y:.8f}")
        return "\n".join(linhas)

    def _atualizar_kpis(self, resultado_dict):
        self._limpar_kpis()
        pontos = resultado_dict.get("resultado", [])
        if pontos:
            t_fin, y_fin = pontos[-1]
            self.layout_kpis.addWidget(MetricCard(f"Valor Final y(tₙ)", f"{y_fin:.6f}"))
            self.layout_kpis.addWidget(MetricCard("Passos (N)", str(len(pontos) - 1)))
            self.layout_kpis.addWidget(MetricCard("Passo h (Δt)", f"{self.last_h:.4f}"))

    def _renderizar_grafico(self, resultado_dict):
        pontos = resultado_dict.get("resultado", [])
        if not pontos or self.parsed_func is None:
            self.plot_canvas.clear()
            return

        nome_metodo = self.combo_metodo.currentText()
        self.plot_canvas.plot_edo(
            f_func=self.parsed_func,
            pontos=pontos,
            t0=self.last_t0,
            y0=self.last_y0,
            tn=self.last_tn,
            h=self.last_h,
            method_name=nome_metodo
        )