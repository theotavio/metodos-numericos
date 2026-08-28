class HistoryTableComponent {
    constructor(container){
        this.container = typeof container === "string" ? document.getElementById(container) : container;
        this.historyLines = [];
        this.gaussSteps = null;
        this.substPassos = null;
    }

    setGaussSteps(etapas, substituicaoPassos, rawLines = []){
        this.gaussSteps = etapas;
        this.substPassos = substituicaoPassos;
        this.historyLines = rawLines || [];
        this.renderGauss();
    }

    setHistory(lines){
        this.gaussSteps = null;
        this.substPassos = null;
        this.historyLines = lines || [];
        this.render();
    }

    _sub(n){
        const subs = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"];
        return String(n).split("").map(d => subs[parseInt(d, 10)] || d).join("");
    }

    renderGauss(){
        if(!this.container){
            return;
        }

        if(!this.gaussSteps || this.gaussSteps.length === 0){
            this.render();
            return;
        }

        let html = `<div class="matrix-steps-timeline">`;

        this.gaussSteps.forEach((step) => {
            const pivo = step.pivo_pos;
            const linhaAtiva = step.linha_ativa;
            const M = step.matriz;
            const numCols = M[0].length;

            html += `
                <div class="matrix-step-card">
                    <div class="matrix-step-header">
                        <div class="matrix-step-title">
                            <span>Etapa ${step.etapa_num}: ${step.titulo}</span>
                        </div>
                        <span class="matrix-op-badge">${step.operacao}</span>
                    </div>
                    <div class="matrix-step-desc">${step.descricao}</div>
                    
                    <div class="matrix-math-box">
                        <div class="matrix-bracket-container">
                            <table class="matrix-display-table">
                                <tbody>
            `;

            M.forEach((row, rIdx) => {
                html += `<tr>`;
                for(let cIdx = 0; cIdx < numCols - 1; cIdx++){
                    const val = row[cIdx];
                    let cellClass = "";
                    if(pivo && pivo[0] === rIdx && pivo[1] === cIdx && step.tipo !== "inicio"){
                        cellClass = "pivot-highlight";
                    }else if(val === 0 && rIdx > cIdx){
                        cellClass = "zero-eliminated";
                    }else if(linhaAtiva !== null && linhaAtiva === rIdx){
                        cellClass = "modified-row";
                    }

                    html += `<td class="${cellClass}">${val.toFixed(4)}</td>`;
                }

                const bVal = row[numCols - 1];
                html += `<td class="b-col">${bVal.toFixed(4)}</td>`;
                html += `</tr>`;
            });

            html += `
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            `;
        });

        if(this.substPassos && this.substPassos.length > 0){
            html += `
                <div class="matrix-step-card">
                    <div class="matrix-step-header">
                        <div class="matrix-step-title">
                            <span>Substituição Regressiva (Solução Final)</span>
                        </div>
                        <span class="matrix-op-badge" style="color: var(--success); background-color: var(--success-subtle); border-color: var(--success);">
                            Vetor Solução
                        </span>
                    </div>
                    <div class="matrix-step-desc">Resolução sequencial das incógnitas a partir da última linha da matriz escalonada:</div>
                    <div class="subst-step-box">
            `;

            this.substPassos.forEach((p) => {
                html += `<div class="subst-step-line">${p}</div>`;
            });

            html += `
                    </div>
                </div>
            `;
        }

        html += `</div>`;
        this.container.innerHTML = html;
    }

    render(){
        if(!this.container){
            return;
        }

        if(!this.historyLines || this.historyLines.length === 0){
            this.container.innerHTML = `
                <div class="plot-placeholder">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                    </svg>
                    <span>Nenhuma iteração realizada ainda.</span>
                </div>
            `;
            return;
        }

        const tableLines = this.historyLines.filter(l => l.includes("|"));
        const infoLines = this.historyLines.filter(l => !l.includes("|"));

        let html = `<div class="table-scroll-container">`;

        if(infoLines.length > 0){
            html += `<div style="padding: 14px 18px; font-family: var(--font-mono); font-size: 12px; background-color: var(--bg-sidebar); border-bottom: 1px solid var(--border); line-height: 1.6;">`;
            infoLines.forEach(il => {
                html += `<div>${il}</div>`;
            });
            html += `</div>`;
        }

        if(tableLines.length > 0){
            html += `<table class="modern-data-table"><thead><tr>`;
            const headerCols = tableLines[0].split("|").map(c => c.trim());
            const numCols = headerCols.length;

            headerCols.forEach(hc => {
                html += `<th>${hc}</th>`;
            });
            html += `</tr></thead><tbody>`;

            for(let i = 1; i < tableLines.length; i++){
                const cols = tableLines[i].split("|").map(c => c.trim());
                html += `<tr>`;
                for(let cIdx = 0; cIdx < numCols; cIdx++){
                    const val = (cIdx < cols.length) ? cols[cIdx] : "—";
                    html += `<td>${val}</td>`;
                }
                html += `</tr>`;
            }
            html += `</tbody></table>`;
        }

        html += `</div>`;
        this.container.innerHTML = html;
    }

    exportCSV(){
        if(!this.historyLines || this.historyLines.length === 0){
            return false;
        }
        const tableLines = this.historyLines.filter(l => l.includes("|"));
        if(tableLines.length === 0){
            const blob = new Blob([this.historyLines.join("\n")], { type: "text/plain;charset=utf-8" });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = `historico_calculo_${Date.now()}.txt`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            return true;
        }

        const csvRows = tableLines.map(l => {
            return l.split("|").map(c => `"${c.trim().replace(/"/g, '""')}"`).join(",");
        });

        const csvContent = "data:text/csv;charset=utf-8," + encodeURIComponent(csvRows.join("\n"));
        const link = document.createElement("a");
        link.setAttribute("href", csvContent);
        link.setAttribute("download", `tabela_iteracoes_${Date.now()}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        return true;
    }

    getTSV(){
        if(!this.historyLines || this.historyLines.length === 0){
            return "";
        }
        const tableLines = this.historyLines.filter(l => l.includes("|"));
        if(tableLines.length === 0){
            return this.historyLines.join("\n");
        }
        return tableLines.map(l => l.split("|").map(c => c.trim()).join("\t")).join("\n");
    }
}

window.HistoryTableComponent = HistoryTableComponent;
