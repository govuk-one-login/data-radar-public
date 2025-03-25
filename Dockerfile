FROM python:3.12-slim-bullseye

RUN apt-get update -y &&  apt-get install --no-install-recommends -y && apt-get upgrade -y  \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
COPY README.md /app/README.md

RUN poetry install


COPY ./assets /app/assets
COPY ./data /app/data
COPY pdAutoRead.py pdAutoRead.py
COPY app.py app.py

EXPOSE 8050
CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:8050", "app:server"]