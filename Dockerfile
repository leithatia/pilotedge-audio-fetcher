FROM python:3.12-alpine

RUN apk add --no-cache ffmpeg

WORKDIR /app

RUN adduser -D -u 10001 appuser

COPY fetch.py .
COPY entrypoint.sh .

RUN pip install --no-cache-dir requests

RUN chmod +x /app/entrypoint.sh \
 && mkdir /work \
 && chown -R appuser:appuser /app /work

USER appuser

ENTRYPOINT ["/app/entrypoint.sh"]

