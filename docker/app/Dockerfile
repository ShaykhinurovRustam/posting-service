FROM python:3.10.13

RUN mkdir /app
WORKDIR /app

COPY /pyproject.toml .
COPY /poetry.lock .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

RUN chmod a+x docker/app/*.sh