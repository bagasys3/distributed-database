from flask import Flask
import mysql.connector
import json
from flask import jsonify, request

app = Flask(__name__)
app.secret_key = "BEDETE"
app.config['MYSQL_HOST'] = '192.168.17.74'
app.config['MYSQL_PORT'] = 4000
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'biodiversity'

db = mysql.connector.connect(
  host="192.168.17.74",
  user="root",
  passwd="",
  database="biodiversity",
  port=4000
)

@app.route('/biodiversity/<id>', methods=['DELETE'])
def delete_biodiversity(id):
    cur = db.cursor();
    cur.execute("DELETE FROM biodiversity WHERE id = {}". format(id));
    db.commit()
    cur.close()
    resp = jsonify('Biodiversity deleted successfully!')
    resp.status_code = 200
    return resp

@app.route('/biodiversity/<id>', methods=['GET'])
def get_biodiversity(id):
    cur = db.cursor()
    cur.execute("SELECT * FROM biodiversity WHERE id = {}". format(id))

    data = []
    for (row) in cur:
        temp = {};
        temp["id"] = row[0];
        temp["county"] = row[1];
        temp["category"] = row[2] ;
        temp["taxonomic_group"] = row[3] ;
        temp["taxonomic_subgroup"] = row[4] ;
        temp["scientific_name"] = row[5] ;
        temp["common_name"] = row[6] ;
        temp["year_last_documented"] = row[7] ;
        temp["ny_listing_status"] = row[8] ;
        temp["federal_listing_status"] = row[9] ;
        temp["state_conservation_rank"] = row[10] ;
        temp["global_conservation_rank"] = row[11] ;
        temp["distribution_status"] = row[12] ;
        data.append(temp)

    db.commit()
    cur.close()
    resp = json.dumps(data)
    return resp

@app.route('/biodiversity', methods=['POST'])
def add_biodiversity():
    request_json = request.json
    county = request_json["county"];
    category = request_json["category"] ;
    taxonomic_group = request_json["taxonomic_group"] ;
    taxonomic_subgroup = request_json["taxonomic_subgroup"] ;
    scientific_name = request_json["scientific_name"] ;
    common_name = request_json["common_name"] ;
    year_last_documented = request_json["year_last_documented"] ;
    ny_listing_status = request_json["ny_listing_status"] ;
    federal_listing_status = request_json["federal_listing_status"] ;
    state_conservation_rank = request_json["state_conservation_rank"];
    global_conservation_rank = request_json["global_conservation_rank"];
    distribution_status = request_json["distribution_status"];

    cur = db.cursor()
    cur.execute("INSERT INTO biodiversity (category, taxonomic_group, taxonomic_subgroup, scientific_name, common_name, state_conservation_rank,year_last_documented, ny_listing_status, federal_listing_status, global_conservation_rank, distribution_status, county) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (category, taxonomic_group, taxonomic_subgroup, scientific_name, common_name, state_conservation_rank,year_last_documented, ny_listing_status, federal_listing_status, global_conservation_rank, distribution_status, county));

    db.commit()
    cur.close()

    resp = jsonify('biodiversity added successfully!')
    resp.status_code = 200
    return resp

@app.route('/biodiversity/<id>', methods=['PUT'])
def update_biodiversity(id):
    request_json = request.json;
    # id = request_json["id"];
    county = request_json["county"];
    category = request_json["category"] ;
    taxonomic_group = request_json["taxonomic_group"] ;
    taxonomic_subgroup = request_json["taxonomic_subgroup"] ;
    scientific_name = request_json["scientific_name"] ;
    common_name = request_json["common_name"] ;
    year_last_documented = request_json["year_last_documented"] ;
    ny_listing_status = request_json["ny_listing_status"] ;
    federal_listing_status = request_json["federal_listing_status"] ;
    state_conservation_rank = request_json["state_conservation_rank"] ;
    global_conservation_rank = request_json["global_conservation_rank"] ;
    distribution_status = request_json["distribution_status"] ;

    cur = db.cursor();
    cur.execute("UPDATE biodiversity SET county = %s, category = %s, taxonomic_group = %s, taxonomic_subgroup = %s, scientific_name = %s, common_name = %s, year_last_documented = %s, ny_listing_status = %s, federal_listing_status = %s, state_conservation_rank = %s, global_conservation_rank = %s, distribution_status = %s WHERE id = %s", (county, category, taxonomic_group, taxonomic_subgroup, scientific_name, common_name, year_last_documented, ny_listing_status, federal_listing_status, state_conservation_rank, global_conservation_rank, distribution_status, id));
    db.commit();
    cur.close();

    resp = jsonify('Biodiversity is updated successfully!');
    resp.status_code = 200;
    return resp;

if __name__ == "__main__":
    app.run()