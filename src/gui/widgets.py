"""
Componentes visuais reutilizáveis para a interface gráfica moderna (PySide6).
Inclui cards, badges, campos de entrada modernos, métricas, tabelas editáveis e visualizadores.
"""

import csv
from PySide6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog, QApplication, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor, QClipboard
from gui import theme


class ModernCard(QFrame):
    """Card elevado com estilo moderno, cantos arredondados e suporte a cabeçalho."""
    def __init__(self, parent=None, title=None, subtitle=None):
        super().__init__(parent)
        self.setProperty("card", True)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(18, 18, 18, 18)
        self.main_layout.setSpacing(12)
        
        if title:
            header_layout = QVBoxLayout()
            header_layout.setSpacing(2)
            
            self.title_label = QLabel(title)
            self.title_label.setProperty("variant", "section")
            header_layout.addWidget(self.title_label)
            
            if subtitle:
                self.sub_label = QLabel(subtitle)
                self.sub_label.setProperty("variant", "caption")
                header_layout.addWidget(self.sub_label)
            
            self.main_layout.addLayout(header_layout)

    def add_widget(self, widget):
        self.main_layout.addWidget(widget)

    def add_layout(self, layout):
        self.main_layout.addLayout(layout)


class ModernInput(QWidget):
    """Campo de entrada com rótulo moderno, placeholder e validações integradas."""
    def __init__(self, label_text, default_value="", placeholder="", tooltip="", parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        self.label = QLabel(label_text)
        self.label.setStyleSheet("font-size: 12px; font-weight: 500;")
        layout.addWidget(self.label)
        
        self.entry = QLineEdit()
        self.entry.setText(str(default_value))
        self.entry.setPlaceholderText(placeholder or str(default_value))
        if tooltip:
            self.entry.setToolTip(tooltip)
            self.label.setToolTip(tooltip)
        
        layout.addWidget(self.entry)

    def set(self, valor):
        self.entry.setText(str(valor))

    def get(self):
        return self.entry.text().strip()

    def get_float(self, nome_campo=None):
        nome = nome_campo or self.label.text()
        texto = self.get()
        if not texto:
            raise ValueError(f"O campo '{nome}' não pode estar vazio.")
        try:
            return float(texto.replace(",", "."))
        except ValueError:
            try:
                import sympy as sp
                expr = sp.sympify(texto.replace(",", "."), locals={"pi": sp.pi, "e": sp.E, "E": sp.E})
                return float(expr.evalf())
            except Exception:
                raise ValueError(f"O campo '{nome}' deve ser um número válido. Recebido: '{texto}'")

    def get_int(self, nome_campo=None):
        nome = nome_campo or self.label.text()
        texto = self.get()
        if not texto:
            raise ValueError(f"O campo '{nome}' não pode estar vazio.")
        try:
            return int(float(texto))
        except ValueError:
            raise ValueError(f"O campo '{nome}' deve ser um número inteiro. Recebido: '{texto}'")


class StatusBadge(QFrame):
    """Badge em formato pílula com indicador colorido de status."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                border-radius: 12px;
                padding: 3px 10px;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 3, 8, 3)
        layout.setSpacing(6)
        
        self.label = QLabel("Pronto")
        self.label.setStyleSheet("font-size: 11px; font-weight: 600;")
        layout.addWidget(self.label)
        self.set_ready()

    def set_ready(self, msg="Pronto"):
        t = theme.get_current_theme()
        self.setStyleSheet(f"background-color: {t['primary_subtle']}; border: 1px solid {t['border']}; border-radius: 10px;")
        self.label.setText(f"● {msg}")
        self.label.setStyleSheet(f"color: {t['text_secondary']}; font-size: 11px; font-weight: 600;")

    def set_running(self, msg="Calculando..."):
        t = theme.get_current_theme()
        self.setStyleSheet(f"background-color: {t['primary_subtle']}; border: 1px solid {t['primary']}; border-radius: 10px;")
        self.label.setText(f"⚙ {msg}")
        self.label.setStyleSheet(f"color: {t['primary']}; font-size: 11px; font-weight: 600;")

    def set_success(self, msg="Sucesso"):
        t = theme.get_current_theme()
        self.setStyleSheet(f"background-color: {t['success_subtle']}; border: 1px solid {t['success']}; border-radius: 10px;")
        self.label.setText(f"✔ {msg}")
        self.label.setStyleSheet(f"color: {t['success']}; font-size: 11px; font-weight: 600;")

    def set_error(self, msg="Erro"):
        t = theme.get_current_theme()
        self.setStyleSheet(f"background-color: {t['danger_subtle']}; border: 1px solid {t['danger']}; border-radius: 10px;")
        self.label.setText(f"✖ {msg}")
        self.label.setStyleSheet(f"color: {t['danger']}; font-size: 11px; font-weight: 600;")


class MetricCard(QFrame):
    """Card de destaque de métrica (KPI) com título, valor proeminente e subtítulo."""
    def __init__(self, title, value="—", subtitle="", parent=None):
        super().__init__(parent)
        self.setProperty("card", True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setProperty("variant", "caption")
        layout.addWidget(self.title_lbl)
        
        self.value_lbl = QLabel(str(value))
        self.value_lbl.setStyleSheet("font-size: 18px; font-weight: 700; font-family: 'Cascadia Code', monospace;")
        layout.addWidget(self.value_lbl)
        
        if subtitle:
            self.sub_lbl = QLabel(subtitle)
            self.sub_lbl.setProperty("variant", "caption")
            layout.addWidget(self.sub_lbl)

    def set_value(self, value):
        self.value_lbl.setText(str(value))


class ModernTable(QTableWidget):
    """Tabela estilizada com suporte a cópia para área de transferência e exportação CSV."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)

    def populate_from_history(self, history_lines):
        """Popula a tabela automaticamente a partir das linhas de histórico do core."""
        self.clear()
        self.setRowCount(0)
        self.setColumnCount(0)
        
        if not history_lines:
            return

        # Procura a linha de cabeçalho tabular com múltiplos separadores '|'
        header_idx = -1
        for i, line in enumerate(history_lines):
            partes = [p.strip() for p in line.split("|")]
            if len(partes) >= 3 and any(keyword in line for keyword in ["Iter", "x_n", "x_i", "xm", "k1", "t_i", "Erro"]):
                header_idx = i
                break

        if header_idx != -1:
            # Tabela de Iterações Clássica
            raw_headers = [h.strip() for h in history_lines[header_idx].split("|")]
            headers = [h if h else f"Col {idx+1}" for idx, h in enumerate(raw_headers)]
            self.setColumnCount(len(headers))
            self.setHorizontalHeaderLabels(headers)

            rows_data = []
            for line in history_lines[header_idx + 1:]:
                if "|" in line:
                    cells = [c.strip() for c in line.split("|")]
                    if len(cells) == len(headers):
                        rows_data.append(cells)

            self.setRowCount(len(rows_data))
            for r, row in enumerate(rows_data):
                for c, val in enumerate(row):
                    item = QTableWidgetItem(val)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                    self.setItem(r, c, item)
            self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.horizontalHeader().setStretchLastSection(True)
        else:
            # Passo a Passo Estruturado (ex: Eliminação de Gauss, Interpolação, Ajuste)
            self.setColumnCount(2)
            self.setHorizontalHeaderLabels(["Passo", "Operação Realizada / Estado da Matriz"])
            
            # Filtra linhas vazias ou puramente de divisão
            linhas_validas = [l for l in history_lines if l.strip() and not l.strip().startswith("---")]
            self.setRowCount(len(linhas_validas))
            for r, linha in enumerate(linhas_validas):
                item_passo = QTableWidgetItem(f"#{r+1:02d}")
                item_passo.setTextAlignment(Qt.AlignCenter)
                item_passo.setFlags(item_passo.flags() ^ Qt.ItemIsEditable)
                self.setItem(r, 0, item_passo)

                item_conteudo = QTableWidgetItem(linha)
                item_conteudo.setFlags(item_conteudo.flags() ^ Qt.ItemIsEditable)
                self.setItem(r, 1, item_conteudo)
                
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def export_to_csv(self, parent_window=None):
        """Exporta os dados da tabela para arquivo CSV."""
        if self.rowCount() == 0:
            return False
            
        path, _ = QFileDialog.getSaveFileName(
            parent_window, "Exportar Dados para CSV", "resultado_iteracoes.csv", "Arquivos CSV (*.csv)"
        )
        if not path:
            return False
            
        with open(path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            headers = [self.horizontalHeaderItem(c).text() for c in range(self.columnCount())]
            writer.writerow(headers)
            for r in range(self.rowCount()):
                row = []
                for c in range(self.columnCount()):
                    item = self.item(r, c)
                    row.append(item.text() if item else "")
                writer.writerow(row)
        return True

    def copy_to_clipboard(self):
        """Copia conteúdo selecionado ou toda a tabela formatada."""
        linhas = []
        headers = [self.horizontalHeaderItem(c).text() for c in range(self.columnCount())]
        linhas.append("\t".join(headers))
        for r in range(self.rowCount()):
            row = []
            for c in range(self.columnCount()):
                item = self.item(r, c)
                row.append(item.text() if item else "")
            linhas.append("\t".join(row))
            
        texto = "\n".join(linhas)
        QApplication.clipboard().setText(texto)
        return True


class DynamicPointsWidget(QWidget):
    """Widget para edição dinâmica de listas de pontos (x, y)."""
    points_changed = Signal()

    def __init__(self, default_points=None, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        btn_bar = QHBoxLayout()
        btn_bar.setSpacing(6)
        
        self.btn_add = QPushButton("+ Adicionar Ponto")
        self.btn_add.setProperty("variant", "ghost")
        self.btn_add.clicked.connect(self.add_row)
        btn_bar.addWidget(self.btn_add)
        
        self.btn_remove = QPushButton("– Remover")
        self.btn_remove.setProperty("variant", "ghost")
        self.btn_remove.clicked.connect(self.remove_row)
        btn_bar.addWidget(self.btn_remove)
        
        self.btn_clear = QPushButton("Limpar")
        self.btn_clear.setProperty("variant", "ghost")
        self.btn_clear.clicked.connect(self.clear_table)
        btn_bar.addWidget(self.btn_clear)
        
        layout.addLayout(btn_bar)
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["x", "y = f(x)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(True)
        self.table.setMaximumHeight(180)
        layout.addWidget(self.table)

        if default_points:
            self.set_points(default_points)
        else:
            for _ in range(3):
                self.add_row()

    def add_row(self, x="", y=""):
        row = self.table.rowCount()
        self.table.insertRow(row)
        item_x = QTableWidgetItem(str(x))
        item_y = QTableWidgetItem(str(y))
        item_x.setTextAlignment(Qt.AlignCenter)
        item_y.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 0, item_x)
        self.table.setItem(row, 1, item_y)
        self.points_changed.emit()

    def remove_row(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)
        elif self.table.rowCount() > 0:
            self.table.removeRow(self.table.rowCount() - 1)
        self.points_changed.emit()

    def clear_table(self):
        self.table.setRowCount(0)
        self.points_changed.emit()

    def set_points(self, points):
        self.table.setRowCount(0)
        for p in points:
            self.add_row(p[0], p[1])

    def get_points(self):
        points = []
        for r in range(self.table.rowCount()):
            item_x = self.table.item(r, 0)
            item_y = self.table.item(r, 1)
            tx = item_x.text().strip() if item_x else ""
            ty = item_y.text().strip() if item_y else ""
            if not tx or not ty:
                raise ValueError(f"Ponto na linha {r+1} está incompleto.")
            try:
                points.append((float(tx.replace(",", ".")), float(ty.replace(",", "."))))
            except ValueError:
                raise ValueError(f"Valores inválidos no ponto da linha {r+1} ('{tx}', '{ty}').")
        if not points:
            raise ValueError("A tabela de pontos está vazia. Adicione ao menos 2 pontos.")
        return points