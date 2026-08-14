import customtkinter as ctk
from gui.base_tab import AbaBase
from gui.widgets import CampoEntrada
from gui import theme
from core import interpolacao


class InterpolacaoTab(AbaBase):
    def __init__(self, tab):
        self.metodos_disponiveis = {
            "Interpolação Linear": "linear",
            "Interpolação Quadrática": "quadratica",
            "Interpolação de Lagrange": "lagrange",
            "Diferenças Divididas (Newton)": "newton_dd",
        }
        self.entradas_pontos = []
        super().__init__(tab, "Interpolação", "Estimativa de valores intermediários a partir de pontos conhecidos")

    def _montar_formulario(self, nome_metodo):
        campos = {}

        n_padrao = 3 if nome_metodo == "quadratica" else 4
        campos["n_pontos"] = CampoEntrada(self.frame_formulario, "Número de pontos", str(n_padrao))
        campos["n_pontos"].pack(fill="x")

        ctk.CTkButton(
            self.frame_formulario, text="Gerar tabela de pontos",
            command=lambda: self._gerar_tabela(campos["n_pontos"], nome_metodo),
            **theme.estilo_botao_secundario()
        ).pack(fill="x", pady=(0, 12))

        self.frame_pontos = ctk.CTkFrame(self.frame_formulario, fg_color="transparent")
        self.frame_pontos.pack(fill="x")

        campos["x_alvo"] = CampoEntrada(self.frame_formulario, "Valor de x a interpolar", "2.5")
        campos["x_alvo"].pack(fill="x", pady=(6, 0))

        if nome_metodo == "quadratica":
            ctk.CTkLabel(
                self.frame_formulario, text="Este método utiliza exatamente 3 pontos.",
                font=theme.FONT_LABEL_ITALICO, text_color=theme.COR_AVISO,
                wraplength=280, justify="left"
            ).pack(fill="x", pady=(8, 0))

        self.frame_formulario.after(50, lambda: self._gerar_tabela(campos["n_pontos"], nome_metodo))
        return campos

    def _gerar_tabela(self, campo_n, nome_metodo):
        for widget in self.frame_pontos.winfo_children():
            widget.destroy()
        self.entradas_pontos = []

        try:
            n = int(float(campo_n.get()))
        except ValueError:
            self._escrever_saida("Número de pontos inválido.")
            return
        if nome_metodo == "quadratica":
            n = 3
        if n < 2 or n > 12:
            self._escrever_saida("O número de pontos deve estar entre 2 e 12.")
            return

        cab = ctk.CTkFrame(self.frame_pontos, fg_color="transparent")
        cab.pack(fill="x")
        ctk.CTkLabel(cab, text="x", width=110, font=theme.FONT_LABEL,
                     text_color=theme.COR_TEXTO_SECUNDARIO).pack(side="left", padx=3)
        ctk.CTkLabel(cab, text="y = f(x)", width=110, font=theme.FONT_LABEL,
                     text_color=theme.COR_TEXTO_SECUNDARIO).pack(side="left", padx=3)

        for _ in range(n):
            linha = ctk.CTkFrame(self.frame_pontos, fg_color="transparent")
            linha.pack(fill="x", pady=2)
            ex = ctk.CTkEntry(linha, width=110, height=30, fg_color=theme.COR_PAINEL_CLARO,
                               border_color=theme.COR_BORDA, corner_radius=5)
            ex.pack(side="left", padx=3)
            ey = ctk.CTkEntry(linha, width=110, height=30, fg_color=theme.COR_PAINEL_CLARO,
                               border_color=theme.COR_BORDA, corner_radius=5)
            ey.pack(side="left", padx=3)
            self.entradas_pontos.append((ex, ey))

    def _ler_pontos(self):
        if not self.entradas_pontos:
            raise ValueError("A tabela de pontos não foi gerada.")
        pontos = []
        for i, (ex, ey) in enumerate(self.entradas_pontos):
            tx, ty = ex.get().strip(), ey.get().strip()
            if tx == "" or ty == "":
                raise ValueError(f"O ponto {i+1} está incompleto.")
            try:
                x, y = float(tx.replace(",", ".")), float(ty.replace(",", "."))
            except ValueError:
                raise ValueError(f"O ponto {i+1} contém valores inválidos.")
            pontos.append((x, y))
        return pontos

    def _executar(self, nome_metodo, campos):
        pontos = self._ler_pontos()
        x_alvo = campos["x_alvo"].get_float("Valor de x a interpolar")

        if nome_metodo == "linear":
            return interpolacao.interpolacao_linear(pontos, x_alvo)
        if nome_metodo == "quadratica":
            if len(pontos) != 3:
                raise ValueError("A interpolação quadrática exige exatamente 3 pontos.")
            return interpolacao.interpolacao_quadratica(pontos, x_alvo)
        if nome_metodo == "lagrange":
            return interpolacao.interpolacao_lagrange(pontos, x_alvo)
        return interpolacao.diferencas_divididas_newton(pontos, x_alvo)

    def _formatar_resultado_final(self, resultado_dict):
        valor = resultado_dict.get("resultado")
        return f"Valor interpolado: y ≈ {valor:.8f}"