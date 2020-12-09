FROM python:3.9.1-slim-buster AS build

ENV VIRTUAL_ENV=/opt/venv
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv $VIRTUAL_ENV && \
    $VIRTUAL_ENV/bin/pip install --upgrade pip
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

FROM build AS build-venv
COPY requirements.txt .
RUN pip install --disable-pip-version-check -r requirements.txt

FROM python:3.9.1-slim-buster AS runtime
COPY --from=build-venv /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /app
WORKDIR /app
ENTRYPOINT ["python", "go-spider.py"]