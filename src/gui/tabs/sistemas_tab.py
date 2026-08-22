"""
Aba de Sistemas Lineares (PySide6).
Implementa Eliminação de Gauss e Gauss-Seidel com editor dinâmico de matrizes espaçoso e nítido,
tabela de escalonamento / iterações e gráficos interativos sem sobreposição.
"""

import numpy as np
from PySide6.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox
)
from PySide6.QtCore import Qt
from gui.base_tab import AbaBase
from gui.widgets import ModernInput, MetricCard
from gui import theme
from core import sistemas_lineares


class SistemasTab(AbaBase):
    def __init__(self, parent=None):
        super().__init__(
            titulo="🧮 Sistemas Lineares — [ Ax = b ]",
            subtitulo="Resolução direta e iterativa de sistemas de equações algébricas lineares Ax = b",
            parent=parent
        )
        self.metodos_disponiveis = {
            "Eliminação de Gauss [ Direto ]": "gauss",
            "Gauss-Seidel [ Iterativo ]": "gauss_seidel",
        }
        self.exemplos_disponiveis = {
            "Sistema 2×2: Interseção de Retas (2x₁ + x₂ = 7)": {
                "n": 2, "A": [[2, 1], [1, -1]], "b": [7, 2], "metodo": "Eliminação de Gauss [ Direto ]"
            },
            "Sistema 3×3: Eliminação de Gauss Clássica": {
                "n": 3, "A": [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], "b": [8, -11, -3], "metodo": "Eliminação de Gauss [ Direto ]"
            },
            "Sistema 3×3: Gauss-Seidel Dominante": {
                "n": 3, "A": [[10, 2, 1], [1, 10, -1], [2, -2, 10]], "b": [14, 11, 26], "tol": "1e-6", "max_iter": "100", "metodo": "Gauss-Seidel [ Iterativo ]"
            },
            "Sistema 4×4: Engenharia de Estruturas": {
                "n": 4, "A": [[4, -1, 0, 0], [-1, 4, -1, 0], [0, -1, 4, -1], [0, 0, -1, 3]], "b": [10, 10, 10, 10], "metodo": "Eliminação de Gauss [ Direto ]"
            },
        }
        self.ordem_atual = 3
        self.grid_entries_A = []
        self.grid_entries_b = []
        self.setup_ui()

    def _montar_formulario(self, nome_metodo):
        campos = {}

        # Controle de Dimensão da Matriz
        row_dim = QHBoxLayout()
        campos["ordem"] = ModernInput("Ordem da Matriz (n)", str(self.ordem_atual), tooltip="Número de equações e incógnitas n×n")
        row_dim.addWidget(campos["ordem"])
        
        btn_gerar = QPushButton("Redimensionar")
        btn_gerar.setProperty("variant", "primary")
        btn_gerar.clicked.connect(lambda: self._redimensionar_matriz(campos["ordem"].get_int("Ordem")))
        row_dim.addWidget(btn_gerar, alignment=Qt.AlignBottom)
        self.layout_formulario.addLayout(row_dim)

        # Botões de ferramentas de matriz
        tools_row = QHBoxLayout()
        tools_row.setSpacing(6)
        
        btn_id = QPushButton("Identidade")
        btn_id.setProperty("variant", "ghost")
        btn_id.clicked.connect(self._preencher_identidade)
        tools_row.addWidget(btn_id)

        btn_clear = QPushButton("Zerar")
        btn_clear.setProperty("variant", "ghost")
        btn_clear.clicked.connect(self._zerar_matriz)
        tools_row.addWidget(btn_clear)

        self.layout_formulario.addLayout(tools_row)

        # Container da Grade de Entradas de Matriz
        self.frame_matriz = QWidget()
        self.layout_grid_matriz = QGridLayout(self.frame_matriz)
        self.layout_grid_matriz.setContentsMargins(0, 8, 0, 8)
        self.layout_grid_matriz.setSpacing(6)
        self.layout_formulario.addWidget(self.frame_matriz)

        if nome_metodo == "gauss_seidel":
            campos["tol"] = ModernInput("Tolerância (tol)", "1e-6", tooltip="Critério de convergência ||e|| < tol")
            campos["max_iter"] = ModernInput("Máx. Iterações", "100", tooltip="Limite de iterações")
            self.layout_formulario.addWidget(campos["tol"])
            self.layout_formulario.addWidget(campos["max_iter"])

        self._gerar_grade(self.ordem_atual)
        return campos

    def _redimensionar_matriz(self, n):
        if n < 2 or n > 8:
            raise ValueError("A ordem da matriz deve estar entre 2 e 8.")
        self.ordem_atual = n
        self._gerar_grade(n)

    def _gerar_grade(self, n):
        while self.layout_grid_matriz.count():
            item = self.layout_grid_matriz.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.grid_entries_A = []
        self.grid_entries_b = []
        t = theme.get_current_theme()

        # Rótulos de Cabeçalho
        for j in range(n):
            lbl = QLabel(f"x{j+1}")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #64748b;")
            self.layout_grid_matriz.addWidget(lbl, 0, j)
            
        lbl_div = QLabel("┃")
        lbl_div.setAlignment(Qt.AlignCenter)
        lbl_div.setStyleSheet(f"color: {t['border_light']}; font-size: 13px; font-weight: bold;")
        self.layout_grid_matriz.addWidget(lbl_div, 0, n)
        
        lbl_b = QLabel("b")
        lbl_b.setAlignment(Qt.AlignCenter)
        lbl_b.setStyleSheet("font-size: 12px; font-weight: 700; color: #2563eb;")
        self.layout_grid_matriz.addWidget(lbl_b, 0, n + 1)

        # Campos de Matriz A e Vetor b com dimensões confortáveis
        for i in range(n):
            linha_A = []
            for j in range(n):
                e = QLineEdit()
                e.setAlignment(Qt.AlignCenter)
                e.setPlaceholderText("0")
                e.setMinimumWidth(54)
                e.setMinimumHeight(32)
                e.setStyleSheet("font-size: 12px; font-weight: 500;")
                e.setText("1" if i == j else "0")
                self.layout_grid_matriz.addWidget(e, i + 1, j)
                linha_A.append(e)
            self.grid_entries_A.append(linha_A)

            div = QLabel("┃")
            div.setAlignment(Qt.AlignCenter)
            div.setStyleSheet(f"color: {t['border_light']}; font-size: 13px; font-weight: bold;")
            self.layout_grid_matriz.addWidget(div, i + 1, n)

            eb = QLineEdit()
            eb.setAlignment(Qt.AlignCenter)
            eb.setPlaceholderText("0")
            eb.setMinimumWidth(56)
            eb.setMinimumHeight(32)
            eb.setStyleSheet("font-size: 12px; font-weight: 600;")
            eb.setText("1")
            self.layout_grid_matriz.addWidget(eb, i + 1, n + 1)
            self.grid_entries_b.append(eb)

    def _preencher_identidade(self):
        for i in range(self.ordem_atual):
            for j in range(self.ordem_atual):
                self.grid_entries_A[i][j].setText("1" if i == j else "0")
            self.grid_entries_b[i].setText("1")

    def _zerar_matriz(self):
        for i in range(self.ordem_atual):
            for j in range(self.ordem_atual):
                self.grid_entries_A[i][j].setText("0")
            self.grid_entries_b[i].setText("0")

    def _carregar_exemplo(self, ex):
        n = ex["n"]
        if "ordem" in self.campos_atuais:
            self.campos_atuais["ordem"].set(str(n))
        self._redimensionar_matriz(n)
        
        for i in range(n):
            for j in range(n):
                self.grid_entries_A[i][j].setText(str(ex["A"][i][j]))
            self.grid_entries_b[i].setText(str(ex["b"][i]))

        if "tol" in self.campos_atuais and "tol" in ex:
            self.campos_atuais["tol"].set(ex["tol"])
        if "max_iter" in self.campos_atuais and "max_iter" in ex:
            self.campos_atuais["max_iter"].set(ex["max_iter"])

    def _ler_matriz_e_vetor(self):
        n = self.ordem_atual
        A, b = [], []
        for i in range(n):
            linha = []
            for j in range(n):
                t = self.grid_entries_A[i][j].text().strip()
                if not t:
                    raise ValueError(f"O elemento A[{i+1},{j+1}] está vazio.")
                try:
                    linha.append(float(t.replace(",", ".")))
                except ValueError:
                    raise ValueError(f"Valor inválido em A[{i+1},{j+1}]: '{t}'")
            A.append(linha)

            tb = self.grid_entries_b[i].text().strip()
            if not tb:
                raise ValueError(f"O elemento b[{i+1}] está vazio.")
            try:
                b.append(float(tb.replace(",", ".")))
            except ValueError:
                raise ValueError(f"Valor inválido em b[{i+1}]: '{tb}'")
        return A, b

    def _executar(self, nome_metodo, campos):
        A, b = self._ler_matriz_e_vetor()
        self.last_A = A
        self.last_b = b

        if nome_metodo == "gauss":
            return sistemas_lineares.eliminacao_gauss(A, b)

        tol = campos["tol"].get_float("Tolerância")
        max_iter = campos["max_iter"].get_int("Máx. iterações")
        if tol <= 0:
            raise ValueError("A tolerância deve ser positiva.")
        if max_iter <= 0:
            raise ValueError("O máximo de iterações deve ser um inteiro positivo.")
        return sistemas_lineares.gauss_seidel(A, b, tol, max_iter)

    def _formatar_resultado_final(self, resultado_dict):
        sol = resultado_dict.get("resultado")
        if sol is None:
            return "Sem solução única encontrada."
        return "Vetor Solução x:\n  " + "\n  ".join(f"x_{i+1} = {val:.8f}" for i, val in enumerate(sol))

    def _atualizar_kpis(self, resultado_dict):
        self._limpar_kpis()
        sol = resultado_dict.get("resultado")
        if sol is not None:
            for i, val in enumerate(sol[:4]):
                self.layout_kpis.addWidget(MetricCard(f"Incógnita x_{i+1}", f"{val:.6f}"))
        if "iteracoes" in resultado_dict:
            self.layout_kpis.addWidget(MetricCard("Iterações (k)", str(resultado_dict["iteracoes"])))

    def _renderizar_grafico(self, resultado_dict):
        sol = resultado_dict.get("resultado")
        if sol is None:
            self.plot_canvas.clear()
            return

        nome_metodo = self.combo_metodo.currentText()
        
        # Extrai erros do histórico se houver (Gauss-Seidel)
        erros = []
        historico = resultado_dict.get("historico", [])
        for l in historico:
            if "|" in l and not any(k in l for k in ["Iter", "AVISO", "Matriz"]):
                partes = [p.strip() for p in l.split("|")]
                if len(partes) >= 2:
                    try:
                        erros.append(float(partes[-1]))
                    except ValueError:
                        pass

        self.plot_canvas.plot_sistemas_completo(
            A=self.last_A,
            b=self.last_b,
            sol=sol,
            erros=erros if erros else None,
            method_name=nome_metodo
        )