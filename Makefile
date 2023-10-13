PROJECT = $(shell basename $(shell pwd))
ID = pikesley/${PROJECT}

default: all

build:
	docker build \
		--build-arg PROJECT=${PROJECT} \
		--tag ${ID} .

run:
	docker run \
		--name ${PROJECT} \
		--volume $(shell pwd):/opt/${PROJECT} \
		--publish 8000:8000 \
		--rm \
		--interactive \
		--tty \
		${ID} bash

exec:
	docker exec \
		--interactive \
		--tty \
		${PROJECT} \
		bash

black:
	python -m black .

isort:
	python -m isort .

format: black isort

lint:
	python -m ruff check .

clean:
	@find . -depth -name .ruff_cache -exec rm -fr {} \;
	@find . -depth -name __pycache__ -exec rm -fr {} \;

all: format lint clean

serve:
	python webserver.py
