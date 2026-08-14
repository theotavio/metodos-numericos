from gui.base_tab import AbaBase
from gui.widgets import CampoEntrada
from core import parsing, edo


class EdoTab(AbaBase):
    def __init__(self, tab):
        self.metodos_disponiveis = {
            "Método de Euler": "euler",
            "Runge-Kutta 2ª ordem": "rk2",
            "Runge-Kutta 4ª ordem": "rk4",
        }
        super().__init__(tab, "Equações Diferenciais Ordinárias", "Solução numérica de PVIs: dy/dt = f(t, y), y(t0) = y0")

    def _montar_formulario(self, nome_metodo):
        campos = {}
        campos["funcao"] = CampoEntrada(self.frame_formulario, "f(t, y)", "y - t**2 + 1")
        campos["funcao"].pack(fill="x")
        campos["t0"] = CampoEntrada(self.frame_formulario, "Tempo inicial (t0)", "0")
        campos["t0"].pack(fill="x")
        campos["y0"] = CampoEntrada(self.frame_formulario, "Valor inicial (y0)", "0.5")
        campos["y0"].pack(fill="x")
        campos["tn"] = CampoEntrada(self.frame_formulario, "Tempo final (tn)", "2")
        campos["tn"].pack(fill="x")
        campos["h"] = CampoEntrada(self.frame_formulario, "Passo (h)", "0.2")
        campos["h"].pack(fill="x")
        return campos

    def _executar(self, nome_metodo, campos):
        funcao_str = campos["funcao"].get()
        if not funcao_str:
            raise ValueError("O campo da função f(t, y) não pode estar vazio.")
        t0 = campos["t0"].get_float("Tempo inicial (t0)")
        y0 = campos["y0"].get_float("Valor inicial (y0)")
        tn = campos["tn"].get_float("Tempo final (tn)")
        h = campos["h"].get_float("Passo (h)")

        _, f = parsing.parse_funcao_2var(funcao_str)

        if nome_metodo == "euler":
            return edo.metodo_euler(f, t0, y0, tn, h)
        if nome_metodo == "rk2":
            return edo.metodo_runge_kutta_2(f, t0, y0, tn, h)
        return edo.metodo_runge_kutta_4(f, t0, y0, tn, h)

    def _formatar_resultado_final(self, resultado_dict):
        pontos = resultado_dict.get("resultado", [])
        if not pontos:
            return "Sem pontos calculados."
        linhas = ["Tabela de pontos (t, y):"]
        for t, y in pontos:
            linhas.append(f"  t = {t:.4f}   ->   y = {y:.8f}")
        t_final, y_final = pontos[-1]
        linhas.append(f"\nAproximação final: y({t_final:.4f}) ≈ {y_final:.8f}")
        return "\n".join(linhas)