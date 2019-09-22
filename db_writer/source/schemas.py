from marshmallow import Schema, fields, validate


class Notification(Schema):
    id = fields.Integer()
    title = fields.String(validate=validate.Length(max=50))
    body = fields.String(validate=validate.Length(max=200))
    send_to = fields.Email(validate=validate.Length(max=50))
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
        exclude = ('id', 'is_deleted')


class NotificationSearch(Schema):
    id = fields.Integer()
    title = fields.String()
    send_to = fields.Email()
    is_sent = fields.Boolean()
    is_deleted = fields.Boolean()


class NotificationOutput(Schema):
    result = fields.List(fields.Nested(Notification))


class NotificationId(Schema):
    id = fields.Integer()


class SendingConfirmation(Schema):
    is_sent = fields.Boolean()
