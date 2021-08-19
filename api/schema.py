from typing import Optional

from pydantic import BaseModel, Field


class CodePayload(BaseModel):
    id: str = Field(..., max_length=8)
    code: str
    description: Optional[str] = None
