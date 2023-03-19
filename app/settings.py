"""Project settings file."""

from pydantic import BaseSettings


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """Dataclass to manage settings.

    Modify this settings to match your requirements, if values are not given here it
    will look for the values on local environment variables.
    """

    PREDICTION_ENDPOINT: str = "http://localhost:8080/make_prediction"
    TRAINING_ENDPOINT: str = "http://localhost:8080/train_model"
    AUTH_FILE_PATH: str = "auth_config.yaml"


class LogConfig(BaseSettings):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "ml-app"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


conf = Settings()
log_conf = LogConfig()
