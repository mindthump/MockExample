FROM python:alpine
LABEL MAINTAINER=mindthump

RUN apk update && pip install pytest

COPY . /app

WORKDIR /app

ENTRYPOINT ["python"]
# Testing CMD: "-m pytest -o junit_family=xunit2 --junitxml=xunit.xml
CMD ["badges.py"]

