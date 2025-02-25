from enum import Enum

from pydantic import BaseModel


class WalletDB(BaseModel):
    id: int
    uuid: str
    balance: int

    class Config:
        orm_mode = True


class OperationType(str, Enum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'


class WalletOperation(BaseModel):
    operationType: OperationType
    amount: float

    class Config:
        schema_extra = {
            'examples': {
                'deposit': {
                    'summary': 'Пополнение баланса',
                    'description': 'Операция пополнения кошелька.',
                    'value': {
                        'operationType': 'DEPOSIT',
                        'amount': 1000
                    }
                },
                'withdraw': {
                    'summary': 'Снятие средств',
                    'description': 'Операция списания средств с кошелька.',
                    'value': {
                        'operationType': 'WITHDRAW',
                        'amount': 500
                    }
                }
            }
        }
