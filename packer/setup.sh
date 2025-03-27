# 1. Update the package lists for upgrades.
echo "Updating package lists..."
sudo apt-get update

# 2.Upgrade the packages on the system.
echo "Upgrading installed packages..."
sudo apt-get upgrade -y

sudo apt install unzip

# install nginx
sudo apt-get install nginx -y

# 3.Install the MySQL client.
sudo apt install mysql-client

echo "Creating Linux group 'csye6225'..."
sudo groupadd -f csye6225
sudo useradd -m -g csye6225 -s /usr/sbin/nologin csye6225_user || echo "User already exists"
ls -ld /home/csye6225_user/


echo "Unziping webapp.tar.gz ..."
cd /opt/csye6225
sudo tar -xzvf /opt/csye6225/webappFlask.tar.gz

# make sure artifacts  must be owned by the user csye6225 and group csye6225
sudo chown -R csye6225_user:csye6225  /opt/csye6225/webappFlask

#setup python environment
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
    mkdir -p ./var/log/webapp && touch ./var/log/webapp/flaskapp.log
"

# config systemd
echo "Configuring systemd for webapp..."

sudo cp webappFlask.service /etc/systemd/system/

sudo systemctl daemon-reload

#enable webapp in ec2 user data  using terraform
#sudo systemctl enable webappFlask
#sudo sleep 5 && echo$(systemctl status webappFlask)

echo "Setup complete."
