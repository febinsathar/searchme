FROM python:3.6-alpine


RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

WORKDIR /home/app

#If we add the requirements and install dependencies first, docker can use cache if requirements don't change
ADD requirements.txt /home/app
RUN pip install -r requirements.txt

ADD . /home/app
CMD start_prod.sh

EXPOSE 5000