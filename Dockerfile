# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

COPY ./scripts /scripts

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# makes all scripts in scripts directory executable.
RUN chmod -R +x /scripts

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files.
RUN python app/manage.py collectstatic --noinput --clear

# add our virtual environment to system path to run python from there and not the base image.
# add /scripts to path so the full path isn't required to run the scripts
ENV PATH="/scripts:/py/bin:$PATH"

# RUN cd app
# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
# CMD cd app; set -xe; python manage.py migrate --noinput; gunicorn app.wsgi:application
CMD ["run.sh"]