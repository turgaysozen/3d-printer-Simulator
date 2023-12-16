FROM python:3.10-alpine
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "server:app", "-b", "0.0.0.0:5000", "--worker-class", "gevent", "--timeout", "60", "--workers", "1"]