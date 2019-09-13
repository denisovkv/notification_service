from asyncpg.pool import Pool


class NotificationManager:

    def __init__(self, con: Pool):
        self.con = con

    async def create(self, **kwargs):
        return await self.con.fetchval('''
            insert into notifications (title, body, send_to, send_at)
            values ($1, $2, $3, $4)
            returning id
        ''', kwargs['title'], kwargs['body'], kwargs['send_to'], kwargs['send_at'])

    async def get(self, **kwargs):
        return await self.con.fetch('''
            select *
            from notifications
            where (id = any($1) or
            title = any($2) or
            send_to = any($3) or
            send_at = any($4)) and
            is_sent = $5 and
            is_deleted = $6
        ''', kwargs['id'], kwargs['title'], kwargs['send_to'],
             kwargs['send_at'], kwargs['is_sent'], kwargs['is_deleted'])

    async def update(self, record_id, **kwargs):

        updated_values = ', '.join([f'{key} = {value}' for key, value in kwargs])
        query = f'''
            update notifications
            {updated_values}
            where id = $1
        '''

        return await self.con.fetchval(query, int(record_id))

    async def delete(self, record_id):
        return await self.con.fetchval('''
            update notifications
            set is_deleted = True
            where id = $1
            returning id
        ''', int(record_id))
