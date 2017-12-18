# -*- coding: utf-8 -*-
from flask import request, jsonify, Blueprint, make_response, send_file, jsonify, Response
import werkzeug.datastructures
import subprocess
import init
import json
import os
import zipfile
import io

mod = Blueprint('group', __name__, url_prefix='group')

def gen_zip(folder_path, group_name):

    file_name="{}.zip".format(group_name)
    zip_folder=os.path.join(init.config['company_zip'], file_name)
    zip_handler = zipfile.ZipFile(zip_folder,'w', zipfile.ZIP_DEFLATED)
    for dirPath, dirNames, fileNames in os.walk(folder_path):
        for f in fileNames:
            if '.csv' in f or '.json' in f:
                filename=os.path.join(dirPath, f)
                base_folder=os.path.basename(dirPath)
                output_folder=os.path.join(base_folder, f)
                zip_handler.write(filename, output_folder)
    zip_handler.close()        

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

@mod.route('/name/query', methods=["POST"])
def download_grouplist_json():
    info = request.get_json(force=True)
    year=info['year']

    #get json data
    file_name="groupName_{}.json".format(year)
    file_path=os.path.join(init.config['company_folder'], file_name)
    if not os.path.exists(file_path):
        return make_response("data not exist!", 400)

    file_handler=open(file_path)
    content=json.load(file_handler)    
    return make_response(json.dumps(content, ensure_ascii=False), 200)

@mod.route('/companylist/query', methods=["POST"])
def download_group_company_json():
    info = request.get_json(force=True)
    year=info['year']
    group_name=info['group_name']

    #get json data
    file_name="{}_{}_list.json".format(group_name, year)
    file_path=os.path.join(init.config['company_folder'], group_name, file_name)
    print(file_path)
    if not os.path.exists(file_path):
        return make_response("data not exist!", 400)

    file_handler=open(file_path)
    content=json.load(file_handler)    
    return make_response(json.dumps(content, ensure_ascii=False), 200)

@mod.route('/download', methods=["POST"])
def download_group_zip():
    info = request.get_json(force=True)
    group_name=info['group_name']

    file_name="{}.zip".format(group_name)
    folder_path=os.path.join(init.config['company_folder'], group_name)
    if not os.path.exists(folder_path):
        return make_response("data not exist", 400)

    file_path=os.path.join(init.config['company_zip'], file_name)
    if not os.path.exists(file_path):
        gen_zip(folder_path, group_name)
        print("not exist {}".format(file_path))
        return send_file(file_path, mimetype='zip')
    else:
        return send_file(file_path, mimetype='zip')   
    
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
        




