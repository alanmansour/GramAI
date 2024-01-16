# Base image
FROM python:3.11.5-slim

EXPOSE $PORT

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements_gapp.txt requirements_gapp.txt
WORKDIR /
RUN pip install -r requirements_gapp.txt --no-cache-dir

COPY src/gramai_gapp.py src/gramai_gapp.py
COPY src/assets src/assets

WORKDIR /src
CMD python gramai_gapp.py 0.0.0.0 $PORT
