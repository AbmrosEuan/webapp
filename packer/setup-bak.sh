# 1. Update the package lists for upgrades.
echo "Updating package lists..."
sudo apt-get update

# 2.Upgrade the packages on the system.
echo "Upgrading installed packages..."
sudo apt-get upgrade -y

sudo apt install unzip

# install nginx
sudo apt-get install nginx -y

# 3.Install the MySQL server.
echo "Installing MySQL server..."
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password 12345678'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password 12345678'

sudo apt-get install -y mysql-server
sudo mysql -u root -p'12345678' -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '12345678'; FLUSH PRIVILEGES;"

# 4.Ensure MySQL is enabled to start on boot
# 启动 MySQL 服务 | Start MySQL service.
echo "Starting MySQL service..."
sudo systemctl enable mysql

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
"
#source venv/bin/activate && pip install -r ./requirements.txt

echo "Starting webapp..."
#source venv/bin/activate && python ./manage.py runserver
sudo cp webappFlask.service /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable webappFlask

sudo sleep 5 && echo$(systemctl status webappFlask)

echo "Setup complete."
