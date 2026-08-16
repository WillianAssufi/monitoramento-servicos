from enum import Enum

class StatusServico(str, Enum):
    up = "UP"
    down = "DOWN"
    aguardando = "AGUARDANDO"
