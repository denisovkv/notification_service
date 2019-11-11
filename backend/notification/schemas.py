from marshmallow import Schema, fields, post_load, pre_load


class Notification(Schema):
    id = fields.Function(lambda obj: str(obj['_id']))
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

    @post_load
    def set_default_to_excluded(self, data, **kwargs):
        data['is_sent'] = False
        data['is_deleted'] = False
        return data


class NotificationUpdatePayload(Notification):
    class Meta:
        exclude = ('id', 'is_sent', 'is_deleted')


class NotificationSearch(Schema):

    class Meta:
        fields = ('id', 'title', 'send_to', 'is_sent', 'is_deleted')

    id = fields.List(fields.String())
    title = fields.List(fields.String())
    send_to = fields.List(fields.Email())
    is_sent = fields.List(fields.Boolean())
    is_deleted = fields.List(fields.Boolean())

    @pre_load
    def prepare_data(self, data, **kwargs):
        prepared_data = {}

        for key in self.Meta.fields:
            try:
                prepared_data.update({key: data.getall(key)})
            except KeyError:
                pass

        return prepared_data

    @post_load
    def prepare_filters(self, data, **kwargs):

        prepared_filters = {'$and': [{key: {'$in': value}} for key, value in data.items() if value]} if data else {}

        return prepared_filters


class NotificationList(Schema):
    result = fields.List(fields.Nested(Notification))
