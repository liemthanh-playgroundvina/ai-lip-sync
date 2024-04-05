# Docker
build:
	docker pull python:3.11-slim-bullseye
	docker build -t ai-lip-sync -f Dockerfile .

start:
	docker compose -f docker-compose.yml down
	docker compose -f docker-compose.yml up -d

stop:
	docker compose -f docker-compose.yml down

#cmd-image:
#	docker run -it --gpus all --rm ai-cover-gen /bin/bash