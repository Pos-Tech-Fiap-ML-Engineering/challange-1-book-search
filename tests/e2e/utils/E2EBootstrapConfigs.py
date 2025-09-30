from dataclasses import dataclass


@dataclass
class E2EBootstrapConfigs:
    service_url: str
    service_token_username: str
    service_token_password: str
