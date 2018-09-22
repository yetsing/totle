set -ex

# 换源
# cp /var/www/club/misc/sources.list /etc/apt/sources.list
# mkdir -p /root/.pip
# cp /var/www/club/misc/pip.conf /root/.pip/pip.conf
# apt-get update

# 系统设置
apt-get -y install  zsh curl ufw
# sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 25
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# 装依赖
add-apt-repository -y ppa:deadsnakes/ppa

debconf-set-selections /var/www/club/database_secret.conf
apt-get install -y mysql-server

debconf-set-selections /var/www/club/postfix.conf
apt-get install -y postfix

apt-get install -y git supervisor nginx python3.6 redis-server
python3.6 /var/www/club/get-pip.py
pip3 install jinja2 flask gevent gunicorn pymysql flask_sqlalchemy flask_mail redis forgerypy eventlet flask-socketio

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# 建立一个软连接
cp /var/www/club/club.conf /etc/supervisor/conf.d/club.conf
cp /var/www/weibo/weibo.conf /etc/supervisor/conf.d/weibo.conf
cp /var/www/chat_room/chat_room.conf /etc/supervisor/conf.d/chat_room.conf
# 不要在 sites-available 里面放任何东西
cp /var/www/club/club.nginx /etc/nginx/sites-enabled/club
chmod -R o+rwx /var/www/club

# 初始化
cd /var/www/club
python3.6 reset.py
cd /var/www/weibo
python3.6 reset.py

# 重启服务器
service supervisor restart
service nginx restart

echo 'success'
echo 'ip'
hostname -I