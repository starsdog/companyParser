import os
import sys
import json

project_dir =os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from dbManager import dbManager

config_file = project_dir + '/config.json'
with open(config_file) as file:
    config=json.load(file)

group_list={}
for year in range(2013, 2014):
    file_name="groupName_{}.json".format(year)
    file_path=os.path.join(config['groupInfo_folder'], file_name)
    file_handler=open(file_path)
    group_list[year]=json.load(file_handler)
    
dbManager=dbManager(config['db_config'])

