#!/bin/bash

# Install Docker, build and launch concerteur server on ubuntu

set -eu

cd /opt

sudo apt-get update

sudo apt-get install -y \
    git \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose

git clone https://github.com/e-lie/concerteurServer.git /opt/concerteur_server

docker-compose up -d -f /opt/concerteur_server/docker-compose.yml

sleep 10

docker ps -a