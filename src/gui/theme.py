"""
Tema moderno e estilização completa para a aplicação de Métodos Numéricos (PySide6 / Qt 6).
Suporta temas Light (padrão) e Dark com design moderno estilo Fluent / Apple / Material.
Elimina completamente bordas brancas indesejadas no modo escuro e garante legibilidade perfeita.
"""

from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt

# ==========================================
# PALETAS DE CORES
# ==========================================

LIGHT_THEME = {
    "name": "light",
    "bg_main": "#f8fafc",
    "bg_sidebar": "#f1f5f9",
    "bg_card": "#ffffff",
    "bg_card_alt": "#f8fafc",
    "bg_card_hover": "#f1f5f9",
    "bg_input": "#f1f5f9",
    "bg_input_focus": "#ffffff",
    "border": "#e2e8f0",
    "border_light": "#cbd5e1",
    
    # Cores de Acento e Status
    "primary": "#2563eb",
    "primary_hover": "#1d4ed8",
    "primary_pressed": "#1e40af",
    "primary_subtle": "rgba(37, 99, 235, 0.12)",
    
    "success": "#059669",
    "success_hover": "#047857",
    "success_subtle": "rgba(5, 150, 105, 0.12)",
    
    "warning": "#d97706",
    "warning_hover": "#b45309",
    "warning_subtle": "rgba(217, 119, 6, 0.12)",
    
    "danger": "#dc2626",
    "danger_hover": "#b91c1c",
    "danger_subtle": "rgba(220, 38, 38, 0.12)",
    
    "info": "#0891b2",
    "purple": "#7c3aed",
    
    # Tipografia
    "text_primary": "#0f172a",
    "text_secondary": "#475569",
    "text_muted": "#94a3b8",
    "text_on_primary": "#ffffff",
    
    # Gráficos (Matplotlib)
    "plot_bg": "#ffffff",
    "plot_fig_bg": "#ffffff",
    "plot_text": "#0f172a",
    "plot_grid": "#e2e8f0",
    "plot_accent": "#0284c7",
    "plot_accent_sec": "#e11d48",
    "plot_accent_ter": "#059669",
    "plot_accent_qua": "#d97706",
}

DARK_THEME = {
    "name": "dark",
    "bg_main": "#0b0f17",
    "bg_sidebar": "#111622",
    "bg_card": "#161d2b",
    "bg_card_alt": "#1a2233",
    "bg_card_hover": "#1f293d",
    "bg_input": "#1a2233",
    "bg_input_focus": "#222c42",
    "border": "#253047",
    "border_light": "#32405d",
    
    # Cores de Acento e Status
    "primary": "#3b82f6",
    "primary_hover": "#2563eb",
    "primary_pressed": "#1d4ed8",
    "primary_subtle": "rgba(59, 130, 246, 0.22)",
    
    "success": "#10b981",
    "success_hover": "#059669",
    "success_subtle": "rgba(16, 185, 129, 0.22)",
    
    "warning": "#f59e0b",
    "warning_hover": "#d97706",
    "warning_subtle": "rgba(245, 158, 11, 0.22)",
    
    "danger": "#ef4444",
    "danger_hover": "#dc2626",
    "danger_subtle": "rgba(239, 68, 68, 0.22)",
    
    "info": "#06b6d4",
    "purple": "#8b5cf6",
    
    # Tipografia
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",
    "text_on_primary": "#ffffff",
    
    # Gráficos (Matplotlib)
    "plot_bg": "#111622",
    "plot_fig_bg": "#161d2b",
    "plot_text": "#f1f5f9",
    "plot_grid": "#253047",
    "plot_accent": "#38bdf8",
    "plot_accent_sec": "#f43f5e",
    "plot_accent_ter": "#10b981",
    "plot_accent_qua": "#fbbf24",
}

# Estado global de tema atual (Padrão: LIGHT_THEME)
_CURRENT_THEME = LIGHT_THEME


def get_current_theme():
    return _CURRENT_THEME


def set_theme(mode="light"):
    global _CURRENT_THEME
    if mode == "dark":
        _CURRENT_THEME = DARK_THEME
    else:
        _CURRENT_THEME = LIGHT_THEME
    return _CURRENT_THEME


def get_stylesheet(theme=None):
    """Gera o QSS completo de acordo com o tema selecionado com zero bordas brancas parasitas."""
    t = theme or _CURRENT_THEME
    
    return f"""
    /* ====================================================================
       ESTILO GLOBAL
       ==================================================================== */
    * {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        color: {t["text_primary"]};
        outline: none;
    }}

    QMainWindow, QDialog, QMessageBox, QWidget#CentralWidget {{
        background-color: {t["bg_main"]};
        color: {t["text_primary"]};
    }}

    /* Remove bordas residuais de frames e scrollareas */
    QFrame {{
        border: none;
        background-color: transparent;
    }}

    QScrollArea {{
        background-color: transparent;
        border: none;
    }}
    QScrollArea > QWidget > QWidget {{
        background-color: transparent;
        border: none;
    }}
    QAbstractScrollArea {{
        background-color: transparent;
        border: none;
    }}

    /* Tooltip */
    QToolTip {{
        background-color: {t["bg_card"]};
        color: {t["text_primary"]};
        border: 1px solid {t["border"]};
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 12px;
    }}

    /* Scrollbars Modernas */
    QScrollBar:vertical {{
        background-color: transparent;
        width: 8px;
        margin: 0px;
    }}
    QScrollBar::handle:vertical {{
        background-color: {t["border"]};
        min-height: 24px;
        border-radius: 4px;
        margin: 2px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: {t["border_light"]};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
    }}

    QScrollBar:horizontal {{
        background-color: transparent;
        height: 8px;
        margin: 0px;
    }}
    QScrollBar::handle:horizontal {{
        background-color: {t["border"]};
        min-width: 24px;
        border-radius: 4px;
        margin: 2px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background-color: {t["border_light"]};
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* ====================================================================
       CARDS & CONTAINERS
       ==================================================================== */
    QFrame[card="true"] {{
        background-color: {t["bg_card"]};
        border: 1px solid {t["border"]};
        border-radius: 12px;
    }}

    QFrame[sidebar="true"] {{
        background-color: {t["bg_sidebar"]};
        border-right: 1px solid {t["border"]};
    }}

    QFrame[header="true"] {{
        background-color: {t["bg_card"]};
        border-bottom: 1px solid {t["border"]};
    }}

    /* ====================================================================
       BOTÕES
       ==================================================================== */
    QPushButton {{
        background-color: {t["bg_input"]};
        color: {t["text_primary"]};
        border: 1px solid {t["border"]};
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton:hover {{
        background-color: {t["bg_card_hover"]};
        border-color: {t["border_light"]};
    }}
    QPushButton:pressed {{
        background-color: {t["border"]};
    }}
    QPushButton:disabled {{
        background-color: {t["bg_input"]};
        color: {t["text_muted"]};
        border-color: {t["border"]};
    }}

    /* Botão Primário */
    QPushButton[variant="primary"] {{
        background-color: {t["primary"]};
        color: {t["text_on_primary"]};
        border: 1px solid {t["primary"]};
        font-weight: 600;
    }}
    QPushButton[variant="primary"]:hover {{
        background-color: {t["primary_hover"]};
        border-color: {t["primary_hover"]};
    }}
    QPushButton[variant="primary"]:pressed {{
        background-color: {t["primary_pressed"]};
    }}

    /* Botão Sucesso / Executar */
    QPushButton[variant="success"] {{
        background-color: {t["success"]};
        color: {t["text_on_primary"]};
        border: 1px solid {t["success"]};
        font-weight: 600;
    }}
    QPushButton[variant="success"]:hover {{
        background-color: {t["success_hover"]};
        border-color: {t["success_hover"]};
    }}

    /* Botão Secundário / Ghost */
    QPushButton[variant="ghost"] {{
        background-color: transparent;
        border: 1px solid transparent;
        color: {t["text_secondary"]};
    }}
    QPushButton[variant="ghost"]:hover {{
        background-color: {t["bg_input"]};
        color: {t["text_primary"]};
        border-color: {t["border"]};
    }}

    /* Botões da Sidebar de Navegação */
    QPushButton[sidebarBtn="true"] {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        color: {t["text_secondary"]};
        text-align: left;
        padding: 10px 14px;
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton[sidebarBtn="true"]:hover {{
        background-color: {t["bg_input"]};
        color: {t["text_primary"]};
    }}
    QPushButton[sidebarBtn="true"][active="true"] {{
        background-color: {t["primary_subtle"]};
        color: {t["primary"]};
        font-weight: 600;
        border-left: 3px solid {t["primary"]};
    }}

    /* ====================================================================
       CAMPOS DE TEXTO & ENTRADAS
       ==================================================================== */
    QLineEdit {{
        background-color: {t["bg_input"]};
        color: {t["text_primary"]};
        border: 1px solid {t["border"]};
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
        selection-background-color: {t["primary"]};
        selection-color: {t["text_on_primary"]};
    }}
    QLineEdit:focus {{
        background-color: {t["bg_input_focus"]};
        border: 1.5px solid {t["primary"]};
    }}
    QLineEdit:disabled {{
        background-color: {t["bg_main"]};
        color: {t["text_muted"]};
    }}

    /* Text Area / Log */
    QTextEdit, QPlainTextEdit {{
        background-color: {t["bg_card"]};
        color: {t["text_primary"]};
        border: 1px solid {t["border"]};
        border-radius: 8px;
        padding: 10px;
        font-family: "Cascadia Code", "Fira Code", "JetBrains Mono", Consolas, Menlo, monospace;
        font-size: 12px;
        line-height: 1.4;
        selection-background-color: {t["primary"]};
        selection-color: {t["text_on_primary"]};
    }}

    /* ====================================================================
       COMBO BOX
       ==================================================================== */
    QComboBox {{
        background-color: {t["bg_input"]};
        color: {t["text_primary"]};
        border: 1px solid {t["border"]};
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
        min-height: 20px;
    }}
    QComboBox:hover {{
        border-color: {t["border_light"]};
    }}
    QComboBox:focus {{
        border: 1.5px solid {t["primary"]};
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 28px;
        border-left: none;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid {t["text_secondary"]};
        margin-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {t["bg_card"]};
        color: {t["text_primary"]};
        border: 1px solid {t["border"]};
        border-radius: 8px;
        padding: 4px;
        selection-background-color: {t["primary_subtle"]};
        selection-color: {t["primary"]};
    }}

    /* ====================================================================
       TABELAS (QTableWidget)
       ==================================================================== */
    QTableWidget {{
        background-color: {t["bg_card"]};
        alternate-background-color: {t["bg_card_alt"]};
        color: {t["text_primary"]};
        border: 1px solid {t["border"]};
        border-radius: 8px;
        gridline-color: {t["border"]};
        font-size: 12px;
        font-family: "Cascadia Code", "Fira Code", "JetBrains Mono", Consolas, Menlo, monospace;
        selection-background-color: {t["primary_subtle"]};
        selection-color: {t["primary"]};
    }}
    QTableWidget::item {{
        color: {t["text_primary"]};
        padding: 6px 8px;
        border: none;
    }}
    QTableWidget::item:selected {{
        background-color: {t["primary_subtle"]};
        color: {t["primary"]};
        font-weight: bold;
    }}
    QHeaderView::section {{
        background-color: {t["bg_sidebar"]};
        color: {t["text_secondary"]};
        border: none;
        border-bottom: 1px solid {t["border"]};
        border-right: 1px solid {t["border"]};
        padding: 8px;
        font-weight: 600;
        font-size: 12px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    QHeaderView::section:hover {{
        background-color: {t["bg_input"]};
        color: {t["text_primary"]};
    }}
    QTableCornerButton::section {{
        background-color: {t["bg_sidebar"]};
        border: none;
    }}

    /* ====================================================================
       TAB WIDGET (Abas de Visualização)
       ==================================================================== */
    QTabWidget::pane {{
        border: 1px solid {t["border"]};
        border-radius: 8px;
        background-color: {t["bg_card"]};
        top: -1px;
    }}
    QTabBar::tab {{
        background-color: {t["bg_sidebar"]};
        color: {t["text_secondary"]};
        border: 1px solid {t["border"]};
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 9px 18px;
        margin-right: 4px;
        font-size: 13px;
        font-weight: 500;
    }}
    QTabBar::tab:hover {{
        background-color: {t["bg_input"]};
        color: {t["text_primary"]};
    }}
    QTabBar::tab:selected {{
        background-color: {t["bg_card"]};
        color: {t["primary"]};
        font-weight: 600;
        border-top: 2px solid {t["primary"]};
    }}

    /* ====================================================================
       BADGES & RÓTULOS
       ==================================================================== */
    QLabel {{
        background-color: transparent;
    }}
    QLabel[variant="title"] {{
        font-size: 20px;
        font-weight: 700;
        color: {t["text_primary"]};
    }}
    QLabel[variant="subtitle"] {{
        font-size: 13px;
        color: {t["text_secondary"]};
    }}
    QLabel[variant="section"] {{
        font-size: 14px;
        font-weight: 600;
        color: {t["text_primary"]};
    }}
    QLabel[variant="caption"] {{
        font-size: 11px;
        color: {t["text_muted"]};
    }}

    /* Splitter */
    QSplitter {{
        background: transparent;
    }}
    QSplitter::handle {{
        background-color: {t["border"]};
        margin: 2px;
        border-radius: 2px;
    }}
    QSplitter::handle:hover {{
        background-color: {t["primary"]};
    }}

    /* Diálogo de Erro / Mensagens */
    QMessageBox {{
        background-color: {t["bg_card"]};
        color: {t["text_primary"]};
    }}
    QMessageBox QLabel {{
        color: {t["text_primary"]};
        font-size: 13px;
    }}
    """