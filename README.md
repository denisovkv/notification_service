# Сервис рассылки уведомлений
## Описание
Сервис рассылки уведомлений в назначенное время. Позволяет создавать, изменять, удалять уведомления, а также получать список уведомлений с заданными параметрами

При наступлении времени отправки отправляет уведомление на указанный адрес почты

## Запуск
Перед запуском необходимо задать параметры конфигурации в файле `.env` (необходимо создать, не отслеживается git) по примеру из `.env.example` для локального применения. Необходимо задать логин `NOTIFIER_LOGIN` и пароль `NOTIFIER_PASSWORD` учетной записи, от имени которой SMTP-сервер `NOTIFIER_SMTP_HOST` будет рассылать уведомления. Время отправки уведомления приводится к `TIMEZONE` 

Выполнить команду `docker-compose up --build`

По умолчанию сервис слушает порт 8080
## API
### POST
#### Создание уведомления
`/api/notification`

Тело запроса:
```
{
    "title": "hello",
    "body": "world",
    "send_to": "foo@bar.ru",
    "send_at": "1970-01-01T00:00:00+04"
}
```
Ответ - id созданного уведомления:
```
{
    "id": 5dc94fef20c0aab3ff8d2dc4
}
```

### GET
#### Получение уведомления по id
`/api/notification/{id}`

Ответ - найденное уведомление:
```
{
    "id": 5dc94fef20c0aab3ff8d2dc4,
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
`/api/notification?title=hello&is_sent=false`

Указание нескольких фильтров расценивается как AND. Для передачи списка вариантов необходимо передать требуемый параметр несколько раз:

`/api/notification?title=hello&title=goodbye&is_sent=false`

Ответ - найденные уведомления:
```
{
    "result": [
        {
        "id": 5dc94fef20c0aab3ff8d2dc4,
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
`/api/notification/{id}`

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
`/api/notification/{id}`

Ответ - 200 Ok
