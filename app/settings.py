"""Project settings file."""

from pydantic import BaseSettings


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """Dataclass to manage settings.

    Modify this settings to match your requirements, if values are not given here it
    will look for the values on local environment variables.
    """

    SERVER_APP_PATH: str = "/volume/p7svr"
    LOGGED_MODEL: str = "/volume/mlruns/868922548984611484/db0a693ec2134778847c85d987023e95/artifacts/model"  # cambiar por modelo pao
    MLFLOW_URL: str = "http://localhost:8968"
    PREDICTION_ENDPOINT: str = "http://localhost:8080/make_prediction"
    AUTH_FILE_PATH: str = "auth_config.yaml"


conf = Settings()
