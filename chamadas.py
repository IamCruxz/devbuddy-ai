"""Chamadas ao Gemini com retentativas e modelo reserva."""

import logging
import random
import time

import httpx
from google.genai import errors

log = logging.getLogger(__name__)

# Ordem de preferência. Para trocar um modelo, mude só esta lista.
MODELOS = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash",
]

TENTATIVAS_POR_MODELO = 3
ESPERA_INICIAL = 1.0  # segundos
ESPERA_MAXIMA = 20.0  # segundos

# Erros temporários: vale a pena tentar de novo.
CODIGOS_TEMPORARIOS = {429, 500, 502, 503, 504, 529}


class TodosModelosFalharam(Exception):
    """Nenhum modelo da lista conseguiu responder."""


def calcular_espera(tentativa):
    """Espera que cresce (1s, 2s, 4s...) com sorteio, até o máximo."""
    teto = min(ESPERA_MAXIMA, ESPERA_INICIAL * 2**tentativa)
    return random.uniform(0, teto)


def gerar_com_fallback(
    chamar,
    modelos=MODELOS,
    tentativas=TENTATIVAS_POR_MODELO,
    dormir=time.sleep,
):
    """Chama chamar(modelo) e devolve o texto.

    Tenta de novo nos erros temporários. Se as tentativas de um modelo
    acabarem, passa para o próximo da lista.
    """
    for modelo in modelos:
        for tentativa in range(tentativas):
            try:
                texto = chamar(modelo)
            except errors.APIError as erro:
                if erro.code == 404:
                    log.warning("Modelo %s não encontrado. Indo para o próximo.", modelo)
                    break
                if erro.code not in CODIGOS_TEMPORARIOS:
                    raise  # 400, 401, 403...: repetir não resolve
                motivo = f"erro {erro.code}"
            except httpx.TransportError:
                motivo = "falha de rede"
            else:
                log.info("Respondeu: %s", modelo)
                return texto

            log.warning(
                "%s: %s (tentativa %d de %d)", modelo, motivo, tentativa + 1, tentativas
            )
            if tentativa < tentativas - 1:
                dormir(calcular_espera(tentativa))

    raise TodosModelosFalharam("Nenhum modelo respondeu.")