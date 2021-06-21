FROM python:3.8-alpine

WORKDIR /

COPY requirements.txt logging_config.json weather_data.json /
RUN ["pip", "install", "-r", "requirements.txt"]

COPY app /

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--log-config", "logging_config.json", "--log-level", "debug"]