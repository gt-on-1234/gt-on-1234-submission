ARG SUPPLY_CHAIN_DATA_FILE

FROM python:3.13-slim AS base

ARG SUPPLY_CHAIN_DATA_FILE
ENV SUPPLY_CHAIN_DATA_FILE=${SUPPLY_CHAIN_DATA_FILE}

COPY . /app
EXPOSE 8080
WORKDIR /app
RUN pip install --no-cache-dir .

ENTRYPOINT ["uvicorn", "supply_chain_network:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
