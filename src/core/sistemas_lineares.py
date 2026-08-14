import numpy as np


def _formatar_matriz(M):
    linhas = []
    for linha in M:
        linhas.append("  ".join(f"{v:>10.4f}" for v in linha))
    return "\n".join(linhas)


def eliminacao_gauss(A, b):
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

    M = np.hstack([A, b.reshape(-1, 1)])
    historico.append("Matriz aumentada inicial [A|b]:")
    historico.append(_formatar_matriz(M))

    try:
        for k in range(n - 1):
            max_linha = np.argmax(np.abs(M[k:, k])) + k
            if abs(M[max_linha, k]) < 1e-14:
                return {"sucesso": False, "resultado": None, "historico": historico,
                        "erro": f"Pivô nulo na coluna {k+1}. Sistema pode ser singular."}

            if max_linha != k:
                M[[k, max_linha]] = M[[max_linha, k]]
                historico.append(f"Troca de linhas L{k+1} <-> L{max_linha+1}:")
                historico.append(_formatar_matriz(M))

            for i in range(k + 1, n):
                fator = M[i, k] / M[k, k]
                M[i, k:] -= fator * M[k, k:]
                historico.append(f"L{i+1} = L{i+1} - ({fator:.6f}) * L{k+1}")

            historico.append(f"Matriz após eliminar coluna {k+1}:")
            historico.append(_formatar_matriz(M))

        if abs(M[n - 1, n - 1]) < 1e-14:
            return {"sucesso": False, "resultado": None, "historico": historico,
                    "erro": "Pivô final nulo. Sistema singular ou indeterminado."}

        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            soma = M[i, n] - np.dot(M[i, i + 1:n], x[i + 1:n])
            x[i] = soma / M[i, i]

        historico.append("Substituição regressiva concluída.")
        return {"sucesso": True, "resultado": x.tolist(), "historico": historico, "erro": None}

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
                "erro": "Elemento nulo na diagonal principal de A. Reordene as equações."}

    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)

    diag_dominante = all(
        abs(A[i, i]) >= sum(abs(A[i, j]) for j in range(n) if j != i) for i in range(n)
    )
    if not diag_dominante:
        historico.append("AVISO: matriz não é estritamente diagonal dominante. Convergência não garantida.")

    historico.append(f"{'Iter':>4} | " + " | ".join([f"x{i+1:<10}" for i in range(n)]) + f" | {'Erro':>12}")

    for it in range(1, max_iter + 1):
        x_novo = x.copy()
        for i in range(n):
            soma1 = np.dot(A[i, :i], x_novo[:i])
            soma2 = np.dot(A[i, i + 1:], x[i + 1:])
            x_novo[i] = (b[i] - soma1 - soma2) / A[i, i]

        erro = np.linalg.norm(x_novo - x, ord=np.inf)
        valores_str = " | ".join([f"{v:<10.6f}" for v in x_novo])
        historico.append(f"{it:>4} | {valores_str} | {erro:>12.6e}")

        x = x_novo
        if erro < tol:
            return {"sucesso": True, "resultado": x.tolist(), "historico": historico, "erro": None,
                    "iteracoes": it}

    return {"sucesso": False, "resultado": x.tolist(), "historico": historico,
            "erro": f"Máximo de iterações ({max_iter}) atingido sem convergência para tolerância {tol}.",
            "iteracoes": max_iter}