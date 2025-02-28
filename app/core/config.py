from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Настройки приложения."""
    app_title: str = 'WalletOpsAPI'
    api_version: str = '1'
    app_description: str = ('Приложение для управления '
                            'балансами виртуальных кошельков.')
    database_url: str = 'sqlite+aiosqlite:///./app/data/wallet.db'
    test_database_url: str = 'sqlite+aiosqlite:///:memory:'
    postgres_user = 'example'
    postgres_password = 'example'
    postgres_db = 'example'

    class Config:
        env_file = '.env'


settings = Settings()
