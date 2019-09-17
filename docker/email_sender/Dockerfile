FROM python:3.7

ARG EMAIL_SENDER_PORT

WORKDIR /email_sender

COPY email_sender/requirements.tx ./

RUN pip install pip --upgrade && \
    pip install -r requirements.txt --no-cache-dir

EXPOSE $EMAIL_SENDER_PORT
