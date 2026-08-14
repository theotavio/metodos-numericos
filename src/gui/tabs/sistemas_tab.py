import customtkinter as ctk
from gui.base_tab import AbaBase
from gui.widgets import CampoEntrada
from gui import theme
from core import sistemas_lineares


class SistemasTab(AbaBase):
    def __init__(self, tab):
        self.metodos_disponiveis = {
            "Eliminação de Gauss": "gauss",
            "Gauss-Seidel": "gauss_seidel",
        }
        self.ordem_atual = None
        self.entradas_matriz = []
        self.entradas_vetor = []
        super().__init__(tab, "Sistemas Lineares", "Métodos diretos e iterativos para resolução de Ax = b")

    def _montar_formulario(self, nome_metodo):
        campos = {}

        campos["ordem"] = CampoEntrada(self.frame_formulario, "Ordem da matriz (n)", "3")
        campos["ordem"].pack(fill="x")

        ctk.CTkButton(
            self.frame_formulario, text="Gerar matriz",
            command=lambda: self._gerar_grade_matriz(campos["ordem"]),
            **theme.estilo_botao_secundario()
        ).pack(fill="x", pady=(0, 12))

        self.frame_matriz = ctk.CTkFrame(self.frame_formulario, fg_color="transparent")
        self.frame_matriz.pack(fill="x")

        if nome_metodo == "gauss_seidel":
            campos["tol"] = CampoEntrada(self.frame_formulario, "Tolerância", "1e-6")
            campos["tol"].pack(fill="x")
            campos["max_iter"] = CampoEntrada(self.frame_formulario, "Máx. iterações", "100")
            campos["max_iter"].pack(fill="x")

        self.frame_formulario.after(50, lambda: self._gerar_grade_matriz(campos["ordem"]))
        return campos

    def _gerar_grade_matriz(self, campo_ordem):
        for widget in self.frame_matriz.winfo_children():
            widget.destroy()
        self.entradas_matriz = []
        self.entradas_vetor = []

        try:
            n = int(float(campo_ordem.get()))
        except ValueError:
            self._escrever_saida("Ordem inválida para gerar a matriz.")
            return
        if n <= 0 or n > 10:
            self._escrever_saida("A ordem deve ser um inteiro entre 1 e 10.")
            return

        ctk.CTkLabel(self.frame_matriz, text="A (coeficientes)  |  b",
                     font=theme.FONT_LABEL, text_color=theme.COR_TEXTO_SECUNDARIO
                     ).grid(row=0, column=0, columnspan=n + 2, sticky="w", pady=(4, 6))

        for i in range(n):
            linha_entries = []
            for j in range(n):
                e = ctk.CTkEntry(self.frame_matriz, width=42, height=30, placeholder_text="0",
                                  fg_color=theme.COR_PAINEL_CLARO, border_color=theme.COR_BORDA, corner_radius=5)
                e.grid(row=i + 1, column=j, padx=2, pady=2)
                linha_entries.append(e)
            self.entradas_matriz.append(linha_entries)

            ctk.CTkLabel(self.frame_matriz, text="│", text_color=theme.COR_TEXTO_SECUNDARIO).grid(
                row=i + 1, column=n, padx=4)

            eb = ctk.CTkEntry(self.frame_matriz, width=50, height=30, placeholder_text="0",
                               fg_color=theme.COR_PAINEL_CLARO, border_color=theme.COR_BORDA, corner_radius=5)
            eb.grid(row=i + 1, column=n + 1, padx=2, pady=2)
            self.entradas_vetor.append(eb)

        self.ordem_atual = n

    def _ler_matriz_e_vetor(self):
        if not self.entradas_matriz:
            raise ValueError("A matriz não foi gerada. Clique em 'Gerar matriz'.")

        n = self.ordem_atual
        A, b = [], []
        for i in range(n):
            linha = []
            for j in range(n):
                texto = self.entradas_matriz[i][j].get().strip()
                if texto == "":
                    raise ValueError(f"O campo A[{i+1}][{j+1}] está vazio.")
                try:
                    linha.append(float(texto.replace(",", ".")))
                except ValueError:
                    raise ValueError(f"O campo A[{i+1}][{j+1}] contém valor inválido: '{texto}'")
            A.append(linha)

            texto_b = self.entradas_vetor[i].get().strip()
            if texto_b == "":
                raise ValueError(f"O campo b[{i+1}] está vazio.")
            try:
                b.append(float(texto_b.replace(",", ".")))
            except ValueError:
                raise ValueError(f"O campo b[{i+1}] contém valor inválido: '{texto_b}'")
        return A, b

    def _executar(self, nome_metodo, campos):
        A, b = self._ler_matriz_e_vetor()

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
        solucao = resultado_dict.get("resultado")
        if solucao is None:
            return "Sem solução."
        return "\n".join(f"x{i+1} = {v:.8f}" for i, v in enumerate(solucao))