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


# country
# category
# taxonomic_group
# taxonomic_subgroup
# scientific_name
# common_name
# year_last_documented
# ny_listing_status
# federal_listing_status
# state_conservation_rank
# global_conservation_rank
# distribution_status

# {
#     "country": "tes",
#     "category": "tes",
#     "taxonomic_group": "tes",
#     "taxonomic_subgroup": "tes",
#     "scientific_name": "tes",
#     "common_name": "tes",
#     "year_last_documented": "tes",
#     "ny_listing_status": "tes",
#     "federal_listing_status": "tes",
#     "state_conservation_rank": "tes",
#     "global_conservation_rank": "tes",
#     "distribution_status": "tes",
# }
