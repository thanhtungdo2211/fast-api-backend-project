import os
import enum
from pydantic_settings import BaseSettings

class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET                     = "NOTSET"
    DEBUG                      = "DEBUG"
    INFO                       = "INFO"
    WARNING                    = "WARNING"
    ERROR                      = "ERROR"
    FATAL                      = "FATAL"

# flake8: noqa
class Configure:
    host: str                  = "0.0.0.0"
    port: int                  = 5000

    # quantity of workers for uvicorn
    workers_count: int         = 1

    # Enable uvicorn reloading
    reload: bool               = False

    VERSION                    = "1.1.0"
    log_level: LogLevel        = LogLevel.INFO
    
    # Authentication
    SECRET_KEY               = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM                = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS = 365

    # Database configuration
    USER_DATABASE       = os.environ.get("USER_DATABASE", "postgres")
    PASSWORD_DATABASE   = os.environ.get("PASSWORD_DATABASE", "postgres")
    HOST_DATABASE       = os.environ.get("HOST_DATABASE", "db")
    PORT_DATABASE       = os.environ.get("PORT_DATABASE", "5432")
    NAME_DATABASE       = os.environ.get("NAME_DATABASE", "postgres")
    URL_DATABASE        = f"postgresql://{USER_DATABASE}:{PASSWORD_DATABASE}@{HOST_DATABASE}:{PORT_DATABASE}/{NAME_DATABASE}"

config = Configure()