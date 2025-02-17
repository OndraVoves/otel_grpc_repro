FROM python:3.11

ENV APP_PORT=9292
EXPOSE $APP_PORT

COPY        . /app
WORKDIR     /app

RUN python -m pip install \
    --no-cache \
    --disable-pip-version-check \
    -r requirements.txt

CMD uvicorn app:app --host=0.0.0.0 --port=${APP_PORT}
