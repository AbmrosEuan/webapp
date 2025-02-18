#!/bin/bash
# 如果命令返回非零状态则立即退出 | Exit immediately if a command exits with a non-zero status.
set -e

# 1. 更新软件包列表 | 1. Update the package lists for upgrades.
echo "Updating package lists..."
sudo apt-get update

# 2. 升级系统中的软件包 | 2. Upgrade the packages on the system.
echo "Upgrading installed packages..."
sudo apt-get upgrade -y

# 3. 安装 MySQL 服务器 | 3. Install the MySQL server.
echo "Installing MySQL server..."
sudo apt-get install -y mysql-server

# 启动 MySQL 服务 | Start MySQL service.
echo "Starting MySQL service..."
sudo systemctl start mysql; sudo service mysql start

# 4. 在 MySQL 中创建数据库 csye6225-webapp | 4. Create the database 'csye6225-webapp' in MySQL.
# 使用 sudo 调用 mysql 命令行工具执行 SQL 语句 | Use sudo to run the mysql command-line tool to execute SQL.
echo "Creating MySQL database 'csye6225-webapp'..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS \`csye6225-webapp\`;"

# 5. 创建新的 Linux 组 csye6225webappGroup | 5. Create a new Linux group 'csye6225webappGroup'.
echo "Creating Linux group 'csye6225webappGroup'..."
sudo groupadd --force csye6225webappGroup

# 6. 创建新的用户 csye6225webapp-user，并设置其主目录，同时加入到 csye6225webappGroup | 6. Create a new user 'csye6225webapp-user', create its home directory and add it to the 'csye6225webappGroup' group.
echo "Creating Linux user 'csye6225webapp-user'..."
# -m：创建用户主目录 | -m: Create the user's home directory.
# -g：指定用户的主组 | -g: Specify the user's primary group.
sudo useradd -m -g csye6225webappGroup csye6225webapp-user || echo "User already exists"

# 7. 解压应用到 /opt/csye6225 目录 | 7. Unzip the application into the /opt/csye6225 directory.
echo "Preparing /opt/csye6225 directory and unzipping application..."
sudo mkdir -p /opt/csye6225
# 请确认 webapp.zip 文件在当前目录中，若不在则请修改路径 | Make sure the webapp.zip file is in the current directory; if not, adjust the path accordingly.
sudo unzip -o webapp.zip -d /opt/csye6225

# 8. 更新 /opt/csye6225 目录及其中内容的权限 | 8. Update the permissions of the /opt/csye6225 directory and its contents.
# 将所有者改为 csye6225webapp-user，组改为 csye6225webappGroup；并设置权限为 755 | Change owner to csye6225webapp-user, group to csye6225webappGroup; set permissions to 755.
echo "Updating permissions on /opt/csye6225 directory..."
sudo chown -R csye6225webapp-user:csye6225webappGroup /opt/csye6225
sudo chmod -R 755 /opt/csye6225

echo "Setup complete."


# before run shell:
#                 chmod +x setup.sh
#                 ./setup.sh
