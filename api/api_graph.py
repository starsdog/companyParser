# -*- coding: utf-8 -*-
from flask import request, jsonify, Blueprint, make_response, send_file
import json
import os
import init

root_dir = os.path.dirname(os.path.abspath(__file__))
mod = Blueprint('graph', __name__, url_prefix='graph')

@mod.route('/download', methods=["POST"])
def download_relation_json():
    info = request.get_json(force=True)
    group=info['group']
    year=info['year']

    file_name="{}_{}_graph.json".format(group, year)
    file_path=os.path.join(init.config['company_folder'], group, file_name)

    if not os.path.exists(file_path):
        return make_response("data not exist!", 400)

    file_handler=open(file_path)
    content=json.load(file_handler)    
    return make_response(json.dumps(content, ensure_ascii=False), 200)
