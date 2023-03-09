"""Project settings file."""

from pydantic import BaseSettings


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """Dataclass to manage settings.

    Modify this settings to match your requirements, if values are not given here it
    will look for the values on local environment variables.
    """

    SERVER_APP_PATH: str = "/volume/p7svr"
    LOGGED_MODEL: str = "app/models/PlainRegression_Model"
    MLFLOW_URL: str = "http://localhost:8968"
    PREDICTION_ENDPOINT: str = "http://localhost:8080/make_prediction"
    AUTH_FILE_PATH: str = "auth_config.yaml"


conf = Settings()
