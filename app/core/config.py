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
    postgres_user: str = 'example'
    postgres_password: str = 'example'
    postgres_db: str = 'example'
    postgres_host: str = 'db'
    postgres_port: str = '5432'

    @property
    def database_url(self) -> str:
        """Формирует URL для подключения к PostgreSQL."""
        return (
            f'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}@'
            f'{self.postgres_host}:{self.postgres_port}/{self.postgres_db}')

    class Config:
        env_file = '.env'


settings = Settings()
