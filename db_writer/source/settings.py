from envparse import Env


env = Env()

DATABASE_USER = env.str('DATABASE_USER', default='someuser')
DATABASE_PASSWORD = env.str('DATABASE_PASSWORD', default='somepassword')
DATABASE_NAME = env.str('DATABASE_NAME', default='somedb')
DATABASE_HOST = env.str('DATABASE_HOST', default='db')
DATABASE_PORT = env.str('DATABASE_PORT', default='5432')

DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

POOL_MIN_SIZE = env.int('POOL_MIN_SIZE', default=1)
POOL_MAX_SIZE = env.int('POOL_MAX_SIZE', default=2)
