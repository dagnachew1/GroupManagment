from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
import json

class TelegramConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    api_token: Annotated[str, "Bot API token from @BotFather"]
    rate_limit: Annotated[int, "Messages per second"] = Field(gt=0, default=1)

class LoggingConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    level: Annotated[str, "Logging level"] = "INFO"
    format: str | None = None

class Config(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    telegram: TelegramConfig
    logging: LoggingConfig

    @classmethod
    def load(cls, path: str | Path = "config.json") -> "Config":
        with open(path) as f:
            data = json.load(f)
            return cls.model_validate(data)

config = Config.load()