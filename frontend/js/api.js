class ApiClient {
    constructor(){
        this.baseUrl = this._detectBaseUrl();
    }

    _detectBaseUrl(){
        if(window.NUMERICOS_API_URL){
            return window.NUMERICOS_API_URL.replace(/\/+$/, "");
        }
        const savedUrl = localStorage.getItem("numericos_api_url");
        if(savedUrl){
            return savedUrl.replace(/\/+$/, "");
        }
        const isLocal = window.location.hostname === "localhost" || 
                        window.location.hostname === "127.0.0.1" || 
                        window.location.hostname === "0.0.0.0" || 
                        window.location.protocol === "file:";
        if(isLocal){
            return "";
        }
        return "https://metodos-numericos-backend.onrender.com";
    }

    setBaseUrl(url){
        this.baseUrl = (url || "").replace(/\/+$/, "");
        if(this.baseUrl){
            localStorage.setItem("numericos_api_url", this.baseUrl);
        }else{
            localStorage.removeItem("numericos_api_url");
        }
    }

    async getModulos(){
        const response = await fetch(`${this.baseUrl}/api/modulos`);
        if(!response.ok){
            throw new Error(`Erro ao carregar catálogo de módulos (HTTP ${response.status})`);
        }
        return await response.json();
    }

    async getPresets(moduloId){
        const response = await fetch(`${this.baseUrl}/api/${moduloId}/presets`);
        if(!response.ok){
            throw new Error(`Erro ao carregar exemplos para ${moduloId} (HTTP ${response.status})`);
        }
        return await response.json();
    }

    async calcular(moduloId, payload){
        const response = await fetch(`${this.baseUrl}/api/${moduloId}/calcular`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if(!response.ok){
            const errorMsg = data.detail || `Erro na requisição (HTTP ${response.status})`;
            throw new Error(errorMsg);
        }
        return data;
    }

    async getSobre(){
        const response = await fetch(`${this.baseUrl}/api/info/sobre`);
        if(!response.ok){
            throw new Error(`Erro ao carregar informações sobre o projeto (HTTP ${response.status})`);
        }
        return await response.json();
    }

    async getLicenca(){
        const response = await fetch(`${this.baseUrl}/api/info/licenca`);
        if(!response.ok){
            throw new Error(`Erro ao carregar licença (HTTP ${response.status})`);
        }
        return await response.json();
    }
}

window.apiClient = new ApiClient();
