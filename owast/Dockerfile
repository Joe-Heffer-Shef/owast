FROM python:slim-bullseye

# Update OS packages
RUN apt-get update && apt-get upgrade --yes && rm -rf /var/lib/apt/lists/*

ARG target_dir=/opt/owast

WORKDIR $target_dir

# Install app files
COPY ./owast $target_dir/owast
COPY ./meta $target_dir/meta

# Install Python package dependencies
RUN pip install -r $target_dir/owast/requirements.txt -r $target_dir/meta/requirements.txt

# Run as non-root user
USER www-data

# Run web app
# https://docs.gunicorn.org/en/stable/run.html
# https://docs.gunicorn.org/en/stable/custom.html?highlight=flask#direct-usage-of-existing-wsgi-apps
CMD ["gunicorn", "--config", "owast/gunicornconfig.py"]
