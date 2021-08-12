from typing import Optional

from pydantic import BaseModel


class CodePayload(BaseModel):
    code: str
    description: Optional[str] = None
