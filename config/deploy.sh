# !/bin/bash

# docker 설치
# docker compose 설치
# dockerhub login

echo "start docker-compose up: ubuntu"
sudo docker compose -f docker-compose.prod.yaml down
sudo docker rmi bshlab671/aid_web
sudo docker pull bshlab671/aid_web
sudo docker compose -f docker-copmose.prod.yaml up -d
