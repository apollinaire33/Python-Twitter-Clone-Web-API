FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get upgrade -y

ADD requirements.txt /code/
WORKDIR /code

RUN pip install -r requirements.txt

WORKDIR /code
COPY . /code/

RUN chmod 755 /code/docker-entrypoint.sh

CMD ["bash", "/code/docker-entrypoint.sh"]