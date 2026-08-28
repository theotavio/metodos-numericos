class SistemasModuleController {
    constructor(container){
        this.container = typeof container === "string" ? document.getElementById(container) : container;
        this.matrixGrid = null;
    }

    render(metodo = "gauss"){
        let html = `
            <div id="sistemas-matrix-container"></div>
        `;

        if(metodo === "gauss_seidel"){
            html += `
                <div class="form-row" style="margin-top: 14px;">
                    <div class="form-group">
                        <label class="form-label" for="inp-sist-tol">Tolerância de Parada (ε)</label>
                        <input type="number" step="any" id="inp-sist-tol" class="form-control" value="0.000001">
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="inp-sist-iter">Máx. Iterações</label>
                        <input type="number" id="inp-sist-iter" class="form-control" value="100">
                    </div>
                </div>
            `;
        }

        this.container.innerHTML = html;

        const gridContainer = this.container.querySelector("#sistemas-matrix-container");
        this.matrixGrid = new MatrixGridComponent(gridContainer, {
            size: 3,
            minSize: 2,
            maxSize: 8
        });

        if(metodo === "gauss"){
            this.matrixGrid.setData(
                [[2.0, 1.0, -1.0], [-3.0, -1.0, 2.0], [-2.0, 1.0, 2.0]],
                [8.0, -11.0, -3.0]
            );
        }else if(metodo === "gauss_seidel"){
            this.matrixGrid.setData(
                [[10.0, 2.0, 1.0], [1.0, 10.0, -1.0], [2.0, -2.0, 10.0]],
                [14.0, 11.0, 26.0]
            );
        }
    }

    getPayload(metodo){
        if(!this.matrixGrid){
            return null;
        }
        const data = this.matrixGrid.getData();
        const payload = {
            metodo,
            A: data.A,
            b: data.b
        };

        if(metodo === "gauss_seidel"){
            payload.tol = parseFloat(this.container.querySelector("#inp-sist-tol")?.value) || 1e-6;
            payload.max_iter = parseInt(this.container.querySelector("#inp-sist-iter")?.value, 10) || 100;
        }

        return payload;
    }

    applyPreset(presetData){
        if(this.matrixGrid && presetData.A && presetData.b){
            this.matrixGrid.setData(presetData.A, presetData.b);
        }
        const inpTol = this.container.querySelector("#inp-sist-tol");
        const inpIter = this.container.querySelector("#inp-sist-iter");
        if(inpTol && presetData.tol !== undefined) inpTol.value = presetData.tol;
        if(inpIter && presetData.max_iter !== undefined) inpIter.value = presetData.max_iter;
    }
}

window.SistemasModuleController = SistemasModuleController;
