FROM python:3.9

RUN python -m pip install --upgrade pip

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential

WORKDIR /app

COPY scm-api/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --src /usr/local/src

COPY . .

EXPOSE 5000
CMD [ "python", "scm-api/Api.py" ]