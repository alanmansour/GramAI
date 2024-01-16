# Base image
FROM python:3.11.5-slim

EXPOSE $PORT

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements_app.txt requirements_app.txt
WORKDIR /
RUN pip install -r requirements_app.txt --no-cache-dir
RUN sudo wget \ https://dvc.org/deb/dvc.list \ -O /etc/apt/sources.list.d/dvc.list
RUN wget -qO - https://dvc.org/deb/iterative.asc | gpg --dearmor > packages.iterative.gpg
RUN sudo install -o root -g root -m 644 packages.iterative.gpg /etc/apt/trusted.gpg.d/
RUN rm -f packages.iterative.gpg
RUN sudo apt update
RUN sudo apt install dvc

COPY src/gramai_app.py src/gramai_app.py
COPY src/config.yaml src/config.yaml

RUN dvc init --no-scm
COPY .dvc/config .dvc/config
COPY models.dvc models.dvc
RUN dvc config core.no_scm true
RUN dvc pull

WORKDIR /src
CMD exec uvicorn gramai_app:app --port $PORT --host 0.0.0.0 --workers 1
