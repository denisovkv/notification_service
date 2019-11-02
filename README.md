# Сервис рассылки уведомлений
## Описание
Сервис рассылки уведомлений в назначенное время. Позволяет создавать, изменять, удалять уведомления, а также получать список уведомлений с заданными параметрами

При наступлении времени отправки отправляет уведомление на указанный адрес почты

## Запуск
Задать параметры конфигурации в файле .env либо в файле .env.override (необходимо создать, не отслеживается git) для локального применения (в частности, логин `NOTIFIER_LOGIN` и пароль `NOTIFIER_PASSWORD` учетной записи, от имени которой SMTP-сервер `NOTIFIER_SMTP_HOST` будет рассылать уведомления)

Выполнить команду docker-compose up --build

По умолчанию сервис слушает порт 8080
## API
### POST
#### Создание уведомления
`/api/notifications`

Тело запроса:
```
{
    "title": "hello",
    "body": "world",
    "send_to": "foo@bar.ru",
    "send_at": "1970-01-01T00:00:00+03"
}
```
Ответ - id созданного уведомления:
```
{
    "id": 1
}
```

### GET
#### Получение уведомления по id
`/api/notifications/{id}`

Ответ - найденное уведомление:
```
{
    "id": 1,
    "title": "hello",
    "body": "world",
    "send_to": "foo@bar.ru",
    "send_at": "1970-01-01T00:00:00",
    "is_sent": false,
    "is_deleted": false
}
```

### GET
#### Получение списка уведомлений, удовлетворяющих заданным параметрам
`/api/search/notifications`

Тело запроса:
```
{
    "title": "hello"
}
```
```
{
    "id": 1
}
```
```
{
    "send_to": "foo@bar.ru"
}
```
Указание нескольких фильтров расценивается как AND:
```
{
    "id": 1,
    "is_sent": false,
    "is_deleted": false,
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
`/api/notifications/{id}`

Тело запроса:
```
{
    "body": "python",
    "send_to": "bar@foo.ru"
}
```
Ответ - 200 Ok

### DELETE
#### Удаление уведомления
`/api/notifications/{id}`

Ответ - 200 Ok
