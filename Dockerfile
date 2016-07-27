FROM ubuntu:trusty
MAINTAINER Ryan Lane <ryan@ryandlane.com>

RUN apt-get update && \
    # For frontend
    apt-get install -y ruby-full npm nodejs nodejs-legacy git git-core && \
    # For backend
    apt-get install -y python python-pip python-dev build-essential libffi-dev

ADD ./requirements.txt /srv/signup/requirements.txt
ADD ./package.json /srv/signup/package.json
ADD ./bower.json /srv/signup/bower.json

WORKDIR /srv/signup

RUN pip install -r requirements.txt

RUN gem install compass && \
    npm install grunt-cli && \
    npm install

ADD . /srv/signup

RUN node_modules/grunt-cli/bin/grunt build

EXPOSE 80

CMD ["gunicorn","wsgi:app","--workers=2","-k","gevent","--access-logfile=-","--error-logfile=-"]
