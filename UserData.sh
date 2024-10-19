#!/bin/bash


#Install git and clone files to the Web Server 
sudo yum update -y   # For Amazon Linux or CentOS
sudo yum install -y git
cd 
mkdir App
sudo mkdir .aws
cd App
git clone https://github.com/roee4643/PokemonApi
cd ..

sudo touch .aws/credentials


sudo mv App home/ec2-user/
sudo mv .aws home/ec2-user/



sudo python3 -m ensurepip --upgrade
sudo /usr/bin/python3 -m pip install --upgrade pip

pip3 install boto3

# Add the AWS credentials as environment variables to the profile
echo "export AWS_ACCESS_KEY_ID= {AWS_ACCESS_KEY_ID} " >> /etc/profile
echo "export AWS_SECRET_ACCESS_KEY= {AWS_SECRET_ACCESS_KEY} " >> /etc/profile
echo "export AWS_SESSION_TOKEN= {AWS_SESSION_TOKEN}">> /etc/profile
echo "export AWS_DEFAULT_REGION=us-west-2" >> /etc/profile

# Apply the changes
source /etc/profile


cd /home/ec2-user/App/PokemonApi
python3 create_databaseDynamo.py
python3 PokemonMainApi2.py

