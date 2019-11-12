from envparse import Env

env = Env()

NOTIFIER_LOGIN = env.str('NOTIFIER_LOGIN', default='login')
NOTIFIER_PASSWORD = env.str('NOTIFIER_PASSWORD', default='password')
NOTIFIER_SMTP_HOST = env.str('NOTIFIER_SMTP_HOST', default='smtp.mail.ru')
NOTIFIER_SMTP_PORT = env.int('NOTIFIER_SMTP_PORT', default=465)

BACKEND_CONFIRM_ENDPOINT = env.str('BACKEND_CONFIRM_ENDPOINT',
                                   default='http://backend:8080/api/notification/confirm')
