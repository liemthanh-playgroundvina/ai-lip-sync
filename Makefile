download_model:
	curl -o ./gfpgan/weights/ai_lip_sync.zip https://aiservices-bucket.s3.ap-southeast-1.amazonaws.com/ai_model/ai-cover/ai_lip_sync.zip
	unzip ./gfpgan/weights/ai_lip_sync.zip -d ./gfpgan/weights
	mv ./gfpgan/weights/wav2lip.pth ./scripts/wav2lip/checkpoints
	mv ./gfpgan/weights/s3fd.pth ./scripts/wav2lip/face_detection/detection/sfd
	mv ./gfpgan/weights/shape_predictor_68_face_landmarks.dat ./scripts/wav2lip/predicator

config:
	cp configs/env.example configs/.env
	# And add params ...

# Docker
build:
	docker pull python:3.11-slim-bullseye
	docker build -t ai-lip-sync -f Dockerfile .

start:
	docker compose -f docker-compose.yml down
	docker compose -f docker-compose.yml up -d

start-prod:
	docker compose -f docker-compose-prod.yml down
	docker compose -f docker-compose-prod.yml up -d

stop:
	docker compose -f docker-compose.yml down

stop-prod:
	docker compose -f docker-compose-prod.yml down

# Checker
cmd-image:
	docker run -it --gpus all --rm ai-lip-sync /bin/bash

cmd-worker:
	docker compose exec worker-ai-lip-sync /bin/bash