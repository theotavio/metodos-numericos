class EdoModuleController {
    constructor(container){
        this.container = typeof container === "string" ? document.getElementById(container) : container;
    }

    render(metodo = "rk4"){
        let html = `
            <div class="form-group">
                <label class="form-label" for="inp-edo-func">Equação Diferencial dy/dt = f(t, y)</label>
                <input type="text" id="inp-edo-func" class="form-control" placeholder="y - t**2 + 1" value="y - t**2 + 1">
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label class="form-label" for="inp-edo-t0">Tempo Inicial (t₀)</label>
                    <input type="number" step="any" id="inp-edo-t0" class="form-control" value="0.0">
                </div>
                <div class="form-group">
                    <label class="form-label" for="inp-edo-y0">Condição Inicial y(t₀)</label>
                    <input type="number" step="any" id="inp-edo-y0" class="form-control" value="0.5">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label class="form-label" for="inp-edo-tn">Tempo Final (tₙ)</label>
                    <input type="number" step="any" id="inp-edo-tn" class="form-control" value="2.0">
                </div>
                <div class="form-group">
                    <label class="form-label" for="inp-edo-h">Tamanho do Passo (h = Δt)</label>
                    <input type="number" step="any" id="inp-edo-h" class="form-control" value="0.2">
                </div>
            </div>
        `;

        this.container.innerHTML = html;
    }

    getPayload(metodo){
        const funcao = this.container.querySelector("#inp-edo-func")?.value.trim() || "";
        const t0 = parseFloat(this.container.querySelector("#inp-edo-t0")?.value) || 0.0;
        const y0 = parseFloat(this.container.querySelector("#inp-edo-y0")?.value) || 0.0;
        const tn = parseFloat(this.container.querySelector("#inp-edo-tn")?.value) || 1.0;
        const h = parseFloat(this.container.querySelector("#inp-edo-h")?.value) || 0.1;

        return {
            metodo,
            funcao,
            t0,
            y0,
            tn,
            h
        };
    }

    applyPreset(presetData){
        const inpFunc = this.container.querySelector("#inp-edo-func");
        const inpT0 = this.container.querySelector("#inp-edo-t0");
        const inpY0 = this.container.querySelector("#inp-edo-y0");
        const inpTn = this.container.querySelector("#inp-edo-tn");
        const inpH = this.container.querySelector("#inp-edo-h");

        if(inpFunc && presetData.funcao) inpFunc.value = presetData.funcao;
        if(inpT0 && presetData.t0 !== undefined) inpT0.value = presetData.t0;
        if(inpY0 && presetData.y0 !== undefined) inpY0.value = presetData.y0;
        if(inpTn && presetData.tn !== undefined) inpTn.value = presetData.tn;
        if(inpH && presetData.h !== undefined) inpH.value = presetData.h;
    }
}

window.EdoModuleController = EdoModuleController;
