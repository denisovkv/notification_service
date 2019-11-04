from marshmallow import Schema, fields, post_load, validate


class Notification(Schema):
    id = fields.Function(lambda obj: str(obj['_id']))
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

    @post_load
    def set_default_to_excluded(self, data, **kwargs):
        data['is_sent'] = False
        data['is_deleted'] = False
        return data


class NotificationUpdatePayload(Notification):
    class Meta:
        exclude = ('id', 'is_sent', 'is_deleted')


class NotificationSearch(Schema):
    id = fields.String()
    title = fields.String()
    send_to = fields.Email()
    is_sent = fields.Boolean()
    is_deleted = fields.Boolean()


class NotificationList(Schema):
    result = fields.List(fields.Nested(Notification))
