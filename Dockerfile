FROM python:slim@sha256:83ff1d245a3d57d04152252d3ef9cb361494d0b3395abd65a5ebe91c401c8e83
COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /uvx /bin/

WORKDIR /app

RUN uv python install 3.13.15

COPY pyproject.toml uv.lock .
RUN uv sync --locked --no-install-project --no-dev

COPY . .
RUN uv run manage.py migrate
RUN uv run manage.py loaddata vote/fixtures/seed.json

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["gunicorn", "valgsystem.wsgi", "--bind", "0.0.0.0:8000"]