FROM python:3.7

ARG DB_WRITER_PORT

WORKDIR /db_writer

COPY db_writer/requirements.txt ./

RUN pip install pip --upgrade && \
    pip install -r requirements.txt --no-cache-dir

COPY docker/utils/wait-for-it.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for-it.sh

EXPOSE $DB_WRITER_PORT
