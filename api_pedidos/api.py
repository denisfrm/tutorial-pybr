from http import HTTPStatus

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse

from api_pedidos.config_logging import logging
from api_pedidos.esquema import Item, HealthCheckResponse, ErrorResponse
from api_pedidos.excecao import (
    PedidoNaoEncontradoError, FalhaDeComunicacaoError
)
from api_pedidos.magalu_api import recuperar_itens_por_pedido

LOGGER = logging.getLogger(__name__)
app = FastAPI()


@app.get(
    "/healthcheck",
    tags=["healthcheck"],
    summary="Integridade do sistema",
    description="Checa se o servidor está online",
    response_model=HealthCheckResponse
)
async def healthcheck():
    LOGGER.debug("Hello healthcheck!")
    return {"status": "ok"}


@app.exception_handler(PedidoNaoEncontradoError)
def tratar_erro_pedido_nao_encontrado(
    _request: Request, _exc: PedidoNaoEncontradoError
):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"message": "Pedido não encontrado"}
    )


@app.exception_handler(FalhaDeComunicacaoError)
def tratar_erro_falha_de_comunicacao(
    _request: Request, _exc: FalhaDeComunicacaoError
):
    return JSONResponse(
        status_code=HTTPStatus.BAD_GATEWAY,
        content={"message": "Falha de comunicação com o servidor remoto"}
    )


@app.get(
    "/orders/{identificacao_do_pedido}/items",
    tags=["pedidos"],
    summary="Itens de um pedido",
    description="Retorna todos os itens de um determinado pedido",
    response_model=list[Item],
    responses={
        HTTPStatus.NOT_FOUND.value: {
            "description": "Pedido não encontrado",
            "model": ErrorResponse,
        },
        HTTPStatus.BAD_GATEWAY.value: {
            "description": "Falha de comunicação com o servidor remoto",
            "model": ErrorResponse,
        }
    }
)
def listar_itens(itens: list[Item] = Depends(recuperar_itens_por_pedido)):
    return itens
