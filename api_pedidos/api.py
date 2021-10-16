from fastapi import FastAPI
from api_pedidos.config_logging import logging


LOGGER = logging.getLogger(__name__)
app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    LOGGER.debug("Hello healthcheck!")
    return {"status": "ok"}
