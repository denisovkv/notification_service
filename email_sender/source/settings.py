from envparse import Env


env = Env()

EMAIL_SENDER_LOGIN = env.str('EMAIL_SENDER_LOGIN', default='login')
EMAIL_SENDER_PASSWORD = env.str('EMAIL_SENDER_PASSWORD', default='password')
EMAIL_SENDER_SMTP_HOST = env.str('EMAIL_SENDER_SMTP_HOST', default='smtp.mail.ru')
EMAIL_SENDER_SMTP_PORT = env.int('EMAIL_SENDER_SMTP_PORT', default=465)
