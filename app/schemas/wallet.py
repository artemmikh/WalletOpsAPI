from pydantic import BaseModel


class WalletDB(BaseModel):
    id: int
    uuid: int
    balance: int

    class Config:
        orm_mode = True
