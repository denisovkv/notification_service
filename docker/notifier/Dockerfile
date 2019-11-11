FROM python:3.7

ARG NOTIFIER_PORT

WORKDIR /notifier

COPY notifier/requirements.txt ./

RUN pip install pip --upgrade && \
    pip install -r requirements.txt --no-cache-dir

EXPOSE $NOTIFIER_PORT
