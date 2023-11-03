# !/bin/bash

# docker 설치
# docker compose 설치
# dockerhub login

echo "start docker-compose up: ubuntu"
sudo docker compose -f docker-compose.test.yaml down
# image 있는지 확인(err 뜨지만 멈추지는 않음)
sudo docker rmi bshlab671/aid_web_test
sudo docker pull bshlab671/aid_web_test
sudo docker compose -f docker-compose.test.yaml up -d
