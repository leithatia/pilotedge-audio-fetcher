FROM python:3.12-slim

WORKDIR /app

RUN useradd -r -u 10001 appuser

COPY fetch.py .
RUN pip install --no-cache-dir requests

RUN chown -R appuser:appuser /app
USER appuser

CMD ["python", "fetch.py"]

