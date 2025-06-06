FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy


ENV UV_PYTHON_INSTALL_DIR=/python


ENV UV_PYTHON_PREFERENCE=only-managed


RUN uv python install 3.13

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM debian:bookworm-slim


COPY --from=builder --chown=python:python /python /python


COPY --from=builder --chown=app:app /app /app
RUN chmod +x /app/entrypoint.sh


ENV PATH="/app/.venv/bin:$PATH"


# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
