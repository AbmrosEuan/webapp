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
sudo apt-get install -y mysql-server

# 4.Ensure MySQL is enabled to start on boot
sudo systemctl enable mysql

# 启动 MySQL 服务 | Start MySQL service.
echo "Starting MySQL service..."

#echo "Creating MySQL database 'csye6225-webapp'..."
sudo mysql -uroot -p'12345678' "CREATE DATABASE IF NOT EXISTS \`csye6225-webapp\`;"
sudo mysql -uroot -p'12345678' "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '12345678'; FLUSH PRIVILEGES;"


# 6. Create a new user 'csye6225webapp-user', create its home directory and add it to the 'csye6225webappGroup' group.
#  -m: Create the user's home directory.
#  -g: Specify the user's primary group.
echo "Creating Linux group 'csye6225'..."
sudo groupadd -f csye6225
sudo useradd -m -g csye6225 -s /usr/sbin/nologin csye6225_user || echo "User already exists"
ls -ld /home/csye6225_user/


# unzip webapp.tar.gz/.zip
sudo cd /opt/csye6225/
ls
#sudo tar -xzvf /opt/csye6225/webapp.tar.gz -C ./
sudo unzip /opt/csye6225/webapp.zip

# make sure artifacts  must be owned by the user csye6225 and group csye6225
sudo chown -R csye6225_user:csye6225  /opt/csye6225/webapp


## 8. 更新 /opt/csye6225 目录及其中内容的权限
#echo "Updating permissions on /opt/csye6225 directory..."
#sudo chown -R csye6225webapp-user:csye6225webappGroup /opt/csye6225
#sudo chmod -R 755 /opt/csye6225

#setup python environment
sudo pwd
sudo cd /opt/csye6225/webapp
sudo apt install python3.12-venv -y

python3 -m venv env
source venv/bin/activate
pip install -r ./webappFlask/requirements.txt


sudo apt-get clean
echo "Setup complete."
