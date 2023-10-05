#!/bin/bash
### Run this on the nfs node for deploying the mongo server
sudo apt-get update
sudo apt-get upgrade

curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get install mongodb

cp -v /local/repository/dbconfig.txt /etc/mongodb.config


sudo systemctl enable mongodb
sudo systemctl start mongodb
sudo apt install python3-pip
pip install pymongo
