from pathlib import Path
from fastapi import APIRouter

router = APIRouter(prefix="/info", tags=["Informações"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LICENSE_FILE = BASE_DIR / "LICENSE"


@router.get("/sobre")
def get_sobre():
    return {
        "projeto": "Métodos Numéricos Computacionais",
        "versao": "3.0.0",
        "autor": "Otávio",
        "descricao": "Aplicação web moderna, responsiva e interativa desenvolvida para estudo, resolução e visualização de problemas clássicos de Cálculo Numérico.",
        "github": "https://github.com/theotavio",
        "sponsor": "https://github.com/sponsors/theotavio",
        "email": "otavioal2907@gmail.com"
    }


@router.get("/licenca")
def get_licenca():
    if LICENSE_FILE.exists():
        texto = LICENSE_FILE.read_text(encoding="utf-8")
    else:
        texto = "MIT License - Copyright (c) 2026 Otávio"
    return {
        "licenca": "MIT",
        "texto": texto
    }
