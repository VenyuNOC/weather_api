FROM python:3.8-alpine

ENV PYTHONRUNUNBUFFERED 1

COPY requirements.txt /usr/src
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r /usr/src/requirements.txt

COPY app /usr/src/

CMD ["python", "/usr/src/app/backend.py"]
