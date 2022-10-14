ARG PYTHON_VERSION=3.10

# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:${PYTHON_VERSION}-alpine as fastapi_python

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# For reference app folder as package
ENV PYTHONPATH=/srv

COPY docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint
RUN chmod +x /usr/local/bin/docker-entrypoint

WORKDIR /srv/app

# Install requirements
COPY requirements.txt .
RUN apk add --no-cache postgresql-libs; \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev; \
    python3 -m pip install -r requirements.txt --no-cache-dir; \
    apk --purge del .build-deps

# Copy project files
COPY ./app .

ENTRYPOINT ["docker-entrypoint"]

CMD ["python3", "main.py"]
