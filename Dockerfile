FROM python:3.9-alpine
LABEL maintainer="Your Name <Dibakar>"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .build-deps \
    build-base postgresql-dev musl-dev && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .build-deps && \ 
    adduser \
        --disabled-password \
        --no-create-home \
        djabgo-user

ENV PATH="/py/bin:$PATH"

USER djabgo-user