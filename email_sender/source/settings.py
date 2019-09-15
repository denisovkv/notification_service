from envparse import Env


env = Env()

DATABASE_USER = env.str('DATABASE_USER', default='postgres')
DATABASE_NAME = env.str('DATABASE_NAME', default='postgres')
DATABASE_HOST = env.str('DATABASE_HOST', default='db')
DATABASE_PORT = env.str('DATABASE_PORT', default='5432')

DATABASE_URL = f'postgresql://{DATABASE_USER}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

EMAIL_SENDER_PERIOD = env.int('EMAIL_SENDER_PERIOD', default=60)
EMAIL_SENDER_LOGIN = env.str('EMAIL_SENDER_LOGIN', default='login')
EMAIL_SENDER_PASSWORD = env.str('EMAIL_SENDER_PASSWORD', default='password')
EMAIL_SENDER_SMTP_HOSTNAME = env.str('EMAIL_SENDER_SMTP_HOSTNAME', default='smtp.mail.ru')
EMAIL_SENDER_SMTP_PORT = env.int('EMAIL_SENDER_SMTP_PORT', default=465)
