FROM python:3.9

RUN python -m pip install --upgrade pip

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential

COPY scm-api /app/scm-api
COPY scm-entities /app/scm-entities
COPY scm-queue /app/scm-queue

WORKDIR /app
RUN pip install -r scm-api/requirements.txt --src /usr/local/src

EXPOSE 5000
CMD [ "python", "-u", "scm-api/Api.py", "-port_number=5000" ]