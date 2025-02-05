from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class DBModel(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: Optional[int] = None
