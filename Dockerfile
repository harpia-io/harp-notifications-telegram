FROM python:3.11.3

WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install "uvicorn[standard]" gunicorn==20.1.0
COPY . .
RUN python setup.py install

CMD ["gunicorn", "harp_notifications_telegram.__main__:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8081", "--workers", "1", "--threads", "8", "--timeout", "120"]