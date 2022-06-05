BUILD_TAG         := local
TS                := $(shell date "+%Y%m%d%H%M%S")

IMAGE_ID_FILE     := .iidfile
IMAGE_ID          ?= $(shell cat $(IMAGE_ID_FILE))
TS                ?= $(shell date "+%Y%m%d%H%M%S")
VERSION           ?= $(shell cat app/VERSION)

APP_NAME		  := stock_db

RELEASE_TAG       := $(VERSION)-$(TS)-$(CI_COMMIT)

local: clean build

build:
	docker build -t $(APP_NAME) \
		--platform=linux/amd64 \
		--iidfile $(IMAGE_ID_FILE) \
		.

clean:
	-docker rmi -f $(IMAGE_ID) 2>/dev/null
	-rm -f $(IMAGE_ID_FILE)

run-local: run-local-clean
	@./runlocal.sh run_local $(IMAGE_ID)

run-local-clean:
	-@./runlocal.sh destroy

stop:
	docker stop $$(docker ps -f "name=stock_db" --format "{{.ID}}")

docker-bash:
	docker exec -it $$(docker ps -f "name=stock_db" --format "{{.ID}}") bash

.PHONY: build stop run
