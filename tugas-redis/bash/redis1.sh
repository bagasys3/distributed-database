sudo apt-get install build-essential tcl -y
sudo apt-get install libjemalloc-dev -y

curl -O http://download.redis.io/redis-stable.tar.gz
tar xzvf redis-stable.tar.gz
cd redis-stable
make
# make test
sudo make install

sudo mkdir /etc/redis

sudo cp /vagrant/config/redis1.conf /etc/redis/redis.conf
sudo cp /vagrant/config/sentinel1.conf /etc/redis-sentinel.conf

sudo cp /vagrant/service/redis.service /etc/systemd/system/redis.service
sudo cp /vagrant/service/redisentinel.service /etc/systemd/system/redisentinel.service

sudo adduser --system --group --no-create-home redis
sudo mkdir /var/lib/redis
sudo chown redis:redis /var/lib/redis
sudo chmod 770 /var/lib/redis

sudo systemctl start redis
sudo systemctl status redis

sudo chmod 777 /etc/redis-sentinel.conf
sudo systemctl start redisentinel
sudo systemctl status redisentinel

sudo chmod -R 777 /etc/redis
sudo systemctl restart redis
sudo systemctl status redis