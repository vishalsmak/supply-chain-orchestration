FROM python:3.9

RUN python -m pip install --upgrade pip

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    python3-dev \
    build-essential

COPY scm-analyze-service /app/scm-analyze-service
COPY scm-db /app/scm-db
COPY scm-entities /app/scm-entities

WORKDIR /app
RUN pip install -r scm-analyze-service/requirements.txt --src /usr/local/src

CMD [ "python", "-u", "scm-analyze-service/service.py" ]