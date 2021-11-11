FROM python:slim-bullseye

# Update OS packages
RUN apt-get update && apt-get upgrade --yes && rm -rf /var/lib/apt/lists/*

WORKDIR /

# Install app files
COPY ./owast /owast

# Install Python package dependencies
RUN pip install -r /owast/requirements.txt

# Run as non-root user
USER www-data

# Run web app
# https://docs.gunicorn.org/en/stable/run.html
# https://docs.gunicorn.org/en/stable/custom.html?highlight=flask#direct-usage-of-existing-wsgi-apps
CMD ["gunicorn", "--config", "/owast/gunicornconfig.py"]
#CMD ["python", "-m", "owast"]
