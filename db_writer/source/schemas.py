from marshmallow import Schema, fields


class Notification(Schema):
    id = fields.Integer()
    title = fields.String()
    body = fields.String()
    send_to = fields.Email()
    send_at = fields.DateTime()
    is_sent = fields.Boolean()
    is_deleted = fields.Boolean()


class NotificationPayload(Notification):
    class Meta:
        exclude = ('id', 'is_sent', 'is_deleted')

    title = fields.String(required=True)
    body = fields.String(required=True)
    send_to = fields.Email(required=True)
    send_at = fields.DateTime(required=True)


class NotificationUpdatePayload(Notification):
    class Meta:
        exclude = ('id', 'is_sent', 'is_deleted')


class NotificationSearch(Schema):
    id = fields.List(fields.Integer())
    title = fields.List(fields.String())
    send_to = fields.List(fields.Email())
    send_at = fields.List(fields.DateTime())
    is_sent = fields.Boolean(missing=False)
    is_deleted = fields.Boolean(missing=False)


class NotificationOutput(Schema):
    result = fields.List(fields.Nested(Notification))


class NotificationId(Schema):
    id = fields.Integer()
