from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'WalletOpsAPI'
    description: str = ('Приложение для управления '
                        'балансами виртуальных кошельков.')
    api_version = '1'

    class Config:
        env_file = '.env'


settings = Settings()
