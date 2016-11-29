#!/usr/bin/env bash

git clone https://github.com/JeffersonLab/xmsg_python.git ./claraweb/build/xmsg
git clone https://github.com/JeffersonLab/clara-python.git ./claraweb/build/clara

cd claraweb

docker-compose -f ../scripts/docker-compose.dev.yml build
docker-compose -f ../scripts/docker-compose.dev.yml up -d
