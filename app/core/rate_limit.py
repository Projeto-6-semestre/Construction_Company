"""Rate limit simples em memoria pro login - sem tentativa ilimitada de senha.

Em memoria (nao Redis/banco) de proposito: o deploy roda uma unica instancia
(Render free, WEB_CONCURRENCY=1), entao nao ha problema de estado nao
compartilhado entre processos; reiniciar o processo so reseta os contadores,
o que e aceitavel - isso e uma barreira contra brute-force trivial, nao um
controle de seguranca critico que precise sobreviver a reinicio.
"""

import time
from collections import defaultdict

_MAX_TENTATIVAS = 5
_JANELA_SEGUNDOS = 15 * 60

_tentativas: dict[str, list[float]] = defaultdict(list)


def _tentativas_na_janela(chave: str) -> list[float]:
    agora = time.monotonic()
    return [t for t in _tentativas.get(chave, []) if agora - t < _JANELA_SEGUNDOS]


def bloqueado(chave: str) -> bool:
    return len(_tentativas_na_janela(chave)) >= _MAX_TENTATIVAS


def registrar_falha(chave: str) -> None:
    _tentativas[chave] = _tentativas_na_janela(chave) + [time.monotonic()]


def limpar(chave: str) -> None:
    _tentativas.pop(chave, None)
