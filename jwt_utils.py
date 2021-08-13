import time
from typing import Dict, Optional, Tuple

import jwt

from config import settings


class JWT:
    @staticmethod
    def encode(payload: Dict[str, Tuple[str, float]]) -> str:
        return jwt.encode(payload, key=settings.jwt_key, algorithm="HS256")

    @staticmethod
    def decode(token: str) -> Optional[Dict[str, Tuple[str, float]]]:
        try:
            payload = jwt.decode(jwt=token, key=settings.jwt_key, algorithms=["HS256"])
            if payload.get("exp") <= time.time():
                payload = None
        except Exception:
            payload = None
        return payload
