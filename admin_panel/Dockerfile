FROM python:3.10

ENV PYTHONUNBUFFERED=1

COPY admin_panel/scripts scripts
RUN ["chmod", "+x", "scripts/web/startup.sh"]

WORKDIR /code
COPY admin_panel/pyproject.toml /code/

RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry==1.1.13

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && pip cache purge \
    && rm -rf /root/.cache/pypoetry/

COPY admin_panel .

