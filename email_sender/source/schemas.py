from marshmallow import Schema, fields


class Notification(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)
    body = fields.String(required=True)
    send_to = fields.Email(required=True)
    send_at = fields.DateTime(required=True)
    is_sent = fields.Boolean()
    is_deleted = fields.Boolean()
