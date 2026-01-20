# ChatAPI

Простой API для чат-приложения, написанный на Python с использованием Django и Django REST Framework.

## Описание

Проект представляет собой backend для чат-приложения, где реализован функционал создания, просмотра, удаления чата
(со всеми сообщениями чата) и отправки сообщений в чат.

## Технологии

- Python 3.13
- Django 5.0
- Django REST Framework 3.14
- PostgreSQL 

## Установка и запуск

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/username/ChatAPI.git
   cd ChatAPI
   git checkout develop
   ```

3. Создайте файл `.env` и добавьте переменные окружения по примеру из `.env.example`

4. Запустите проект с помощью Docker:
   ```bash
   docker-compose up
   ```

   Это запустит:
   - Django приложение на http://localhost:8000
   - PostgreSQL базу данных

## Использование

API доступен по адресу http://localhost:8000/api/

Доступные endpoints:
- `POST /api/chats/` - создание чата
- `GET /api/chats/<int:pk>/` - получение чата с последними сообщениями (параметр limit для указания количества сообщений)
- `DELETE /api/chats/<int:pk>/` - удаление чата
- `POST /api/chats/<int:pk>/messages/` - отправка сообщения в чат

## Структура проекта

```
chat/
├── models.py       # Модели чата и сообщений
├── views.py        # Представления API
├── serializers.py  # Сериализаторы для моделей
├── urls.py         # URL-ы приложения
├── validators.py   # Валидаторы данных
├── tests.py        # Тесты
config/
├── urls.py         # Главные URL-ы
├── asgi.py         # ASGI конфигурация
├── settings.py     # Настройки Django
manage.py           # Django management commands
Dockerfile          # Docker конфигурация
docker-compose.yaml # Запуск всех сервисов
logs/               # Логи приложения
```

## Тестирование

Для запуска тестов выполните команду:
```bash
docker-compose exec back pytest
```

Тестовое покрытие кода составляет 98%.

---

Автор: Коурдаков Илья
