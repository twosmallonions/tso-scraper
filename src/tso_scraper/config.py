import os
from dataclasses import dataclass


@dataclass
class Config:
    secret: str

    @classmethod
    def from_env(cls) -> 'Config':
        secret = os.getenv('SCRAPER_AUTH_SECRET')
        if secret is None:
            msg = 'SCRAPER_AUTH_SECRET is required'
            raise ValueError(msg)
        return cls(secret=secret)


config = Config.from_env()
