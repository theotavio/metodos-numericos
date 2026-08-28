class RaizesModuleController {
    constructor(container){
        this.container = typeof container === "string" ? document.getElementById(container) : container;
    }

    render(metodo = "bissecao"){
        let html = `
            <div class="form-group">
                <label class="form-label" for="inp-raizes-func">
                    ${metodo === "iteracao_linear" ? "Função de Iteração φ(x)" : "Função f(x)"}
                </label>
                <input type="text" id="inp-raizes-func" class="form-control" 
                       placeholder="${metodo === "iteracao_linear" ? "(x+2)**(1/3)" : "x**3 - x - 2"}" 
                       value="${metodo === "iteracao_linear" ? "(x+2)**(1/3)" : "x**3 - x - 2"}">
            </div>
        `;

        if(metodo === "bissecao" || metodo === "cordas" || metodo === "pegaso"){
            html += `
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label" for="inp-raizes-a">Limite Inferior (a)</label>
                        <input type="number" step="any" id="inp-raizes-a" class="form-control" value="1.0">
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="inp-raizes-b">Limite Superior (b)</label>
                        <input type="number" step="any" id="inp-raizes-b" class="form-control" value="2.0">
                    </div>
                </div>
            `;
        }else if(metodo === "newton"){
            html += `
                <div class="form-group">
                    <label class="form-label" for="inp-raizes-x0">Estimativa Inicial (x₀)</label>
                    <input type="number" step="any" id="inp-raizes-x0" class="form-control" value="1.5">
                </div>
                <div class="form-group">
                    <label class="form-label" for="sel-raizes-deriv">Modo de Cálculo da Derivada f'(x)</label>
                    <select id="sel-raizes-deriv" class="form-select">
                        <option value="simbolica" selected>Simbólica [ SymPy / Analítica ]</option>
                        <option value="central">Diferença Finita Central [ O(h²) ]</option>
                        <option value="progressiva">Diferença Finita Progressiva [ O(h) ]</option>
                        <option value="regressiva">Diferença Finita Regressiva [ O(h) ]</option>
                        <option value="complexa">Passo Complexo [ Complex-Step ]</option>
                        <option value="manual">Manual [ Inserir f'(x) ]</option>
                    </select>
                </div>
                <div id="wrapper-raizes-h" class="form-group" style="display: none;">
                    <label class="form-label" for="inp-raizes-h">Passo de Diferenciação (h)</label>
                    <input type="number" step="any" id="inp-raizes-h" class="form-control" value="0.000001">
                </div>
                <div id="wrapper-raizes-df" class="form-group" style="display: none;">
                    <label class="form-label" for="inp-raizes-df">Expressão Analítica de f'(x)</label>
                    <input type="text" id="inp-raizes-df" class="form-control" placeholder="3*x**2 - 1">
                </div>
            `;
        }else if(metodo === "secante"){
            html += `
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label" for="inp-raizes-x0">Primeiro Chute (x₀)</label>
                        <input type="number" step="any" id="inp-raizes-x0" class="form-control" value="1.0">
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="inp-raizes-x1">Segundo Chute (x₁)</label>
                        <input type="number" step="any" id="inp-raizes-x1" class="form-control" value="2.0">
                    </div>
                </div>
            `;
        }else if(metodo === "iteracao_linear"){
            html += `
                <div class="form-group">
                    <label class="form-label" for="inp-raizes-x0">Estimativa Inicial (x₀)</label>
                    <input type="number" step="any" id="inp-raizes-x0" class="form-control" value="1.5">
                </div>
            `;
        }

        html += `
            <div class="form-row">
                <div class="form-group">
                    <label class="form-label" for="inp-raizes-tol">Tolerância (ε)</label>
                    <input type="number" step="any" id="inp-raizes-tol" class="form-control" value="0.000001">
                </div>
                <div class="form-group">
                    <label class="form-label" for="inp-raizes-iter">Máx. Iterações</label>
                    <input type="number" id="inp-raizes-iter" class="form-control" value="100">
                </div>
            </div>
        `;

        this.container.innerHTML = html;

        if(metodo === "newton"){
            const selDeriv = this.container.querySelector("#sel-raizes-deriv");
            const wrapH = this.container.querySelector("#wrapper-raizes-h");
            const wrapDf = this.container.querySelector("#wrapper-raizes-df");

            if(selDeriv){
                selDeriv.addEventListener("change", () => {
                    const val = selDeriv.value;
                    wrapH.style.display = (val === "central" || val === "progressiva" || val === "regressiva" || val === "complexa") ? "block" : "none";
                    wrapDf.style.display = (val === "manual") ? "block" : "none";
                });
            }
        }
    }

    getPayload(metodo){
        const funcao = this.container.querySelector("#inp-raizes-func")?.value.trim() || "";
        const tol = parseFloat(this.container.querySelector("#inp-raizes-tol")?.value) || 1e-6;
        const max_iter = parseInt(this.container.querySelector("#inp-raizes-iter")?.value, 10) || 100;

        const payload = {
            metodo,
            funcao,
            tol,
            max_iter
        };

        if(metodo === "bissecao" || metodo === "cordas" || metodo === "pegaso"){
            payload.a = parseFloat(this.container.querySelector("#inp-raizes-a")?.value);
            payload.b = parseFloat(this.container.querySelector("#inp-raizes-b")?.value);
        }else if(metodo === "newton"){
            payload.x0 = parseFloat(this.container.querySelector("#inp-raizes-x0")?.value);
            payload.tipo_derivada = this.container.querySelector("#sel-raizes-deriv")?.value || "simbolica";
            payload.h_derivada = parseFloat(this.container.querySelector("#inp-raizes-h")?.value) || 1e-6;
            payload.df_manual = this.container.querySelector("#inp-raizes-df")?.value.trim() || null;
        }else if(metodo === "secante"){
            payload.x0 = parseFloat(this.container.querySelector("#inp-raizes-x0")?.value);
            payload.x1 = parseFloat(this.container.querySelector("#inp-raizes-x1")?.value);
        }else if(metodo === "iteracao_linear"){
            payload.x0 = parseFloat(this.container.querySelector("#inp-raizes-x0")?.value);
        }

        return payload;
    }

    applyPreset(presetData){
        const inpFunc = this.container.querySelector("#inp-raizes-func");
        const inpA = this.container.querySelector("#inp-raizes-a");
        const inpB = this.container.querySelector("#inp-raizes-b");
        const inpX0 = this.container.querySelector("#inp-raizes-x0");
        const inpX1 = this.container.querySelector("#inp-raizes-x1");
        const selDeriv = this.container.querySelector("#sel-raizes-deriv");
        const inpH = this.container.querySelector("#inp-raizes-h");
        const inpDf = this.container.querySelector("#inp-raizes-df");
        const inpTol = this.container.querySelector("#inp-raizes-tol");
        const inpIter = this.container.querySelector("#inp-raizes-iter");

        if(inpFunc && presetData.funcao) inpFunc.value = presetData.funcao;
        if(inpA && presetData.a !== undefined) inpA.value = presetData.a;
        if(inpB && presetData.b !== undefined) inpB.value = presetData.b;
        if(inpX0 && presetData.x0 !== undefined) inpX0.value = presetData.x0;
        if(inpX1 && presetData.x1 !== undefined) inpX1.value = presetData.x1;
        if(inpTol && presetData.tol !== undefined) inpTol.value = presetData.tol;
        if(inpIter && presetData.max_iter !== undefined) inpIter.value = presetData.max_iter;

        if(selDeriv && presetData.tipo_derivada){
            selDeriv.value = presetData.tipo_derivada;
            selDeriv.dispatchEvent(new Event("change"));
        }
        if(inpH && presetData.h_derivada !== undefined) inpH.value = presetData.h_derivada;
        if(inpDf && presetData.df_manual) inpDf.value = presetData.df_manual;
    }
}

window.RaizesModuleController = RaizesModuleController;
