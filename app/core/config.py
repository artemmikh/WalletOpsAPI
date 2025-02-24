from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'WalletOpsAPI'
    api_version = '1'
    description: str = ('Приложение для управления '
                        'балансами виртуальных кошельков.')
    database_url: str = 'sqlite+aiosqlite:///./wallet.db'

    class Config:
        env_file = '.env'


settings = Settings()
