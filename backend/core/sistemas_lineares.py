import numpy as np

SUBSCRIPT_MAP = str.maketrans("0123456789ijkmnpt", "₀₁₂₃₄₅₆₇₈₉ᵢⱼₖₘₙₚₜ")


def _sub(text) -> str:
    return str(text).translate(SUBSCRIPT_MAP)


def _formatar_matriz_txt(M):
    linhas = []
    for row in M:
        vals = "  ".join(f"{float(v):>10.4f}" for v in row[:-1])
        linhas.append(f"[ {vals}  |  {float(row[-1]):>10.4f} ]")
    return "\n".join(linhas)


def eliminacao_gauss(A, b):
    historico = []
    etapas = []
    substituicao_passos = []

    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao interpretar matriz/vetor: {exc}"}

    n = len(b)
    if A.shape != (n, n):
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Dimensões incompatíveis: A é {A.shape}, b tem tamanho {n}."}

    M = np.hstack([A, b.reshape(-1, 1)])
    
    etapas.append({
        "etapa_num": 0,
        "titulo": "Matriz Aumentada Inicial [A | b]",
        "descricao": "Sistema linear original antes do início do escalonamento.",
        "operacao": "Formulação do Sistema",
        "matriz": [[float(val) for val in row] for row in M],
        "pivo_pos": [0, 0],
        "linha_ativa": None,
        "tipo": "inicio"
    })
    historico.append("Etapa 0: Matriz Aumentada Inicial [A | b]")
    historico.append(_formatar_matriz_txt(M))

    try:
        etapa_contador = 1
        for k in range(n - 1):
            max_linha = int(np.argmax(np.abs(M[k:, k])) + k)
            if abs(M[max_linha, k]) < 1e-14:
                return {"sucesso": False, "resultado": None, "historico": historico,
                        "erro": f"Pivô nulo na coluna {k+1}. O sistema pode ser singular ou indeterminado."}

            if max_linha != k:
                M[[k, max_linha]] = M[[max_linha, k]]
                etapas.append({
                    "etapa_num": int(etapa_contador),
                    "titulo": f"Pivoteamento Parcial na Coluna {_sub(k+1)}",
                    "descricao": f"Troca de linhas L{_sub(k+1)} ↔ L{_sub(max_linha+1)} para maximizar o pivô a{_sub(k+1)}{_sub(k+1)} = {float(M[k, k]):.4f}.",
                    "operacao": f"L{_sub(k+1)} ↔ L{_sub(max_linha+1)}",
                    "matriz": [[float(val) for val in row] for row in M],
                    "pivo_pos": [int(k), int(k)],
                    "linha_ativa": int(max_linha),
                    "tipo": "pivot"
                })
                historico.append(f"Etapa {etapa_contador}: Pivoteamento L{_sub(k+1)} ↔ L{_sub(max_linha+1)}")
                historico.append(_formatar_matriz_txt(M))
                etapa_contador += 1

            for i in range(k + 1, n):
                fator = float(M[i, k] / M[k, k])
                M[i, k:] -= fator * M[k, k:]
                M[i, k] = 0.0

                etapas.append({
                    "etapa_num": int(etapa_contador),
                    "titulo": f"Eliminação do Elemento a{_sub(i+1)}{_sub(k+1)}",
                    "descricao": f"Multiplicador m{_sub(i+1)}{_sub(k+1)} = a{_sub(i+1)}{_sub(k+1)} / a{_sub(k+1)}{_sub(k+1)} = {fator:.6f}.",
                    "operacao": f"L{_sub(i+1)} ← L{_sub(i+1)} - ({fator:.4f}) · L{_sub(k+1)}",
                    "multiplicador": float(fator),
                    "matriz": [[float(val) for val in row] for row in M],
                    "pivo_pos": [int(k), int(k)],
                    "linha_ativa": int(i),
                    "tipo": "eliminacao"
                })
                historico.append(f"Etapa {etapa_contador}: L{_sub(i+1)} ← L{_sub(i+1)} - ({fator:.4f})·L{_sub(k+1)}")
                historico.append(_formatar_matriz_txt(M))
                etapa_contador += 1

        if abs(M[n - 1, n - 1]) < 1e-14:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": "Pivô final nulo. Sistema singular ou indeterminado."}

        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            soma_termos = float(np.dot(M[i, i + 1:n], x[i + 1:n]))
            x[i] = float((M[i, n] - soma_termos) / M[i, i])

            termos_str = ""
            for j in range(i + 1, n):
                coef = float(M[i, j])
                termos_str += f" - ({coef:.4f})·({float(x[j]):.4f})"

            passo_txt = f"x{_sub(i+1)} = [{float(M[i, n]):.4f}{termos_str}] / {float(M[i, i]):.4f} = {float(x[i]):.6f}"
            substituicao_passos.insert(0, passo_txt)

        historico.append("\nSubstituição Regressiva:")
        for sp in substituicao_passos:
            historico.append(f"  {sp}")

        return {
            "sucesso": True,
            "resultado": [float(v) for v in x],
            "historico": historico,
            "etapas_gauss": etapas,
            "substituicao_passos": substituicao_passos,
            "erro": None
        }

    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro durante a eliminação de Gauss: {exc}"}


def gauss_seidel(A, b, tol=1e-6, max_iter=100, x0=None):
    historico = []
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
    except Exception as exc:
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Erro ao interpretar matriz/vetor: {exc}"}

    n = len(b)
    if A.shape != (n, n):
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": f"Dimensões incompatíveis: A é {A.shape}, b tem tamanho {n}."}

    if np.any(np.diag(A) == 0):
        return {"sucesso": False, "resultado": None, "historico": historico,
                "erro": "Elemento nulo detectado na diagonal principal de A. Reordene as equações."}

    linhas_dominancia = []
    estritamente_dominante = True
    for i in range(n):
        diag_val = float(abs(A[i, i]))
        soma_outros = float(sum(abs(A[i, j]) for j in range(n) if j != i))
        dom = bool(diag_val > soma_outros)
        if not dom:
            estritamente_dominante = False
        linhas_dominancia.append({
            "linha": int(i + 1),
            "diag": float(diag_val),
            "soma_outros": float(soma_outros),
            "dominante": dom
        })

    dominancia_info = {
        "estritamente_dominante": bool(estritamente_dominante),
        "linhas": linhas_dominancia
    }

    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)

    cols_str = " | ".join([f"x{_sub(i+1):<10}" for i in range(n)])
    historico.append(f"{'k':>4} | {cols_str} | {'Erro ||e||∞':>14}")

    valores_0 = " | ".join([f"{float(v):<10.6f}" for v in x])
    historico.append(f"{0:>4} | {valores_0} | {'—':>14}")

    for it in range(1, max_iter + 1):
        x_novo = x.copy()
        for i in range(n):
            soma1 = np.dot(A[i, :i], x_novo[:i])
            soma2 = np.dot(A[i, i + 1:], x[i + 1:])
            x_novo[i] = (b[i] - soma1 - soma2) / A[i, i]

        erro = float(np.linalg.norm(x_novo - x, ord=np.inf))
        valores_str = " | ".join([f"{float(v):<10.6f}" for v in x_novo])
        historico.append(f"{it:>4} | {valores_str} | {erro:>14.6e}")

        x = x_novo
        if erro < tol:
            return {
                "sucesso": True,
                "resultado": [float(v) for v in x],
                "historico": historico,
                "dominancia_info": dominancia_info,
                "erro": None,
                "iteracoes": int(it)
            }

    return {
        "sucesso": False,
        "resultado": [float(v) for v in x],
        "historico": historico,
        "dominancia_info": dominancia_info,
        "erro": f"Máximo de iterações ({max_iter}) atingido sem convergência para tolerância {tol}.",
        "iteracoes": int(max_iter)
    }
