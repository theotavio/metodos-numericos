import customtkinter as ctk

COR_FUNDO = "#0f1117"
COR_PAINEL = "#171a23"
COR_PAINEL_CLARO = "#1e222d"
COR_ACENTO = "#5b8cff"
COR_ACENTO_HOVER = "#4470e0"
COR_SUCESSO = "#33c37f"
COR_SUCESSO_HOVER = "#28a06a"
COR_ERRO = "#ff5c5c"
COR_AVISO = "#e8b84b"
COR_TEXTO = "#e6e8f0"
COR_TEXTO_SECUNDARIO = "#9aa0b4"
COR_BORDA = "#2a2f3d"

FONTE_BASE = "Segoe UI"
FONTE_MONO = "Cascadia Mono"

FONT_TITULO_APP = (FONTE_BASE, 24, "bold")
FONT_SUBTITULO_APP = (FONTE_BASE, 13)
FONT_TITULO_ABA = (FONTE_BASE, 18, "bold")
FONT_SECAO = (FONTE_BASE, 13, "bold")
FONT_LABEL = (FONTE_BASE, 12)
FONT_LABEL_ITALICO = (FONTE_BASE, 11, "italic")
FONT_BOTAO = (FONTE_BASE, 13, "bold")
FONT_SAIDA = (FONTE_MONO, 12)


def aplicar_tema():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")


def estilo_botao_primario():
    return {
        "fg_color": COR_ACENTO,
        "hover_color": COR_ACENTO_HOVER,
        "font": FONT_BOTAO,
        "corner_radius": 8,
        "height": 40,
    }


def estilo_botao_executar():
    return {
        "fg_color": COR_SUCESSO,
        "hover_color": COR_SUCESSO_HOVER,
        "font": FONT_BOTAO,
        "corner_radius": 8,
        "height": 42,
        "text_color": "#04140c",
    }


def estilo_botao_secundario():
    return {
        "fg_color": "transparent",
        "hover_color": COR_PAINEL_CLARO,
        "border_width": 1,
        "border_color": COR_BORDA,
        "font": FONT_LABEL,
        "corner_radius": 8,
        "height": 34,
        "text_color": COR_TEXTO_SECUNDARIO,
    }


def estilo_painel():
    return {
        "fg_color": COR_PAINEL,
        "corner_radius": 12,
        "border_width": 1,
        "border_color": COR_BORDA,
    }


def estilo_entry():
    return {
        "fg_color": COR_PAINEL_CLARO,
        "border_color": COR_BORDA,
        "corner_radius": 6,
        "height": 34,
    }