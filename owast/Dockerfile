FROM python:slim-bullseye

# Update OS packages (and remove package info to save space)
# "Official Debian and Ubuntu images automatically run apt-get clean, so explicit invocation is not required."
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
RUN apt-get update && apt-get upgrade --yes && rm -rf /var/lib/apt/lists/*

ARG target_dir=/opt/owast

WORKDIR $target_dir

# Install app files
COPY ./owast $target_dir/owast

# Install Python package dependencies
RUN pip install -r $target_dir/owast/requirements.txt

# Run as non-root user
USER www-data

# Run web app
# https://docs.gunicorn.org/en/stable/run.html
# https://docs.gunicorn.org/en/stable/custom.html?highlight=flask#direct-usage-of-existing-wsgi-apps
CMD ["gunicorn", "--config", "owast/gunicornconfig.py"]
