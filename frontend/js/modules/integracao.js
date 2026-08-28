class IntegracaoModuleController {
    constructor(container){
        this.container = typeof container === "string" ? document.getElementById(container) : container;
    }

    render(metodo = "simpson13"){
        let html = `
            <div class="form-group">
                <label class="form-label" for="inp-integ-func">Função Integranda f(x)</label>
                <input type="text" id="inp-integ-func" class="form-control" placeholder="x**2" value="x**2">
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label class="form-label" for="inp-integ-a">Limite Inferior (a)</label>
                    <input type="number" step="any" id="inp-integ-a" class="form-control" value="0.0">
                </div>
                <div class="form-group">
                    <label class="form-label" for="inp-integ-b">Limite Superior (b)</label>
                    <input type="number" step="any" id="inp-integ-b" class="form-control" value="2.0">
                </div>
            </div>
        `;

        if(metodo !== "gauss2p"){
            const defaultN = (metodo === "simpson38") ? 6 : (metodo === "simpson13" ? 6 : 10);
            html += `
                <div class="form-group">
                    <label class="form-label" for="inp-integ-n">Número de Subintervalos (n)</label>
                    <input type="number" id="inp-integ-n" class="form-control" value="${defaultN}">
                </div>
            `;
            if(metodo === "simpson13"){
                html += `<div class="form-helper-note">Aviso: A Regra 1/3 de Simpson exige 'n' PAR.</div>`;
            }else if(metodo === "simpson38"){
                html += `<div class="form-helper-note">Aviso: A Regra 3/8 de Simpson exige 'n' MÚLTIPLO DE 3.</div>`;
            }
        }else{
            html += `<div class="form-helper-note">Quadratura Gaussiana utiliza 2 pontos de Legendre tabelados (exatidão polinomial de grau ≤ 3).</div>`;
        }

        this.container.innerHTML = html;
    }

    getPayload(metodo){
        const funcao = this.container.querySelector("#inp-integ-func")?.value.trim() || "";
        const a = parseFloat(this.container.querySelector("#inp-integ-a")?.value) || 0.0;
        const b = parseFloat(this.container.querySelector("#inp-integ-b")?.value) || 1.0;
        const inpN = this.container.querySelector("#inp-integ-n");
        const n = inpN ? parseInt(inpN.value, 10) || 10 : 2;

        return {
            metodo,
            funcao,
            a,
            b,
            n
        };
    }

    applyPreset(presetData){
        const inpFunc = this.container.querySelector("#inp-integ-func");
        const inpA = this.container.querySelector("#inp-integ-a");
        const inpB = this.container.querySelector("#inp-integ-b");
        const inpN = this.container.querySelector("#inp-integ-n");

        if(inpFunc && presetData.funcao) inpFunc.value = presetData.funcao;
        if(inpA && presetData.a !== undefined) inpA.value = presetData.a;
        if(inpB && presetData.b !== undefined) inpB.value = presetData.b;
        if(inpN && presetData.n !== undefined) inpN.value = presetData.n;
    }
}

window.IntegracaoModuleController = IntegracaoModuleController;
