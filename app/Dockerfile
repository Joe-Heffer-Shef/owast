FROM python:slim-bullseye

COPY app /app
WORKDIR /app

RUN pip install -r requirements.txt

#CMD ["gunicorn", "'app_factory:create_app()'"]
CMD ["python", "."]
