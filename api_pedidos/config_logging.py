import logging.config

logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "standard": {
                "format": (
                    "%(asctime)s - [%(levelname)s] %(name)s [%(process)d] "
                    "[%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
                ),
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        },
        "loggers": {
            "api_pedidos": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
        },
    }
)
