# Clustering MongoDB

### Infrastruktur
Cluster terdiri dari :

- 2 Config Server
    mongo_config_1 192.168.33.11 Ubuntu-18.04 512 MB
    mongo_config_2 192.168.33.12 Ubuntu-18.04 512 MB
- 1 Query Router
    mongo_query_router 192.168.33.13 Ubuntu-18.04 512 MB
- 3 Data/Shard Server
    mongo_shard_1 192.168.33.14 Ubuntu-18.04 512 MB
    mongo_shard_2 192.168.33.15 Ubuntu-18.04 512 MB
    mongo_shard_3 192.168.33.16 Ubuntu-18.04 512 MB

### Dataset

Dataset yang digunakan adalah **Biodiversity by County - Distribution of Animals, Plants and Natural Communities** yang diambil dari situs [Data Gov](https://catalog.data.gov/dataset).

[**Biodiversity by County - Distribution of Animals, Plants and Natural Communities**](https://catalog.data.gov/dataset/biodiversity-by-county-distribution-of-animals-plants-and-natural-communities)

Dataset berjumlah 20018 baris dan memiliki 12 kolom.



Sistem ini diimplementasikan dengan: 
- Mesin dengan Sistem Operasi Ubuntu 18.04
- Virtual Machine : Virtualbox
- Vagrant
- MongoDB

## Implementasi

###  script Vagrantfile
```
$ vagrant init
```

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "mongo_config_1" do |mongo_config_1|
    mongo_config_1.vm.hostname = "mongo-config-1"
    mongo_config_1.vm.box = "bento/ubuntu-18.04"
    mongo_config_1.vm.network "private_network", ip: "192.168.33.11"
    
    mongo_config_1.vm.provider "virtualbox" do |vb|
      vb.name = "mongo-config-1"
      vb.gui = false
      vb.memory = "512"
    end

    mongo_config_1.vm.provision "shell", path: "provision/allhosts.sh", privileged: false
  end

  config.vm.define "mongo_config_2" do |mongo_config_2|
    mongo_config_2.vm.hostname = "mongo-config-2"
    mongo_config_2.vm.box = "bento/ubuntu-18.04"
    mongo_config_2.vm.network "private_network", ip: "192.168.33.12"
    
    mongo_config_2.vm.provider "virtualbox" do |vb|
      vb.name = "mongo-config-2"
      vb.gui = false
      vb.memory = "512"
    end

    mongo_config_2.vm.provision "shell", path: "provision/allhosts.sh", privileged: false
  end

  config.vm.define "mongo_shard_1" do |mongo_shard_1|
    mongo_shard_1.vm.hostname = "mongo-shard-1"
    mongo_shard_1.vm.box = "bento/ubuntu-18.04"
    mongo_shard_1.vm.network "private_network", ip: "192.168.33.13"
    
    mongo_shard_1.vm.provider "virtualbox" do |vb|
      vb.name = "mongo-shard-1"
      vb.gui = false
      vb.memory = "512"
    end

    mongo_shard_1.vm.provision "shell", path: "provision/allhosts.sh", privileged: false
  end

  config.vm.define "mongo_shard_2" do |mongo_shard_2|
    mongo_shard_2.vm.hostname = "mongo-shard-2"
    mongo_shard_2.vm.box = "bento/ubuntu-18.04"
    mongo_shard_2.vm.network "private_network", ip: "192.168.33.14"
    
    mongo_shard_2.vm.provider "virtualbox" do |vb|
      vb.name = "mongo-shard-2"
      vb.gui = false
      vb.memory = "512"
    end

    mongo_shard_2.vm.provision "shell", path: "provision/allhosts.sh", privileged: false
  end

  config.vm.define "mongo_shard_3" do |mongo_shard_3|
    mongo_shard_3.vm.hostname = "mongo-shard-3"
    mongo_shard_3.vm.box = "bento/ubuntu-18.04"
    mongo_shard_3.vm.network "private_network", ip: "192.168.33.15"
        
    mongo_shard_3.vm.provider "virtualbox" do |vb|
      vb.name = "mongo-shard-3"
      vb.gui = false
      vb.memory = "512"
    end

    mongo_shard_3.vm.provision "shell", path: "provision/allhosts.sh", privileged: false
  end

  config.vm.define "mongo_query_router" do |mongo_query_router|
    mongo_query_router.vm.hostname = "mongo-query-router"
    mongo_query_router.vm.box = "bento/ubuntu-18.04"
    mongo_query_router.vm.network "private_network", ip: "192.168.33.16"
    
    mongo_query_router.vm.provider "virtualbox" do |vb|
      vb.name = "mongo-query-router"
      vb.gui = false
      vb.memory = "512"
    end

    mongo_query_router.vm.provision "shell", path: "provision/allhosts.sh", privileged: false
  end

end
```

### Script Provision Vagrant
**`allhosts.sh`**.

File [**allhosts.sh**](provision/allhosts.sh)

```bash
# Add hostname
sudo bash -c \\"echo '192.168.33.11 mongo-config-1' >> /etc/hosts\\"
sudo bash -c \\"echo '192.168.33.12 mongo-config-2' >> /etc/hosts\\"
sudo bash -c \\"echo '192.168.33.13 mongo-query-router' >> /etc/hosts\\"
sudo bash -c \\"echo '192.168.33.14 mongo-shard-1' >> /etc/hosts\\"
sudo bash -c \\"echo '192.168.33.15 mongo-shard-2' >> /etc/hosts\\"
sudo bash -c \\"echo '192.168.33.16 mongo-shard-3' >> /etc/hosts\\"

# Copy APT sources list
sudo cp /vagrant/sources/sources.list /etc/apt/
sudo cp /vagrant/sources/mongodb-org-4.2.list /etc/apt/sources.list.d/

# Add MongoDB repo key
sudo apt-get install gnupg
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -

# Update Repository
sudo apt-get update
# sudo apt-get upgrade -y

# Install MongoDB
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo service mongod start
```

###  Build Virtualbox
```
$ vagrant up
```

### Konfigurasi Config Server
```
$ vagrant ssh mongo_config_1
$ vagrant ssh mongo_config_2
```

**BuatAdministrative User**

pada setiap mongo server
```
(mongo-config-#) $ mongo
mongo> use admin
mongo> db.createUser({user: "username", pwd: "password", roles: [ "root"] } )
```

**Konfigurasi Config Server**
```conf
.....
net:
  port: 27019
  bindIp: <sesuai IP server>
....
....
replication:
  replSetName: configReplSet

sharding:
  clusterRole: "configsvr"
....
```
restart mongodb
```
(mongo-config-#) $ sudo systemctl restart mongod
```

Jalankan perintah berikut pada salah satu config server
```
(mongo-config-1) $ mongo 192.168.33.11:27019 -u mongo-admin -p --authenticationDatabase admin
```

Inisialisasi replica set
```json
rs.initiate(
    { _id: "configReplSet", configsvr: true, members: [
            { _id: 0, host: "192.168.33.11:27019" },
            { _id: 1, host: "192.168.33.12:27019" } 
        ] 
    }
)
```

```
mongo> rs.initiate( { _id: "configReplSet", configsvr: true, members: [ { _id: 0, host: "192.168.33.11:27019" }, { _id: 1, host: "192.168.33.12:27019" } ] } )
```

### Konfigurasi Query Router

Masuk host query router.
```
$ vagrant ssh mongo-query-router
```

Buat file konfigurasi.
```conf
# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongos.log

# network interfaces
net:
  port: 27017
  bindIp: 192.168.33.13

sharding:
  configDB: configReplSet/192.168.33.11:27019,192.168.33.12:27019
```

**Service Query Router**

membuat service untuk mongos. Buatlah file service `mongos.service`.
```
service
[Unit]
Description=Mongo Cluster Router
After=network.target

[Service]
User=mongodb
Group=mongodb
ExecStart=/usr/bin/mongos --config /etc/mongos.conf
# file size
LimitFSIZE=infinity
# cpu time
LimitCPU=infinity
# virtual memory size
LimitAS=infinity
# open files
LimitNOFILE=64000
# processes/threads
LimitNPROC=64000
# total threads (user+kernel)
TasksMax=infinity
TasksAccounting=false

[Install]
WantedBy=multi-user.target
```

###  Konfigurasi Shard Server
masuk ke masing-masing node
```
$ vagrant ssh mongo_shard_1
$ vagrant ssh mongo_shard_2
$ vagrant ssh mongo_shard_3
```

**Membuat Administrative Username**
```
(mongo-config-#) $ mongo
mongo> use admin
mongo> db.createUser({user: "username", pwd: "password", roles: [ "root"] } )
```

**Konfigurasi Shard Server**
1. Mengubah file konfigurasi shard server
    Buat file konfigurasi untuk masing-masing shard server. Yang perlu diperhatikan pada masing-masing file konfigurasi adalah:

    ```
    conf
    bindIp: <IP masing-masing server>
    ....
    ....
    sharding:
      clusterRole: "shardsvr"
    ```

2. Menambahkan shard ke dalam mongoDB cluster.
    Di salah satu shard sever, masuk ke dalam query router.
    ```
    (mongo-shard-1) $ mongo 192.168.33.13:27017 -u mongo-admin -p --authenticationDatabase admin
    ```
    ```
    sh.addShard("192.168.33.14:27017")
    sh.addShard("192.168.33.15:27017")
    sh.addShard("192.168.33.16:27017")
    ```

3. Mengaktifkan sharding pada level database dan collection

    Pertama masuk ke dalam query router (pada salah satu shard server).
    ```
    (mongo-shard-1) $ mongo 192.168.33.16:27017 -u mongo-admin -p --authenticationDatabase admin
    ```
    Untuk mengaktifkan sharding pada level database, beralih pada salah satu database yang hendak diaktifkan shardingnya.

    ```
    mongos> use healthMeasure
    mongos> sh.enableSharding("healthMeasure)
    mongos> db.healthMeasure.ensureIndex( { _id: "hashed"} )
    sh.shardCollection( "healthMeasure.healthMeasureCollection", { "_id" : "hashed" } )
    ```

## Import Dataset

```
$ mongoimport -h [host:port] -u [username] -d [database_name] -c [collection_name] --type CSV --file [path/to/file.csv] --headerline --authenticationDatabase admin
```

Perintah tersebut dijalankan pada query router

```
$ mongoimport -h 192.168.33.13:27017 -u mongo-admin -d populationData -c populationCollection --type CSV --file /vagrant/dataset/data_real.csv --headerline --authenticationDatabase admin
```

## API CRUD
    ```
    from flask import Flask
    from flask_pymongo import PyMongo
    from flask import jsonify, request
    from bson.json_util import dumps
    from bson.objectid import ObjectId

    app = Flask(__name__)
    app.secret_key = "ddb"
    app.config["MONGO_URI"] = "mongodb://mongo-admin:password@192.168.33.13:27017/biodiversity?retryWrites=false&authSource=admin"
    mongo = PyMongo(app)


    @app.route("/biodiversity", methods=['GET'])
    def get_biodiversities():
        biodiversities = mongo.db.biodiversity_collection.find()
        resp = dumps(biodiversities)
        return resp


    @app.route("/biodiversity", methods=['POST'])
    def add_biodiversities():
        request_json = request.json
        biodiversity_country = request_json["country"]
        biodiversity_category = request_json["category"]
        biodiversity_taxonomic_group = request_json["taxonomic_group"]
        biodiversity_taxonomic_subgroup = request_json["taxonomic_subgroup"]
        biodiversity_scientific_name = request_json["scientific_name"]
        biodiversity_common_name = request_json["common_name"]
        biodiversity_year_last_documented = request_json["year_last_documented"]
        biodiversity_ny_listing_status = request_json["ny_listing_status"]
        biodiversity_federal_listing_status = request_json["federal_listing_status"]
        biodiversity_state_conservation_rank = request_json["state_conservation_rank"]
        biodiversity_global_conservation_rank = request_json["global_conservation_rank"]
        biodiversity_distribution_status = request_json["distribution_status"]

        biodiversity_id = mongo.db.biodiversity_collection.insert({
            'country': biodiversity_country,
            'category': biodiversity_category,
            'taxonomic_group': biodiversity_taxonomic_group,
            'taxonomic_subgroup': biodiversity_taxonomic_subgroup,
            'scientific_name': biodiversity_scientific_name,
            'common_name': biodiversity_common_name,
            'year_last_documented': biodiversity_year_last_documented,
            'ny_listing_status': biodiversity_ny_listing_status,
            'federal_listing_status': biodiversity_federal_listing_status,
            'state_conservation_rank': biodiversity_state_conservation_rank,
            'global_conservation_rank': biodiversity_global_conservation_rank,
            'distribution_status': biodiversity_distribution_status,
        })

        resp = jsonify(
            'Biodiversity added successfully! with id = {}'.format(biodiversity_id))
        resp.status_code = 200
        return resp


    @app.route('/biodiversity/<id>', methods=['PUT'])
    def update_news(id):
        request_json = request.json
        biodiversity_id = request_json["_id"]
        biodiversity_country = request_json["country"]
        biodiversity_category = request_json["category"]
        biodiversity_taxonomic_group = request_json["taxonomic_group"]
        biodiversity_taxonomic_subgroup = request_json["taxonomic_subgroup"]
        biodiversity_scientific_name = request_json["scientific_name"]
        biodiversity_common_name = request_json["common_name"]
        biodiversity_year_last_documented = request_json["year_last_documented"]
        biodiversity_ny_listing_status = request_json["ny_listing_status"]
        biodiversity_federal_listing_status = request_json["federal_listing_status"]
        biodiversity_state_conservation_rank = request_json["state_conservation_rank"]
        biodiversity_global_conservation_rank = request_json["global_conservation_rank"]
        biodiversity_distribution_status = request_json["distribution_status"]

        mongo.db.biodiversity_collection.update_one(
            {'_id': ObjectId(biodiversity_id['$oid'])
            if '$oid' in biodiversity_id else ObjectId(biodiversity_id)},
            {
                '$set': {
                    'country': biodiversity_country,
                    'category': biodiversity_category,
                    'taxonomic_group': biodiversity_taxonomic_group,
                    'taxonomic_subgroup': biodiversity_taxonomic_subgroup,
                    'scientific_name': biodiversity_scientific_name,
                    'common_name': biodiversity_common_name,
                    'year_last_documented': biodiversity_year_last_documented,
                    'ny_listing_status': biodiversity_ny_listing_status,
                    'federal_listing_status': biodiversity_federal_listing_status,
                    'state_conservation_rank': biodiversity_state_conservation_rank,
                    'global_conservation_rank': biodiversity_global_conservation_rank,
                    'distribution_status': biodiversity_distribution_status,
                }
            }
        )

        resp = jsonify(
            'Biodiversity updated successfully! with id = {}'.format(biodiversity_id))
        resp.status_code = 200
        return resp


    @app.route('/biodiversity/<id>', methods=['DELETE'])
    def biodiversity(id):
        mongo.db.biodiversity_collection.delete_one({'_id': ObjectId(id)})
        resp = jsonify(
            'Biodiversity deleted successfully! with id = {}'.format(id))
        resp.status_code = 200
        return resp


    @app.route('/biodiversity/distinct_category', methods=['GET'])
    def distinct_category_biodiversity():
        facet_biodiversity = mongo.db.biodiversity_collection.distinct("category")
        resp = dumps(facet_biodiversity)
        return resp


    @app.route('/biodiversity/count_category', methods=['GET'])
    def count_category_biodiversity():
        category_biodiversity = mongo.db.biodiversity_collection.aggregate([
            {"$group": {
                "_id": "$category",
                "count": {"$sum": 1}
            }
            }
        ])
        resp = dumps(category_biodiversity)
        return resp


    if __name__ == "__main__":
    app.run()
    ```
