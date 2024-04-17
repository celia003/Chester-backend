# # Dockerfile

# # Pull base image
# # FROM python:3.7
# FROM python:3.11
# # FROM alpine:3.19

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set work directory
# WORKDIR /src

# # RUN apt update

# # Install dependencies
# # COPY ../requirements.txt /code/
# COPY requirements.txt /src/
# # COPY packages /code/
# ENV TZ=Europe/Madrid
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# RUN pip3 install -r requirements.txt
# # RUN pip3 install --find-links packages *
# # RUN pip3 install packages

# # Copy project
# # COPY /media/disk01/projects/docker_oxen/code /code/
# COPY src /src/

#######################


ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-alpine as base

# set work directory
WORKDIR /src

## set env variables
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE 1
# Python environmental variable that allows the Python output to be sent straight to the terminal when set to a non-empty string or executed
ENV PYTHONUNBUFFERED 1

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    base_app

# install dependencies
RUN apk --no-cache add curl


# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# copy project
COPY ./src/ /src/

RUN chown -R base_app:base_app /src
RUN python manage.py collectstatic --settings=app.settings --noinput

USER base_app
