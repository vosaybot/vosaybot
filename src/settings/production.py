from settings.base import BaseConfig


class Config(BaseConfig):
    debug: bool


settings = Config(debug=False)
__all__ = ["settings"]
