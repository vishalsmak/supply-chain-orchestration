FROM python:3.9

RUN python -m pip install --upgrade pip

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential

COPY scm-dash /app/scm-dash
COPY scm-db /app/scm-db
COPY scm-entities /app/scm-entities

WORKDIR /app
RUN pip install -r scm-dash/requirements.txt --src /usr/local/src

EXPOSE 4000
CMD [ "python", "-u", "scm-dash/dashboard.py" ]