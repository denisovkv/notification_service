FROM python:3.7

ARG DB_WRITER_PORT

WORKDIR /db_writer

COPY db_writer/requirements.txt ./

RUN pip install pip --upgrade && \
    pip install -r requirements.txt --no-cache-dir

EXPOSE $DB_WRITER_PORT
