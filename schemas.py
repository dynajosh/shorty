from pydantic import BaseModel

class URLBase(BaseModel):
    target_url : str

class URL(BaseModel):
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True

class URLInfo(URL):
    url: str
    admin_url: str