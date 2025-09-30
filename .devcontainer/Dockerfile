FROM mcr.microsoft.com/devcontainers/python:1-3.12

ENV PYTHONUNBUFFERED=1

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends vim tmux yq jq

# Install poetry
RUN pipx install poetry

# Set user to non-root
USER 1000:1000
ENV HOME=/home/vscode

# Install pyenv
RUN curl https://pyenv.run/ | /bin/bash
