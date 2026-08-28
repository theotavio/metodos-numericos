class AjusteModuleController {
    constructor(container){
        this.container = typeof container === "string" ? document.getElementById(container) : container;
        this.pointsTable = null;
        this.multiTable = null;
    }

    render(metodo = "simples"){
        if(metodo === "simples"){
            this.container.innerHTML = `
                <div id="ajuste-points-container"></div>
            `;
            const ptsContainer = this.container.querySelector("#ajuste-points-container");
            this.pointsTable = new PointsTableComponent(ptsContainer, {
                minPoints: 2,
                defaultPoints: [[1.0, 2.1], [2.0, 3.9], [3.0, 6.2], [4.0, 7.8], [5.0, 10.1]]
            });
            this.multiTable = null;
        }else{
            this.container.innerHTML = `
                <div id="ajuste-multi-container"></div>
            `;
            const multiContainer = this.container.querySelector("#ajuste-multi-container");
            this.multiTable = new MultiTableComponent(multiContainer, {
                nObs: 5,
                nVars: 2
            });
            this.pointsTable = null;
        }
    }

    getPayload(metodo){
        if(metodo === "simples"){
            if(!this.pointsTable){
                return null;
            }
            return {
                metodo: "simples",
                pontos: this.pointsTable.getPoints()
            };
        }else{
            if(!this.multiTable){
                return null;
            }
            const data = this.multiTable.getData();
            return {
                metodo: "multiplo",
                X: data.X,
                y: data.y
            };
        }
    }

    applyPreset(presetData){
        if(presetData.metodo === "simples" && this.pointsTable && presetData.pontos){
            this.pointsTable.setPoints(presetData.pontos);
        }else if(presetData.metodo === "multiplo" && this.multiTable && presetData.dados){
            this.multiTable.setData(presetData.dados, presetData.n_obs, presetData.n_vars);
        }
    }
}

window.AjusteModuleController = AjusteModuleController;
