from asyncpg.pool import Pool


class NotificationManager:

    def __init__(self, con: Pool):
        self.con = con

    async def create(self, **kwargs):
        return await self.con.fetchrow('''
            insert into notifications (title, body, send_to, send_at)
            values ($1, $2, $3, $4)
            returning id as id
        ''', kwargs['title'], kwargs['body'], kwargs['send_to'], kwargs['send_at'])

    async def get(self, **kwargs):
        return await self.con.fetch('''
            select *
            from notifications
            where (id = any($1) or
            title = any($2) or
            send_to = any($3)) and
            is_deleted = $4
        ''', kwargs['id'], kwargs['title'], kwargs['send_to'], kwargs['is_deleted'])

    async def update(self, record_id, **kwargs):

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
