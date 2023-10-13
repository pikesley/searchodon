FROM python:3.11

ARG PROJECT

RUN apt-get update && apt-get install -y make
RUN pip install --upgrade pip

COPY ./ /opt/${PROJECT}
WORKDIR /opt/${PROJECT}
RUN python -m pip install .[test]
