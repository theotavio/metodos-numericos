import customtkinter as ctk
from gui.base_tab import AbaBase
from gui.widgets import CampoEntrada
from gui import theme
from core import ajuste_curvas


class AjusteTab(AbaBase):
    def __init__(self, tab):
        self.metodos_disponiveis = {
            "Ajuste Linear Simples": "simples",
            "Ajuste Linear Múltiplo": "multiplo",
        }
        self.entradas_pontos = []
        self.entradas_x_mult = []
        self.entradas_y_mult = []
        super().__init__(tab, "Ajuste de Curvas", "Regressão pelo método dos mínimos quadrados")

    def _montar_formulario(self, nome_metodo):
        campos = {}

        if nome_metodo == "simples":
            campos["n_pontos"] = CampoEntrada(self.frame_formulario, "Número de pontos (x, y)", "5")
            campos["n_pontos"].pack(fill="x")
            ctk.CTkButton(
                self.frame_formulario, text="Gerar tabela",
                command=lambda: self._gerar_tabela_simples(campos["n_pontos"]),
                **theme.estilo_botao_secundario()
            ).pack(fill="x", pady=(0, 12))
            self.frame_pontos = ctk.CTkFrame(self.frame_formulario, fg_color="transparent")
            self.frame_pontos.pack(fill="x")
            self.frame_formulario.after(50, lambda: self._gerar_tabela_simples(campos["n_pontos"]))
        else:
            campos["n_obs"] = CampoEntrada(self.frame_formulario, "Número de observações", "5")
            campos["n_obs"].pack(fill="x")
            campos["n_vars"] = CampoEntrada(self.frame_formulario, "Número de variáveis independentes", "2")
            campos["n_vars"].pack(fill="x")
            ctk.CTkButton(
                self.frame_formulario, text="Gerar tabela",
                command=lambda: self._gerar_tabela_multipla(campos["n_obs"], campos["n_vars"]),
                **theme.estilo_botao_secundario()
            ).pack(fill="x", pady=(0, 12))
            self.frame_pontos = ctk.CTkFrame(self.frame_formulario, fg_color="transparent")
            self.frame_pontos.pack(fill="x")
            self.frame_formulario.after(50, lambda: self._gerar_tabela_multipla(campos["n_obs"], campos["n_vars"]))

        return campos

    def _gerar_tabela_simples(self, campo_n):
        for widget in self.frame_pontos.winfo_children():
            widget.destroy()
        self.entradas_pontos = []

        try:
            n = int(float(campo_n.get()))
        except ValueError:
            self._escrever_saida("Número de pontos inválido.")
            return
        if n < 2 or n > 20:
            self._escrever_saida("O número de pontos deve estar entre 2 e 20.")
            return

        cab = ctk.CTkFrame(self.frame_pontos, fg_color="transparent")
        cab.pack(fill="x")
        ctk.CTkLabel(cab, text="x", width=110, font=theme.FONT_LABEL,
                     text_color=theme.COR_TEXTO_SECUNDARIO).pack(side="left", padx=3)
        ctk.CTkLabel(cab, text="y", width=110, font=theme.FONT_LABEL,
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

    def _gerar_tabela_multipla(self, campo_obs, campo_vars):
        for widget in self.frame_pontos.winfo_children():
            widget.destroy()
        self.entradas_x_mult = []
        self.entradas_y_mult = []

        try:
            n_obs = int(float(campo_obs.get()))
            n_vars = int(float(campo_vars.get()))
        except ValueError:
            self._escrever_saida("Valores inválidos para gerar a tabela.")
            return
        if n_obs < 3 or n_obs > 20 or n_vars < 1 or n_vars > 6:
            self._escrever_saida("Observações entre 3-20 e variáveis entre 1-6.")
            return

        cab = ctk.CTkFrame(self.frame_pontos, fg_color="transparent")
        cab.pack(fill="x")
        for j in range(n_vars):
            ctk.CTkLabel(cab, text=f"x{j+1}", width=70, font=theme.FONT_LABEL,
                         text_color=theme.COR_TEXTO_SECUNDARIO).pack(side="left", padx=2)
        ctk.CTkLabel(cab, text="y", width=70, font=theme.FONT_LABEL,
                     text_color=theme.COR_TEXTO_SECUNDARIO).pack(side="left", padx=2)

        for _ in range(n_obs):
            linha = ctk.CTkFrame(self.frame_pontos, fg_color="transparent")
            linha.pack(fill="x", pady=2)
            entradas_x = []
            for _ in range(n_vars):
                ex = ctk.CTkEntry(linha, width=70, height=30, fg_color=theme.COR_PAINEL_CLARO,
                                   border_color=theme.COR_BORDA, corner_radius=5)
                ex.pack(side="left", padx=2)
                entradas_x.append(ex)
            ey = ctk.CTkEntry(linha, width=70, height=30, fg_color=theme.COR_PAINEL_CLARO,
                               border_color=theme.COR_BORDA, corner_radius=5)
            ey.pack(side="left", padx=2)
            self.entradas_x_mult.append(entradas_x)
            self.entradas_y_mult.append(ey)

    def _executar(self, nome_metodo, campos):
        if nome_metodo == "simples":
            if not self.entradas_pontos:
                raise ValueError("A tabela de pontos não foi gerada.")
            pontos = []
            for i, (ex, ey) in enumerate(self.entradas_pontos):
                tx, ty = ex.get().strip(), ey.get().strip()
                if tx == "" or ty == "":
                    raise ValueError(f"O ponto {i+1} está incompleto.")
                try:
                    pontos.append((float(tx.replace(",", ".")), float(ty.replace(",", "."))))
                except ValueError:
                    raise ValueError(f"O ponto {i+1} contém valores inválidos.")
            return ajuste_curvas.ajuste_linear_simples(pontos)

        if not self.entradas_x_mult:
            raise ValueError("A tabela de observações não foi gerada.")
        X, y = [], []
        for i, (entradas_x, ey) in enumerate(zip(self.entradas_x_mult, self.entradas_y_mult)):
            linha_x = []
            for j, ex in enumerate(entradas_x):
                t = ex.get().strip()
                if t == "":
                    raise ValueError(f"O valor x{j+1} da observação {i+1} está vazio.")
                try:
                    linha_x.append(float(t.replace(",", ".")))
                except ValueError:
                    raise ValueError(f"Valor inválido em x{j+1}, observação {i+1}.")
            X.append(linha_x)

            ty = ey.get().strip()
            if ty == "":
                raise ValueError(f"O valor y da observação {i+1} está vazio.")
            try:
                y.append(float(ty.replace(",", ".")))
            except ValueError:
                raise ValueError(f"Valor de y inválido na observação {i+1}.")

        return ajuste_curvas.ajuste_linear_multiplo(X, y)

    def _formatar_resultado_final(self, resultado_dict):
        r = resultado_dict.get("resultado")
        if "a0" in r:
            return f"y = {r['a0']:.6f} + {r['a1']:.6f}·x\nR² = {r['r2']:.6f}"
        coefs = r["coeficientes"]
        linhas = [f"β0 (intercepto) = {coefs[0]:.6f}"]
        linhas += [f"β{i} = {c:.6f}" for i, c in enumerate(coefs[1:], start=1)]
        linhas.append(f"R² = {r['r2']:.6f}")
        return "\n".join(linhas)