from envparse import Env


env = Env()

DATABASE_URL = env.str('DATABASE_URL', default='sqlite:///../db/notification_service.db')

EMAIL_SENDER_ENDPOINT = env.str('EMAIL_SENDER_ENDPOINT',
                                default='http://notification_service_email_sender_1:8081/api/tasks')
