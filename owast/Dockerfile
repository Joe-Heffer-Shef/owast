FROM python:slim-bullseye

COPY owast owast

RUN pip install -r owast/requirements.txt

#CMD ["gunicorn", "'owast.app_factory:create_app()'"]
CMD ["python", "-m", "owast"]
