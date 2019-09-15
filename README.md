# Сервис рассылки уведомлений
## Описание
Сервис рассылки уведомлений в назначенное время. Позволяет создавать, изменять, удалять и получать список уведомлений.

При наступлении времени отправки отправляет уведомление на указанный адрес почты.

## Запуск
Задать параметры конфигурации в файле .env либо в файле .env.override (необходимо создать, не отслеживается git) для локального применения (логины, пароли и т.д.)

Также при необходимости изменить часовой пояс БД в файле ./db/postgresql.conf. По умолчанию установлен Europe/Moscow

Выполнить команду docker-compose run --build
## API
### POST
#### Создание уведомления
`/notifications`

Запрос:
```
{
    "title": "hello",
    "body": "world",
    "send_to": "foo@bar.ru",
    "send_at": "1970-01-01T00:00:00"
}
```
Ответ - id созданного уведомления:
```
{
    "id": 1
}
```

### Get
#### Получение списка уведомлений, удовлетворяющих заданным параметрам
`/notifications`

Запрос:
```
{
    "title": ["hello"]
}
```
```
{
    "id": [1, 2, 3]
}
```
```
{
    "send_to": ["foo@bar.ru", "bar@foo.ru"]
}
```
Ответ - найденные уведомления:
```
{
    "result": [
        {
        "id": 1,
        "title": "hello",
        "body": "world",
        "send_to": "foo@bar.ru",
        "send_at": "1970-01-01T00:00:00",
        "is_sent": false,
        "is_deleted": false
        }
    ]
}
```
### PATCH
#### Изменение уведомления
`/notifications/1`

Запрос:
```
{
    "body": "python",
    "send_to": "bar@foo.ru"
}
```
Ответ - id измененного уведомления:
```
{
    "id": 1
}
```
Если переданный в запросе id не был найден:
```
{}
```
### DELETE
#### Удаление уведомления
`/notifications/1`

Ответ - id удаленного уведомления:
```
{
    "id": 1
}
```
Если переданный в запросе id не был найден:
```
{}
```
