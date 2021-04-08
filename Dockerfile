FROM python:3.8

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /

EXPOSE 1234

# CMD alembic upgrade head && \
CMD gunicorn app.main:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:1234

