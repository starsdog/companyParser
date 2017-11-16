# -*- coding: utf-8 -*-
import csv
import json
import argparse
import os
from dbManager import dbManager 

class companyAnalysis(object):
    def __init__(self, config_file):
        with open(config_file) as file:
            self.config = json.load(file)

        self.factory_corp=self.config['factory']
        self.company_group=self.config['companyGroup']
        self.group_list=self.config['groupList']
        self.taxcode_list=self.config['taxcodeList']
        self.kind=self.config['kind']

        self.dbManager=dbManager(self.config['db_config'])
            
    def check_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def parseThaubing(self):   
        input_handler=open(self.factory_corp, 'r')
        reader=csv.DictReader(input_handler)
        factory_set=set()
        for row in reader:
            factory_set.add(row['corp_no'])
        input_handler.close()
        print(len(factory_set))

        input_handler=open(self.company_group, 'r')
        reader=csv.DictReader(input_handler)
        group_set=set()
        for row in reader:
            group_set.add(row['taxcode'])
        print(len(group_set))

        common_set=factory_set.intersection(group_set) 
        print(common_set)  
        print(len(common_set))  

    def generate_group_no(self):
        input_handler=open(self.company_group, 'r')
        reader=csv.DictReader(input_handler)
        
        group_list=set()
        for row in reader:
            group_no=row['group']
            group_list.add(group_no)

        output_handler=open(self.group_list, 'w')
        output_handler.write(json.dumps(list(group_list)))
        output_handler.close()

    def generate_taxcode_list(self):
        input_handler=open(self.company_group, 'r')
        reader=csv.DictReader(input_handler)

        taxcode_list={}
        for row in reader:
            company_name=row['sublist.source']
            company_taxcode=row['taxcode.source']

            if company_name not in taxcode_list:
                taxcode_list[company_name]=company_taxcode

            company_name=row['sublist.target']
            company_taxcode=row['taxcode.target']

            if company_name not in taxcode_list:
                taxcode_list[company_name]=company_taxcode
                            
        output_handler=open(self.taxcode_list, 'w')
        output_handler.write(json.dumps(taxcode_list, ensure_ascii=False))
        output_handler.close()
        
    def setup_company_db(self):
        input_handler=open(self.config['groupInfo'], 'r')
        reader=json.load(input_handler)

        stock_input=open(self.config['stock_map'])
        stock_map=json.load(stock_input)
    
        for group in reader:
            group_no=group['group_no']
            company_list=group['company_list']

            for company in company_list:
                item={"company_name":company[0], "group_infoq":json.dumps({self.config['start']:group_no})}
                print(item)
                if company[0] in stock_map:
                    item['stock']=stock_map[company[0]]
                self.dbManager.insert_company(item)    


    def generate_group_list(self):
        input_handler=open(self.company_group, 'r')
        reader=csv.DictReader(input_handler)

        taxcode_input=open(self.taxcode_list, 'r')
        taxcode_map=json.load(taxcode_input)

        stock_input=open(self.config['stock_map'])
        stock_map=json.load(stock_input)
        inv_stock={v:k for k, v in stock_map.items()}
    
        group_company_list={}
        group_stock={}
        for row in reader:
            group_no=row['group']
            source_company=row['sublist.source']
            target_company=row['sublist.target']
            market=row['market']
            stock=int(row['stock'])
            if len(source_company)==1:
                #print(row)
                continue
            if len(target_company)==1:
                #print(row)
                continue

            if group_no not in group_company_list:
                group_company_list[group_no]=set([source_company])
                group_company_list[group_no].add(target_company)
            else:
                group_company_list[group_no].add(source_company)    
                group_company_list[group_no].add(target_company) 

            if group_no not in group_stock:
                if stock in inv_stock:
                    group_stock[group_no]=set([inv_stock[stock]])
            else:
                if stock in inv_stock:
                    group_stock[group_no].add(inv_stock[stock])   
                            
        for group_no in group_company_list:    
            company_list=list(group_company_list[group_no])
            updated_company_list=[]
            for company_name in company_list:
                if company_name in taxcode_map:
                    updated_company_list.append([company_name, taxcode_map[company_name]])
            group_company_list[group_no]=updated_company_list
        
        group_info_list=[]
        group_name_list={}
        for group_no in group_company_list:
            group_info_item={"group_no":group_no, "company_list":group_company_list[group_no]}
            if group_no in group_stock:
                group_info_item["group_name_list"]=list(group_stock[group_no])
            else:
                group_info_item["group_name_list"]=[]    
            group_info_list.append(group_info_item)   
            group_name_list[group_no]=group_info_item["group_name_list"]

        file_name="groupInfo_{}.json".format(self.config['start'])
        self.check_folder(self.config['groupInfo_folder'])
        file_path=os.path.join(self.config['groupInfo_folder'], file_name)
        output_handler=open(file_path, 'w')
        output_handler.write(json.dumps(group_info_list, ensure_ascii=False))
        output_handler.close()        

        file_name="groupName_{}.json".format(self.config['start'])
        file_path=os.path.join(self.config['groupInfo_folder'], file_name)
        output_handler=open(file_path, 'w')
        output_handler.write(json.dumps(group_name_list, ensure_ascii=False))
        output_handler.close()        

if __name__=="__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--task', metavar='parse', type=str, nargs=1, required=True,
        help='Specify a task to do. (parse)')

    args = arg_parser.parse_args()

    if args.task!=None:
        task=args.task[0]

    with open('config.json') as file:
        project_config=json.load(file)

    analysis=companyAnalysis('config.json') 
    if task=='thaubing':   
        analysis.parseThaubing() 
    elif task=='generate_group_no':
        analysis.generate_group_no()
    elif task=='generate_taxcode':
        analysis.generate_taxcode_list()
    elif task=='generate_group_list':
        analysis.generate_group_list() 
    elif task=='setup_company_db':
        analysis.setup_company_db()       
    else:
        print("no match task")        