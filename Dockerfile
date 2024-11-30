FROM python:3.12
COPY --from=ghcr.io/astral-sh/uv:0.5.2 /uv /bin/uv

ENV UV_LINK_MODE=copy
WORKDIR /app
COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-cache --compile-bytecode && \
    uv pip install .

EXPOSE 50051

LABEL org.opencontainers.image.source="https://github.com/twosmallonions/tso-scraper"
LABEL org.opencontainers.image.description="TSO recipe scraper"
LABEL org.opencontainers.image.licenses=MIT

ENTRYPOINT [ "/app/.venv/bin/python", "-m", "tso_scraper.main"]
