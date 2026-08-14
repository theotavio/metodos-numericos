import customtkinter as ctk
from gui import theme
from gui.widgets import CartaoSecao, BadgeStatus


class AbaBase:
    def __init__(self, tab, titulo, subtitulo=""):
        self.tab = tab
        self.campos_atuais = {}

        self.tab.configure(fg_color=theme.COR_FUNDO)

        cabecalho = ctk.CTkFrame(tab, fg_color="transparent")
        cabecalho.pack(fill="x", padx=20, pady=(18, 10))
        ctk.CTkLabel(cabecalho, text=titulo, font=theme.FONT_TITULO_ABA,
                     text_color=theme.COR_TEXTO).pack(anchor="w")
        if subtitulo:
            ctk.CTkLabel(cabecalho, text=subtitulo, font=theme.FONT_LABEL,
                         text_color=theme.COR_TEXTO_SECUNDARIO).pack(anchor="w", pady=(2, 0))

        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        container.grid_columnconfigure(0, weight=0, minsize=340)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.painel_esquerdo = ctk.CTkScrollableFrame(
            container, width=340, fg_color=theme.COR_PAINEL, corner_radius=12,
            border_width=1, border_color=theme.COR_BORDA, label_text="",
        )
        self.painel_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

        ctk.CTkLabel(self.painel_esquerdo, text="Método", font=theme.FONT_SECAO,
                     text_color=theme.COR_TEXTO_SECUNDARIO).pack(anchor="w", padx=4, pady=(4, 4))

        self.seletor_metodo = ctk.CTkOptionMenu(
            self.painel_esquerdo, values=list(self.metodos_disponiveis.keys()),
            command=self._on_metodo_selecionado, fg_color=theme.COR_PAINEL_CLARO,
            button_color=theme.COR_ACENTO, button_hover_color=theme.COR_ACENTO_HOVER,
            dropdown_fg_color=theme.COR_PAINEL_CLARO, font=theme.FONT_LABEL, height=36,
        )
        self.seletor_metodo.pack(fill="x", pady=(0, 16))

        self.frame_formulario = ctk.CTkFrame(self.painel_esquerdo, fg_color="transparent")
        self.frame_formulario.pack(fill="both", expand=True)

        self.botao_executar = ctk.CTkButton(
            self.painel_esquerdo, text="▶  Executar", command=self._on_executar,
            **theme.estilo_botao_executar()
        )
        self.botao_executar.pack(fill="x", pady=(18, 8))

        self.botao_limpar = ctk.CTkButton(
            self.painel_esquerdo, text="Limpar saída", command=self._limpar_saida,
            **theme.estilo_botao_secundario()
        )
        self.botao_limpar.pack(fill="x")

        painel_direito = ctk.CTkFrame(container, fg_color=theme.COR_PAINEL, corner_radius=12,
                                       border_width=1, border_color=theme.COR_BORDA)
        painel_direito.grid(row=0, column=1, sticky="nsew")

        cab_saida = ctk.CTkFrame(painel_direito, fg_color="transparent")
        cab_saida.pack(fill="x", padx=16, pady=(14, 6))
        ctk.CTkLabel(cab_saida, text="Resultado e histórico de iterações",
                     font=theme.FONT_SECAO, text_color=theme.COR_TEXTO).pack(side="left")
        self.badge_status = BadgeStatus(cab_saida, texto="")
        self.badge_status.pack(side="right")

        self.textbox_saida = ctk.CTkTextbox(
            painel_direito, font=theme.FONT_SAIDA, wrap="none",
            fg_color=theme.COR_FUNDO, corner_radius=8, border_width=1,
            border_color=theme.COR_BORDA, text_color=theme.COR_TEXTO,
        )
        self.textbox_saida.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self._on_metodo_selecionado(self.seletor_metodo.get())

    def _limpar_frame_formulario(self):
        for widget in self.frame_formulario.winfo_children():
            widget.destroy()
        self.campos_atuais = {}

    def _on_metodo_selecionado(self, nome_exibido):
        self._limpar_frame_formulario()
        nome_metodo = self.metodos_disponiveis[nome_exibido]
        self.campos_atuais = self._montar_formulario(nome_metodo)

    def _limpar_saida(self):
        self.textbox_saida.delete("1.0", "end")
        self.badge_status.configure(text="")

    def _escrever_saida(self, texto):
        self.textbox_saida.insert("end", texto + "\n")

    def _exibir_resultado(self, resultado_dict, cabecalho=""):
        self._limpar_saida()
        if cabecalho:
            self._escrever_saida(cabecalho)
            self._escrever_saida("-" * 64 + "\n")

        historico = resultado_dict.get("historico", [])
        if historico:
            self._escrever_saida("HISTÓRICO DE ITERAÇÕES\n")
            for linha in historico:
                self._escrever_saida(linha)
            self._escrever_saida("")

        if resultado_dict.get("sucesso"):
            self._escrever_saida("RESULTADO FINAL")
            self._escrever_saida(self._formatar_resultado_final(resultado_dict))
            if "iteracoes" in resultado_dict:
                self._escrever_saida(f"\nTotal de iterações: {resultado_dict['iteracoes']}")
            self.badge_status.configure(text="● sucesso", text_color=theme.COR_SUCESSO)
        else:
            self._escrever_saida("ERRO")
            self._escrever_saida(resultado_dict.get("erro", "Erro desconhecido."))
            self.badge_status.configure(text="● erro", text_color=theme.COR_ERRO)

    def _formatar_resultado_final(self, resultado_dict):
        return str(resultado_dict.get("resultado"))

    def _on_executar(self):
        nome_exibido = self.seletor_metodo.get()
        nome_metodo = self.metodos_disponiveis[nome_exibido]
        try:
            resultado = self._executar(nome_metodo, self.campos_atuais)
            self._exibir_resultado(resultado, cabecalho=f"Método: {nome_exibido}")
        except ValueError as ve:
            self._limpar_saida()
            self._escrever_saida("ERRO DE VALIDAÇÃO")
            self._escrever_saida(str(ve))
            self.badge_status.configure(text="● erro", text_color=theme.COR_ERRO)
        except ZeroDivisionError as zde:
            self._limpar_saida()
            self._escrever_saida("DIVISÃO POR ZERO")
            self._escrever_saida(str(zde))
            self.badge_status.configure(text="● erro", text_color=theme.COR_ERRO)
        except Exception as exc:
            self._limpar_saida()
            self._escrever_saida("ERRO INESPERADO")
            self._escrever_saida(f"{type(exc).__name__}: {exc}")
            self.badge_status.configure(text="● erro", text_color=theme.COR_ERRO)

    def _montar_formulario(self, nome_metodo):
        raise NotImplementedError

    def _executar(self, nome_metodo, campos):
        raise NotImplementedError