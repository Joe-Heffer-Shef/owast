FROM python:slim-bullseye

# Update OS packages
RUN apt-get update && apt-get upgrade --yes && rm -rf /var/lib/apt/lists/*

WORKDIR /

# Install app files
COPY ./owast /opt/owast
COPY ./meta /opt/meta

# Install Python package dependencies
RUN pip install -r /opt/owast/requirements.txt -r /opt/meta/requirements.txt

# Run as non-root user
USER www-data

# Run web app
# https://docs.gunicorn.org/en/stable/run.html
# https://docs.gunicorn.org/en/stable/custom.html?highlight=flask#direct-usage-of-existing-wsgi-apps
CMD ["gunicorn", "--config", "/opt/owast/gunicornconfig.py"]
