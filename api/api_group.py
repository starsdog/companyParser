# -*- coding: utf-8 -*-
from flask import request, jsonify, Blueprint, make_response, send_file
import init
import json
import os

mod = Blueprint('group', __name__, url_prefix='group')

@mod.route('/list/query', methods=["POST"])
def download_relation_json():
    info = request.get_json(force=True)
    year=info['year']

    #get json data
    file_name="groupInfo_{}.json".format(year)
    file_path=os.path.join(init.project_dir, file_name)
    if not os.path.exists(file_path):
        return make_response("data not exist!", 400)

    file_handler=open(file_path)
    content=json.load(file_handler)    
    return make_response(json.dumps(content, ensure_ascii=False), 200)
