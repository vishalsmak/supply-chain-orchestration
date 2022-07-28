FROM python:3.9

RUN python -m pip install --upgrade pip

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    python3-dev \
    build-essential

WORKDIR /app

COPY scm-intake-service/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --src /usr/local/src

COPY . .

CMD [ "python", "-u", "scm-intake-service/service.py" ]