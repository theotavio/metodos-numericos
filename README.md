<div align="center">

# Métodos Numéricos Computacionais

**Aplicação web moderna, responsiva e interativa para resolução e visualização de problemas clássicos de Cálculo Numérico**,
construída com backend em **FastAPI (Python 3.10+)** e frontend modular em **HTML5 / CSS3 / JavaScript** com gráficos interativos via **Plotly.js**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SymPy](https://img.shields.io/badge/SymPy-1.12%2B-3B5526?style=for-the-badge&logo=python&logoColor=white)](https://www.sympy.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.26%2B-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Plotly](https://img.shields.io/badge/Plotly.js-2.35%2B-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/javascript/)

[![License](https://img.shields.io/badge/License-MIT-33C37F?style=for-the-badge)](#licença)
[![Platform](https://img.shields.io/badge/Platform-Web-0f1117?style=for-the-badge)](#acesso-online-aplicação-web)
[![Status](https://img.shields.io/badge/Status-Ativo-33C37F?style=for-the-badge)](#)

</div>

---

## Sumário

- [Visão Geral & Recursos](#visão-geral--recursos)
- [Métodos Implementados](#métodos-implementados)
- [Atalhos de Teclado](#atalhos-de-teclado)
- [Acesso Online (Aplicação Web)](#acesso-online-aplicação-web)
- [Guia do Desenvolvedor (Execução Local)](#guia-do-desenvolvedor-execução-local)
  - [1. Clonando o Repositório](#1-clonando-o-repositório)
  - [2. Configurando o Ambiente Virtual](#2-configurando-o-ambiente-virtual)
  - [3. Instalando as Dependências](#3-instalando-as-dependências)
  - [4. Executando a Aplicação Web](#4-executando-a-aplicação-web)
  - [5. Documentação Interativa da API (Swagger)](#5-documentação-interativa-da-api-swagger)
- [Sobre o Autor & Contato](#sobre-o-autor--contato)
- [Licença](#licença)

---

## Visão Geral & Recursos

- **Design System Claro & Moderno**: Tema claro de alto contraste e legibilidade, com espaçamento generoso e menu lateral retrátil (toggle).
- **Gráficos Interativos de Alta Precisão (Plotly.js)**:
  - **Raízes**: Curva suave $f(x)$, linha de referência $y=0$, realce do intervalo $[a, b]$, chute inicial $x₀$ e anotação visual destacada da raiz $x^*$.
  - **Sistemas Lineares**: Representação geométrica de retas concorrentes ($2\times 2$), barras de solução e curvas de convergência logarítmica (Gauss-Seidel).
  - **Interpolação**: Curva contínua do polinômio $P(x)$, nós conhecidos e projeção com guias pontilhadas para o ponto de consulta $x^*$.
  - **Ajuste de Curvas**: Diagrama de dispersão, reta ajustada de regressão, linhas verticais de resíduos e gráfico de paridade (Real vs Previsto).
  - **Integração Numérica**: Área sombreada sob a curva delimitada no intervalo $[a, b]$ e linhas verticais demarcando os nós de partição.
  - **EDOs**: Trajetória da solução $(t, y)$ combinada com o **campo de direções (slope field)** de alto contraste no plano de fase.
- **Tabelas de Iterações Detalhadas**: Exibição passo a passo de todas as fórmulas matemáticas utilizadas em cada método.
- **Exemplos Rápidos em 1 Clique**: Presets clássicos de livros-texto e aplicações de engenharia para carregamento e validação imediata em todos os módulos.
- **Exportação & Produtividade**:
  - Exportação direta das tabelas de iteração para arquivos **CSV**.
  - Cópia formatada de resumos e métricas para a Área de Transferência.
  - Exportação dos gráficos em alta definição (**PNG**).

---

## Métodos Implementados

<table>
<tr>
<td valign="top" width="50%">

### Raízes de Funções [ f(x) = 0 ]
- Bisseção [ Intervalar ]
- Newton-Raphson com múltiplos modos de derivada:
  - **Simbólica** (Analítica exata via SymPy)
  - **Diferenças Finitas** (Central $\mathcal{O}(h^2)$, Progressiva $\mathcal{O}(h)$, Regressiva $\mathcal{O}(h)$)
  - **Passo Complexo** (*Complex-Step* com precisão $\sim 10^{-16}$)
  - **Manual** (Expressão analítica de $f'(x)$ informada pelo usuário)
- Método da Secante [ Quasi-Newton ]
- Método das Cordas [ Falsa Posição ]
- Método de Pégaso [ Acelerado ]
- Iteração Linear [ Ponto Fixo ]

### Sistemas Lineares [ Ax = b ]
- Eliminação de Gauss (com pivoteamento parcial)
- Gauss-Seidel (com verificação de dominância diagonal)

### Interpolação [ P(x) ]
- Interpolação Linear
- Interpolação Quadrática
- Interpolação de Lagrange
- Diferenças Divididas de Newton

</td>
<td valign="top" width="50%">

### Integração Numérica [ ∫ f(x)dx ]
- Regra dos Trapézios
- Regra 1/3 de Simpson
- Regra 3/8 de Simpson
- Quadratura Gaussiana (2 pontos de Legendre)

### Ajuste de Curvas [ ŷ = a₀+a₁x ]
- Regressão Linear Simples (mínimos quadrados com $R^2$)
- Regressão Linear Múltipla (mínimos quadrados matricial com $R^2$)

### Equações Diferenciais Ordinárias [ dy/dt = f(t, y) ]
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
| `F5` ou `Ctrl + Enter` | Executar o cálculo do método selecionado |
| `Ctrl + C` | Copiar tabela de iterações ou resumo de métricas |
| `Esc` | Fechar modais abertos |

---

## Acesso Online (Aplicação Web)

Acesse a aplicação diretamente no seu navegador através do GitHub Pages, sem necessidade de instalação local:

**Link de Acesso**: [https://theotavio.github.io/metodos-numericos](https://theotavio.github.io/metodos-numericos)

> **Nota sobre o backend em nuvem**: Caso a API no Render esteja em modo de repouso (*cold start* por inatividade), o primeiro cálculo pode levar cerca de 30 a 50 segundos para inicializar a instância gratuita. Os cálculos seguintes responderão de forma imediata.

---

## Guia do Desenvolvedor (Execução Local)

### 1. Clonando o Repositório

```bash
git clone https://github.com/theotavio/metodos-numericos.git
cd metodos-numericos
```

### 2. Configurando o Ambiente Virtual

```bash
# Criação do ambiente virtual
python -m venv venv

# Ativação no Linux / macOS:
source venv/bin/activate

# Ativação no Windows:
venv\Scripts\activate
```

### 3. Instalando as Dependências

```bash
pip install -r requirements.txt
```

### 4. Executando a Aplicação Web

```bash
python main.py
```

O servidor local será inicializado em `http://127.0.0.1:8000` e a interface web será aberta automaticamente no seu navegador.

### 5. Documentação Interativa da API (Swagger)

Com o servidor em execução, acesse a documentação interativa em:
- **Swagger UI**: `http://127.0.0.1:8000/api/docs`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc`

---

## Sobre o Autor & Contato

- **GitHub**: [github.com/theotavio](https://github.com/theotavio)
- **Sponsor**: [github.com/sponsors/theotavio](https://github.com/sponsors/theotavio)
- **E-mail**: `otavioal2907@gmail.com`

---

## Licença

Distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.