from typing import List, Optional

from pydantic import BaseModel


class ShortUrlBase(BaseModel):
    url: str


class ShortUrlCreate(ShortUrlBase):
    url: str


class ShortUrl(ShortUrlBase):
    id: int
    url: str
    short: str

    class Config:
        orm_mode = True


