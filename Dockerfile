FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /code
COPY . /code/

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

RUN chmod 755 /code/run_web.sh && chmod 755 /code/run_celery.sh

CMD ["bash", "/code/run_web.sh"]