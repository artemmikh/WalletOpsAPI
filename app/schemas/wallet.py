from pydantic import BaseModel


class WalletDB(BaseModel):
    id: int
    uuid: str
    balance: int

    class Config:
        orm_mode = True
