import customtkinter as ctk
from gui import theme


class CampoEntrada:
    def __init__(self, parent, rotulo, valor_padrao="", largura=None):
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.label = ctk.CTkLabel(self.frame, text=rotulo, font=theme.FONT_LABEL,
                                   anchor="w", text_color=theme.COR_TEXTO_SECUNDARIO)
        self.label.pack(side="top", anchor="w", pady=(0, 3))
        entry_kwargs = theme.estilo_entry()
        if largura:
            entry_kwargs["width"] = largura
        self.entry = ctk.CTkEntry(self.frame, placeholder_text=valor_padrao, **entry_kwargs)
        self.entry.pack(side="top", fill="x", pady=(0, 10))

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def set(self, valor):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(valor))

    def get(self):
        return self.entry.get().strip()

    def get_float(self, nome_campo):
        texto = self.get()
        if texto == "":
            raise ValueError(f"O campo '{nome_campo}' não pode estar vazio.")
        try:
            return float(texto.replace(",", "."))
        except ValueError:
            raise ValueError(f"O campo '{nome_campo}' deve ser numérico. Valor: '{texto}'")

    def get_int(self, nome_campo):
        texto = self.get()
        if texto == "":
            raise ValueError(f"O campo '{nome_campo}' não pode estar vazio.")
        try:
            return int(float(texto))
        except ValueError:
            raise ValueError(f"O campo '{nome_campo}' deve ser inteiro. Valor: '{texto}'")


class CartaoSecao(ctk.CTkFrame):
    def __init__(self, parent, titulo, **kwargs):
        estilo = theme.estilo_painel()
        estilo.update(kwargs)
        super().__init__(parent, **estilo)
        if titulo:
            ctk.CTkLabel(self, text=titulo, font=theme.FONT_SECAO,
                         text_color=theme.COR_TEXTO).pack(anchor="w", padx=16, pady=(14, 6))

    def corpo(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=16, pady=(0, 14))
        return frame


class BadgeStatus(ctk.CTkLabel):
    def __init__(self, parent, texto="", cor=None):
        cor = cor or theme.COR_TEXTO_SECUNDARIO
        super().__init__(parent, text=texto, font=theme.FONT_LABEL_ITALICO, text_color=cor)


def tabela_pontos_editavel(parent, n_inicial=3, colunas=("x", "y")):
    linhas = []
    frame = ctk.CTkFrame(parent, fg_color="transparent")

    cab = ctk.CTkFrame(frame, fg_color="transparent")
    cab.pack(fill="x")
    for c in colunas:
        ctk.CTkLabel(cab, text=c, font=theme.FONT_LABEL, width=90,
                     text_color=theme.COR_TEXTO_SECUNDARIO).pack(side="left", padx=3)

    corpo = ctk.CTkFrame(frame, fg_color="transparent")
    corpo.pack(fill="x")

    def adicionar_linha():
        linha_frame = ctk.CTkFrame(corpo, fg_color="transparent")
        linha_frame.pack(fill="x", pady=2)
        entradas = []
        for _ in colunas:
            e = ctk.CTkEntry(linha_frame, width=90, **{k: v for k, v in theme.estilo_entry().items() if k != "height"})
            e.pack(side="left", padx=3)
            entradas.append(e)
        linhas.append(entradas)
        return entradas

    for _ in range(n_inicial):
        adicionar_linha()

    return frame, linhas, adicionar_linha