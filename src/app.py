"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    
    members = jackson_family.get_all_members()
    response_body =  members
      
       
    

    return jsonify(response_body),200

@app.route("/member",methods=["POST"])
def agregar_member():
    new_member = request.json
   
    jackson_family.add_member(new_member)
    return jsonify("success"),200
    
@app.route("/member/<int:member_id>", methods=["DELETE"])
def eliminado_member(member_id):
    delete_member=jackson_family.delete_member(member_id)
    if not delete_member:
        return jsonify({"familiar no encontrado"}),400

    return jsonify({"done":True}),200

@app.route("/member/<int:member_id>",methods=["GET"])
def traer_un_miembro(member_id):
    response = jackson_family.get_member(member_id)
    if not response:
        return jsonify("miembro no encontrado"),400
    return jsonify(response),200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)