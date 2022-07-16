# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster

# Use /app folder as a directory where the source code is stored.
WORKDIR /app
# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# copy all necessary directories across to image
COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY ./scripts /scripts

# Install system packages required by Wagtail and Django.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update --yes --quiet && \
    apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev && \
    rm -rf /var/lib/apt/lists/* && \
    /py/bin/pip install -r /requirements.txt && \
    # user that will be used in the container
    adduser --disabled-password --no-create-home wagtail && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    # set user as the owner of the directory so it has necessary permissions
    chown -R wagtail:wagtail /vol && \
    # provide read & write permissions
    chmod -R 755 /vol && \
    # makes all scripts in scripts directory executable.
    chmod -R +x /scripts

# # Install the application server. I am using uWSGI now
# RUN /py/bin/pip install "gunicorn==20.0.4"

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# add our virtual environment to system path to run python from there and not the base image.
# add /scripts to path so the full path isn't required to run the scripts
ENV PATH="/scripts:/py/bin:$PATH"

# Runtime command that executes when "docker run" is called, it does the
CMD ["run.sh"]
