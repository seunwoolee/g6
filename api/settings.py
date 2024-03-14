import os
from typing import Any, Dict

from pydantic import BaseModel


class EnvLoader:
    def load(self) -> Dict[str, Any]:
        return dict(os.environ)


class ApiSetting(BaseModel):
    REST_API_VERSION: str = "v1"

    AUTH_ALGORITHM: str = "HS256"
    AUTH_ISSUER: str = "g6_rest_api"  # JWT 발급자

    ACCESS_TOKEN_EXPIRE_MINUTES: float = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: float = 60 * 24 * 14  # 14 days

    # JWT Secret Key
    # 보안을 위해 .env파일의 환경변수를 설정해야 합니다.
    ACCESS_TOKEN_SECRET_KEY: str = "access_token_secret_key"
    REFRESH_TOKEN_SECRET_KEY: str = "refresh_token_secret_key"


# .env 파일을 읽어서 환경변수를 설정합니다.
SETTINGS = ApiSetting.model_validate(EnvLoader().load())

