"""
Janela Principal da Aplicação de Métodos Numéricos Computacionais (PySide6 / Qt 6).
Navegação lateral moderna por módulos com símbolos matemáticos, tema Light como padrão com alternador para Dark,
janela espaçosa e atalhos de teclado ágeis.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QStackedWidget, QFrame, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from gui import theme
from gui.tabs.raizes_tab import RaizesTab
from gui.tabs.sistemas_tab import SistemasTab
from gui.tabs.interpolacao_tab import InterpolacaoTab
from gui.tabs.ajuste_tab import AjusteTab
from gui.tabs.integracao_tab import IntegracaoTab
from gui.tabs.edo_tab import EdoTab


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurações da Janela (Espaçosa e responsiva)
        self.setWindowTitle("Métodos Numéricos Computacionais")
        self.resize(1500, 920)
        self.setMinimumSize(1150, 720)
        
        # Modo Claro como padrão
        self.current_theme_mode = "light"
        theme.set_theme("light")
        self.nav_buttons = []
        
        self._init_ui()
        self._aplicar_estilo()
        self._setup_atalhos()

    def _init_ui(self):
        # Widget Central
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ==========================================
        # SIDEBAR DE NAVEGAÇÃO
        # ==========================================
        self.sidebar = QFrame()
        self.sidebar.setProperty("sidebar", True)
        self.sidebar.setFixedWidth(280)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(16, 22, 16, 18)
        sidebar_layout.setSpacing(6)

        # Logotipo & Título
        header_frame = QWidget()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(6, 0, 6, 14)
        header_layout.setSpacing(3)

        lbl_app_logo = QLabel("∑  Métodos Numéricos")
        lbl_app_logo.setStyleSheet("font-size: 17px; font-weight: 800; letter-spacing: -0.3px;")
        header_layout.addWidget(lbl_app_logo)

        lbl_app_sub = QLabel("Cálculo Numérico & Algoritmos")
        lbl_app_sub.setStyleSheet("font-size: 11px; color: #64748b; font-weight: 500;")
        header_layout.addWidget(lbl_app_sub)

        sidebar_layout.addWidget(header_frame)

        # Separador Superior
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: rgba(125, 125, 125, 0.15); max-height: 1px; margin-bottom: 8px;")
        sidebar_layout.addWidget(sep)

        # Seção de Módulos
        lbl_modulos = QLabel("MÓDULOS DE CÁLCULO")
        lbl_modulos.setStyleSheet("font-size: 10px; font-weight: 700; color: #94a3b8; padding-left: 8px; margin-bottom: 4px;")
        sidebar_layout.addWidget(lbl_modulos)

        # Botões de Navegação com Fórmulas e Símbolos
        items = [
            ("🔍  Raízes  [ f(x) = 0 ]", 0),
            ("🧮  Sistemas  [ Ax = b ]", 1),
            ("📈  Interpolação  [ P(x) ]", 2),
            ("📉  Ajuste  [ ŷ = a₀+a₁x ]", 3),
            ("∫   Integração  [ ∫f(x)dx ]", 4),
            ("🌀  EDOs  [ dy/dt = f(t,y) ]", 5),
        ]

        for text, index in items:
            btn = QPushButton(text)
            btn.setProperty("sidebarBtn", True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked=False, idx=index: self._navegar_para(idx))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        # Separador Inferior
        sep_bottom = QFrame()
        sep_bottom.setFrameShape(QFrame.HLine)
        sep_bottom.setStyleSheet("background-color: rgba(125, 125, 125, 0.15); max-height: 1px; margin-bottom: 8px;")
        sidebar_layout.addWidget(sep_bottom)

        # Botão de Alternância de Tema
        self.btn_tema = QPushButton("🌙  Modo Escuro")
        self.btn_tema.setProperty("variant", "ghost")
        self.btn_tema.setCursor(Qt.PointingHandCursor)
        self.btn_tema.clicked.connect(self._alternar_tema)
        sidebar_layout.addWidget(self.btn_tema)

        lbl_version = QLabel("v2.0 • PySide6 / Qt 6")
        lbl_version.setAlignment(Qt.AlignCenter)
        lbl_version.setStyleSheet("font-size: 10px; color: #94a3b8; margin-top: 4px;")
        sidebar_layout.addWidget(lbl_version)

        main_layout.addWidget(self.sidebar)

        # ==========================================
        # ÁREA DE CONTEÚDO PRINCIPAL (STACKED WIDGET)
        # ==========================================
        self.stack = QStackedWidget()
        
        self.tab_raizes = RaizesTab(self)
        self.tab_sistemas = SistemasTab(self)
        self.tab_interpolacao = InterpolacaoTab(self)
        self.tab_ajuste = AjusteTab(self)
        self.tab_integracao = IntegracaoTab(self)
        self.tab_edo = EdoTab(self)

        self.stack.addWidget(self.tab_raizes)
        self.stack.addWidget(self.tab_sistemas)
        self.stack.addWidget(self.tab_interpolacao)
        self.stack.addWidget(self.tab_ajuste)
        self.stack.addWidget(self.tab_integracao)
        self.stack.addWidget(self.tab_edo)

        main_layout.addWidget(self.stack, 1)

        # Inicia na primeira aba
        self._navegar_para(0)

    def _navegar_para(self, index):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _alternar_tema(self):
        if self.current_theme_mode == "light":
            self.current_theme_mode = "dark"
            theme.set_theme("dark")
            self.btn_tema.setText("☀️  Modo Claro")
        else:
            self.current_theme_mode = "light"
            theme.set_theme("light")
            self.btn_tema.setText("🌙  Modo Escuro")

        self._aplicar_estilo()

        # Atualiza o tema de todos os canvases de gráfico
        for tab in [self.tab_raizes, self.tab_sistemas, self.tab_interpolacao,
                    self.tab_ajuste, self.tab_integracao, self.tab_edo]:
            tab.plot_canvas.apply_theme()
            if tab.ultimo_resultado and tab.ultimo_resultado.get("sucesso"):
                tab._renderizar_grafico(tab.ultimo_resultado)
            else:
                tab.plot_canvas.clear()

    def _aplicar_estilo(self):
        qss = theme.get_stylesheet()
        QApplication.instance().setStyleSheet(qss)

    def _setup_atalhos(self):
        # Atalhos Ctrl+1 até Ctrl+6 para alternar módulos
        for idx in range(6):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{idx+1}"), self)
            shortcut.activated.connect(lambda i=idx: self._navegar_para(i))

        # Atalho Ctrl+T para alternar tema
        shortcut_theme = QShortcut(QKeySequence("Ctrl+T"), self)
        shortcut_theme.activated.connect(self._alternar_tema)

        # Atalho F5 ou Ctrl+Enter para executar cálculo na aba atual
        shortcut_run1 = QShortcut(QKeySequence("F5"), self)
        shortcut_run1.activated.connect(self._executar_aba_atual)
        shortcut_run2 = QShortcut(QKeySequence("Ctrl+Return"), self)
        shortcut_run2.activated.connect(self._executar_aba_atual)

    def _executar_aba_atual(self):
        current_tab = self.stack.currentWidget()
        if hasattr(current_tab, "_on_executar"):
            current_tab._on_executar()