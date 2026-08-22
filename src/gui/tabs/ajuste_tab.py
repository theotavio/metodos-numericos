"""
Aba de Ajuste de Curvas e Regressão Linear (PySide6).
Implementa Regressão Linear Simples e Múltipla via Mínimos Quadrados com cálculo de R²,
gráfico de resíduos e plot de paridade (Real vs Previsto).
"""

import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from gui.base_tab import AbaBase
from gui.widgets import ModernInput, DynamicPointsWidget, MetricCard
from gui import theme
from core import ajuste_curvas


class AjusteTab(AbaBase):
    def __init__(self, parent=None):
        super().__init__(
            titulo="📉 Ajuste de Curvas — [ ŷ = a₀ + a₁x ]",
            subtitulo="Regressão linear simples e múltipla pelo Método dos Mínimos Quadrados com coeficiente R²",
            parent=parent
        )
        self.metodos_disponiveis = {
            "Ajuste Linear Simples [ ŷ = a₀ + a₁x ]": "simples",
            "Ajuste Linear Múltiplo [ ŷ = β₀ + ∑ βⱼxⱼ ]": "multiplo",
        }
        self.exemplos_disponiveis = {
            "Regressão Simples: Dados de Laboratório": {
                "metodo": "Ajuste Linear Simples [ ŷ = a₀ + a₁x ]",
                "pontos": [(1.0, 2.1), (2.0, 3.9), (3.0, 6.2), (4.0, 7.8), (5.0, 10.1)]
            },
            "Regressão Simples: Temperatura vs Resistência (Ohm)": {
                "metodo": "Ajuste Linear Simples [ ŷ = a₀ + a₁x ]",
                "pontos": [(20, 100.2), (30, 104.1), (40, 107.9), (50, 111.8), (60, 115.7)]
            },
            "Regressão Múltipla: 2 Variáveis Independentes": {
                "metodo": "Ajuste Linear Múltiplo [ ŷ = β₀ + ∑ βⱼxⱼ ]",
                "n_obs": 5, "n_vars": 2,
                "dados": [
                    [50, 1, 150],
                    [70, 2, 210],
                    [85, 3, 270],
                    [110, 3, 340],
                    [130, 4, 410]
                ]
            }
        }
        self.points_widget = None
        self.table_mult = None
        self.last_pontos_simples = []
        self.setup_ui()

    def _montar_formulario(self, nome_metodo):
        campos = {}

        if nome_metodo == "simples":
            lbl = QLabel("Tabela de Pontos Experimentais (xᵢ, yᵢ):")
            lbl.setStyleSheet("font-size: 12px; font-weight: 500;")
            self.layout_formulario.addWidget(lbl)

            padrao = [(1.0, 2.1), (2.0, 3.9), (3.0, 6.2), (4.0, 7.8), (5.0, 10.1)]
            self.points_widget = DynamicPointsWidget(default_points=padrao)
            self.layout_formulario.addWidget(self.points_widget)
        else:
            row_cfg = QHBoxLayout()
            campos["n_obs"] = ModernInput("Nº de Observações (n)", "5", tooltip="Linhas de dados observados")
            campos["n_vars"] = ModernInput("Nº de Variáveis (k)", "2", tooltip="Colunas independentes x1, x2, ...")
            row_cfg.addWidget(campos["n_obs"])
            row_cfg.addWidget(campos["n_vars"])
            self.layout_formulario.addLayout(row_cfg)

            btn_gerar = QPushButton("Gerar Grade de Observações")
            btn_gerar.setProperty("variant", "primary")
            btn_gerar.clicked.connect(lambda: self._gerar_tabela_multipla(
                campos["n_obs"].get_int("Nº de Observações"),
                campos["n_vars"].get_int("Nº de Variáveis")
            ))
            self.layout_formulario.addWidget(btn_gerar)

            self.table_mult = QTableWidget()
            self.table_mult.setMaximumHeight(200)
            self.layout_formulario.addWidget(self.table_mult)
            self._gerar_tabela_multipla(5, 2)

        return campos

    def _gerar_tabela_multipla(self, n_obs, n_vars):
        if n_obs < 3 or n_obs > 50 or n_vars < 1 or n_vars > 10:
            raise ValueError("Observações entre 3 e 50, e variáveis entre 1 e 10.")
        if n_obs <= n_vars:
            raise ValueError(f"O número de observações ({n_obs}) deve ser maior que o número de variáveis ({n_vars}).")

        self.table_mult.clear()
        self.table_mult.setRowCount(n_obs)
        self.table_mult.setColumnCount(n_vars + 1)
        headers = [f"x{j+1}" for j in range(n_vars)] + ["y (alvo)"]
        self.table_mult.setHorizontalHeaderLabels(headers)
        self.table_mult.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i in range(n_obs):
            for j in range(n_vars):
                item = QTableWidgetItem(str((i + 1) * (j + 1)))
                item.setTextAlignment(Qt.AlignCenter)
                self.table_mult.setItem(i, j, item)
            item_y = QTableWidgetItem(str((i + 1) * 3 + 2))
            item_y.setTextAlignment(Qt.AlignCenter)
            self.table_mult.setItem(i, n_vars, item_y)

    def _carregar_exemplo(self, ex):
        if self.combo_metodo.currentText() == "Ajuste Linear Simples [ ŷ = a₀ + a₁x ]":
            if self.points_widget and "pontos" in ex:
                self.points_widget.set_points(ex["pontos"])
        else:
            if "n_obs" in ex and "n_vars" in ex and "dados" in ex:
                n_obs = ex["n_obs"]
                n_vars = ex["n_vars"]
                if "n_obs" in self.campos_atuais:
                    self.campos_atuais["n_obs"].set(str(n_obs))
                if "n_vars" in self.campos_atuais:
                    self.campos_atuais["n_vars"].set(str(n_vars))
                self._gerar_tabela_multipla(n_obs, n_vars)
                
                dados = ex["dados"]
                for i in range(min(n_obs, len(dados))):
                    for j in range(n_vars + 1):
                        self.table_mult.item(i, j).setText(str(dados[i][j]))

    def _ler_dados_multiplos(self):
        n_obs = self.table_mult.rowCount()
        n_cols = self.table_mult.columnCount()
        n_vars = n_cols - 1

        X, y = [], []
        for i in range(n_obs):
            linha_x = []
            for j in range(n_vars):
                item = self.table_mult.item(i, j)
                t = item.text().strip() if item else ""
                if not t:
                    raise ValueError(f"Célula x{j+1} na observação {i+1} está vazia.")
                try:
                    linha_x.append(float(t.replace(",", ".")))
                except ValueError:
                    raise ValueError(f"Valor inválido em x{j+1}, observação {i+1}: '{t}'")
            X.append(linha_x)

            item_y = self.table_mult.item(i, n_vars)
            ty = item_y.text().strip() if item_y else ""
            if not ty:
                raise ValueError(f"Célula y na observação {i+1} está vazia.")
            try:
                y.append(float(ty.replace(",", ".")))
            except ValueError:
                raise ValueError(f"Valor inválido em y, observação {i+1}: '{ty}'")

        return np.array(X, dtype=float), np.array(y, dtype=float)

    def _executar(self, nome_metodo, campos):
        if nome_metodo == "simples":
            pontos = self.points_widget.get_points()
            self.last_pontos_simples = pontos
            return ajuste_curvas.ajuste_linear_simples(pontos)
        else:
            X, y = self._ler_dados_multiplos()
            self.last_X = X
            self.last_y = y
            return ajuste_curvas.ajuste_linear_multiplo(X, y)

    def _formatar_resultado_final(self, resultado_dict):
        r = resultado_dict.get("resultado", {})
        if "a0" in r:
            sinal = "+" if r["a1"] >= 0 else "-"
            return f"Equação da Reta de Regressão:\n  ŷ = {r['a0']:.6f} {sinal} {abs(r['a1']):.6f}·x\n\nQualidade do Ajuste:\n  R² = {r['r2']:.6f} ({r['r2']*100:.2f}% da variância explicada)"
        
        coefs = r.get("coeficientes", [])
        linhas = ["Equação do Modelo Multivariável:", f"  ŷ = {coefs[0]:.6f}"]
        for i, c in enumerate(coefs[1:], start=1):
            sinal = "+" if c >= 0 else "-"
            linhas.append(f"      {sinal} {abs(c):.6f}·x{i}")
        linhas.append(f"\nQualidade do Ajuste:\n  R² = {r.get('r2', 0):.6f} ({r.get('r2', 0)*100:.2f}%)")
        return "\n".join(linhas)

    def _atualizar_kpis(self, resultado_dict):
        self._limpar_kpis()
        r = resultado_dict.get("resultado", {})
        if "r2" in r:
            self.layout_kpis.addWidget(MetricCard("Coeficiente R²", f"{r['r2']:.4f}", subtitle=f"{r['r2']*100:.1f}% explicado"))
        if "a0" in r:
            self.layout_kpis.addWidget(MetricCard("Intercepto (a₀)", f"{r['a0']:.4f}"))
            self.layout_kpis.addWidget(MetricCard("Inclinação (a₁)", f"{r['a1']:.4f}"))

    def _renderizar_grafico(self, resultado_dict):
        r = resultado_dict.get("resultado", {})
        if not r:
            self.plot_canvas.clear()
            return

        if self.combo_metodo.currentText() == "Ajuste Linear Simples [ ŷ = a₀ + a₁x ]":
            self.plot_canvas.plot_ajuste_simples(
                pontos=self.last_pontos_simples,
                a0=r["a0"],
                a1=r["a1"],
                r2=r["r2"]
            )
        else:
            coefs = np.array(r["coeficientes"])
            Xb = np.hstack([np.ones((self.last_X.shape[0], 1)), self.last_X])
            y_pred = Xb @ coefs
            self.plot_canvas.plot_ajuste_multiplo(
                y_true=self.last_y,
                y_pred=y_pred,
                r2=r["r2"]
            )