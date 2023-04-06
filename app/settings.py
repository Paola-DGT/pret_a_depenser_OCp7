"""Project settings file."""

from pydantic import BaseSettings


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """Dataclass to manage settings.

    Modify this settings to match your requirements, if values are not given here it
    will look for the values on local environment variables.
    """

    # On deploier les services dashboard et backend sur la meme instance sur le cloud,
    #   en consequence, les services sont en local host DE L' INSTANCE CLOUD!, puis
    #   Nginx est configuré en reverse proxy pour redirectioner le domain en https sur
    #   le port du dashboard.
    PREDICTION_ENDPOINT: str = "https://pao-app.online/api/make_prediction"
    GET_FI_ENDPOINT: str = "https://pao-app.online/api/get_feature_importance"
    GET_CUSTOMER: str = "https://pao-app.online/api/get_customer"
    GET_ACCEPTED_DESC_ENDPOINT: str = (
        "https://pao-app.online/api/get_accepted_description"
    )
    TRAINING_ENDPOINT: str = "https://pao-app.online/api/train_model"
    SAVE_DECISION_ENDPOINT: str = "https://pao-app.online/api/decision"
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
