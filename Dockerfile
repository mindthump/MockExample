FROM python:alpine
LABEL MAINTAINER=mindthump

RUN apk update && pip install pytest

COPY . /app

WORKDIR /app

# Testing command-line: "pytest -o junit_family=xunit2 --junitxml=xunit.xml"
CMD ["python", "badges.py"]

