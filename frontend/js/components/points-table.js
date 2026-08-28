class PointsTableComponent {
    constructor(container, options = {}){
        this.container = typeof container === "string" ? document.getElementById(container) : container;
        this.minPoints = options.minPoints || 2;
        this.points = options.defaultPoints || [[0.0, 1.0], [1.0, 3.0], [2.0, 2.0], [3.0, 5.0]];
        this.init();
    }

    init(){
        this.render();
    }

    setPoints(points){
        if(!points || !Array.isArray(points)){
            return;
        }
        this.points = points.map(p => [parseFloat(p[0]) || 0.0, parseFloat(p[1]) || 0.0]);
        this.render();
    }

    getPoints(){
        const rows = this.container.querySelectorAll(".point-row");
        const pts = [];
        rows.forEach(r => {
            const xInput = r.querySelector(".pt-x");
            const yInput = r.querySelector(".pt-y");
            if(xInput && yInput){
                pts.push([parseFloat(xInput.value) || 0.0, parseFloat(yInput.value) || 0.0]);
            }
        });
        return pts;
    }

    addPoint(x = 0.0, y = 0.0){
        this.points = this.getPoints();
        this.points.push([x, y]);
        this.render();
    }

    removePoint(index){
        this.points = this.getPoints();
        if(this.points.length > this.minPoints){
            this.points.splice(index, 1);
            this.render();
        }
    }

    render(){
        if(!this.container){
            return;
        }

        let html = `
            <div class="points-editor-wrapper">
                <div class="points-toolbar">
                    <button type="button" class="btn btn-ghost btn-sm btn-add-point">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="12" y1="5" x2="12" y2="19"></line>
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                        </svg>
                        <span>Adicionar Ponto</span>
                    </button>
                    <button type="button" class="btn btn-ghost btn-sm btn-clear-points">Limpar</button>
                    <span style="font-size: 11px; color: var(--text-muted); margin-left: auto;">Total: ${this.points.length} nós</span>
                </div>

                <div class="points-table-container">
                    <table class="points-table">
                        <thead>
                            <tr>
                                <th style="width: 35px;">i</th>
                                <th>Abscissa (xᵢ)</th>
                                <th>Ordenada (yᵢ)</th>
                                <th style="width: 40px;"></th>
                            </tr>
                        </thead>
                        <tbody>
        `;

        this.points.forEach((p, idx) => {
            html += `
                <tr class="point-row" data-index="${idx}">
                    <td style="color: var(--text-muted); font-size: 11px;">${idx + 1}</td>
                    <td>
                        <input type="number" step="any" class="pt-x" value="${p[0]}">
                    </td>
                    <td>
                        <input type="number" step="any" class="pt-y" value="${p[1]}">
                    </td>
                    <td>
                        <button type="button" class="points-row-btn-delete" data-index="${idx}" title="Remover ponto">
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </td>
                </tr>
            `;
        });

        html += `
                        </tbody>
                    </table>
                </div>
            </div>
        `;

        this.container.innerHTML = html;

        const btnAdd = this.container.querySelector(".btn-add-point");
        if(btnAdd){
            btnAdd.addEventListener("click", () => {
                const current = this.getPoints();
                const lastX = current.length > 0 ? current[current.length - 1][0] : 0.0;
                this.addPoint(lastX + 1.0, 0.0);
            });
        }

        const btnClear = this.container.querySelector(".btn-clear-points");
        if(btnClear){
            btnClear.addEventListener("click", () => {
                const empty = [];
                for(let i = 0; i < this.minPoints; i++){
                    empty.push([i, 0.0]);
                }
                this.setPoints(empty);
            });
        }

        const deleteBtns = this.container.querySelectorAll(".points-row-btn-delete");
        deleteBtns.forEach(btn => {
            btn.addEventListener("click", (e) => {
                const idx = parseInt(btn.getAttribute("data-index"), 10);
                this.removePoint(idx);
            });
        });
    }
}

window.PointsTableComponent = PointsTableComponent;
