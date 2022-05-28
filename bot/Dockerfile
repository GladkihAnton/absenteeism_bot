FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY bot/pyproject.toml /code/

RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry==1.1.13

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && pip cache purge \
    && rm -rf /root/.cache/pypoetry/

COPY bot .
