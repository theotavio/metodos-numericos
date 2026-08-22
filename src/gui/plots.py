"""
Módulo de visualização gráfica interativa integrado ao PySide6 via Matplotlib (Qt6Agg).
Interface 100% em português com botões de ação explícitos e visíveis em ambos os modos (Light e Dark).
Renderização limpa, nítida e sem sobreposição de textos.
"""

import numpy as np
import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QSizePolicy, QLabel, QFrame
)
from PySide6.QtCore import Qt
from gui import theme


class ModernPlotCanvas(QWidget):
    """Widget container com Matplotlib Figure e barra de ferramentas moderna com botões explícitos."""
    def __init__(self, parent=None, width=6, height=4.5, dpi=100):
        super().__init__(parent)
        
        self.grid_enabled = True
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)
        
        # Figura Matplotlib
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Barra nativa do matplotlib (invisível, usamos para delegar as ações de pan/zoom)
        self._mpl_toolbar = NavigationToolbar2QT(self.canvas, self)
        self._mpl_toolbar.setVisible(False)

        # Barra Superior de Controles do Gráfico com Botões Explícitos
        top_bar = QHBoxLayout()
        top_bar.setSpacing(6)

        self.btn_home = QPushButton("🏠 Início")
        self.btn_home.setProperty("variant", "ghost")
        self.btn_home.setToolTip("Restaura o enquadramento original da curva")
        self.btn_home.clicked.connect(self._mpl_toolbar.home)
        top_bar.addWidget(self.btn_home)

        self.btn_pan = QPushButton("✋ Mover")
        self.btn_pan.setProperty("variant", "ghost")
        self.btn_pan.setCheckable(True)
        self.btn_pan.setToolTip("Arrasta e move a visualização do gráfico")
        self.btn_pan.clicked.connect(self._toggle_pan)
        top_bar.addWidget(self.btn_pan)

        self.btn_zoom = QPushButton("🔍 Zoom")
        self.btn_zoom.setProperty("variant", "ghost")
        self.btn_zoom.setCheckable(True)
        self.btn_zoom.setToolTip("Aplica zoom na área retangular selecionada")
        self.btn_zoom.clicked.connect(self._toggle_zoom)
        top_bar.addWidget(self.btn_zoom)

        self.btn_toggle_grid = QPushButton("🔲 Grade")
        self.btn_toggle_grid.setProperty("variant", "ghost")
        self.btn_toggle_grid.setToolTip("Liga ou desliga as linhas de grade do gráfico")
        self.btn_toggle_grid.clicked.connect(self._toggle_grid)
        top_bar.addWidget(self.btn_toggle_grid)

        top_bar.addStretch()

        self.btn_save = QPushButton("💾 Salvar HD")
        self.btn_save.setProperty("variant", "ghost")
        self.btn_save.setToolTip("Salva a imagem do gráfico em alta resolução (PNG/SVG/PDF)")
        self.btn_save.clicked.connect(lambda: self.save_plot(self))
        top_bar.addWidget(self.btn_save)

        self.layout.addLayout(top_bar)
        self.layout.addWidget(self.canvas)
        
        self.apply_theme()
        self.clear()

    def _toggle_pan(self):
        if self.btn_zoom.isChecked():
            self.btn_zoom.setChecked(False)
        self._mpl_toolbar.pan()

    def _toggle_zoom(self):
        if self.btn_pan.isChecked():
            self.btn_pan.setChecked(False)
        self._mpl_toolbar.zoom()

    def _toggle_grid(self):
        """Alterna as linhas de grade de todos os eixos na figura."""
        self.grid_enabled = not self.grid_enabled
        for ax in self.fig.axes:
            if self.grid_enabled:
                ax.grid(True, linestyle="--", alpha=0.35, color=self.t["plot_grid"])
            else:
                ax.grid(False)
        self.canvas.draw_idle()

    def apply_theme(self):
        """Ajusta cores da figura para o tema atual (dark/light)."""
        t = theme.get_current_theme()
        self.fig.patch.set_facecolor(t["plot_fig_bg"])
        self.t = t

    def clear(self):
        """Limpa a figura e exibe uma mensagem neutra em português."""
        self.apply_theme()
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(self.t["plot_bg"])
        ax.text(
            0.5, 0.5, "Execute um método numérico para visualizar o gráfico interativo.",
            horizontalalignment="center", verticalalignment="center",
            transform=ax.transAxes, color=self.t["text_muted"], fontsize=12, fontweight="500"
        )
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(self.t["plot_grid"])
        self.canvas.draw_idle()

    def _setup_ax(self, ax, title="", xlabel="Eixo X", ylabel="Eixo Y"):
        t = self.t
        ax.set_facecolor(t["plot_bg"])
        ax.set_title(title, color=t["plot_text"], fontsize=12, fontweight="bold", pad=12)
        ax.set_xlabel(xlabel, color=t["text_secondary"], fontsize=10, labelpad=6)
        ax.set_ylabel(ylabel, color=t["text_secondary"], fontsize=10, labelpad=6)
        ax.tick_params(colors=t["text_secondary"], labelsize=9)
        if self.grid_enabled:
            ax.grid(True, linestyle="--", alpha=0.35, color=t["plot_grid"])
        else:
            ax.grid(False)
        for spine in ax.spines.values():
            spine.set_color(t["plot_grid"])

    def save_plot(self, parent_window=None):
        """Salva a figura atual em alta resolução com diálogo em português."""
        path, _ = QFileDialog.getSaveFileName(
            parent_window, "Salvar Gráfico em Alta Resolução", "grafico_metodo.png",
            "Imagens PNG (*.png);;Vetor SVG (*.svg);;Documento PDF (*.pdf)"
        )
        if path:
            self.fig.savefig(path, dpi=300, bbox_inches="tight", facecolor=self.fig.get_facecolor())
            return True
        return False

    # =========================================================================
    # GRÁFICOS ESPECÍFICOS POR MÉTODO (100% EM PORTUGUÊS & SEM BORRÕES)
    # =========================================================================

    def plot_raizes(self, f, a=None, b=None, root=None, x0=None, method_name="", phi=None):
        """Plota f(x), o eixo y=0, o intervalo inicial e a raiz encontrada."""
        self.apply_theme()
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        t = self.t

        pontos_ref = [p for p in [a, b, root, x0] if p is not None]
        if pontos_ref:
            min_x, max_x = min(pontos_ref), max(pontos_ref)
            delta = max((max_x - min_x) * 0.4, 1.5)
            x_start, x_end = min_x - delta, max_x + delta
        else:
            x_start, x_end = -5, 5

        xs = np.linspace(x_start, x_end, 500)
        try:
            ys = np.array([float(f(x)) for x in xs])
            ys = np.nan_to_num(ys, nan=0.0, posinf=1e4, neginf=-1e4)
            p95 = np.percentile(np.abs(ys), 95) if len(ys) > 0 else 10
            y_limit = max(p95 * 1.5, 5)
            ys = np.clip(ys, -y_limit, y_limit)
            
            ax.plot(xs, ys, label="Função f(x)", color=t["plot_accent"], linewidth=2.2)
        except Exception:
            pass

        # Linha zero de referência
        ax.axhline(0, color=t["text_muted"], linestyle="--", linewidth=1.2, alpha=0.7, label="Eixo f(x) = 0")

        # Intervalo inicial [a, b]
        if a is not None and b is not None:
            ax.axvspan(a, b, color=t["primary"], alpha=0.12, label=f"Intervalo inicial [{a:.2f}, {b:.2f}]")
            ax.axvline(a, color=t["primary"], linestyle=":", alpha=0.6)
            ax.axvline(b, color=t["primary"], linestyle=":", alpha=0.6)

        # Chute inicial
        if x0 is not None:
            try:
                ax.scatter([x0], [float(f(x0))], color=t["warning"], s=70, zorder=5, label=f"Chute inicial x₀ = {x0:.4f}")
            except Exception:
                pass

        # Raiz calculada com anotação visual
        if root is not None:
            try:
                fy = float(f(root))
                ax.scatter([root], [fy], color=t["plot_accent_ter"], s=110, zorder=6,
                           edgecolor=t["text_primary"], linewidth=1.5, label=f"Raiz calculada x* ≈ {root:.6f}")
                ax.annotate(
                    f"Raiz x* ≈ {root:.6f}\nResíduo = {fy:.2e}",
                    xy=(root, fy), xytext=(18, 18), textcoords="offset points",
                    color=t["text_primary"], fontsize=9, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.4", fc=t["bg_card"], ec=t["plot_accent_ter"], alpha=0.9),
                    arrowprops=dict(arrowstyle="->", color=t["plot_accent_ter"], lw=1.5)
                )
            except Exception:
                pass

        self._setup_ax(ax, title=f"Visualização da Raiz — {method_name}", xlabel="Variável Independente (x)", ylabel="Valor da Função f(x)")
        ax.legend(facecolor=t["bg_card"], edgecolor=t["border"], labelcolor=t["text_primary"], fontsize=9)
        self.fig.tight_layout()
        self.canvas.draw_idle()

    def plot_sistemas_completo(self, A, b, sol=None, erros=None, method_name=""):
        """Plota sistemas lineares com nitidez: 2D para sistemas 2x2, ou barras limpas e curva de convergência para n>=3."""
        self.apply_theme()
        self.fig.clear()
        t = self.t

        n = len(b)
        if n == 2 and sol is not None:
            # Gráfico de interseção 2D
            ax = self.fig.add_subplot(111)
            x_center = sol[0] if sol else 0
            xs = np.linspace(x_center - 8, x_center + 8, 200)

            cores = [t["plot_accent"], t["plot_accent_sec"]]
            for i in range(2):
                a1, a2 = A[i][0], A[i][1]
                bi = b[i]
                if abs(a2) > 1e-9:
                    ys = (bi - a1 * xs) / a2
                    ax.plot(xs, ys, label=f"Equação {i+1}: {a1:.2f}x₁ + {a2:.2f}x₂ = {bi:.2f}", color=cores[i], lw=2.2)
                else:
                    ax.axvline(bi / a1, label=f"Equação {i+1}: x₁ = {bi/a1:.2f}", color=cores[i], lw=2.2)

            ax.scatter([sol[0]], [sol[1]], color=t["plot_accent_ter"], s=120, zorder=6,
                       edgecolor=t["text_primary"], linewidth=1.5, label=f"Solução: ({sol[0]:.4f}, {sol[1]:.4f})")
            ax.annotate(
                f"Solução x:\nx₁ = {sol[0]:.4f}\nx₂ = {sol[1]:.4f}",
                xy=(sol[0], sol[1]), xytext=(18, 18), textcoords="offset points",
                color=t["text_primary"], fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.4", fc=t["bg_card"], ec=t["plot_accent_ter"], alpha=0.9),
                arrowprops=dict(arrowstyle="->", color=t["plot_accent_ter"], lw=1.5)
            )

            self._setup_ax(ax, title="Interseção Geométrica das Equações (Sistema 2×2)", xlabel="Incógnita x₁", ylabel="Incógnita x₂")
            ax.legend(facecolor=t["bg_card"], edgecolor=t["border"], labelcolor=t["text_primary"], fontsize=9)
        else:
            # Gráficos n >= 3
            if erros and len(erros) > 1:
                # Gauss-Seidel: Subplot 1 (Erro Logarítmico) | Subplot 2 (Solução em Barras)
                ax1 = self.fig.add_subplot(121)
                iters = list(range(1, len(erros) + 1))
                ax1.semilogy(iters, erros, marker="o", color=t["plot_accent"], linewidth=2.2, markersize=5.5, label="Erro ||e||∞")
                self._setup_ax(ax1, title="Convergência das Iterações", xlabel="Iteração (k)", ylabel="Erro Logarítmico")
                ax1.legend(facecolor=t["bg_card"], edgecolor=t["border"], labelcolor=t["text_primary"], fontsize=9)

                ax2 = self.fig.add_subplot(122)
                nomes_x = [f"x{i+1}" for i in range(len(sol))]
                cores_barras = [t["plot_accent_ter"] if s >= 0 else t["plot_accent_sec"] for s in sol]
                barras = ax2.bar(nomes_x, sol, color=cores_barras, edgecolor=t["border"], width=0.5)
                ax2.axhline(0, color=t["text_muted"], linestyle="--", alpha=0.7)
                
                # Ajusta limites do eixo Y com folga para os rótulos não cortarem
                max_y = max(np.max(sol), 0)
                min_y = min(np.min(sol), 0)
                range_y = max(max_y - min_y, 1.0)
                ax2.set_ylim(min_y - 0.25 * range_y, max_y + 0.25 * range_y)

                for bar, val in zip(barras, sol):
                    offset = 0.05 * range_y if val >= 0 else -0.08 * range_y
                    va = 'bottom' if val >= 0 else 'top'
                    ax2.text(bar.get_x() + bar.get_width()/2, val + offset, f"{val:.4f}",
                             ha='center', va=va, color=t["text_primary"], fontsize=9, fontweight='bold')
                
                self._setup_ax(ax2, title="Vetor Solução x", xlabel="Incógnitas", ylabel="Valor de xᵢ")
            else:
                # Eliminação de Gauss: Gráfico de Barras Amplo e Nítido
                ax = self.fig.add_subplot(111)
                nomes_x = [f"Incógnita x{i+1}" for i in range(len(sol))]
                cores_barras = [t["primary"] if s >= 0 else t["plot_accent_sec"] for s in sol]
                barras = ax.bar(nomes_x, sol, color=cores_barras, edgecolor=t["border"], width=0.45)
                ax.axhline(0, color=t["text_muted"], linestyle="--", alpha=0.7)
                
                max_y = max(np.max(sol), 0)
                min_y = min(np.min(sol), 0)
                range_y = max(max_y - min_y, 1.0)
                ax.set_ylim(min_y - 0.25 * range_y, max_y + 0.25 * range_y)

                for bar, val in zip(barras, sol):
                    offset = 0.05 * range_y if val >= 0 else -0.08 * range_y
                    va = 'bottom' if val >= 0 else 'top'
                    ax.text(bar.get_x() + bar.get_width()/2, val + offset, f"x = {val:.6f}",
                            ha='center', va=va, color=t["text_primary"], fontsize=10, fontweight='bold',
                            bbox=dict(boxstyle="round,pad=0.2", fc=t["bg_card"], ec=t["border"], alpha=0.85))
                
                self._setup_ax(ax, title=f"Vetor Solução Encontrado — {method_name}", xlabel="Incógnitas do Sistema", ylabel="Valor Calculado")

        self.fig.tight_layout()
        self.canvas.draw_idle()

    def plot_interpolacao(self, pontos, x_alvo, y_alvo, poly_coeffs=None, method_name=""):
        """Plota os pontos dados, o polinômio contínuo e a estimativa interpolada."""
        self.apply_theme()
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        t = self.t

        xs = [p[0] for p in pontos]
        ys = [p[1] for p in pontos]
        
        min_x, max_x = min(xs + [x_alvo]), max(xs + [x_alvo])
        delta = max((max_x - min_x) * 0.15, 0.5)
        x_dense = np.linspace(min_x - delta, max_x + delta, 300)

        try:
            poly = np.poly1d(np.polyfit(xs, ys, len(xs) - 1))
            y_dense = poly(x_dense)
            ax.plot(x_dense, y_dense, label="Polinômio Interpolador P(x)", color=t["plot_accent"], linewidth=2.2)
        except Exception:
            pass

        # Pontos conhecidos
        ax.scatter(xs, ys, color=t["plot_accent_sec"], s=80, zorder=5, edgecolor=t["text_primary"],
                   linewidth=1.2, label=f"Pontos Conhecidos (N={len(pontos)})")

        # Ponto alvo calculado
        ax.scatter([x_alvo], [y_alvo], color=t["plot_accent_ter"], s=120, zorder=6,
                   edgecolor=t["text_primary"], linewidth=1.5, label=f"Valor Interpolado: P({x_alvo:.3f}) = {y_alvo:.4f}")

        # Guias pontilhadas
        ax.axvline(x_alvo, color=t["plot_accent_ter"], linestyle=":", alpha=0.7)
        ax.axhline(y_alvo, color=t["plot_accent_ter"], linestyle=":", alpha=0.7)

        ax.annotate(
            f"P({x_alvo:.4f}) ≈ {y_alvo:.6f}",
            xy=(x_alvo, y_alvo), xytext=(18, 18), textcoords="offset points",
            color=t["text_primary"], fontsize=9, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc=t["bg_card"], ec=t["plot_accent_ter"], alpha=0.9),
            arrowprops=dict(arrowstyle="->", color=t["plot_accent_ter"], lw=1.5)
        )

        self._setup_ax(ax, title=f"Polinômio Interpolador — {method_name}", xlabel="x", ylabel="P(x)")
        ax.legend(facecolor=t["bg_card"], edgecolor=t["border"], labelcolor=t["text_primary"], fontsize=9)
        self.fig.tight_layout()
        self.canvas.draw_idle()

    def plot_ajuste_simples(self, pontos, a0, a1, r2):
        """Plota os pontos experimentais, a reta de regressão e os segmentos de resíduos."""
        self.apply_theme()
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        t = self.t

        xs = np.array([p[0] for p in pontos], dtype=float)
        ys = np.array([p[1] for p in pontos], dtype=float)

        min_x, max_x = np.min(xs), np.max(xs)
        delta = max((max_x - min_x) * 0.15, 1.0)
        x_line = np.linspace(min_x - delta, max_x + delta, 200)
        y_line = a0 + a1 * x_line

        sinal = "+" if a1 >= 0 else "-"
        eq_str = f"Reta: y = {a0:.4f} {sinal} {abs(a1):.4f}x (R² = {r2:.4f})"
        ax.plot(x_line, y_line, label=eq_str, color=t["plot_accent"], linewidth=2.4)

        # Segmentos de resíduos
        y_pred = a0 + a1 * xs
        for i, (xi, yi, ypi) in enumerate(zip(xs, ys, y_pred)):
            lbl = "Resíduos (Erros)" if i == 0 else None
            ax.plot([xi, xi], [yi, ypi], color=t["plot_accent_sec"], linestyle=":", alpha=0.6, lw=1.2, label=lbl)

        # Pontos experimentais
        ax.scatter(xs, ys, color=t["plot_accent_sec"], s=75, zorder=5,
                   edgecolor=t["text_primary"], linewidth=1.2, label=f"Dados Experimentais (N={len(pontos)})")

        self._setup_ax(ax, title="Regressão Linear Simples por Mínimos Quadrados", xlabel="Variável Independente (x)", ylabel="Variável Dependente (y)")
        ax.legend(facecolor=t["bg_card"], edgecolor=t["border"], labelcolor=t["text_primary"], fontsize=9)
        self.fig.tight_layout()
        self.canvas.draw_idle()

    def plot_ajuste_multiplo(self, y_true, y_pred, r2):
        """Plota o gráfico de paridade (Real vs Previsto) para regressão linear múltipla."""
        self.apply_theme()
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        t = self.t

        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        min_v, max_v = min(np.min(y_true), np.min(y_pred)), max(np.max(y_true), np.max(y_pred))
        delta = max((max_v - min_v) * 0.1, 1.0)
        ref_line = np.linspace(min_v - delta, max_v + delta, 100)

        ax.plot(ref_line, ref_line, label="Ajuste Perfeito 1:1 (y = ŷ)", color=t["text_muted"], linestyle="--", lw=1.5)
        ax.scatter(y_true, y_pred, color=t["plot_accent"], s=75, edgecolor=t["text_primary"],
                   label=f"Observações do Modelo (R² = {r2:.4f})", zorder=5)

        self._setup_ax(ax, title="Regressão Múltipla — Paridade Real vs Previsto", xlabel="y Observado (Valor Real)", ylabel="y Estimado (Pelo Modelo)")
        ax.legend(facecolor=t["bg_card"], edgecolor=t["border"], labelcolor=t["text_primary"], fontsize=9)
        self.fig.tight_layout()
        self.canvas.draw_idle()

    def plot_integracao(self, f, a, b, n, method_name, result_val):
        """Plota a curva, a área preenchida da aproximação e as barras verticais de nós."""
        self.apply_theme()
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        t = self.t

        delta = max((b - a) * 0.2, 0.5)
        xs = np.linspace(a - delta, b + delta, 400)
        try:
            ys = np.array([float(f(x)) for x in xs])
            ax.plot(xs, ys, label="Função f(x)", color=t["plot_accent"], linewidth=2.2)
        except Exception:
            pass

        if n and n > 0:
            x_nodes = np.linspace(a, b, n + 1)
            try:
                y_nodes = [float(f(x)) for x in x_nodes]
                ax.fill_between(x_nodes, y_nodes, alpha=0.25, color=t["primary"],
                                label=f"Área Calculada ≈ {result_val:.6f}")
                for xn, yn in zip(x_nodes, y_nodes):
                    ax.vlines(xn, 0, yn, color=t["primary"], linestyle=":", alpha=0.7)
            except Exception:
                pass

        ax.axhline(0, color=t["text_muted"], linestyle="--", linewidth=0.8, alpha=0.6)
        
        self._setup_ax(ax, title=f"Integração Numérica — {method_name}", xlabel="x", ylabel="f(x)")
        ax.legend(facecolor=t["bg_card"], edgecolor=t["border"], labelcolor=t["text_primary"], fontsize=9)
        self.fig.tight_layout()
        self.canvas.draw_idle()

    def plot_edo(self, f_func, pontos, t0, y0, tn, h, method_name):
        """Plota a trajetória numérica do PVI e o campo de direções no plano."""
        self.apply_theme()
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        t = self.t

        ts = [p[0] for p in pontos]
        ys = [p[1] for p in pontos]

        min_t, max_t = min(ts), max(ts)
        min_y, max_y = min(ys), max(ys)
        dt = max((max_t - min_t) * 0.1, 0.2)
        dy = max((max_y - min_y) * 0.2, 1.0)

        # Campo de Direções (Slope Field)
        try:
            grid_t = np.linspace(min_t - dt, max_t + dt, 16)
            grid_y = np.linspace(min_y - dy, max_y + dy, 14)
            T, Y = np.meshgrid(grid_t, grid_y)
            
            S = np.zeros_like(T)
            for i in range(T.shape[0]):
                for j in range(T.shape[1]):
                    try:
                        S[i, j] = float(f_func(T[i, j], Y[i, j]))
                    except Exception:
                        S[i, j] = 0.0
            
            N = np.sqrt(1 + S**2)
            U = 1.0 / N
            V = S / N
            ax.quiver(T, Y, U, V, color=t["text_muted"], alpha=0.35, scale=25, headwidth=2.5, label="Campo de Direções")
        except Exception:
            pass

        # Trajetória
        ax.plot(ts, ys, label=f"Solução ({method_name})", color=t["plot_accent"], linewidth=2.4, zorder=5)
        ax.scatter(ts, ys, color=t["plot_accent_sec"], s=40, zorder=6)

        # Pontos inicial e final
        ax.scatter([t0], [y0], color=t["plot_accent_qua"], s=95, zorder=7,
                   edgecolor=t["text_primary"], label=f"Início: y({t0:.2f}) = {y0:.2f}")
        ax.scatter([ts[-1]], [ys[-1]], color=t["plot_accent_ter"], s=95, zorder=7,
                   edgecolor=t["text_primary"], label=f"Final: y({ts[-1]:.2f}) ≈ {ys[-1]:.4f}")

        self._setup_ax(ax, title=f"Solução de EDO — {method_name}", xlabel="Tempo (t)", ylabel="Variável de Estado y(t)")
        ax.legend(facecolor=t["bg_card"], edgecolor=t["border"], labelcolor=t["text_primary"], fontsize=9)
        self.fig.tight_layout()
        self.canvas.draw_idle()
