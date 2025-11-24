FROM python:3.13-slim

# TEMPLATE: Add any system dependencies your service needs
# Example: RUN apt-get update && apt-get install -y package-name
RUN apt-get update && apt-get install -y libmagic1 build-essential

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create necessary directories
RUN mkdir -p /app

# TEMPLATE: Update the source code path with your service name
# Copy necessary files into the container
COPY ./pyproject.toml /app
COPY ./uv.lock /app
COPY ./src /app/src
COPY ./evals /app/evals

# Set working directory
WORKDIR /app

# Install dependencies using uv, build wheel as test for prod
RUN --mount=type=secret,id=uv_index_gemfury_username,env=UV_INDEX_GEMFURY_USERNAME \
    uv sync --frozen --no-dev && \
    uv build

# Update PATH to include Python scripts
ENV PATH=/usr/local/bin:$PATH

# TEMPLATE: Command to run the app at container start
CMD ["uv", "run", "--frozen", "--no-sync", "fastapi", "dev", "src/main.py", "--host", "0.0.0.0", "--port", "8080"]
