# !/bin/bash

# docker 설치
# docker compose 설치
# dockerhub login

echo "start docker-compose up: ubuntu"
sudo docker compose -f docker-compose.prod.yaml down
# image 있는지 확인(err 뜨지만 멈추지는 않음)
sudo docker rmi bshlab671/aid_web
sudo docker pull bshlab671/aid_web
sudo docker compose -f docker-compose.prod.yaml up -d
