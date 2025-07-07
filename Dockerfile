FROM python:3.10-alpine

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.7.19 /uv /tmp/

COPY ./requirements.txt /app/

RUN /tmp/uv pip install --system -r "/app/requirements.txt"

ADD . .

RUN rm -rf /tmp /app/requirements.txt

CMD [ "python", "/app/main.py" ]
