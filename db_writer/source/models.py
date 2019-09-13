from marshmallow import Schema, fields


class Notification(Schema):
    id = fields.Integer()
    title = fields.String()
    body = fields.String()
    mail_to = fields.Email()
    send_time = fields.DateTime()
    is_sent = fields.Boolean()
