class NotificationManager:

    def __init__(self, con):
        self.con = con

    async def create(self, **kwargs):
        return await self.con.fetchrow('''
            insert into notifications (title, body, send_to, send_at)
            values ($1, $2, $3, $4)
            returning id as id
        ''', kwargs['title'], kwargs['body'], kwargs['send_to'], kwargs['send_at'])

    async def get(self, **kwargs):

        query = 'select * from notifications'

        # Самописные фильтры sql омг -_-
        if not all(i is None for i in kwargs.values()):
            query += ' where '

            filters = [f'{key} = any(ARRAY{value})' for key, value in kwargs.items() if key in ['id', 'title', 'send_to'] and value]

            if kwargs['is_sent'] is not None:
                filters.append(f'is_sent = {kwargs["is_sent"]}')

            if kwargs['is_deleted'] is not None:
                filters.append(f'is_deleted = {kwargs["is_deleted"]}')

            query += ' and '.join(filters)

        return await self.con.fetch(query)

    async def update(self, record_id, **kwargs):

        # Для апдейта интовых и иных значений, для которых не требуются кавычки при SET-е,
        # придется писать другой join и добавлять условия в генераторах списка типа isinstance.
        updated_values = ', '.join([f'{key} = \'{value}\'' for key, value in kwargs.items()])
        query = f'''
            update notifications
            set {updated_values}
            where id = $1
            returning id as id
        '''

        return await self.con.fetchrow(query, int(record_id)) if updated_values else None

    async def delete(self, record_id):
        return await self.con.fetchrow('''
            update notifications
            set is_deleted = True
            where id = $1
            returning id as id
        ''', int(record_id))
