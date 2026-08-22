"""
Aba de Raízes de Funções (PySide6).
Implementa Bisseção, Newton-Raphson, Cordas, Pégaso e Iteração Linear com visualização gráfica e presets.
"""

from PySide6.QtWidgets import QLabel
from gui.base_tab import AbaBase
from gui.widgets import ModernInput, MetricCard
from gui import theme
from core import parsing, raizes


class RaizesTab(AbaBase):
    def __init__(self, parent=None):
        super().__init__(
            titulo="🔍 Raízes de Funções — [ f(x) = 0 ]",
            subtitulo="Isolamento e refinamento de raízes de equações algébricas e transcendentes f(x) = 0",
            parent=parent
        )
        self.metodos_disponiveis = {
            "Bisseção [ Intervalar ]": "bissecao",
            "Newton-Raphson [ Tangente f'(x) ]": "newton",
            "Método das Cordas [ Secante ]": "cordas",
            "Método de Pégaso [ Acelerado ]": "pegaso",
            "Iteração Linear [ Ponto Fixo x = φ(x) ]": "iteracao_linear",
        }
        self.exemplos_disponiveis = {
            "Polinomial: x³ - x - 2 = 0 em [1, 2]": {
                "metodo": "Bisseção [ Intervalar ]", "funcao": "x**3 - x - 2", "a": "1", "b": "2", "tol": "1e-6", "max_iter": "100"
            },
            "Newton-Raphson: x² - 2 = 0 (x0 = 1.5)": {
                "metodo": "Newton-Raphson [ Tangente f'(x) ]", "funcao": "x**2 - 2", "x0": "1.5", "tol": "1e-8", "max_iter": "50"
            },
            "Transcendente: exp(-x) - x = 0 em [0, 1]": {
                "metodo": "Método das Cordas [ Secante ]", "funcao": "exp(-x) - x", "a": "0", "b": "1", "tol": "1e-6", "max_iter": "100"
            },
            "Trigonométrica: sin(x) - x/2 = 0 em [1, 2.5]": {
                "metodo": "Método de Pégaso [ Acelerado ]", "funcao": "sin(x) - x/2", "a": "1", "b": "2.5", "tol": "1e-6", "max_iter": "100"
            },
            "Ponto Fixo: phi(x) = (x+2)^(1/3) (x0 = 1.5)": {
                "metodo": "Iteração Linear [ Ponto Fixo x = φ(x) ]", "funcao": "(x+2)**(1/3)", "x0": "1.5", "tol": "1e-6", "max_iter": "50"
            },
        }
        self.parsed_expr = None
        self.parsed_func = None
        self.setup_ui()

    def _montar_formulario(self, nome_metodo):
        campos = {}

        if nome_metodo == "iteracao_linear":
            campos["funcao"] = ModernInput(
                "Função de Iteração φ(x) — forma x = φ(x)",
                default_value="(x+2)**(1/3)",
                placeholder="(x+2)**(1/3)",
                tooltip="Digite a função de iteração φ(x) tal que x = φ(x)"
            )
        else:
            campos["funcao"] = ModernInput(
                "Função f(x) = 0",
                default_value="x**3 - x - 2",
                placeholder="Ex: x**3 - x - 2, sin(x) - x/2, exp(-x) - x",
                tooltip="Função em notação SymPy/Python"
            )
        self.layout_formulario.addWidget(campos["funcao"])

        if nome_metodo in ("bissecao", "cordas", "pegaso"):
            campos["a"] = ModernInput("Limite Inferior do Intervalo (a)", "1", tooltip="Início do intervalo de busca [a, b]")
            campos["b"] = ModernInput("Limite Superior do Intervalo (b)", "2", tooltip="Fim do intervalo de busca [a, b]")
            self.layout_formulario.addWidget(campos["a"])
            self.layout_formulario.addWidget(campos["b"])
        else:
            campos["x0"] = ModernInput("Estimativa Inicial (x₀)", "1.5", tooltip="Chute inicial x₀ para o algoritmo")
            self.layout_formulario.addWidget(campos["x0"])

        campos["tol"] = ModernInput("Critério de Parada / Tolerância (tol)", "1e-6", tooltip="Erro máximo permitido |xₖ₊₁ - xₖ| < tol")
        campos["max_iter"] = ModernInput("Máximo de Iterações (k_max)", "100", tooltip="Limite de iterações")
        self.layout_formulario.addWidget(campos["tol"])
        self.layout_formulario.addWidget(campos["max_iter"])

        if nome_metodo == "iteracao_linear":
            lbl_aviso = QLabel("Nota: A convergência exige |φ'(x)| < 1 na vizinhança da raiz.")
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
        if "x0" in self.campos_atuais and "x0" in ex:
            self.campos_atuais["x0"].set(ex["x0"])
        if "tol" in self.campos_atuais and "tol" in ex:
            self.campos_atuais["tol"].set(ex["tol"])
        if "max_iter" in self.campos_atuais and "max_iter" in ex:
            self.campos_atuais["max_iter"].set(ex["max_iter"])

    def _executar(self, nome_metodo, campos):
        funcao_str = campos["funcao"].get()
        if not funcao_str:
            raise ValueError("O campo da função f(x) não pode estar vazio.")

        tol = campos["tol"].get_float("Tolerância")
        max_iter = campos["max_iter"].get_int("Máx. iterações")
        if tol <= 0:
            raise ValueError("A tolerância deve ser estritamente positiva.")
        if max_iter <= 0:
            raise ValueError("O número máximo de iterações deve ser um inteiro positivo.")

        expr, f = parsing.parse_funcao_1var(funcao_str)
        self.parsed_expr = expr
        self.parsed_func = f

        if nome_metodo == "bissecao":
            a = campos["a"].get_float("Limite inferior (a)")
            b = campos["b"].get_float("Limite superior (b)")
            if a >= b:
                raise ValueError("O limite inferior (a) deve ser estritamente menor que o superior (b).")
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
                raise ValueError("O limite inferior (a) deve ser estritamente menor que o superior (b).")
            return raizes.metodo_cordas(f, a, b, tol, max_iter)

        if nome_metodo == "pegaso":
            a = campos["a"].get_float("Limite inferior (a)")
            b = campos["b"].get_float("Limite superior (b)")
            if a >= b:
                raise ValueError("O limite inferior (a) deve ser estritamente menor que o superior (b).")
            return raizes.metodo_pegaso(f, a, b, tol, max_iter)

        # Iteração linear (ponto fixo)
        x0 = campos["x0"].get_float("Estimativa inicial (x0)")
        return raizes.metodo_iteracao_linear(f, x0, tol, max_iter)

    def _formatar_resultado_final(self, resultado_dict):
        raiz = resultado_dict.get("resultado")
        if raiz is None:
            return "Sem raiz calculada."
        try:
            f_val = float(self.parsed_func(raiz))
            return f"Raiz aproximada:\n  x* ≈ {raiz:.10f}\n\nResíduo:\n  |f(x*)| = {abs(f_val):.6e}"
        except Exception:
            return f"Raiz aproximada:\n  x* ≈ {raiz:.10f}"

    def _atualizar_kpis(self, resultado_dict):
        self._limpar_kpis()
        raiz = resultado_dict.get("resultado")
        if raiz is not None:
            self.layout_kpis.addWidget(MetricCard("Raiz Estimada x*", f"{raiz:.8f}"))
            try:
                f_val = float(self.parsed_func(raiz))
                self.layout_kpis.addWidget(MetricCard("Resíduo |f(x*)|", f"{abs(f_val):.2e}"))
            except Exception:
                pass
        if "iteracoes" in resultado_dict:
            self.layout_kpis.addWidget(MetricCard("Iterações (k)", str(resultado_dict["iteracoes"])))

    def _renderizar_grafico(self, resultado_dict):
        nome_metodo = self.combo_metodo.currentText()
        root = resultado_dict.get("resultado")
        
        a, b, x0 = None, None, None
        if "a" in self.campos_atuais and "b" in self.campos_atuais:
            try:
                a = self.campos_atuais["a"].get_float()
                b = self.campos_atuais["b"].get_float()
            except Exception:
                pass
        if "x0" in self.campos_atuais:
            try:
                x0 = self.campos_atuais["x0"].get_float()
            except Exception:
                pass

        self.plot_canvas.plot_raizes(
            f=self.parsed_func, a=a, b=b, root=root, x0=x0, method_name=nome_metodo
        )