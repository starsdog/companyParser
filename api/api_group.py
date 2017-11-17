# -*- coding: utf-8 -*-
from flask import request, jsonify, Blueprint, make_response, send_file,jsonify
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
    file_path=os.path.join(init.config['groupInfo_folder'], file_name)
    if not os.path.exists(file_path):
        return make_response("data not exist!", 400)

    file_handler=open(file_path)
    content=json.load(file_handler)    
    return make_response(json.dumps(content, ensure_ascii=False), 200)

@mod.route('/parent/query', methods=["POST"])
def query_parent_group():
    info = request.get_json(force=True)
    company_name=info['company_name']

    parent_info=init.dbManager.query_parent(company_name)
    if parent_info==None:
        return make_response(jsonify({"errorCode":-1, "error":"沒有這家公司的資訊"}), 200)  

    group_no_info=json.loads(parent_info['group_info'])
    group_result=[]
    for key in group_no_info:
        group_no=group_no_info[key]
        group_item={"year":key, "group_no":group_no, "group_name":init.group_list[int(key)][group_no]}
        group_result.append(group_item)
    return make_response(jsonify({"errorCode":0, "result":group_result}), 200)    
        




