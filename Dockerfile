FROM python:3.9-slim-buster

RUN useradd app

WORKDIR /app

COPY src/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY src /app

EXPOSE 5000

USER app

CMD ["python", "app.py"]
