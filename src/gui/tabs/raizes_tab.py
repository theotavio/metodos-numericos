"""
Aba de Raízes de Funções (PySide6).
Implementa Bisseção, Newton-Raphson (com múltiplos tipos de derivadas),
Secante, Cordas, Pégaso e Iteração Linear com visualização gráfica e presets.
"""

from PySide6.QtWidgets import QLabel
from gui.base_tab import AbaBase
from gui.widgets import ModernInput, ModernSelect, MetricCard
from gui import theme
from core import parsing, raizes, derivadas


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
            "Método da Secante [ Quasi-Newton ]": "secante",
            "Método das Cordas [ Falsa Posição ]": "cordas",
            "Método de Pégaso [ Acelerado ]": "pegaso",
            "Iteração Linear [ Ponto Fixo x = φ(x) ]": "iteracao_linear",
        }
        self.exemplos_disponiveis = {
            "Polinomial: x³ - x - 2 = 0 em [1, 2]": {
                "metodo": "Bisseção [ Intervalar ]",
                "funcao": "x**3 - x - 2",
                "a": "1",
                "b": "2",
                "tol": "1e-6",
                "max_iter": "100"
            },
            "Newton-Raphson (Simbólica): x² - 2 = 0 (x0 = 1.5)": {
                "metodo": "Newton-Raphson [ Tangente f'(x) ]",
                "funcao": "x**2 - 2",
                "tipo_derivada": "simbolica",
                "x0": "1.5",
                "tol": "1e-8",
                "max_iter": "50"
            },
            "Newton-Raphson (Dif. Finita Central): exp(-x) - x = 0": {
                "metodo": "Newton-Raphson [ Tangente f'(x) ]",
                "funcao": "exp(-x) - x",
                "tipo_derivada": "central",
                "h_derivada": "1e-6",
                "x0": "0.5",
                "tol": "1e-8",
                "max_iter": "50"
            },
            "Newton-Raphson (Passo Complexo): sin(x) - x/2 = 0": {
                "metodo": "Newton-Raphson [ Tangente f'(x) ]",
                "funcao": "sin(x) - x/2",
                "tipo_derivada": "complexa",
                "h_derivada": "1e-20",
                "x0": "2.0",
                "tol": "1e-8",
                "max_iter": "50"
            },
            "Newton-Raphson (Derivada Manual): x³ - 2x - 5 = 0": {
                "metodo": "Newton-Raphson [ Tangente f'(x) ]",
                "funcao": "x**3 - 2*x - 5",
                "tipo_derivada": "manual",
                "df_manual": "3*x**2 - 2",
                "x0": "2.0",
                "tol": "1e-8",
                "max_iter": "50"
            },
            "Método da Secante: x³ - x - 2 = 0 (x0=1, x1=2)": {
                "metodo": "Método da Secante [ Quasi-Newton ]",
                "funcao": "x**3 - x - 2",
                "x0": "1.0",
                "x1": "2.0",
                "tol": "1e-6",
                "max_iter": "100"
            },
            "Transcendente: exp(-x) - x = 0 em [0, 1]": {
                "metodo": "Método das Cordas [ Falsa Posição ]",
                "funcao": "exp(-x) - x",
                "a": "0",
                "b": "1",
                "tol": "1e-6",
                "max_iter": "100"
            },
            "Trigonométrica: sin(x) - x/2 = 0 em [1, 2.5]": {
                "metodo": "Método de Pégaso [ Acelerado ]",
                "funcao": "sin(x) - x/2",
                "a": "1",
                "b": "2.5",
                "tol": "1e-6",
                "max_iter": "100"
            },
            "Ponto Fixo: phi(x) = (x+2)^(1/3) (x0 = 1.5)": {
                "metodo": "Iteração Linear [ Ponto Fixo x = φ(x) ]",
                "funcao": "(x+2)**(1/3)",
                "x0": "1.5",
                "tol": "1e-6",
                "max_iter": "50"
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

        if nome_metodo == "newton":
            campos["tipo_derivada"] = ModernSelect(
                "Tipo de Cálculo da Derivada f'(x)",
                items=derivadas.TIPOS_DERIVADAS,
                default_value="Simbólica [ SymPy / Analítica ]",
                tooltip="Escolha como a derivada f'(x) será computada pelo método de Newton-Raphson"
            )
            self.layout_formulario.addWidget(campos["tipo_derivada"])

            campos["df_manual"] = ModernInput(
                "Expressão da Derivada f'(x)",
                default_value="3*x**2 - 1",
                placeholder="Ex: 3*x**2 - 1, 2*x, cos(x) - 0.5",
                tooltip="Digite a fórmula analítica da derivada f'(x)"
            )
            self.layout_formulario.addWidget(campos["df_manual"])

            campos["h_derivada"] = ModernInput(
                "Passo de Diferenciação (h)",
                default_value="1e-6",
                placeholder="Ex: 1e-6 (diferenças finitas) ou 1e-20 (passo complexo)",
                tooltip="Incremento h usado para calcular a derivada numericamente"
            )
            self.layout_formulario.addWidget(campos["h_derivada"])

            # Atualiza visibilidade dos campos dinâmicos da derivada
            def _atualizar_campos_derivada(texto):
                tipo = campos["tipo_derivada"].get_value()
                if tipo == "manual":
                    campos["df_manual"].setVisible(True)
                    campos["h_derivada"].setVisible(False)
                elif tipo in ("central", "progressiva", "regressiva", "complexa"):
                    campos["df_manual"].setVisible(False)
                    campos["h_derivada"].setVisible(True)
                    if tipo == "complexa" and campos["h_derivada"].get() == "1e-6":
                        campos["h_derivada"].set("1e-20")
                    elif tipo != "complexa" and campos["h_derivada"].get() == "1e-20":
                        campos["h_derivada"].set("1e-6")
                else:  # Simbólica
                    campos["df_manual"].setVisible(False)
                    campos["h_derivada"].setVisible(False)

            campos["tipo_derivada"].currentTextChanged.connect(_atualizar_campos_derivada)
            _atualizar_campos_derivada(campos["tipo_derivada"].get())

        if nome_metodo in ("bissecao", "cordas", "pegaso"):
            campos["a"] = ModernInput("Limite Inferior do Intervalo (a)", "1", tooltip="Início do intervalo de busca [a, b]")
            campos["b"] = ModernInput("Limite Superior do Intervalo (b)", "2", tooltip="Fim do intervalo de busca [a, b]")
            self.layout_formulario.addWidget(campos["a"])
            self.layout_formulario.addWidget(campos["b"])
        elif nome_metodo == "secante":
            campos["x0"] = ModernInput("Primeira Estimativa Inicial (x₀)", "1.0", tooltip="Primeiro ponto inicial para a reta secante")
            campos["x1"] = ModernInput("Segunda Estimativa Inicial (x₁)", "2.0", tooltip="Segundo ponto inicial para a reta secante")
            self.layout_formulario.addWidget(campos["x0"])
            self.layout_formulario.addWidget(campos["x1"])
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
        if "tipo_derivada" in self.campos_atuais and "tipo_derivada" in ex:
            self.campos_atuais["tipo_derivada"].set(ex["tipo_derivada"])
        if "df_manual" in self.campos_atuais and "df_manual" in ex:
            self.campos_atuais["df_manual"].set(ex["df_manual"])
        if "h_derivada" in self.campos_atuais and "h_derivada" in ex:
            self.campos_atuais["h_derivada"].set(ex["h_derivada"])
        if "a" in self.campos_atuais and "a" in ex:
            self.campos_atuais["a"].set(ex["a"])
        if "b" in self.campos_atuais and "b" in ex:
            self.campos_atuais["b"].set(ex["b"])
        if "x0" in self.campos_atuais and "x0" in ex:
            self.campos_atuais["x0"].set(ex["x0"])
        if "x1" in self.campos_atuais and "x1" in ex:
            self.campos_atuais["x1"].set(ex["x1"])
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
            tipo_deriv = campos["tipo_derivada"].get_value()

            h_val = 1e-6
            if tipo_deriv in ("central", "progressiva", "regressiva", "complexa"):
                h_val = campos["h_derivada"].get_float("Passo de diferenciação (h)")
                if h_val <= 0:
                    raise ValueError("O passo de diferenciação (h) deve ser estritamente positivo.")

            manual_str = campos["df_manual"].get() if tipo_deriv == "manual" else None

            df, desc_deriv, expr_deriv = derivadas.construir_derivada(
                tipo=tipo_deriv,
                f=f,
                expr_sympy=expr,
                variavel="x",
                h=h_val,
                expressao_manual_str=manual_str
            )

            resultado = raizes.metodo_newton_raphson(f, df, x0, tol, max_iter)
            resultado["historico"].insert(0, f"Método de Derivação: {desc_deriv}\n")
            resultado["descricao_derivada"] = desc_deriv
            return resultado

        if nome_metodo == "secante":
            x0 = campos["x0"].get_float("Primeira estimativa inicial (x0)")
            x1 = campos["x1"].get_float("Segunda estimativa inicial (x1)")
            return raizes.metodo_secante(f, x0, x1, tol, max_iter)

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
        detalhes = []
        if "descricao_derivada" in resultado_dict:
            detalhes.append(f"Derivada Utilizada:\n  {resultado_dict['descricao_derivada']}\n")
        try:
            f_val = float(self.parsed_func(raiz))
            detalhes.append(f"Raiz aproximada:\n  x* ≈ {raiz:.10f}\n\nResíduo:\n  |f(x*)| = {abs(f_val):.6e}")
        except Exception:
            detalhes.append(f"Raiz aproximada:\n  x* ≈ {raiz:.10f}")
        return "\n".join(detalhes)

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