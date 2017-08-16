# -*- coding: utf-8 -*-
from flask import request, jsonify, Blueprint, make_response
import json
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
mod = Blueprint('graph', __name__, url_prefix='graph')

@mod.route('/download', methods=["POST"])
def download_relation_json():
    info = request.get_json(force=True)
    source=info['source']
    uuid=str(info['uuid'])
    is_save_file=info['toFile']

    #get json data
    if not is_save_file:    
        source=source+'_show'
    file_name="{}_2014.json".format(uuid)
    file_path=os.path.join(root_dir, source, uuid, file_name)
    if not os.path.exists(file_path):
        return make_response("data not exist!", 400)

    file_handler=open(file_path)
    content=json.load(file_handler)    
    if not is_save_file:
        return make_response(json.dumps(content, ensure_ascii=False), 200)
    else:
        response = make_response(json.dumps(content, ensure_ascii=False))
        response.headers["Content-Disposition"] = "attachment; filename=graph.json"
        return response
