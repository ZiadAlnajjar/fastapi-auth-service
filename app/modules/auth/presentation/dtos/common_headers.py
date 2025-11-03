from typing import Optional

from pydantic import BaseModel


class CommonHeaders(BaseModel):
    x_refresh_token: Optional[str] = None
