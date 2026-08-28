class ChartRenderer {
    constructor(containerId = "plot-canvas"){
        this.containerId = containerId;
        this.currentData = null;
        this.currentModulo = null;
        this.currentMode = "zoom";
    }

    getContainer(){
        return document.getElementById(this.containerId);
    }

    clear(){
        const container = this.getContainer();
        if(!container){
            return;
        }

        this.currentData = null;
        this.currentModulo = null;

        container.innerHTML = `
            <div class="plot-placeholder">
                <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="20" x2="18" y2="10"></line>
                    <line x1="12" y1="20" x2="12" y2="4"></line>
                    <line x1="6" y1="20" x2="6" y2="14"></line>
                </svg>
                <span>Execute um método numérico para visualizar o gráfico interativo.</span>
            </div>
        `;
    }

    getDefaultLayout(title, xlabel, ylabel){
        return {
            title: {
                text: title,
                font: { size: 14, color: "#0f172a", family: "-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" },
                x: 0.05
            },
            paper_bgcolor: "#ffffff",
            plot_bgcolor: "#ffffff",
            font: { color: "#0f172a", size: 12 },
            xaxis: {
                title: { text: xlabel, font: { size: 12, color: "#475569" } },
                gridcolor: "#e2e8f0",
                zerolinecolor: "#94a3b8",
                tickfont: { color: "#475569", size: 11 }
            },
            yaxis: {
                title: { text: ylabel, font: { size: 12, color: "#475569" } },
                gridcolor: "#e2e8f0",
                zerolinecolor: "#94a3b8",
                tickfont: { color: "#475569", size: 11 }
            },
            margin: { l: 60, r: 25, t: 45, b: 50 },
            autosize: true,
            showlegend: true,
            dragmode: this.currentMode,
            legend: {
                orientation: "h",
                y: -0.22,
                x: 0,
                font: { size: 11, color: "#475569" }
            }
        };
    }

    render(moduloId, plotData){
        if(!plotData){
            this.clear();
            return;
        }

        this.currentModulo = moduloId;
        this.currentData = plotData;
        const container = this.getContainer();
        if(!container || !window.Plotly){
            return;
        }

        if(moduloId === "raizes"){
            this.plotRaizes(plotData);
        }else if(moduloId === "sistemas"){
            this.plotSistemas(plotData);
        }else if(moduloId === "interpolacao"){
            this.plotInterpolacao(plotData);
        }else if(moduloId === "ajuste"){
            this.plotAjuste(plotData);
        }else if(moduloId === "integracao"){
            this.plotIntegracao(plotData);
        }else if(moduloId === "edo"){
            this.plotEdo(plotData);
        }
    }

    plotRaizes(data){
        const traces = [];

        traces.push({
            x: data.xs,
            y: data.ys,
            mode: "lines",
            name: "Função f(x)",
            line: { color: "#0284c7", width: 2.4 }
        });

        traces.push({
            x: [data.xs[0], data.xs[data.xs.length - 1]],
            y: [0, 0],
            mode: "lines",
            name: "Eixo f(x) = 0",
            line: { color: "#94a3b8", width: 1.4, dash: "dash" },
            showlegend: true
        });

        if(data.x0 !== null && data.x0 !== undefined){
            traces.push({
                x: [data.x0],
                y: [0],
                mode: "markers",
                name: `Chute inicial (x₀ = ${data.x0})`,
                marker: { color: "#d97706", size: 10, symbol: "circle" }
            });
        }

        if(data.root !== null && data.root !== undefined){
            traces.push({
                x: [data.root],
                y: [0],
                mode: "markers+text",
                name: `Raiz Calculada (x* ≈ ${data.root.toFixed(6)})`,
                marker: { color: "#059669", size: 13, symbol: "diamond" },
                text: [`x* ≈ ${data.root.toFixed(6)}`],
                textposition: "top center",
                textfont: { size: 11, color: "#059669" }
            });
        }

        const layout = this.getDefaultLayout(
            `Visualização da Raiz — ${data.metodo || ""}`,
            "Variável Independente (x)",
            "Valor da Função f(x)"
        );

        if(data.a !== null && data.b !== null && data.a !== undefined && data.b !== undefined){
            layout.shapes = [{
                type: "rect",
                xref: "x",
                yref: "paper",
                x0: data.a,
                x1: data.b,
                y0: 0,
                y1: 1,
                fillcolor: "rgba(37, 99, 235, 0.12)",
                line: { color: "#2563eb", width: 1, dash: "dot" }
            }];
        }

        Plotly.newPlot(this.containerId, traces, layout, { responsive: true, displayModeBar: false });
    }

    plotSistemas(data){
        if(data.type === "2d_lines"){
            const traces = [];
            const palette = ["#0284c7", "#e11d48"];

            data.lines.forEach((l, idx) => {
                if(l.vertical){
                    traces.push({
                        x: [l.x_vert, l.x_vert],
                        y: [-10, 10],
                        mode: "lines",
                        name: l.eq,
                        line: { color: palette[idx % palette.length], width: 2.2 }
                    });
                }else{
                    traces.push({
                        x: l.xs,
                        y: l.ys,
                        mode: "lines",
                        name: l.eq,
                        line: { color: palette[idx % palette.length], width: 2.2 }
                    });
                }
            });

            if(data.sol && data.sol.length >= 2){
                traces.push({
                    x: [data.sol[0]],
                    y: [data.sol[1]],
                    mode: "markers+text",
                    name: `Ponto Solução: (${data.sol[0].toFixed(4)}, ${data.sol[1].toFixed(4)})`,
                    marker: { color: "#059669", size: 13, symbol: "circle" },
                    text: [`(${data.sol[0].toFixed(4)}, ${data.sol[1].toFixed(4)})`],
                    textposition: "top right",
                    textfont: { size: 11, color: "#059669" }
                });
            }

            const layout = this.getDefaultLayout(
                "Interseção Geométrica das Equações Lineares (2×2)",
                "Incógnita x₁",
                "Incógnita x₂"
            );
            Plotly.newPlot(this.containerId, traces, layout, { responsive: true, displayModeBar: false });

        }else{
            if(data.erros && data.erros.length > 1){
                const traceBar = {
                    x: data.labels,
                    y: data.sol,
                    type: "bar",
                    name: "Vetor Solução x",
                    marker: { color: "#2563eb" },
                    xaxis: "x",
                    yaxis: "y"
                };

                const traceConv = {
                    x: data.erros.map((_, i) => i + 1),
                    y: data.erros,
                    type: "scatter",
                    mode: "lines+markers",
                    name: "Convergência ||e||∞",
                    line: { color: "#e11d48", width: 2.2 },
                    marker: { size: 6 },
                    xaxis: "x2",
                    yaxis: "y2"
                };

                const layout = this.getDefaultLayout("Solução do Sistema e Curva de Convergência", "Incógnitas", "Valor");
                layout.grid = { rows: 1, columns: 2, pattern: "independent" };
                layout.yaxis2 = {
                    type: "log",
                    title: { text: "Erro Logarítmico", font: { size: 12, color: "#475569" } },
                    gridcolor: "#e2e8f0"
                };
                layout.xaxis2 = {
                    title: { text: "Iteração (k)", font: { size: 12, color: "#475569" } },
                    gridcolor: "#e2e8f0"
                };

                Plotly.newPlot(this.containerId, [traceBar, traceConv], layout, { responsive: true, displayModeBar: false });
            }else{
                const trace = {
                    x: data.labels,
                    y: data.sol,
                    type: "bar",
                    name: "Vetor Solução x",
                    marker: { color: "#2563eb" }
                };

                const layout = this.getDefaultLayout("Vetor Solução do Sistema Linear", "Incógnitas", "Valor Calculado");
                Plotly.newPlot(this.containerId, [trace], layout, { responsive: true, displayModeBar: false });
            }
        }
    }

    plotInterpolacao(data){
        const traces = [];

        traces.push({
            x: data.x_dense,
            y: data.y_dense,
            mode: "lines",
            name: "Polinômio Interpolador P(x)",
            line: { color: "#0284c7", width: 2.4 }
        });

        traces.push({
            x: data.xs_known,
            y: data.ys_known,
            mode: "markers",
            name: `Nós Conhecidos (N=${data.xs_known.length})`,
            marker: { color: "#e11d48", size: 9, symbol: "circle" }
        });

        traces.push({
            x: [data.x_alvo],
            y: [data.y_alvo],
            mode: "markers+text",
            name: `Interpolação P(${data.x_alvo}) = ${data.y_alvo.toFixed(4)}`,
            marker: { color: "#059669", size: 13, symbol: "star" },
            text: [`P(${data.x_alvo}) ≈ ${data.y_alvo.toFixed(4)}`],
            textposition: "top center",
            textfont: { size: 11, color: "#059669" }
        });

        const layout = this.getDefaultLayout(
            `Curva do Polinômio Interpolador — ${data.metodo || ""}`,
            "Variável Independente (x)",
            "Polinômio P(x)"
        );

        layout.shapes = [
            {
                type: "line",
                x0: data.x_alvo,
                x1: data.x_alvo,
                y0: Math.min(...data.y_dense),
                y1: data.y_alvo,
                line: { color: "#059669", width: 1.5, dash: "dot" }
            },
            {
                type: "line",
                x0: Math.min(...data.x_dense),
                x1: data.x_alvo,
                y0: data.y_alvo,
                y1: data.y_alvo,
                line: { color: "#059669", width: 1.5, dash: "dot" }
            }
        ];

        Plotly.newPlot(this.containerId, traces, layout, { responsive: true, displayModeBar: false });
    }

    plotAjuste(data){
        const traces = [];

        if(data.type === "simples"){
            traces.push({
                x: data.x_line,
                y: data.y_line,
                mode: "lines",
                name: `Reta: ŷ = ${data.a0.toFixed(4)} + ${data.a1.toFixed(4)}x (R² = ${data.r2.toFixed(4)})`,
                line: { color: "#0284c7", width: 2.6 }
            });

            if(data.residuals){
                data.residuals.forEach((res, i) => {
                    traces.push({
                        x: res.x,
                        y: res.y,
                        mode: "lines",
                        line: { color: "#e11d48", width: 1.2, dash: "dot" },
                        showlegend: i === 0,
                        name: "Resíduos eᵢ = yᵢ - ŷᵢ"
                    });
                });
            }

            traces.push({
                x: data.xs_pts,
                y: data.ys_pts,
                mode: "markers",
                name: `Dados Experimentais (N=${data.xs_pts.length})`,
                marker: { color: "#e11d48", size: 9, symbol: "circle" }
            });

            const layout = this.getDefaultLayout(
                "Regressão Linear Simples por Mínimos Quadrados",
                "Variável Independente (x)",
                "Variável Dependente (y)"
            );
            Plotly.newPlot(this.containerId, traces, layout, { responsive: true, displayModeBar: false });

        }else{
            traces.push({
                x: data.ref_line_x,
                y: data.ref_line_y,
                mode: "lines",
                name: "Ajuste Perfeito 1:1 (y = ŷ)",
                line: { color: "#94a3b8", width: 1.8, dash: "dash" }
            });

            traces.push({
                x: data.y_true,
                y: data.y_pred,
                mode: "markers",
                name: `Observações do Modelo (R² = ${data.r2.toFixed(4)})`,
                marker: { color: "#2563eb", size: 10, symbol: "circle" }
            });

            const layout = this.getDefaultLayout(
                "Regressão Linear Múltipla — Paridade Real vs Previsto",
                "y Observado (Valor Real)",
                "y Estimado (Pelo Modelo ŷ)"
            );
            Plotly.newPlot(this.containerId, traces, layout, { responsive: true, displayModeBar: false });
        }
    }

    plotIntegracao(data){
        const traces = [];

        traces.push({
            x: data.xs_curve,
            y: data.ys_curve,
            mode: "lines",
            name: "Função f(x)",
            line: { color: "#0284c7", width: 2.4 }
        });

        if(data.xs_area && data.ys_area){
            traces.push({
                x: data.xs_area,
                y: data.ys_area,
                fill: "tozeroy",
                mode: "none",
                name: `Área sob a curva [${data.a}, ${data.b}] ≈ ${data.integral_val.toFixed(6)}`,
                fillcolor: "rgba(37, 99, 235, 0.22)",
                hoverinfo: "none"
            });
        }

        if(data.x_nodes && data.y_nodes){
            data.x_nodes.forEach((xn, idx) => {
                const yn = data.y_nodes[idx];
                traces.push({
                    x: [xn, xn],
                    y: [0, yn],
                    mode: "lines",
                    line: { color: "#2563eb", width: 1.5, dash: "dash" },
                    showlegend: idx === 0,
                    name: "Subintervalos Discretos (Nós xᵢ)"
                });
            });

            traces.push({
                x: data.x_nodes,
                y: data.y_nodes,
                mode: "markers",
                name: "Nós Amostrados f(xᵢ)",
                marker: { color: "#2563eb", size: 6 }
            });
        }

        const layout = this.getDefaultLayout(
            `Integração Numérica Definida — ${data.metodo || ""}`,
            "Variável Independente (x)",
            "Valor da Função f(x)"
        );

        Plotly.newPlot(this.containerId, traces, layout, { responsive: true, displayModeBar: false });
    }

    plotEdo(data){
        const traces = [];

        if(data.vectors && data.vectors.length > 0){
            data.vectors.forEach((v, i) => {
                traces.push({
                    x: [v.t0, v.t1],
                    y: [v.y0, v.y1],
                    mode: "lines",
                    line: { color: "#334155", width: 1.8 },
                    showlegend: i === 0,
                    name: "Campo de Direções (Slope Field)",
                    hoverinfo: "none"
                });
            });
        }

        traces.push({
            x: data.ts,
            y: data.ys,
            mode: "lines+markers",
            name: `Trajetória Numérica (${data.metodo || ""})`,
            line: { color: "#2563eb", width: 2.6 },
            marker: { color: "#e11d48", size: 6 }
        });

        traces.push({
            x: [data.t0],
            y: [data.y0],
            mode: "markers",
            name: `Condição Inicial: y(t₀ = ${data.t0}) = ${data.y0}`,
            marker: { color: "#d97706", size: 11, symbol: "circle" }
        });

        const lastT = data.ts[data.ts.length - 1];
        const lastY = data.ys[data.ys.length - 1];
        traces.push({
            x: [lastT],
            y: [lastY],
            mode: "markers+text",
            name: `Valor Final: y(tₙ = ${lastT.toFixed(2)}) ≈ ${lastY.toFixed(4)}`,
            marker: { color: "#059669", size: 12, symbol: "diamond" },
            text: [`y(${lastT.toFixed(2)}) ≈ ${lastY.toFixed(4)}`],
            textposition: "top center",
            textfont: { size: 11, color: "#059669" }
        });

        const layout = this.getDefaultLayout(
            `Solução de EDO no Plano de Fase — ${data.metodo || ""}`,
            "Tempo (t)",
            "Variável de Estado y(t)"
        );

        Plotly.newPlot(this.containerId, traces, layout, { responsive: true, displayModeBar: false });
    }

    setDragMode(mode){
        const container = this.getContainer();
        if(!container || !window.Plotly){
            return;
        }
        this.currentMode = mode;
        Plotly.relayout(container, { dragmode: mode });
    }

    zoomIn(){
        const container = this.getContainer();
        if(!container || !window.Plotly){
            return;
        }
        Plotly.relayout(container, {
            'xaxis.range[0]': container._fullLayout.xaxis.range[0] * 0.8,
            'xaxis.range[1]': container._fullLayout.xaxis.range[1] * 0.8,
            'yaxis.range[0]': container._fullLayout.yaxis.range[0] * 0.8,
            'yaxis.range[1]': container._fullLayout.yaxis.range[1] * 0.8
        });
    }

    zoomOut(){
        const container = this.getContainer();
        if(!container || !window.Plotly){
            return;
        }
        Plotly.relayout(container, {
            'xaxis.range[0]': container._fullLayout.xaxis.range[0] * 1.25,
            'xaxis.range[1]': container._fullLayout.xaxis.range[1] * 1.25,
            'yaxis.range[0]': container._fullLayout.yaxis.range[0] * 1.25,
            'yaxis.range[1]': container._fullLayout.yaxis.range[1] * 1.25
        });
    }

    resetView(){
        const container = this.getContainer();
        if(!container || !window.Plotly){
            return;
        }
        Plotly.relayout(container, {
            'xaxis.autorange': true,
            'yaxis.autorange': true
        });
    }

    async savePlot(format = "png"){
        const container = this.getContainer();
        if(!container || !window.Plotly){
            return false;
        }
        try{
            await Plotly.downloadImage(container, {
                format: format,
                filename: `grafico_${this.currentModulo || 'metodo'}`,
                width: 1200,
                height: 800,
                scale: 2
            });
            return true;
        }catch(e){
            return false;
        }
    }
}

window.chartRenderer = new ChartRenderer();
