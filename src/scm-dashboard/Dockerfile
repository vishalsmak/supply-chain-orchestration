FROM python:3.9

RUN python -m pip install --upgrade pip

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential

COPY scm-dashboard /app/scm-dashboard
COPY scm-db /app/scm-db
COPY scm-common /app/scm-common

WORKDIR /app
RUN pip install -r scm-dashboard/requirements.txt --src /usr/local/src

EXPOSE 4000
CMD [ "python", "-u", "scm-dashboard/run.py", "-port_number=4000" ]