class MatrixGridComponent {
    constructor(container, options = {}){
        this.container = typeof container === "string" ? document.getElementById(container) : container;
        this.size = options.size || 3;
        this.minSize = options.minSize || 2;
        this.maxSize = options.maxSize || 8;
        this.A = [];
        this.b = [];
        this.init();
    }

    _sub(n){
        const subs = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"];
        return String(n).split("").map(d => subs[parseInt(d, 10)] || d).join("");
    }

    init(){
        this.render();
    }

    setSize(n){
        this.size = Math.max(this.minSize, Math.min(this.maxSize, n));
        this.render();
    }

    setData(A, b){
        this.size = b.length;
        this.render();
        for(let i = 0; i < this.size; i++){
            for(let j = 0; j < this.size; j++){
                const input = this.container.querySelector(`.matrix-cell-a[data-row="${i}"][data-col="${j}"]`);
                if(input && A[i] && A[i][j] !== undefined){
                    input.value = A[i][j];
                }
            }
            const inputB = this.container.querySelector(`.matrix-cell-b[data-row="${i}"]`);
            if(inputB && b[i] !== undefined){
                inputB.value = b[i];
            }
        }
    }

    getData(){
        const A = [];
        const b = [];

        for(let i = 0; i < this.size; i++){
            const row = [];
            for(let j = 0; j < this.size; j++){
                const input = this.container.querySelector(`.matrix-cell-a[data-row="${i}"][data-col="${j}"]`);
                row.push(input ? parseFloat(input.value) || 0.0 : 0.0);
            }
            A.push(row);
            const inputB = this.container.querySelector(`.matrix-cell-b[data-row="${i}"]`);
            b.push(inputB ? parseFloat(inputB.value) || 0.0 : 0.0);
        }

        return { A, b, n: this.size };
    }

    render(){
        if(!this.container){
            return;
        }

        let html = `
            <div class="matrix-editor-wrapper">
                <div class="matrix-toolbar">
                    <label class="form-label" style="margin: 0;">Dimensão (n):</label>
                    <select class="form-select matrix-size-select" style="width: 80px; padding: 4px 8px;">
        `;

        for(let s = this.minSize; s <= this.maxSize; s++){
            html += `<option value="${s}" ${s === this.size ? "selected" : ""}>${s} × ${s}</option>`;
        }

        html += `
                    </select>
                    <button type="button" class="btn btn-ghost btn-sm btn-matrix-identity" title="Preencher com Matriz Identidade">Identidade</button>
                    <button type="button" class="btn btn-ghost btn-sm btn-matrix-clear" title="Zerar todos os coeficientes">Zerar</button>
                </div>

                <div class="matrix-grid-scroll">
                    <table class="matrix-grid-table">
                        <thead>
                            <tr>
        `;

        for(let j = 0; j < this.size; j++){
            html += `<th class="matrix-header-cell">x${this._sub(j + 1)}</th>`;
        }
        html += `
                                <th class="matrix-sep-cell">|</th>
                                <th class="matrix-header-cell b-header">b</th>
                            </tr>
                        </thead>
                        <tbody>
        `;

        for(let i = 0; i < this.size; i++){
            html += `<tr>`;
            for(let j = 0; j < this.size; j++){
                const defaultVal = (i === j) ? "1.0" : "0.0";
                html += `
                    <td>
                        <input type="number" step="any" class="matrix-input-cell matrix-cell-a" 
                               data-row="${i}" data-col="${j}" value="${defaultVal}">
                    </td>
                `;
            }
            html += `
                <td class="matrix-sep-cell">|</td>
                <td>
                    <input type="number" step="any" class="matrix-input-cell matrix-cell-b b-cell" 
                           data-row="${i}" value="0.0">
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

        const sizeSelect = this.container.querySelector(".matrix-size-select");
        if(sizeSelect){
            sizeSelect.addEventListener("change", (e) => {
                this.setSize(parseInt(e.target.value, 10));
            });
        }

        const btnId = this.container.querySelector(".btn-matrix-identity");
        if(btnId){
            btnId.addEventListener("click", () => {
                for(let i = 0; i < this.size; i++){
                    for(let j = 0; j < this.size; j++){
                        const input = this.container.querySelector(`.matrix-cell-a[data-row="${i}"][data-col="${j}"]`);
                        if(input){
                            input.value = (i === j) ? "1.0" : "0.0";
                        }
                    }
                    const inputB = this.container.querySelector(`.matrix-cell-b[data-row="${i}"]`);
                    if(inputB){
                        inputB.value = "0.0";
                    }
                }
            });
        }

        const btnClear = this.container.querySelector(".btn-matrix-clear");
        if(btnClear){
            btnClear.addEventListener("click", () => {
                const inputs = this.container.querySelectorAll(".matrix-input-cell");
                inputs.forEach(inp => inp.value = "0.0");
            });
        }
    }
}

window.MatrixGridComponent = MatrixGridComponent;
