class InterpolacaoModuleController {
    constructor(container){
        this.container = typeof container === "string" ? document.getElementById(container) : container;
        this.pointsTable = null;
    }

    render(metodo = "lagrange"){
        let minPts = 2;
        let defaultPts = [[0.0, 1.0], [1.0, 3.0], [2.0, 2.0], [3.0, 5.0]];

        if(metodo === "quadratica"){
            minPts = 3;
            defaultPts = [[1.0, 2.0], [2.0, 5.0], [4.0, 17.0]];
        }else if(metodo === "linear"){
            minPts = 2;
            defaultPts = [[0.0, 0.0], [2.0, 14.0], [4.0, 48.0], [6.0, 102.0]];
        }

        let html = `
            <div class="form-group">
                <label class="form-label" for="inp-interp-xalvo">Ponto Alvo de Interpolação (x*)</label>
                <input type="number" step="any" id="inp-interp-xalvo" class="form-control" value="1.5">
            </div>
            <div id="interpolacao-points-container" style="margin-top: 10px;"></div>
        `;

        if(metodo === "quadratica"){
            html += `<div class="form-helper-note" style="margin-top: 10px;">Aviso: A interpolação quadrática exige exatamente 3 pontos.</div>`;
        }

        this.container.innerHTML = html;

        const ptsContainer = this.container.querySelector("#interpolacao-points-container");
        this.pointsTable = new PointsTableComponent(ptsContainer, {
            minPoints: minPts,
            defaultPoints: defaultPts
        });
    }

    getPayload(metodo){
        if(!this.pointsTable){
            return null;
        }
        const pontos = this.pointsTable.getPoints();
        const x_alvo = parseFloat(this.container.querySelector("#inp-interp-xalvo")?.value) || 0.0;

        return {
            metodo,
            pontos,
            x_alvo
        };
    }

    applyPreset(presetData){
        if(presetData.x_alvo !== undefined){
            const inpX = this.container.querySelector("#inp-interp-xalvo");
            if(inpX) inpX.value = presetData.x_alvo;
        }
        if(this.pointsTable && presetData.pontos){
            this.pointsTable.setPoints(presetData.pontos);
        }
    }
}

window.InterpolacaoModuleController = InterpolacaoModuleController;
