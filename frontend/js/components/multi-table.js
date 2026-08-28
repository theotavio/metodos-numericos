class MultiTableComponent {
    constructor(container, options = {}){
        this.container = typeof container === "string" ? document.getElementById(container) : container;
        this.nObs = options.nObs || 5;
        this.nVars = options.nVars || 2;
        this.data = options.defaultData || [
            [50.0, 1.0, 150.0],
            [70.0, 2.0, 210.0],
            [85.0, 3.0, 270.0],
            [110.0, 3.0, 340.0],
            [130.0, 4.0, 410.0]
        ];
        this.init();
    }

    _sub(n){
        const subs = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"];
        return String(n).split("").map(d => subs[parseInt(d, 10)] || d).join("");
    }

    init(){
        this.render();
    }

    setDimensions(nObs, nVars){
        this.nObs = Math.max(3, Math.min(20, nObs));
        this.nVars = Math.max(1, Math.min(5, nVars));
        const newData = [];
        for(let i = 0; i < this.nObs; i++){
            const row = [];
            for(let j = 0; j < this.nVars + 1; j++){
                if(this.data[i] && this.data[i][j] !== undefined){
                    row.push(this.data[i][j]);
                }else{
                    row.push(0.0);
                }
            }
            newData.push(row);
        }
        this.data = newData;
        this.render();
    }

    setData(data, nObs, nVars){
        this.nObs = nObs || data.length;
        this.nVars = nVars || (data[0].length - 1);
        this.data = data;
        this.render();
    }

    getData(){
        const X = [];
        const y = [];

        for(let i = 0; i < this.nObs; i++){
            const xRow = [];
            for(let j = 0; j < this.nVars; j++){
                const inp = this.container.querySelector(`.multi-cell-x[data-row="${i}"][data-col="${j}"]`);
                xRow.push(inp ? parseFloat(inp.value) || 0.0 : 0.0);
            }
            X.push(xRow);
            const inpY = this.container.querySelector(`.multi-cell-y[data-row="${i}"]`);
            y.push(inpY ? parseFloat(inpY.value) || 0.0 : 0.0);
        }

        return { X, y, nObs: this.nObs, nVars: this.nVars };
    }

    render(){
        if(!this.container){
            return;
        }

        let html = `
            <div class="points-editor-wrapper">
                <div class="matrix-toolbar">
                    <label class="form-label" style="margin: 0;">Observações (N):</label>
                    <input type="number" min="3" max="20" class="form-control inp-n-obs" value="${this.nObs}" style="width: 60px; padding: 4px 6px;">
                    <label class="form-label" style="margin: 0; margin-left: 6px;">Variáveis (k):</label>
                    <input type="number" min="1" max="5" class="form-control inp-n-vars" value="${this.nVars}" style="width: 55px; padding: 4px 6px;">
                </div>

                <div class="multi-table-container">
                    <table class="multi-table">
                        <thead>
                            <tr>
                                <th style="width: 30px;">#</th>
        `;

        for(let j = 0; j < this.nVars; j++){
            html += `<th>x${this._sub(j + 1)}</th>`;
        }
        html += `
                                <th class="y-header">y (Alvo)</th>
                            </tr>
                        </thead>
                        <tbody>
        `;

        for(let i = 0; i < this.nObs; i++){
            html += `<tr><td style="color: var(--text-muted); font-size: 11px;">${i + 1}</td>`;
            for(let j = 0; j < this.nVars; j++){
                const val = (this.data[i] && this.data[i][j] !== undefined) ? this.data[i][j] : 0.0;
                html += `
                    <td>
                        <input type="number" step="any" class="multi-cell-x" data-row="${i}" data-col="${j}" value="${val}">
                    </td>
                `;
            }
            const yVal = (this.data[i] && this.data[i][this.nVars] !== undefined) ? this.data[i][this.nVars] : 0.0;
            html += `
                <td>
                    <input type="number" step="any" class="multi-cell-y" data-row="${i}" value="${yVal}" style="border-color: var(--primary); font-weight: 600;">
                </td>
            </tr>`;
        }

        html += `
                        </tbody>
                    </table>
                </div>
            </div>
        `;

        this.container.innerHTML = html;

        const inpObs = this.container.querySelector(".inp-n-obs");
        const inpVars = this.container.querySelector(".inp-n-vars");

        const updateDims = () => {
            const obs = parseInt(inpObs.value, 10) || 5;
            const vars = parseInt(inpVars.value, 10) || 2;
            this.setDimensions(obs, vars);
        };

        if(inpObs){
            inpObs.addEventListener("change", updateDims);
        }
        if(inpVars){
            inpVars.addEventListener("change", updateDims);
        }
    }
}

window.MultiTableComponent = MultiTableComponent;
