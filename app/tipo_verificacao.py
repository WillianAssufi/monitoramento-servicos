from enum import Enum

class TipoVerificacao(str, Enum):
    http = "http"
    playwright = "playwright"