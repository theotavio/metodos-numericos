document.addEventListener("DOMContentLoaded", async () => {
    const sidebar = document.getElementById("sidebar");
    const btnSidebarToggle = document.getElementById("btn-sidebar-toggle");
    const selectMetodo = document.getElementById("select-metodo");
    const selectPreset = document.getElementById("select-preset");
    const formContainer = document.getElementById("module-form-container");
    const btnExecutar = document.getElementById("btn-executar");
    const btnLimpar = document.getElementById("btn-limpar");
    const statusBadge = document.getElementById("status-badge");
    const executionTimeLabel = document.getElementById("execution-time");
    
    const btnCopiarResumo = document.getElementById("btn-copiar-resumo");
    const btnExportCsv = document.getElementById("btn-export-csv");
    const btnSavePlot = document.getElementById("btn-save-plot");

    const btnPlotPan = document.getElementById("btn-plot-pan");
    const btnPlotZoom = document.getElementById("btn-plot-zoom");
    const btnPlotZoomIn = document.getElementById("btn-plot-zoomin");
    const btnPlotZoomOut = document.getElementById("btn-plot-zoomout");
    const btnPlotReset = document.getElementById("btn-plot-reset");

    const modalDisclaimerBackdrop = document.getElementById("modal-disclaimer-backdrop");
    const modalDisclaimerClose = document.getElementById("modal-disclaimer-close");
    const chkDisclaimerDontShow = document.getElementById("chk-disclaimer-dontshow");

    const modalServerLoadingBackdrop = document.getElementById("modal-server-loading-backdrop");
    const serverLoadingStatusText = document.getElementById("server-loading-status-text");

    const modalErrorBackdrop = document.getElementById("modal-error-backdrop");
    const modalErrorTitle = document.getElementById("modal-error-title");
    const modalErrorBody = document.getElementById("modal-error-body");
    const modalErrorClose = document.getElementById("modal-error-close");

    const modalAboutBackdrop = document.getElementById("modal-about-backdrop");
    const modalAboutClose = document.getElementById("modal-about-close");
    const btnOpenAbout = document.getElementById("btn-open-about");
    const btnCopyEmail = document.getElementById("btn-copy-email");
    const aboutEmailText = document.getElementById("about-email-text");

    const modalLicenseBackdrop = document.getElementById("modal-license-backdrop");
    const modalLicenseClose = document.getElementById("modal-license-close");
    const btnOpenLicense = document.getElementById("btn-open-license");
    const licenseTextContainer = document.getElementById("license-text-container");

    const moduleHeaderTitle = document.getElementById("module-header-title");
    const moduleHeaderSymbol = document.getElementById("module-header-symbol");
    const moduleHeaderSubtitle = document.getElementById("module-header-subtitle");

    const summaryTitle = document.getElementById("summary-title");
    const kpisGrid = document.getElementById("kpis-grid");
    const summaryMathDetails = document.getElementById("summary-math-details");

    const historyTable = new HistoryTableComponent("history-table-container");

    const moduleControllers = {
        raizes: new RaizesModuleController(formContainer),
        sistemas: new SistemasModuleController(formContainer),
        interpolacao: new InterpolacaoModuleController(formContainer),
        ajuste: new AjusteModuleController(formContainer),
        integracao: new IntegracaoModuleController(formContainer),
        edo: new EdoModuleController(formContainer)
    };

    let modulosCatalog = [];
    let currentModuleId = "raizes";
    let currentMetodoId = "bissecao";
    let currentPresets = {};
    let lastCalculationResponse = null;

    function checkAndShowDisclaimer(){
        const dismissed = localStorage.getItem("numericos_disclaimer_dismissed");
        if(dismissed !== "true" && modalDisclaimerBackdrop){
            modalDisclaimerBackdrop.classList.add("open");
        }
    }

    if(modalDisclaimerClose){
        modalDisclaimerClose.addEventListener("click", () => {
            if(chkDisclaimerDontShow && chkDisclaimerDontShow.checked){
                localStorage.setItem("numericos_disclaimer_dismissed", "true");
            }
            modalDisclaimerBackdrop.classList.remove("open");
        });
    }

    function showToast(message, type = "info", duration = 3000){
        const container = document.getElementById("toast-container");
        if(!container){
            return;
        }

        const toast = document.createElement("div");
        toast.className = `toast-message ${type}`;
        toast.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            <span>${message}</span>
        `;

        container.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateY(10px)";
            toast.style.transition = "all 0.2s ease";
            setTimeout(() => toast.remove(), 250);
        }, duration);
    }

    function setStatus(state, message, timeMs = null){
        statusBadge.className = `status-badge ${state}`;
        const dot = statusBadge.querySelector(".status-dot") || document.createElement("span");
        dot.className = "status-dot";
        statusBadge.innerHTML = "";
        statusBadge.appendChild(dot);

        const textSpan = document.createElement("span");
        textSpan.textContent = message;
        statusBadge.appendChild(textSpan);

        if(timeMs !== null){
            executionTimeLabel.textContent = `(${timeMs.toFixed(1)} ms)`;
        }else{
            executionTimeLabel.textContent = "";
        }
    }

    function showErrorModal(title, message){
        modalErrorTitle.textContent = title || "Falha no Cálculo Numérico";
        modalErrorBody.textContent = message || "Ocorreu um erro inesperado ao executar o método.";
        modalErrorBackdrop.classList.add("open");
    }

    modalErrorClose.addEventListener("click", () => {
        modalErrorBackdrop.classList.remove("open");
    });

    const inpApiUrl = document.getElementById("inp-api-url");
    const btnSaveApiUrl = document.getElementById("btn-save-api-url");

    if(modalAboutClose){
        modalAboutClose.addEventListener("click", () => {
            modalAboutBackdrop.classList.remove("open");
        });
    }

    if(btnOpenAbout){
        btnOpenAbout.addEventListener("click", async () => {
            if(inpApiUrl){
                inpApiUrl.value = window.apiClient.baseUrl;
            }
            modalAboutBackdrop.classList.add("open");
        });
    }

    if(btnSaveApiUrl && inpApiUrl){
        btnSaveApiUrl.addEventListener("click", async () => {
            const newUrl = inpApiUrl.value.trim();
            window.apiClient.setBaseUrl(newUrl);
            modalAboutBackdrop.classList.remove("open");
            showToast("URL da API atualizada! Verificando conexão...", "info");
            await ensureServerReady();
            await loadCatalog();
            await switchModule(currentModuleId);
        });
    }

    if(btnCopyEmail && aboutEmailText){
        btnCopyEmail.addEventListener("click", () => {
            const email = aboutEmailText.textContent.trim();
            navigator.clipboard.writeText(email).then(() => {
                showToast("E-mail copiado para a Área de Transferência!", "success");
            });
        });
    }

    if(modalLicenseClose){
        modalLicenseClose.addEventListener("click", () => {
            modalLicenseBackdrop.classList.remove("open");
        });
    }

    if(btnOpenLicense){
        btnOpenLicense.addEventListener("click", async () => {
            modalLicenseBackdrop.classList.add("open");
            try{
                const data = await window.apiClient.getLicenca();
                if(licenseTextContainer){
                    licenseTextContainer.textContent = data.texto;
                }
            }catch(e){
                if(licenseTextContainer){
                    licenseTextContainer.textContent = "MIT License - Copyright (c) 2026 Otávio";
                }
            }
        });
    }

    window.addEventListener("click", (e) => {
        if(e.target === modalDisclaimerBackdrop){
            modalDisclaimerBackdrop.classList.remove("open");
        }
        if(e.target === modalErrorBackdrop){
            modalErrorBackdrop.classList.remove("open");
        }
        if(e.target === modalAboutBackdrop){
            modalAboutBackdrop.classList.remove("open");
        }
        if(e.target === modalLicenseBackdrop){
            modalLicenseBackdrop.classList.remove("open");
        }
    });

    window.addEventListener("keydown", (e) => {
        if(e.key === "Escape"){
            if(modalDisclaimerBackdrop){
                modalDisclaimerBackdrop.classList.remove("open");
            }
            if(modalErrorBackdrop){
                modalErrorBackdrop.classList.remove("open");
            }
            if(modalAboutBackdrop){
                modalAboutBackdrop.classList.remove("open");
            }
            if(modalLicenseBackdrop){
                modalLicenseBackdrop.classList.remove("open");
            }
        }
    });

    if(btnSidebarToggle && sidebar){
        btnSidebarToggle.addEventListener("click", () => {
            sidebar.classList.toggle("collapsed");
            setTimeout(() => {
                if(window.Plotly && document.getElementById("plot-canvas")){
                    window.Plotly.Plots.resize(document.getElementById("plot-canvas"));
                }
            }, 300);
        });
    }

    if(btnPlotPan){
        btnPlotPan.addEventListener("click", () => {
            window.chartRenderer.setDragMode("pan");
            btnPlotPan.classList.add("active");
            if(btnPlotZoom){
                btnPlotZoom.classList.remove("active");
            }
            showToast("Modo 'Mover Gráfico' ativado.", "info", 1500);
        });
    }

    if(btnPlotZoom){
        btnPlotZoom.addEventListener("click", () => {
            window.chartRenderer.setDragMode("zoom");
            btnPlotZoom.classList.add("active");
            if(btnPlotPan){
                btnPlotPan.classList.remove("active");
            }
            showToast("Modo 'Zoom por Caixa' ativado.", "info", 1500);
        });
    }

    if(btnPlotZoomIn){
        btnPlotZoomIn.addEventListener("click", () => {
            window.chartRenderer.zoomIn();
        });
    }

    if(btnPlotZoomOut){
        btnPlotZoomOut.addEventListener("click", () => {
            window.chartRenderer.zoomOut();
        });
    }

    if(btnPlotReset){
        btnPlotReset.addEventListener("click", () => {
            window.chartRenderer.resetView();
            showToast("Visualização do gráfico restaurada para a posição original.", "info", 1500);
        });
    }

    const tabNavButtons = document.querySelectorAll(".tab-nav-btn");
    const tabPanes = document.querySelectorAll(".tab-pane");

    tabNavButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetTab = btn.getAttribute("data-tab");
            tabNavButtons.forEach(b => b.classList.remove("active"));
            tabPanes.forEach(p => p.classList.remove("active"));

            btn.classList.add("active");
            const activePane = document.getElementById(`tab-${targetTab}`);
            if(activePane){
                activePane.classList.add("active");
            }

            if(targetTab === "plot" && window.chartRenderer.currentData){
                window.chartRenderer.render(currentModuleId, window.chartRenderer.currentData);
            }
        });
    });

    async function loadCatalog(){
        try{
            modulosCatalog = await window.apiClient.getModulos();
        }catch(e){}
    }

    async function switchModule(moduloId){
        currentModuleId = moduloId;

        document.querySelectorAll(".nav-item").forEach(item => {
            if(item.getAttribute("data-module") === moduloId){
                item.classList.add("active");
            }else{
                item.classList.remove("active");
            }
        });

        const modInfo = modulosCatalog.find(m => m.id === moduloId);
        if(modInfo){
            moduleHeaderTitle.textContent = modInfo.nome;
            moduleHeaderSymbol.textContent = modInfo.simbolo;
            moduleHeaderSubtitle.textContent = modInfo.descricao;

            selectMetodo.innerHTML = "";
            modInfo.metodos.forEach((m, i) => {
                const opt = document.createElement("option");
                opt.value = m.id;
                opt.textContent = m.nome;
                if(i === 0){
                    opt.selected = true;
                }
                selectMetodo.appendChild(opt);
            });
            currentMetodoId = modInfo.metodos[0].id;
        }

        await loadPresets(moduloId);
        renderCurrentForm();

        window.chartRenderer.clear();
        historyTable.setHistory([]);
        clearSummary();
        setStatus("ready", "Pronto");
    }

    async function loadPresets(moduloId){
        try{
            currentPresets = await window.apiClient.getPresets(moduloId);
            selectPreset.innerHTML = `<option value="">— Selecione um Exemplo —</option>`;
            Object.keys(currentPresets).forEach(name => {
                const opt = document.createElement("option");
                opt.value = name;
                opt.textContent = name;
                selectPreset.appendChild(opt);
            });
        }catch(e){}
    }

    function renderCurrentForm(){
        const controller = moduleControllers[currentModuleId];
        if(controller){
            controller.render(currentMetodoId);
        }
    }

    function clearSummary(){
        summaryTitle.textContent = "Nenhum cálculo realizado ainda.";
        kpisGrid.innerHTML = "";
        if(summaryMathDetails){
            summaryMathDetails.innerHTML = "";
        }
    }

    function renderSummary(response){
        if(!response.sucesso){
            summaryTitle.textContent = "Cálculo não convergiu ou gerou erro.";
            kpisGrid.innerHTML = "";
            if(summaryMathDetails){
                summaryMathDetails.innerHTML = "";
            }
            return;
        }

        summaryTitle.textContent = "Resumo dos Resultados e Métricas Calculadas";
        kpisGrid.innerHTML = "";

        if(response.kpis && response.kpis.length > 0){
            response.kpis.forEach(kpi => {
                const card = document.createElement("div");
                card.className = "kpi-card";
                card.innerHTML = `
                    <div class="kpi-title">${kpi.title}</div>
                    <div class="kpi-value">${kpi.value}</div>
                    ${kpi.subtitle ? `<div class="kpi-sub">${kpi.subtitle}</div>` : ""}
                `;
                kpisGrid.appendChild(card);
            });
        }

        if(summaryMathDetails){
            if(response.detalhes_matematicos && response.detalhes_matematicos.length > 0){
                summaryMathDetails.style.display = "flex";
                summaryMathDetails.innerHTML = response.detalhes_matematicos.map(d => `
                    <div><strong>${d.label}:</strong> ${d.value}</div>
                `).join("");
            }else{
                summaryMathDetails.style.display = "none";
            }
        }
    }

    async function executarCalculo(){
        const controller = moduleControllers[currentModuleId];
        if(!controller){
            return;
        }

        let payload;
        try{
            payload = controller.getPayload(currentMetodoId);
        }catch(err){
            showErrorModal("Erro de Parâmetro", err.message);
            return;
        }

        if(!payload){
            return;
        }

        setStatus("running", "Calculando...");
        btnExecutar.disabled = true;

        try{
            const data = await window.apiClient.calcular(currentModuleId, payload);
            lastCalculationResponse = data;

            if(data.sucesso){
                setStatus("success", "Concluído", data.tempo_ms);
                showToast("Cálculo realizado com sucesso!", "success");
            }else{
                setStatus("error", "Não Convergiu", data.tempo_ms);
                showErrorModal("Aviso de Não Convergência", data.erro || "O método não convergiu para os parâmetros informados.");
            }

            if(data.plot_data){
                window.chartRenderer.render(currentModuleId, data.plot_data);
            }else{
                window.chartRenderer.clear();
            }

            if(currentModuleId === "sistemas" && data.etapas_gauss && data.etapas_gauss.length > 0){
                historyTable.setGaussSteps(data.etapas_gauss, data.substituicao_passos, data.historico);
            }else{
                historyTable.setHistory(data.historico);
            }
            renderSummary(data);

        }catch(error){
            setStatus("error", "Erro");
            showErrorModal("Erro na Execução", error.message);
        }finally{
            btnExecutar.disabled = false;
        }
    }

    document.querySelectorAll(".nav-item").forEach(item => {
        item.addEventListener("click", () => {
            const modId = item.getAttribute("data-module");
            if(modId && modId !== currentModuleId){
                switchModule(modId);
            }
        });
    });

    selectMetodo.addEventListener("change", (e) => {
        currentMetodoId = e.target.value;
        renderCurrentForm();
    });

    selectPreset.addEventListener("change", (e) => {
        const presetName = e.target.value;
        if(!presetName || !currentPresets[presetName]){
            return;
        }

        const pData = currentPresets[presetName];
        if(pData.metodo && pData.metodo !== currentMetodoId){
            selectMetodo.value = pData.metodo;
            currentMetodoId = pData.metodo;
            renderCurrentForm();
        }

        const controller = moduleControllers[currentModuleId];
        if(controller){
            controller.applyPreset(pData);
            showToast(`Exemplo carregado: ${presetName}`, "info");
        }
    });

    btnExecutar.addEventListener("click", executarCalculo);

    btnLimpar.addEventListener("click", () => {
        renderCurrentForm();
        selectPreset.value = "";
        window.chartRenderer.clear();
        historyTable.setHistory([]);
        clearSummary();
        setStatus("ready", "Pronto");
        showToast("Dados resetados para os padrões.", "info");
    });

    btnCopiarResumo.addEventListener("click", () => {
        const tsv = historyTable.getTSV();
        if(tsv){
            navigator.clipboard.writeText(tsv).then(() => {
                showToast("Tabela/Resumo copiado para a Área de Transferência!", "success");
            });
        }else{
            showToast("Nenhum dado para copiar.", "info");
        }
    });

    btnExportCsv.addEventListener("click", () => {
        const ok = historyTable.exportCSV();
        if(ok){
            showToast("Arquivo CSV exportado com sucesso!", "success");
        }else{
            showToast("Nenhuma tabela de iterações disponível para exportação.", "info");
        }
    });

    btnSavePlot.addEventListener("click", async () => {
        const ok = await window.chartRenderer.savePlot("png");
        if(ok){
            showToast("Gráfico salvo em alta resolução (PNG)!", "success");
        }else{
            showToast("Nenhum gráfico disponível para salvar.", "info");
        }
    });

    window.addEventListener("keydown", (e) => {
        if(e.ctrlKey && e.key >= "1" && e.key <= "6"){
            e.preventDefault();
            const mods = ["raizes", "sistemas", "interpolacao", "ajuste", "integracao", "edo"];
            const idx = parseInt(e.key, 10) - 1;
            if(mods[idx]){
                switchModule(mods[idx]);
            }
        }

        if(e.key === "F5" || (e.ctrlKey && e.key === "Enter")){
            e.preventDefault();
            executarCalculo();
        }
    });

    async function ensureServerReady(){
        let serverReady = false;
        let secondsElapsed = 0;
        let intervalId = null;

        if(modalServerLoadingBackdrop){
            modalServerLoadingBackdrop.classList.add("open");
        }
        setStatus("running", "Iniciando servidor...");

        intervalId = setInterval(() => {
            secondsElapsed += 1;
            if(serverLoadingStatusText){
                serverLoadingStatusText.textContent = `Conectando ao servidor (${secondsElapsed}s)...`;
            }
        }, 1000);

        while(!serverReady){
            try{
                await window.apiClient.checkHealth();
                serverReady = true;
            }catch(e){
                await new Promise((resolve) => setTimeout(resolve, 1500));
            }
        }

        if(intervalId){
            clearInterval(intervalId);
        }

        if(modalServerLoadingBackdrop){
            modalServerLoadingBackdrop.classList.remove("open");
        }
        setStatus("ready", "Pronto");
    }

    await ensureServerReady();
    await loadCatalog();
    await switchModule("raizes");
    checkAndShowDisclaimer();
});
