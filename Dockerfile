FROM python:alpine
LABEL MAINTAINER=mindthump

RUN apk update && apk add pytest

COPY . /app

WORKDIR /app

CMD /bin/sh