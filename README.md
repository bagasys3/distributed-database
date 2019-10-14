# distributed-database

# Desain Infrastruktur

## Gambar

![Desain Infrastruktur](design/desain.png)

## Spesifikasi

- 3 MySQL Server Ubuntu 18.04 RAM 1024MB IP 192.168.17.74 - 192.168.17.76
- 1 Proxy MySQL Ubuntu 18.04 RAM 1024MB IP 192.168.17.77
- 1 Apache Web Server Ubuntu 18.04 RAM 1024MB Localhost

# Dokumentasi Vagrant Tugas ETS BDT

## Vagrant File

### 5 Konfigurasi dasar vagrant

`config.vm.box` - Operating System

`config.vm.provider` - Provider yang digunakan. Contoh: virtual Box

`config.vm.network`- Bagaimana host (komputer kita) melihat box.

`config.vm.synced_folder` Bagaimana kita mengakses file-file dari komputer kita

`config.vm.provision`- Apa yang kita ingin pasang atau atur. Contoh: install php, install mysql server.

### vagrantFile

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

Vagrant.configure("2") do |config|
  
  # MySQL Cluster dengan 3 node
  (1..3).each do |i|
    config.vm.define "db#{i}" do |node|
      node.vm.hostname = "db#{i}"
      node.vm.box = "bento/ubuntu-16.04" 
      node.vm.network "private_network", ip: "192.168.17.#{73+i}"

      # Opsional. Edit sesuai dengan nama network adapter di komputer
      #node.vm.network "public_network", bridge: "Qualcomm Atheros QCA9377 Wireless Network Adapter"
      
      node.vm.provider "virtualbox" do |vb|
        vb.name = "db#{i}"
        vb.gui = false
        vb.memory = "512"
      end
  
      node.vm.provision "shell", path: "deployMySQL1#{i}.sh", privileged: false
    end
  end
```

Code di atas melakukan iterasi i dari 1 sampai 3. Lalu di setiap iterasi didefinisikan sebuahbox. Terbentuk 3 box dengan hostname `db1`, `db2`, `db3`, Operating System `bento/ubuntu-16.04`, ip `192.168.17.74`, `192.168.17.75`, `192.168.17.76`. 

Lalu untuk untuk providernya digunakan virtualbox dengan nama `db1`, `db2`, `db3`, tidak menggunakan gui, dan memory 512MB.

Terakhir, untuk masing-masing vm dilakukan provisioniing, dengan memanggil file bash yang sesuai dengan masing-masing VM. Dalam file bash inilah setup dari box.

```ruby
config.vm.define "proxy" do |proxy|
    proxy.vm.hostname = "proxy"
    proxy.vm.box = "bento/ubuntu-16.04"
    proxy.vm.network "private_network", ip: "192.168.17.77"
    #proxy.vm.network "public_network",  bridge: "Qualcomm Atheros QCA9377 Wireless Network Adapter"
    
    proxy.vm.provider "virtualbox" do |vb|
      vb.name = "proxy"
      vb.gui = false
      vb.memory = "512"
    end

    proxy.vm.provision "shell", path: "deployProxySQL.sh", privileged: false
  end

end
```

Code di atas mendefinisikan sebuah box dengan hostname `proxy` , Operating System `bento/ubuntu-16.04`, ip `192.168.17.77`. Provider yang digunakan adalah virtualbox dengan nama proxy, tanpa GUI, dan memory 512MB. Lalu terakhir dilakukan provisioning dengan menjalankan file bash `deployProxySQL.sh` 



## File Bash yang Dipanggil vagrantFile untuk Provisioning

### deployMySQL11.sh Provisioning untuk db1

```ruby
# Changing the APT sources.list to kambing.ui.ac.id
sudo cp '/vagrant/sources.list' '/etc/apt/sources.list'

# Updating the repo with the new sources
sudo apt-get update -y

# Install required library
sudo apt-get install libaio1
sudo apt-get install libmecab2

# Get MySQL binaries
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-common_5.7.23-1ubuntu16.04_amd64.deb
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-community-client_5.7.23-1ubuntu16.04_amd64.deb
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-client_5.7.23-1ubuntu16.04_amd64.deb
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-community-server_5.7.23-1ubuntu16.04_amd64.deb

# Setting input for installation
sudo debconf-set-selections <<< 'mysql-community-server mysql-community-server/root-pass password admin'
sudo debconf-set-selections <<< 'mysql-community-server mysql-community-server/re-root-pass password admin'

# Install MySQL Community Server
sudo dpkg -i mysql-common_5.7.23-1ubuntu16.04_amd64.deb
sudo dpkg -i mysql-community-client_5.7.23-1ubuntu16.04_amd64.deb
sudo dpkg -i mysql-client_5.7.23-1ubuntu16.04_amd64.deb
sudo dpkg -i mysql-community-server_5.7.23-1ubuntu16.04_amd64.deb

# Allow port on firewall
sudo ufw allow 33061
sudo ufw allow 3306

# Copy MySQL configurations
sudo cp /vagrant/my11.cnf /etc/mysql/my.cnf

# Restart MySQL services
sudo service mysql restart

# Cluster bootstrapping
sudo mysql -u root -padmin < /vagrant/cluster_bootstrap.sql
sudo mysql -u root -padmin < /vagrant/addition_to_sys.sql
sudo mysql -u root -padmin < /vagrant/create_proxysql_user.sql
```

Di atas adalah perintah-perintah yang dijalankan pada terminal box `db1`. Ini adalah setup untuk box `db1` Hal-hal yang dilakukan adalah

- Changing the APT sources.list to kambing.ui.ac.id
- Updating the repo with the new sources
- Install required library
-  Get MySQL binaries
- Setting input for installation
- Install MySQL Community Server
-  Allow port on firewall
-  Copy MySQL configurations
- Restart MySQL services
- Cluster bootstrapping

### deployMySQL12.sh Provisioning untuk db2

```ruby
# Changing the APT sources.list to kambing.ui.ac.id
sudo cp '/vagrant/sources.list' '/etc/apt/sources.list'

# Updating the repo with the new sources
sudo apt-get update -y

# Install required library
sudo apt-get install libaio1
sudo apt-get install libmecab2

# Get MySQL binaries
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-common_5.7.23-1ubuntu16.04_amd64.deb
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-community-client_5.7.23-1ubuntu16.04_amd64.deb
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-client_5.7.23-1ubuntu16.04_amd64.deb
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-community-server_5.7.23-1ubuntu16.04_amd64.deb

# Setting input for installation
sudo debconf-set-selections <<< 'mysql-community-server mysql-community-server/root-pass password admin'
sudo debconf-set-selections <<< 'mysql-community-server mysql-community-server/re-root-pass password admin'

# Install MySQL Community Server
sudo dpkg -i mysql-common_5.7.23-1ubuntu16.04_amd64.deb
sudo dpkg -i mysql-community-client_5.7.23-1ubuntu16.04_amd64.deb
sudo dpkg -i mysql-client_5.7.23-1ubuntu16.04_amd64.deb
sudo dpkg -i mysql-community-server_5.7.23-1ubuntu16.04_amd64.deb

# Allow port on firewall
sudo ufw allow 33061
sudo ufw allow 3306

# Copy MySQL configurations
sudo cp /vagrant/my12.cnf /etc/mysql/my.cnf

# Restart MySQL services
sudo service mysql restart

# Cluster bootstrapping
sudo mysql -u root -padmin < /vagrant/cluster_member.sql
```

Di atas adalah perintah-perintah yang dijalankan pada terminal box `db2`. Ini adalah setup untuk box `db2` Hal-hal yang dilakukan adalah

- Changing the APT sources.list to kambing.ui.ac.id
- Updating the repo with the new sources
- Install required library
-  Get MySQL binaries
- Setting input for installation
- Install MySQL Community Server
-  Allow port on firewall
-  Copy MySQL configurations
- Restart MySQL services
- Cluster bootstrapping

### deployMySQL13.sh Provisioning untuk db3

```ruby
# Changing the APT sources.list to kambing.ui.ac.id
sudo cp '/vagrant/sources.list' '/etc/apt/sources.list'

# Updating the repo with the new sources
sudo apt-get update -y

# Install required library
sudo apt-get install libaio1
sudo apt-get install libmecab2

# Get MySQL binaries
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-common_5.7.23-1ubuntu16.04_amd64.deb
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-community-client_5.7.23-1ubuntu16.04_amd64.deb
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-client_5.7.23-1ubuntu16.04_amd64.deb
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-community-server_5.7.23-1ubuntu16.04_amd64.deb

# Setting input for installation
sudo debconf-set-selections <<< 'mysql-community-server mysql-community-server/root-pass password admin'
sudo debconf-set-selections <<< 'mysql-community-server mysql-community-server/re-root-pass password admin'

# Install MySQL Community Server
sudo dpkg -i mysql-common_5.7.23-1ubuntu16.04_amd64.deb
sudo dpkg -i mysql-community-client_5.7.23-1ubuntu16.04_amd64.deb
sudo dpkg -i mysql-client_5.7.23-1ubuntu16.04_amd64.deb
sudo dpkg -i mysql-community-server_5.7.23-1ubuntu16.04_amd64.deb

# Allow port on firewall
sudo ufw allow 33061
sudo ufw allow 3306

# Copy MySQL configurations
sudo cp /vagrant/my13.cnf /etc/mysql/my.cnf

# Restart MySQL services
sudo service mysql restart

# Cluster bootstrapping
sudo mysql -u root -padmin < /vagrant/cluster_member.sql
```

Di atas adalah perintah-perintah yang dijalankan pada terminal box `db3`.  Hal-hal yang dilakukan adalah

- Changing the APT sources.list to kambing.ui.ac.id
- Updating the repo with the new sources
- Install required library
-  Get MySQL binaries
- Setting input for installation
- Install MySQL Community Server
-  Allow port on firewall
-  Copy MySQL configurations
- Restart MySQL services
- Cluster bootstrapping

### deployProxySQL.sh Provisioning untuk proxy

```ruby
# Changing the APT sources.list to kambing.ui.ac.id
sudo cp '/vagrant/sources.list' '/etc/apt/sources.list'

# Updating the repo with the new sources
sudo apt-get update -y

cd /tmp
curl -OL https://github.com/sysown/proxysql/releases/download/v1.4.4/proxysql_1.4.4-ubuntu16_amd64.deb
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-common_5.7.23-1ubuntu16.04_amd64.deb
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-community-client_5.7.23-1ubuntu16.04_amd64.deb
curl -OL https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-client_5.7.23-1ubuntu16.04_amd64.deb

sudo apt-get install libaio1
sudo apt-get install libmecab2

sudo dpkg -i proxysql_1.4.4-ubuntu16_amd64.deb
sudo dpkg -i mysql-common_5.7.23-1ubuntu16.04_amd64.deb
sudo dpkg -i mysql-community-client_5.7.23-1ubuntu16.04_amd64.deb
sudo dpkg -i mysql-client_5.7.23-1ubuntu16.04_amd64.deb

sudo ufw allow 33061
sudo ufw allow 3306

sudo systemctl start proxysql
sudo mysql -u admin -padmin -h 127.0.0.1 -P 6032 < /vagrant/proxysql.sql
```

Di atas adalah perintah-perintah yang dijalankan pada terminal box `proxy`.  Hal-hal yang dilakukan adalah

- Changing the APT sources.list to kambing.ui.ac.id
- Updating the repo with the new sources

- Install required library
-  Get MySQL binaries
- Setting input for installation
- Install MySQL Community Server
-  Allow port on firewall
- Copy MySQL configurations
- Restart MySQL services
- Cluster bootstrapping

## Konfigurasi MySQL

### Konfigurasi untuk `db1` my11.cnf

Berikut konfigurasi untuk `/etc/mysql/my.cnf` untuk `db1` . Konfigurasi kita, kita letakkan di bawah `!includedir`.

#### Boilerplate Group Replication Settings

Bagian pertama dari pengaturan ini adalah pengaturan umum yang dibutuhkan group replikasi.

```
!includedir /etc/mysql/conf.d/
!includedir /etc/mysql/mysql.conf.d/

[mysqld]

# General replication settings
gtid_mode = ON
enforce_gtid_consistency = ON
master_info_repository = TABLE
relay_log_info_repository = TABLE
binlog_checksum = NONE
log_slave_updates = ON
log_bin = binlog
binlog_format = ROW
transaction_write_set_extraction = XXHASH64
loose-group_replication_bootstrap_group = OFF
loose-group_replication_start_on_boot = ON
loose-group_replication_ssl_mode = REQUIRED
loose-group_replication_recovery_use_ssl = 1
```

#### Shared Group Replication Setting

```

# Shared replication group configuration
loose-group_replication_group_name = "8f22f846-9922-4139-b2b7-097d185a93cb"
loose-group_replication_ip_whitelist = "192.168.17.74, 192.168.17.75, 192.168.17.76"
loose-group_replication_group_seeds = "192.168.17.74:33061, 192.168.17.75:33061, 192.168.17.76:33061"
```

#### Memilih Single atau Multi Master

di sini kita memilih multi master dengan menulis  

`loose-group_replication_single_primary_mode = OFF
loose-group_replication_enforce_update_everywhere_checks = ON`

```
# Single or Multi-primary mode? Uncomment these two lines
# for multi-primary mode, where any host can accept writes
loose-group_replication_single_primary_mode = OFF
loose-group_replication_enforce_update_everywhere_checks = ON
```

#### Host-Specific Configuration Settings

```
# Host specific replication configuration
server_id = 11
bind-address = "192.168.17.74"
report_host = "192.168.17.74"
loose-group_replication_local_address = "192.168.17.74:33061"
```

di bagian ini kita mengatur:

- The server ID
- The address to bind to
- The address to report to other members
- The local replication address and listening port

## File SQL

### cluster_bootstrap.sql

Mematikan pencatatan query atau binary log

```mysql
SET SQL_LOG_BIN=0
```

Membuat user untuk replikasi kelompok

```mysql
CREATE USER 'repl'@'%' IDENTIFIED BY 'password' REQUIRE SSL;
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
FLUSH PRIVILEGES;
```

Mengaktifkan kembali pencatatan query atau binary log

```mysql
SET SQL_LOG_BIN=1;
```

Mengganti parameter untuk replikasi log

```mysql
CHANGE MASTER TO MASTER_USER='repl', MASTER_PASSWORD='password' FOR CHANNEL 'group_replication_recovery';
```

Memasang plugin untuk replikasi ke

```mysql
INSTALL PLUGIN group_replication SONAME 'group_replication.so';
```



Perintah ini dijalankan saat pertama kali mengaktifkan group replication

```mysql
SET GLOBAL group_replication_bootstrap_group=ON;
START GROUP_REPLICATION;
SET GLOBAL group_replication_bootstrap_group=OFF;

CREATE DATABASE lsapp;
```

### cluster_member.sql

Sama seperti cluster_bootstrap.sql, tapi tidak ada bagian terakhir

```mysql
SET SQL_LOG_BIN=0;
CREATE USER 'repl'@'%' IDENTIFIED BY 'password' REQUIRE SSL;
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
FLUSH PRIVILEGES;
SET SQL_LOG_BIN=1;
CHANGE MASTER TO MASTER_USER='repl', MASTER_PASSWORD='password' FOR CHANNEL 'group_replication_recovery';
INSTALL PLUGIN group_replication SONAME 'group_replication.so';
```

### create_proxysql_user.sql

Membuat user bernama monitor untuk proxy

```mysql
CREATE USER 'monitor'@'%' IDENTIFIED BY 'monitorpassword';
GRANT SELECT on sys.* to 'monitor'@'%';
FLUSH PRIVILEGES;
```

Membuat user untuk digunakan oleh aplikasi

```mysql
CREATE USER 'lsappuser'@'%' IDENTIFIED BY 'lsapppassword';
GRANT ALL PRIVILEGES on lsapp.* to 'lsappuser'@'%';
FLUSH PRIVILEGES;
```

### proxysql.sql

Ini merupakan setup untuk MySQL pada proxy

```mysql
UPDATE global_variables SET variable_value='admin:admin' WHERE variable_name='admin-admin_credentials';
LOAD ADMIN VARIABLES TO RUNTIME;
SAVE ADMIN VARIABLES TO DISK;

UPDATE global_variables SET variable_value='monitor' WHERE variable_name='mysql-monitor_username';
LOAD MYSQL VARIABLES TO RUNTIME;
SAVE MYSQL VARIABLES TO DISK;

INSERT INTO mysql_group_replication_hostgroups (writer_hostgroup, backup_writer_hostgroup, reader_hostgroup, offline_hostgroup, active, max_writers, writer_is_also_reader, max_transactions_behind) VALUES (2, 4, 3, 1, 1, 3, 1, 100);

INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES (2, '192.168.17.74', 3306);
INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES (2, '192.168.17.75', 3306);
INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES (2, '192.168.17.76', 3306);

LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;

INSERT INTO mysql_users(username, password, default_hostgroup) VALUES ('lsappuser', 'lsapppassword', 2);
LOAD MYSQL USERS TO RUNTIME;
SAVE MYSQL USERS TO DISK;
```

