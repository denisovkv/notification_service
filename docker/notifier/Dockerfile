FROM python:3.7

ARG NOTIFIER_PORT

WORKDIR /notifier

COPY notifier/requirements.txt ./

RUN pip install pip --upgrade && \
    pip install -r requirements.txt --no-cache-dir

COPY docker/utils/wait-for-it.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/wait-for-it.sh

EXPOSE $NOTIFIER_PORT
