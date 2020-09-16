FROM python:alpine

ENV PYTHONRUNUNBUFFERED 1

COPY app requirements.txt /usr/src/
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r /usr/src/requirements.txt

CMD ["python", "/usr/src/app/main.py"]
