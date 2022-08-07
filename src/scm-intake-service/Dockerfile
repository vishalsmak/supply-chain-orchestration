FROM python:3.9

RUN python -m pip install --upgrade pip

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    python3-dev \
    build-essential

COPY scm-intake-service /app/scm-intake-service
COPY scm-entities /app/scm-entities
COPY scm-queue /app/scm-queue
COPY scm-db /app/scm-db

WORKDIR /app
RUN pip install -r scm-intake-service/requirements.txt --src /usr/local/src

CMD [ "python", "-u", "scm-intake-service/service.py" ]