FROM python:3.12
COPY --from=ghcr.io/astral-sh/uv:0.5.2 /uv /bin/uv

ENV UV_LINK_MODE=copy
WORKDIR /app
COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-cache --compile-bytecode

EXPOSE 8000

ENTRYPOINT [ "/app/.venv/bin/fastapi", "run", "src/tso_api/main.py" ]
