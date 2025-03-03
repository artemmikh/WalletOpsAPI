# Wallet API

## Описание

Приложение для управления балансом кошелька через REST API. Позволяет пополнять
баланс, снимать средства и получать информацию о текущем состоянии кошелька.

## Cтек

- **FastAPI** — фреймворк для создания REST API
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM для работы с БД
- **Alembic** — миграции базы данных
- **Docker, Docker Compose** — контейнеризация
- **Pytest** — тестирование

## Запуск проекта

1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/artemmikh/WalletOpsAPI.git
   cd WalletOpsAPI
   ```

2. Создайте файл `.env` на основе `.env.example` и укажите параметры
   подключения к базе данных.

3. Запустите приложение в контейнерах:
   ```sh
   docker-compose up --build
   ```

4. Выполните миграции:
   ```sh
   docker compose exec backend alembic upgrade head
   ```

Приложение будет доступно по адресу `http://localhost:8000/docs`.

## API Эндпоинты

### 1. Пополнение/снятие средств

**POST** `/api/v1/wallets/{WALLET_UUID}/operation`

"operationType" может быть "DEPOSIT" (пополнение) или "WITHDRAW" (снятие
средств).

#### Тело запроса:

```json
{
  "operationType": "DEPOSIT",
  "amount": 1000
}

```

#### Возможные ответы:

- `200 OK` — операция выполнена успешно
- `400 Bad Request` — неверный JSON или недостаточно средств
- `404 Not Found` — кошелек не найден

---

### 2. Получение баланса кошелька

**GET** `/api/v1/wallets/{WALLET_UUID}`

#### Возможные ответы:

- `200 OK` — возвращает баланс кошелька
- `404 Not Found` — кошелек не найден

### 3. Создание кошелька

Создание кошелька с уникальным UUID и нулевым балансом

**POST** `/api/v1/wallets/`

## Тестирование

Для запуска тестов выполните:

```sh
docker-compose exec backend pytest
```

## Обработка конкурентного доступа

Для предотвращения проблем при одновременных запросах к
одному кошельку (1000 RPS) используется механизм транзакций
и блокировка записей в БД (`SELECT ... FOR UPDATE`).

## Параметры приложения и базы

Параметры приложения и базы данных можно изменять через переменные окружения в
`.env`, без необходимости пересборки контейнеров.