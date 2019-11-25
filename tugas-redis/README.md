# Implementasi Redis Cluster pada Wordpress
Bagas Yanuar S.
- [Implementasi Redis Cluster pada Wordpress](#implementasi-redis-cluster-pada-wordpress)
  - [1. Diagram Arsitektur Sistem](#1-diagram-arsitektur-sistem)
  - [2. Script provision](#2-script-provision)
  - [4. Services](#4-services)
  - [5. Script Bash untuk Aktivasi Service](#5-script-bash-untuk-aktivasi-service)
  - [6. Menghidupkan VM](#6-menghidupkan-vm)
  - [7. Memastikan Clustering Berjalan](#7-memastikan-clustering-berjalan)
  - [8. Pengujian Fail Over](#8-pengujian-fail-over)
  - [9. Instalasi Wordpress](#9-instalasi-wordpress)
  - [11. Instalasi Redis Object Cache pada wordpress1 <a name="rediscache"></a>](#11-instalasi-redis-object-cache-pada-wordpress1-a-name%22rediscache%22a)
  - [10. Pengujian dengan JMeter](#10-pengujian-dengan-jmeter)
## 1.  Diagram Arsitektur Sistem
![alt text](/images/arsitektur.jpg "Arsitektur Sistem")

|   Server    |      OS      |  RAM   |      IP       |
| :---------: | :----------: | :----: | :-----------: |
| wordpress 1 | Ubuntu 18.04 | 512 MB | 192.168.17.74 |
| wordpress 2 | Ubuntu 18.04 | 512 MB | 192.168.17.75 |
|   redis 1   | Ubuntu 18.04 | 512 MB | 192.168.17.76 |
|   redis 2   | Ubuntu 18.04 | 512 MB | 192.168.17.77 |
|   redis 3   | Ubuntu 18.04 | 512 MB | 192.168.17/78 |

Implementasi
 Membuat `Vagrantfile`
```
    $ vagrant init
```
    Dengan perintah tersebut, dibuatlah file `Vagrantfile`. Yang berisi tentang konfigurasi VM.

## 2. Script provision
    ```
    sudo cp /vagrant/sources/hosts /etc/hosts
    sudo cp '/vagrant/sources/sources.list' '/etc/apt/'

    sudo apt update -y
    ```
1. File Konfigurasi
   `redis1.conf`
   ```
    bind 192.168.17.76
    port 6379
    dir "/etc/redis"
   ```
   `redis2.conf`
   ```
    bind 192.168.17.77
    port 6379
    dir "/etc/redis"
    slaveof 192.168.17.76 6379
   ```
   `redis3.conf`
   ```
    bind 192.168.17.78
    port 6379
    dir "/etc/redis"
    slaveof 192.168.17.76 6379
   ```
   `sentinel1.conf`
   ```
    bind 192.168.17.76
    port 26379

    sentinel monitor redis-cluster 192.168.17.76 6379 2
    sentinel down-after-milliseconds redis-cluster 5000
    sentinel parallel-syncs redis-cluster 1
    sentinel failover-timeout redis-cluster 10000
   ```
   `sentinel2.conf`
   ```
    bind 192.168.17.77
    port 26379

    sentinel monitor redis-cluster 192.168.17.76 6379 2
    sentinel down-after-milliseconds redis-cluster 5000
    sentinel parallel-syncs redis-cluster 1
    sentinel failover-timeout redis-cluster 10000
   ```
   `sentinel3.conf`
   ```
    bind 192.168.17.78
    port 26379

    sentinel monitor redis-cluster 192.168.17.76 6379 2
    sentinel down-after-milliseconds redis-cluster 5000
    sentinel parallel-syncs redis-cluster 1
    sentinel failover-timeout redis-cluster 10000
   ```
## 4. Services
   
   `redis.service`
    ```
   [Unit]
    Description=Redis In-Memory Data Store
    After=network.target

    [Service]
    User=redis
    Group=redis
    ExecStart=/usr/local/bin/redis-server /etc/redis/redis.conf
    ExecStop=/usr/local/bin/redis-cli shutdown
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
   
   `redisentinel.service`
    ```
    [Unit]
    Description=Redis Sentinel
    After=network.target

    [Service]
    User=redis
    Group=redis
    ExecStart=/usr/local/bin/redis-server /etc/redis-sentinel.conf --sentinel
    ExecStop=/usr/local/bin/redis-cli shutdown
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

## 5. Script Bash untuk Aktivasi Service
   
   `redis1.sh`
    ```
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
    ```

    `redis2.sh`
    ```
    sudo apt-get install build-essential tcl -y
    sudo apt-get install libjemalloc-dev -y

    curl -O http://download.redis.io/redis-stable.tar.gz
    tar xzvf redis-stable.tar.gz
    cd redis-stable
    make
    # make test
    sudo make install

    sudo mkdir /etc/redis

    sudo cp /vagrant/config/redis2.conf /etc/redis/redis.conf
    sudo cp /vagrant/config/sentinel2.conf /etc/redis-sentinel.conf

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
    ```

    `redis3.sh`
    ```
    sudo apt-get install build-essential tcl -y
    sudo apt-get install libjemalloc-dev -y

    curl -O http://download.redis.io/redis-stable.tar.gz
    tar xzvf redis-stable.tar.gz
    cd redis-stable
    make
    # make test
    sudo make install

    sudo mkdir /etc/redis

    sudo cp /vagrant/config/redis3.conf /etc/redis/redis.conf
    sudo cp /vagrant/config/sentinel3.conf /etc/redis-sentinel.conf

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
    ```
    
    `wordpress.sh`
    ```
    # Install Apache2
    sudo apt install apache2 -y
    sudo ufw allow in "Apache Full"

    # Install PHP
    sudo apt install php libapache2-mod-php php-mysql php-pear php-dev -y
    sudo a2enmod mpm_prefork && sudo a2enmod php7.0
    sudo pecl install redis
    sudo echo 'extension=redis.so' >> /etc/php/7.2/apache2/php.ini

    # Install MySQL
    sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password admin'
    sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password admin'
    sudo apt install mysql-server -y
    sudo mysql_secure_installation -y
    sudo ufw allow 3306

    # Configure MySQL for Wordpress
    sudo mysql -u root -padmin < /vagrant/sql/wordpress.sql

    # Install Wordpress
    cd /tmp
    wget -c http://wordpress.org/latest.tar.gz
    tar -xzvf latest.tar.gz
    sudo mkdir -p /var/www/html
    sudo mv wordpress/* /var/www/html
    sudo cp /vagrant/wp-config.php /var/www/html/
    sudo chown -R www-data:www-data /var/www/html/
    sudo chmod -R 755 /var/www/html/
    sudo systemctl restart apache2
    ```
## 6. Menghidupkan VM
   ```
    $ vagrant up
   ```
   untuk setiap redis server, jalankan `redis1.sh`, `redis2.sh`, `redis3.sh`. Script tersebut menginstall service redis dan redis sentinel. Setelah service terpasang, untuk selanjutnya service hanya perlu distart `sudo systemctl start redis` `sudo systemctl start redisentinel`.
   
   Untuk memastikan service-service yang bersangkutan telah berjalan dapat dilakukan perintah `sudo systemctl status redis`, `sudo systemctl status redisentinel` 

## 7. Memastikan Clustering Berjalan
   akses cli redis dengan perintah
   `redis-cli -h 192.168.17.76`, `redis-cli -h 192.168.17.77`, `redis-cli -h 192.168.17.78`

   pada cli redis masing-masing server, jalankan perintah `info replication`. Berikut adalah gambar hasil perintah tersebut.

    ![Info Replication 1](/images/inforeplication2.png "inforeplication")

    ![Info Replication 2](/images/inforeplication3.png "inforeplication")

    ![Info Replication 3](/images/inforeplication4.png "inforeplication")


## 8.  Pengujian Fail Over
    Pengujian Fail Over dilakukan dengan cara menghentikan service server master, dan melihat apakah cluster akan tetap berjalan dengan memilih master yang baru atau tidak. Berikut adalah hasilnya.

    Pada awalnya `192.168.17.76` memiliki role sebagai master. Kini, `192.168.17.78` memiliki role sebagai master.
    ![Hasil Pengujian Fail Over](/images/hasilfailover.png "hasilfailover")

## 9. Instalasi Wordpress
    instalasi dapat dilakukan dengan mengunjungi alamat pada `192.168.17.74/index.php`, `192.168.17.75/index.php` browser, dan mengikuti tahapan dan petunjuk yang ada.

    Berikut adalah gambar website wordpress
    ![Website](/images/website.png "website")

## 11. Instalasi Redis Object Cache pada wordpress1 <a name="rediscache"></a>
    i. Login di `/wp-admin`, di bagian `Plugins`, cari dan install `Redis Cache Object`.
    ii. Pada `/var/www/html/wp-config.ph` di server wordpress1, tambah konfigurasi berikut.
    ```
    define('FS_METHOD', 'direct');
    define('WP_REDIS_SENTINEL', 'redis-cluster');
    define('WP_REDIS_SERVERS', ['tcp://192.168.17.76:26379', 'tcp://192.168.17.77:26379', 'tcp://192.168.17.78:26379']);
    ```
    iii. Aktifkan Plugin Redis Cache. Pada bagian `Diagnostic` akan terlihat seperti berikut
    ![diagnostic](/images/diagnostic.png "diagnostic")
    
## 10. Pengujian dengan JMeter
    
    Install `JDK` dan `JRE`, lalu install `JMeter`.
    Berikut adalah alamat yang berisi petunjuk instalasi `JDK`, `JRE`, `JMeter`
    [Instalasi JDK JRE](https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-on-ubuntu-18-04 "Instalasi JDK JRE")

    [Instalasi JMeter](https://jmeter.apache.org/download_jmeter.cgi "Instalasi Jmeter")
    
    Berikut adalah hasil pengujian dengan JMETER
    i. 50 koneksi
    ![jmeter50](/images/jmeter50.png "jmeter50")
    
    ii. 174 koneksi
    ![jmeter174](/images/jmeter174.png "jmeter174")
    iii. 274 koneksi
    ![jmeter274](/images/jmeter274.png "jmeter274")
    
    Kesimpulan Pengujian
    Dari hasil pengujian, terlihat hasilnya lebih baik pada pengujian tanpa redis cache. Adapun mengapa hal ini terjadi, kemungkinan adalah karena banyaknya request pada server redis lebih banyak dari pada request pada mysql. Hal tersebut menyebabkan overhead lebih dominan dari pada performa yang meningkat. Kemungkinan yang lain adalah alokasi RAM yang terlalu kecil.
    Untuk itu, dapat dicoba untuk menambah alokasi RAM, dan menggunakan redis cache pada kondisi yang memang membutuhkan/dapat memaksimalkan pengaruh.