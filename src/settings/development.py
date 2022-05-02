from pydantic import Field

from settings.base import BaseConfig


class Config(BaseConfig):
    debug: bool = Field(default=False)


settings = Config()
__all__ = ["settings"]
