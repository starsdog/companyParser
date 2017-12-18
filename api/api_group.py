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

def gen_zip(folder_name, group_name):

    file_name="{}".format(group_name)
    zf = zipfile.ZipFile(file_name,'w')
    for root, folders, files in os.walk(folder_name):
        for sfile in files:
            aFile = os.path.join(root, sfile)
            zf.write(aFile)
    zf.close()        

def zip_gen(file_list):
    zip_process = subprocess.Popen(['zip', '-r', '-j'] + file_list, stdout=subprocess.PIPE)

    while not zip_process.poll():
        line = zip_process.stdout.read()
        if len(line)>0:
            yield line
        else:
            zip_process.stdout.close()
            break
    try:
        zip_process.wait(5) # Wait child process for at most 5 seoncds.
    except subprocess.TimeoutExpired as e:
        logger.error('Timeout: {}'.format(e.cmd))

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
        return make_response("data not exist!", 400)

    file_path=os.path.join(init.config['company_folder'], file_name)

    files=[]    
    file_path=os.path.join(init.config['company_folder'], group_name, 'G1101_2013.csv')
    memory_file = io.BytesIO()
    files=[]    
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for individualFile in files:
            zf.write(individualFile)
    memory_file.seek(0)        
    return send_file(memory_file, attachment_filename=file_name, as_attachment=True)        

    '''
    files=[]    
    file_path=os.path.join(init.config['company_folder'], group_name, 'G1101_2013.csv')
    files.append(file_path)
    zip_generator = zip_gen(files)
    d = werkzeug.datastructures.Headers()
    d.add(
        'Content-Disposition',
        'attachment',
        filename='{}.zip'.format(group_name)
        )
    return Response(zip_generator, mimetype='application/octet-stream', headers=d)
    '''

    #send_file(zf, attachment_filename='{}.zip'.format(group_name), as_attachment=True)
    
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
        




