#!/bin/bash


#Install git and clone files to the Web Server 
sudo yum update -y   # For Amazon Linux or CentOS
sudo yum install -y git
cd 
mkdir App
cd App
git clone https://github.com/roee4643/PokemonApi
sudo python3 -m ensurepip --upgrade
sudo /usr/bin/python3 -m pip install --upgrade pip
sudo chmod u+w /App/gitLab/PokemonDB.json
sudo chown ec2-user /App/PokemonApi/PokemonDB.json



#sudo python3 -m venv myenv
#sudo source myenv/bin/activate
#sudo pip install boto3




