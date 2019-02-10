FROM python:3.7-slim
# MAINTAINER Joshua Rincon <joshua.rincon@gmail.com>

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends

ENV INSTALL_PATH /felinefolia
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# temporary fix for https://github.com/celery/celery/issues/4849 
# remove when ^4.1.2 is released
RUN pip install --upgrade https://github.com/celery/celery/tarball/master

COPY . .
RUN pip install --editable .

CMD gunicorn -c "python:config.gunicorn" "felinefolia.app:create_app()"
