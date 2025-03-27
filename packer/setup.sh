## 1. Update the package lists for upgrades.
#echo "Updating package lists..."
#sudo apt-get update
#
## 2.Upgrade the packages on the system.
#echo "Upgrading installed packages..."
#sudo apt-get upgrade -y
#
#sudo apt install unzip
#
## install nginx
#sudo apt-get install nginx -y
#
## 3.Install the MySQL client.
#sudo apt install mysql-client
#
#echo "Creating Linux group 'csye6225'..."
#sudo groupadd -f csye6225
#sudo useradd -m -g csye6225 -s /usr/sbin/nologin csye6225_user || echo "User already exists"
#ls -ld /home/csye6225_user/
#
#
#echo "Unziping webapp.tar.gz ..."
#cd /opt/csye6225
#sudo tar -xzvf /opt/csye6225/webappFlask.tar.gz
#
## make sure artifacts  must be owned by the user csye6225 and group csye6225
#sudo chown -R csye6225_user:csye6225  /opt/csye6225/webappFlask
#
##setup python environment
#pwd
#sudo apt install python3.12-venv -y
#sudo apt-get clean
#
#echo "Creating python venv..."
#echo $(pwd)
#
#cd /opt/csye6225/webappFlask
#
#echo $(pwd)
#echo $(ls -al)
#
#sudo -u csye6225_user  python3 -m venv venv
#echo $(ls -al)
#
#sudo -u csye6225_user bash -c "
#    source venv/bin/activate &&
#    pip install -r ./requirements.txt
#    pwd
#    ls -al
#    mkdir -p ./var/log/webapp && touch ./var/log/webapp/flaskapp.log
#"
#
## config systemd
#echo "Configuring systemd for webapp..."
#
#sudo cp webappFlask.service /etc/systemd/system/
#
#sudo systemctl daemon-reload
#
#echo "Setup complete."
#
##install and config cloudwatch agent
##install
#sudo apt install -y wget
#wget https://amazoncloudwatch-agent.s3.amazonaws.com/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
#sudo dpkg -i amazon-cloudwatch-agent.deb
#
##create log file
#sudo mkdir -p /var/log/csye6225/webapp_log/
#sudo touch  /var/log/csye6225/webapp_log/flaskapp.log
#sudo chown -R csye6225_user:csye6225 /var/log/csye6225
#
##config and start agent
# sudo bash -c "
#    /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
#    -a fetch-config \
#    -m ec2 \
#    -c file:/opt/csye6225/webappFlask/config/cloud_watch_agent.json \
#    -s
#  "
#
#sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status
#
#sudo systemctl enable amazon-cloudwatch-agent
#
#
