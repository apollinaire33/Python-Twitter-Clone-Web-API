FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /code
COPY . /code/

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

RUN chmod 755 /code/docker-entrypoint.sh

CMD ["bash", "/code/docker-entrypoint.sh"]