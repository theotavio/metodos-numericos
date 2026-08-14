import customtkinter as ctk
from gui import theme
from gui.tabs.raizes_tab import RaizesTab
from gui.tabs.sistemas_tab import SistemasTab
from gui.tabs.interpolacao_tab import InterpolacaoTab
from gui.tabs.ajuste_tab import AjusteTab
from gui.tabs.integracao_tab import IntegracaoTab
from gui.tabs.edo_tab import EdoTab


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        theme.aplicar_tema()
        self.configure(fg_color=theme.COR_FUNDO)

        self.title("Métodos Numéricos Computacionais")
        self.geometry("1920x1080")
        self.minsize(960, 620)

        cabecalho = ctk.CTkFrame(self, fg_color="transparent")
        cabecalho.pack(fill="x", padx=24, pady=(20, 4))

        bloco_titulo = ctk.CTkFrame(cabecalho, fg_color="transparent")
        bloco_titulo.pack(side="left")
        ctk.CTkLabel(bloco_titulo, text="Métodos Numéricos Computacionais",
                     font=theme.FONT_TITULO_APP, text_color=theme.COR_TEXTO).pack(anchor="w")
        ctk.CTkLabel(bloco_titulo, text="Erros · Sistemas Lineares · Raízes · Interpolação · Integração · EDOs · Ajuste de Curvas",
                     font=theme.FONT_SUBTITULO_APP, text_color=theme.COR_TEXTO_SECUNDARIO).pack(anchor="w", pady=(2, 0))

        self.tabview = ctk.CTkTabview(
            self, anchor="nw", fg_color=theme.COR_FUNDO,
            segmented_button_fg_color=theme.COR_PAINEL,
            segmented_button_selected_color=theme.COR_ACENTO,
            segmented_button_selected_hover_color=theme.COR_ACENTO_HOVER,
            segmented_button_unselected_color=theme.COR_PAINEL,
            segmented_button_unselected_hover_color=theme.COR_PAINEL_CLARO,
            text_color=theme.COR_TEXTO,
        )
        self.tabview.pack(fill="both", expand=True, padx=18, pady=18)

        nomes_abas = [
            "Raízes de Funções",
            "Sistemas Lineares",
            "Interpolação",
            "Ajuste de Curvas",
            "Integração Numérica",
            "EDOs",
        ]
        for nome in nomes_abas:
            self.tabview.add(nome)

        RaizesTab(self.tabview.tab("Raízes de Funções"))
        SistemasTab(self.tabview.tab("Sistemas Lineares"))
        InterpolacaoTab(self.tabview.tab("Interpolação"))
        AjusteTab(self.tabview.tab("Ajuste de Curvas"))
        IntegracaoTab(self.tabview.tab("Integração Numérica"))
        EdoTab(self.tabview.tab("EDOs"))