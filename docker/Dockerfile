FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    file \
    poppler-utils \
    bc \
    ghostscript \
    python \
    python-flask \
    gunicorn \
&& rm -rf /var/lib/apt/lists/*

ADD src /faas/

CMD ["gunicorn", \
        "--bind", "0.0.0.0:5000", \
        "--workers", "4", \
        "--preload", \
        "--reload", \
        "--chdir", "/faas", \
        "api:app"]
