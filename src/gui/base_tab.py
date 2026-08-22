"""
Classe base para todas as abas de métodos numéricos (PySide6).
Oferece layout moderno em duas colunas, seletor de métodos, carregador de presets,
área de resultados focada (Gráfico Interativo, Tabela de Iterações e Resumo & Métricas)
e janelas flutuantes informativas de erro.
"""

import time
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QLabel,
    QComboBox, QPushButton, QTabWidget, QScrollArea,
    QFrame, QApplication, QMessageBox, QSizePolicy
)
from PySide6.QtCore import Qt
from gui import theme
from gui.widgets import ModernCard, StatusBadge, MetricCard, ModernTable
from gui.plots import ModernPlotCanvas


class AbaBase(QWidget):
    def __init__(self, titulo, subtitulo="", parent=None):
        super().__init__(parent)
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.campos_atuais = {}
        self.ultimo_resultado = None
        self.metodos_disponiveis = {}
        self.exemplos_disponiveis = {}

    def setup_ui(self):
        """Monta o layout da aba após a subclasse definir seus métodos e exemplos."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(14)

        # Cabeçalho da Aba
        cabecalho = QVBoxLayout()
        cabecalho.setSpacing(3)
        
        lbl_titulo = QLabel(self.titulo)
        lbl_titulo.setProperty("variant", "title")
        cabecalho.addWidget(lbl_titulo)
        
        if self.subtitulo:
            lbl_sub = QLabel(self.subtitulo)
            lbl_sub.setProperty("variant", "subtitle")
            cabecalho.addWidget(lbl_sub)
            
        main_layout.addLayout(cabecalho)

        # Splitter Principal (Painel Esquerdo: Formulário | Painel Direito: Resultados)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        main_layout.addWidget(self.splitter, 1)

        # ==========================================
        # PAINEL ESQUERDO: CONTROLES E FORMULÁRIO
        # ==========================================
        self.left_scroll = QScrollArea()
        self.left_scroll.setWidgetResizable(True)
        self.left_scroll.setFrameShape(QFrame.NoFrame)
        self.left_scroll.setMinimumWidth(330)
        self.left_scroll.setMaximumWidth(450)
        
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 8, 0)
        left_layout.setSpacing(12)

        # Card de Configuração do Método
        card_config = ModernCard(title="Configuração do Método")
        
        lbl_metodo = QLabel("Algoritmo de Resolução:")
        lbl_metodo.setStyleSheet("font-size: 12px; font-weight: 500;")
        card_config.add_widget(lbl_metodo)
        
        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(list(self.metodos_disponiveis.keys()))
        self.combo_metodo.currentTextChanged.connect(self._on_metodo_alterado)
        card_config.add_widget(self.combo_metodo)

        if self.exemplos_disponiveis:
            lbl_exemplo = QLabel("Exemplo Pré-configurado:")
            lbl_exemplo.setStyleSheet("font-size: 12px; font-weight: 500; margin-top: 6px;")
            card_config.add_widget(lbl_exemplo)
            
            self.combo_exemplos = QComboBox()
            self.combo_exemplos.addItem("— Selecione um Exemplo —")
            self.combo_exemplos.addItems(list(self.exemplos_disponiveis.keys()))
            self.combo_exemplos.currentTextChanged.connect(self._on_exemplo_selecionado)
            card_config.add_widget(self.combo_exemplos)

        left_layout.addWidget(card_config)

        # Card de Parâmetros Dinâmicos
        self.card_params = ModernCard(title="Parâmetros de Entrada")
        self.frame_formulario = QWidget()
        self.layout_formulario = QVBoxLayout(self.frame_formulario)
        self.layout_formulario.setContentsMargins(0, 0, 0, 0)
        self.layout_formulario.setSpacing(10)
        self.card_params.add_widget(self.frame_formulario)
        left_layout.addWidget(self.card_params)

        # Ações (Executar e Limpar)
        actions_card = ModernCard()
        
        self.btn_executar = QPushButton("▶  Executar Cálculo")
        self.btn_executar.setProperty("variant", "success")
        self.btn_executar.setMinimumHeight(44)
        self.btn_executar.clicked.connect(self._on_executar)
        actions_card.add_widget(self.btn_executar)

        self.btn_limpar = QPushButton("↺  Limpar Dados")
        self.btn_limpar.setProperty("variant", "ghost")
        self.btn_limpar.clicked.connect(self._limpar_saida)
        actions_card.add_widget(self.btn_limpar)

        left_layout.addWidget(actions_card)
        left_layout.addStretch()
        
        self.left_scroll.setWidget(left_container)
        self.splitter.addWidget(self.left_scroll)

        # ==========================================
        # PAINEL DIREITO: RESULTADOS & VISUALIZAÇÕES
        # ==========================================
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(8, 0, 0, 0)
        right_layout.setSpacing(10)

        # Barra Superior de Status & Ações de Exportação
        top_bar = QHBoxLayout()
        
        self.badge_status = StatusBadge()
        top_bar.addWidget(self.badge_status)
        
        self.lbl_tempo = QLabel("")
        self.lbl_tempo.setProperty("variant", "caption")
        top_bar.addWidget(self.lbl_tempo)
        
        top_bar.addStretch()

        self.btn_copiar = QPushButton("📋 Copiar Resumo")
        self.btn_copiar.setProperty("variant", "ghost")
        self.btn_copiar.clicked.connect(self._copiar_resultado)
        top_bar.addWidget(self.btn_copiar)

        self.btn_export_csv = QPushButton("📊 Exportar CSV")
        self.btn_export_csv.setProperty("variant", "ghost")
        self.btn_export_csv.clicked.connect(self._exportar_csv)
        top_bar.addWidget(self.btn_export_csv)

        self.btn_export_plot = QPushButton("💾 Salvar Gráfico")
        self.btn_export_plot.setProperty("variant", "ghost")
        self.btn_export_plot.clicked.connect(self._salvar_grafico)
        top_bar.addWidget(self.btn_export_plot)

        right_layout.addLayout(top_bar)

        # Abas de Visualização (Gráfico, Tabela de Iterações e Resumo)
        self.tabs_resultado = QTabWidget()
        
        # Aba 1: Gráfico Interativo
        self.plot_canvas = ModernPlotCanvas(self)
        self.tabs_resultado.addTab(self.plot_canvas, "📊 Gráfico Interativo")

        # Aba 2: Tabela de Iterações
        self.table_iteracoes = ModernTable(self)
        self.tabs_resultado.addTab(self.table_iteracoes, "📋 Tabela de Iterações")

        # Aba 3: Resumo & Métricas
        self.widget_resumo = QWidget()
        self.layout_resumo = QVBoxLayout(self.widget_resumo)
        self.layout_resumo.setContentsMargins(20, 20, 20, 20)
        self.layout_resumo.setSpacing(16)
        
        self.lbl_resumo_titulo = QLabel("Nenhum cálculo realizado ainda.")
        self.lbl_resumo_titulo.setProperty("variant", "section")
        self.layout_resumo.addWidget(self.lbl_resumo_titulo)

        self.lbl_resumo_detalhes = QLabel("Selecione os parâmetros e clique em 'Executar Cálculo' para visualizar os resultados.")
        self.lbl_resumo_detalhes.setStyleSheet("font-size: 13px; color: #64748b; line-height: 1.5;")
        self.lbl_resumo_detalhes.setWordWrap(True)
        self.layout_resumo.addWidget(self.lbl_resumo_detalhes)
        
        self.layout_kpis = QHBoxLayout()
        self.layout_kpis.setSpacing(12)
        self.layout_resumo.addLayout(self.layout_kpis)
        self.layout_resumo.addStretch()
        
        self.tabs_resultado.addTab(self.widget_resumo, "💡 Resumo & Métricas")

        right_layout.addWidget(self.tabs_resultado, 1)
        self.splitter.addWidget(right_container)

        # Configura proporções do splitter (33% esquerda, 67% direita)
        self.splitter.setSizes([380, 800])

        if self.combo_metodo.count() > 0:
            self._on_metodo_alterado(self.combo_metodo.currentText())

    def _limpar_formulario(self):
        while self.layout_formulario.count():
            item = self.layout_formulario.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.campos_atuais = {}

    def _on_metodo_alterado(self, nome_exibido):
        if not nome_exibido or nome_exibido not in self.metodos_disponiveis:
            return
        self._limpar_formulario()
        nome_metodo = self.metodos_disponiveis[nome_exibido]
        self.campos_atuais = self._montar_formulario(nome_metodo)

    def _on_exemplo_selecionado(self, nome_exemplo):
        if not nome_exemplo or nome_exemplo not in self.exemplos_disponiveis:
            return
        exemplo = self.exemplos_disponiveis[nome_exemplo]
        if "metodo" in exemplo and exemplo["metodo"] in self.metodos_disponiveis:
            self.combo_metodo.setCurrentText(exemplo["metodo"])
        self._carregar_exemplo(exemplo)

    def _limpar_saida(self):
        self.table_iteracoes.clear()
        self.table_iteracoes.setRowCount(0)
        self.table_iteracoes.setColumnCount(0)
        self.plot_canvas.clear()
        self.badge_status.set_ready("Pronto")
        self.lbl_tempo.setText("")
        self.lbl_resumo_titulo.setText("Nenhum cálculo realizado ainda.")
        self.lbl_resumo_detalhes.setText("Selecione os parâmetros e clique em 'Executar Cálculo' para visualizar os resultados.")
        self._limpar_kpis()

    def _limpar_kpis(self):
        while self.layout_kpis.count():
            item = self.layout_kpis.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _mostrar_dialogo_erro(self, titulo, mensagem):
        """Apresenta uma janela flutuante moderna com a mensagem de erro."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(f"<b>{titulo}</b>")
        msg_box.setInformativeText(mensagem)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.button(QMessageBox.Ok).setText("Entendido")
        msg_box.exec()

    def _copiar_resultado(self):
        tab_idx = self.tabs_resultado.currentIndex()
        if tab_idx == 1:
            self.table_iteracoes.copy_to_clipboard()
            self.badge_status.set_ready("Tabela Copiada!")
        else:
            if self.ultimo_resultado and self.ultimo_resultado.get("sucesso"):
                res_str = self._formatar_resultado_final(self.ultimo_resultado)
                QApplication.clipboard().setText(res_str)
                self.badge_status.set_ready("Resumo Copiado!")
            else:
                QApplication.clipboard().setText(self.lbl_resumo_titulo.text())

    def _exportar_csv(self):
        if self.table_iteracoes.rowCount() > 0:
            if self.table_iteracoes.export_to_csv(self):
                self.badge_status.set_success("CSV Exportado!")
        else:
            QMessageBox.information(self, "Exportar Dados", "Não há registros na tabela de iterações para exportar.")

    def _salvar_grafico(self):
        if self.plot_canvas.save_plot(self):
            self.badge_status.set_success("Gráfico Salvo!")

    def _exibir_resultado(self, resultado_dict, cabecalho="", tempo_ms=0.0):
        self.ultimo_resultado = resultado_dict
        self.lbl_tempo.setText(f"Tempo: {tempo_ms:.2f} ms")

        historico = resultado_dict.get("historico", [])
        if historico:
            self.table_iteracoes.populate_from_history(historico)

        if resultado_dict.get("sucesso"):
            self.badge_status.set_success("Concluído com Sucesso")
            res_str = self._formatar_resultado_final(resultado_dict)
            self.lbl_resumo_titulo.setText("Cálculo Finalizado com Sucesso")
            self.lbl_resumo_detalhes.setText(res_str)
            self._atualizar_kpis(resultado_dict)
            self._renderizar_grafico(resultado_dict)
        else:
            self.badge_status.set_error("Falha no Cálculo")
            erro_msg = resultado_dict.get("erro", "Erro desconhecido durante o cálculo.")
            self.lbl_resumo_titulo.setText(f"Erro: {erro_msg}")
            self.lbl_resumo_detalhes.setText("O método não convergiu ou encontrou uma inconsistência matemática.")
            self._limpar_kpis()
            self.plot_canvas.clear()
            # Exibe janela flutuante de erro
            self._mostrar_dialogo_erro("Falha no Cálculo Numérico", erro_msg)

    def _on_executar(self):
        nome_exibido = self.combo_metodo.currentText()
        if nome_exibido not in self.metodos_disponiveis:
            return
        nome_metodo = self.metodos_disponiveis[nome_exibido]
        
        self.badge_status.set_running("Calculando...")
        QApplication.processEvents()

        t_start = time.perf_counter()
        try:
            resultado = self._executar(nome_metodo, self.campos_atuais)
            tempo_ms = (time.perf_counter() - t_start) * 1000.0
            self._exibir_resultado(resultado, cabecalho=f"Método: {nome_exibido}", tempo_ms=tempo_ms)
        except ValueError as ve:
            self._limpar_saida()
            self.badge_status.set_error("Erro de Entrada")
            self.lbl_resumo_titulo.setText(f"Erro de Validação: {ve}")
            self._mostrar_dialogo_erro("Erro nos Dados de Entrada", str(ve))
        except ZeroDivisionError as zde:
            self._limpar_saida()
            self.badge_status.set_error("Divisão por Zero")
            self.lbl_resumo_titulo.setText("Divisão por zero detectada.")
            self._mostrar_dialogo_erro("Divisão por Zero", f"Ocorreu uma divisão por zero durante o cálculo:\n{zde}")
        except Exception as exc:
            self._limpar_saida()
            self.badge_status.set_error("Erro Inesperado")
            self.lbl_resumo_titulo.setText(f"Erro: {exc}")
            self._mostrar_dialogo_erro("Erro Inesperado", f"{type(exc).__name__}:\n{exc}")

    # ==========================================
    # MÉTODOS A SEREM SOBRESCRITOS PELAS ABAS
    # ==========================================
    def _montar_formulario(self, nome_metodo):
        raise NotImplementedError

    def _executar(self, nome_metodo, campos):
        raise NotImplementedError

    def _formatar_resultado_final(self, resultado_dict):
        return str(resultado_dict.get("resultado"))

    def _carregar_exemplo(self, exemplo_dict):
        pass

    def _atualizar_kpis(self, resultado_dict):
        self._limpar_kpis()
        res = resultado_dict.get("resultado")
        if res is not None and isinstance(res, (int, float)):
            self.layout_kpis.addWidget(MetricCard("Valor Calculado", f"{res:.8f}"))
        if "iteracoes" in resultado_dict:
            self.layout_kpis.addWidget(MetricCard("Iterações", str(resultado_dict["iteracoes"])))

    def _renderizar_grafico(self, resultado_dict):
        pass