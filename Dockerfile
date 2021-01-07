FROM python:3.8

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /

EXPOSE 8000

# CMD alembic upgrade head && \
CMD gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0

