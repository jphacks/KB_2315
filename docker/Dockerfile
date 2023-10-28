FROM python:3.11-slim

COPY ../. /src
WORKDIR /src

ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID dev &&  \
    useradd -l -m -u $UID -g $GID dev && \
    pip install -r requirements.lock --no-cache-dir

USER dev
CMD ["python", "main.py"]