#!/bin/bash


#Install git and clone files to the Web Server 
sudo yum update -y   # For Amazon Linux or CentOS
sudo yum install -y git
cd 
mkdir App
cd App
git clone https://github.com/roee4643/gitLab
sudo python3 -m ensurepip --upgrade
sudo /usr/bin/python3 -m pip install --upgrade pip
sudo chmod u+w /App/gitLab/PokemonDB.json
sudo chown ec2-user /App/gitLab/PokemonDB.json



#sudo yum install -y python3-venv
#python3 -m venv venv
#source venv/bin/activate
#pip3 install -r requirements.txt
#python3 PokemonMainApi.py   # Replace with your app's entry point



