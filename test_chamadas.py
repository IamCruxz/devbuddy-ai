import httpx
import pytest
from google.genai import errors

from chamadas import (
    ESPERA_MAXIMA,
    TodosModelosFalharam,
    calcular_espera,
    gerar_com_fallback,
)

MODELOS = ["modelo-a", "modelo-b"]


def erro_api(codigo):
    """Cria um erro de API falso, só com o código."""
    corpo = {"error": {"code": codigo, "message": "teste", "status": "TESTE"}}
    if codigo >= 500:
        return errors.ServerError(codigo, corpo)
    return errors.ClientError(codigo, corpo)


class ChamadaFalsa:
    """Finge ser a chamada ao Gemini.

    Devolve ou levanta, em ordem, o que a gente combinar. Guarda quais
    modelos foram chamados, para conferir a sequência no final.
    """

    def __init__(self, resultados):
        self.resultados = list(resultados)
        self.modelos_chamados = []

    def __call__(self, modelo):
        self.modelos_chamados.append(modelo)
        resultado = self.resultados.pop(0)
        if isinstance(resultado, Exception):
            raise resultado
        return resultado


def rodar(chamada, tentativas=3):
    """Roda o wrapper sem esperar de verdade e devolve texto e esperas."""
    esperas = []
    texto = gerar_com_fallback(
        chamada, modelos=MODELOS, tentativas=tentativas, dormir=esperas.append
    )
    return texto, esperas


def test_responde_de_primeira():
    chamada = ChamadaFalsa(["ok"])
    texto, esperas = rodar(chamada)
    assert texto == "ok"
    assert chamada.modelos_chamados == ["modelo-a"]
    assert esperas == []


@pytest.mark.parametrize("codigo", [429, 500, 502, 503, 504, 529])
def test_repete_nos_erros_temporarios(codigo):
    chamada = ChamadaFalsa([erro_api(codigo), "ok"])
    texto, esperas = rodar(chamada)
    assert texto == "ok"
    assert chamada.modelos_chamados == ["modelo-a", "modelo-a"]
    assert len(esperas) == 1


def test_repete_na_falha_de_rede():
    chamada = ChamadaFalsa([httpx.ConnectError("sem rede"), "ok"])
    texto, _ = rodar(chamada)
    assert texto == "ok"
    assert chamada.modelos_chamados == ["modelo-a", "modelo-a"]


def test_passa_para_o_proximo_modelo_depois_de_esgotar_as_tentativas():
    chamada = ChamadaFalsa([erro_api(503)] * 3 + ["ok"])
    texto, esperas = rodar(chamada)
    assert texto == "ok"
    assert chamada.modelos_chamados == ["modelo-a"] * 3 + ["modelo-b"]
    # Espera entre tentativas, mas não depois da última.
    assert len(esperas) == 2


def test_modelo_nao_encontrado_pula_sem_repetir():
    chamada = ChamadaFalsa([erro_api(404), "ok"])
    texto, esperas = rodar(chamada)
    assert texto == "ok"
    assert chamada.modelos_chamados == ["modelo-a", "modelo-b"]
    assert esperas == []


@pytest.mark.parametrize("codigo", [400, 401, 403])
def test_nao_repete_erros_que_repetir_nao_resolve(codigo):
    chamada = ChamadaFalsa([erro_api(codigo)])
    with pytest.raises(errors.APIError):
        gerar_com_fallback(chamada, modelos=MODELOS, dormir=lambda s: None)
    assert chamada.modelos_chamados == ["modelo-a"]


def test_todos_os_modelos_falham():
    chamada = ChamadaFalsa([erro_api(503)] * 6)
    with pytest.raises(TodosModelosFalharam):
        gerar_com_fallback(
            chamada, modelos=MODELOS, tentativas=3, dormir=lambda s: None
        )
    assert len(chamada.modelos_chamados) == 6


def test_espera_nunca_passa_do_maximo():
    for tentativa in range(20):
        assert 0 <= calcular_espera(tentativa) <= ESPERA_MAXIMA