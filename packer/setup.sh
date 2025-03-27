#!/bin/bash

# 1. Update the package lists for upgrades.
echo "Updating package lists..."
sudo apt-get update



# 2.Upgrade the packages on the system.
echo "Upgrading installed packages..."
sudo apt-get upgrade -y
sudo apt install unzip



# 3.install nginx
sudo apt-get install nginx -y



# 4.Install the MySQL client.
sudo apt install mysql-client -y



#5.creating user/user group for webapp
echo "Creating Linux group 'csye6225'..."
sudo groupadd -f csye6225
sudo useradd -m -g csye6225 -s /usr/sbin/nologin csye6225_user || echo "User already exists"
ls -ld /home/csye6225_user/



#6. unzip webapp
echo "Unziping webapp.tar.gz ..."
cd /opt/csye6225

sudo tar -xzvf /opt/csye6225/webappFlask.tar.gz

#chown to webapp
sudo chown -R csye6225_user:csye6225  /opt/csye6225/webappFlask



#7.setup python environment
pwd
sudo apt install python3.12-venv -y
sudo apt-get clean

echo "Creating python venv..."
echo $(pwd)

cd /opt/csye6225/webappFlask

echo $(pwd)
echo $(ls -al)

sudo -u csye6225_user  python3 -m venv venv
echo $(ls -al)

sudo -u csye6225_user bash -c "
    source venv/bin/activate &&
    pip install -r ./requirements.txt
    pwd
    ls -al
"



#8.install and config cloudwatch agent
#install agent
sudo apt install -y wget
wget https://amazoncloudwatch-agent.s3.amazonaws.com/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb

#config and start agent:
#this processes will be done by terraform...



#9.config systemd for webapp
echo "Configuring systemd for webapp..."

sudo cp webappFlask.service /etc/systemd/system/
sudo systemctl daemon-reload

echo "Setup complete."









#set up complete
echo "ec2 Setup complete."