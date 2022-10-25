from dataclasses import dataclass


@dataclass
class Credentials:
    site: str
    merchant_id: str
    username: str
    password: str
