<div align="center">

# Métodos Numéricos Computacionais

**Aplicação desktop moderna e interativa para resolução e visualização de problemas clássicos de Cálculo Numérico**,
construída em Python com interface gráfica nativa via **PySide6 (Qt 6)** e gráficos dinâmicos via **Matplotlib**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-Qt%206-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython-6/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8%2B-11557c?style=for-the-badge)](https://matplotlib.org/)
[![SymPy](https://img.shields.io/badge/SymPy-1.12%2B-3B5526?style=for-the-badge&logo=python&logoColor=white)](https://www.sympy.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.26%2B-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)

[![License](https://img.shields.io/badge/License-MIT-33C37F?style=for-the-badge)](#licença)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-0f1117?style=for-the-badge)](#guia-do-desenvolvedor)
[![Status](https://img.shields.io/badge/Status-Ativo-33C37F?style=for-the-badge)](#)

</div>

---

## Sumário

- [Visão Geral & Recursos](#visão-geral--recursos)
- [Métodos Implementados](#métodos-implementados)
- [Atalhos de Teclado](#atalhos-de-teclado)
- [Guia do Desenvolvedor](#guia-do-desenvolvedor)
  - [1. Clonando o Repositório](#1-clonando-o-repositório)
  - [2. Configurando o Ambiente Virtual](#2-configurando-o-ambiente-virtual)
  - [3. Instalando as Dependências](#3-instalando-as-dependências)
  - [4. Executando a Aplicação](#4-executando-a-aplicação)
  - [5. Testando os Métodos](#5-testando-os-métodos)
  - [6. Adicionando Novos Métodos Numéricos](#6-adicionando-novos-métodos-numéricos)
- [Licença](#licença)

---

## Visão Geral & Recursos

- 🎨 **Interface Moderna & Temas**: Modo Claro (*Light*) como padrão e Modo Escuro (*Dark*) com alternância instantânea via botão ou atalho `Ctrl + T`.
- 📊 **Gráficos Interativos Integrados (Matplotlib)**:
  - **Raízes**: Curva suave $f(x)$, eixo zero, realce do intervalo $[a, b]$, chute $x_0$ e anotação visual destacada da raiz $x^*$.
  - **Sistemas Lineares**: Representação geométrica de retas concorrentes ($2\times 2$) e curvas de erro/convergência logarítmica (Gauss-Seidel).
  - **Interpolação**: Curva contínua do polinômio $P(x)$, nós conhecidos e projeção com guias pontilhadas para o ponto de consulta $x^*$.
  - **Ajuste de Curvas**: Diagrama de dispersão, reta ajustada de regressão, linhas verticais de resíduos e gráfico de paridade (Real vs Previsto).
  - **Integração Numérica**: Área sombreada sob a curva e linhas verticais delimitadoras dos subintervalos discretos.
  - **EDOs**: Trajetória da solução $(t, y)$ combinada com o **campo de direções (slope field)** no plano de fase.
- 📋 **Exemplos Rápidos em 1 Clique**: Presets clássicos de livros-texto para carregamento e validação imediata em todos os módulos.
- 💾 **Exportação & Produtividade**:
  - Exportação direta das tabelas de iteração para arquivos **CSV**.
  - Cópia formatada de resumos e métricas para a Área de Transferência.
  - Exportação dos gráficos em alta definição (**PNG, SVG, PDF**).
- 🚨 **Tratamento Amigável de Erros**: Mensagens de validação e alertas matemáticos exibidos em janelas flutuantes explicativas.

---

## Métodos Implementados

<table>
<tr>
<td valign="top" width="50%">

### 🔍 Raízes de Funções
- Bisseção
- Newton-Raphson (derivada simbólica via SymPy)
- Método das Cordas
- Método de Pégaso
- Iteração Linear (Ponto Fixo)

### 🧮 Sistemas Lineares
- Eliminação de Gauss (com pivoteamento parcial)
- Gauss-Seidel

### 📈 Interpolação
- Interpolação Linear
- Interpolação Quadrática
- Interpolação de Lagrange
- Diferenças Divididas de Newton

</td>
<td valign="top" width="50%">

### ∫ Integração Numérica
- Regra dos Trapézios
- Regra 1/3 de Simpson
- Regra 3/8 de Simpson
- Quadratura Gaussiana (2 pontos de Legendre)

### 📉 Ajuste de Curvas
- Regressão Linear Simples (mínimos quadrados com $R^2$)
- Regressão Linear Múltipla (mínimos quadrados matricial com $R^2$)

### 🌀 Equações Diferenciais Ordinárias
- Método de Euler
- Runge-Kutta de 2ª ordem (Heun)
- Runge-Kutta de 4ª ordem (Clássico)

</td>
</tr>
</table>

---

## Atalhos de Teclado

| Atalho | Ação |
|---|---|
| `Ctrl + 1` a `Ctrl + 6` | Alternar entre os módulos de cálculo |
| `Ctrl + T` | Alternar entre Modo Claro e Modo Escuro |
| `F5` ou `Ctrl + Enter` | Executar o cálculo do método selecionado |
| `Ctrl + C` | Copiar dados da tabela selecionada |

---

## Guia do Desenvolvedor

Este guia detalha o passo a passo completo para configurar o ambiente de desenvolvimento local, executar e estender a aplicação.

### 1. Clonando o Repositório

```bash
git clone https://github.com/theotavio/metodos-numericos.git
cd metodos-numericos
```

### 2. Configurando o Ambiente Virtual

Recomenda-se utilizar um ambiente virtual isolado com Python 3.10 ou superior:

```bash
# Criação do ambiente virtual
python -m venv venv

# Ativação no Linux / macOS:
source venv/bin/activate

# Ativação no Windows (Prompt de Comando / PowerShell):
venv\Scripts\activate
```

### 3. Instalando as Dependências

Com o ambiente ativado, instale os pacotes listados no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Executando a Aplicação

Inicie o ponto de entrada principal:

```bash
python src/main.py
```

### 5. Testando os Métodos

Para rodar uma validação rápida de todos os métodos e presets em modo offscreen/headless:

```bash
python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src').resolve()))
from PySide6.QtWidgets import QApplication
from gui.app import App
app = QApplication(sys.argv)
window = App()
for tab in [window.tab_raizes, window.tab_sistemas, window.tab_interpolacao, window.tab_ajuste, window.tab_integracao, window.tab_edo]:
    for ex in tab.exemplos_disponiveis:
        tab._on_exemplo_selecionado(ex)
        tab._on_executar()
        assert tab.ultimo_resultado['sucesso'] == True
print('Todos os testes passaram com sucesso!')
"
```

### 6. Adicionando Novos Métodos Numéricos

1. **Implementação Matemática**: Crie a função pura em `src/core/<modulo>.py`. Ela deve receber os parâmetros matemáticos e retornar o dicionário padrão:
   ```python
   {
       "sucesso": True,       # ou False em caso de falha matemática
       "resultado": ...,      # valor numérico, vetor ou lista de pontos
       "historico": [...],    # linhas de log/iterações formatadas
       "erro": None           # mensagem de erro caso sucesso seja False
   }
   ```
2. **Integração na Interface**:
   - Abra a aba correspondente em `src/gui/tabs/<modulo>_tab.py`.
   - Adicione o novo método ao dicionário `self.metodos_disponiveis`.
   - Adicione presets de teste em `self.exemplos_disponiveis`.
   - Ajuste `_montar_formulario`, `_executar` e `_renderizar_grafico` se o novo algoritmo exigir campos ou plotagens específicas.

---

## Licença

Distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.