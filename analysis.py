# -*- coding: utf-8 -*-
import csv
import json
import argparse
import os
from dbManager import dbManager 
from openpyxl import load_workbook

class companyAnalysis(object):
    def __init__(self, config_file):
        with open(config_file) as file:
            self.config = json.load(file)

        self.taxcode_index=self.config['taxcode_index']
        self.kind=self.config['kind']

        self.dbManager=dbManager(self.config['db_config'])
            
    def check_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def parseThaubing(self):  
        '''
        check coverage of fine_corp and group_realtion data
        ''' 
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
        file_name="groupdata.taxcode.{}.csv".format(self.config['start'])
        file_path=os.path.join(self.company_group, file_name)
        input_handler=open(file_path, 'r')
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
        
    def generate_taxcode_ronny(self):
        file_path=os.path.join(self.config['factory_folder'],'taxcode_index.csv')
        input_handler=open(file_path, 'r')
        reader=csv.DictReader(input_handler)

        file_path=os.path.join(self.config['factory_folder'],'taxcode_index.json')
        output_handler=open(file_path, 'w')

        taxcode_list={}
        for row in reader:
            if row['type']=='公司':
                taxcode_list[row['#id']]=row['name']

        output_handler.write(json.dumps(taxcode_list, ensure_ascii=False))
        output_handler.close()         

    def setup_company_db(self):
        file_name="groupInfo_{}.json".format(self.config['start'])
        file_path=os.path.join(self.config['groupInfo_folder'], file_name)
        input_handler=open(file_path, 'r')
        reader=json.load(input_handler)

        stock_input=open(self.config['stock_map'])
        stock_map=json.load(stock_input)
    
        for group in reader:
            group_no=group['group_no']
            company_list=group['company_list']

            for company in company_list:
                item={"company_name":company[0], "group_info":json.dumps({self.config['start']:group_no})}
                print(item)
                if company[0] in stock_map:
                    item['stock']=stock_map[company[0]]
                self.dbManager.insert_company(item)    

    def generate_factory_fine_list(self):
        '''
        transfrom fine_corp csv to find_corp.json
        '''
        self.check_folder(self.config['factory_folder'])
        file_path=os.path.join(self.config['factory_folder'],'taxcode_index.json')
        input_handler=open(file_path, 'r')
        taxcode_map=json.load(input_handler)
        inv_taxcode={v:k for k, v in taxcode_map.items()}
        
        file_path=os.path.join(self.config['factory_folder'],'fine_corp.csv')
        fine_handler=open(file_path, 'r')
        reader=csv.DictReader(fine_handler)

        factory_fine_list={}
        for row in reader:
            taxcode=row['corp_id']
            if taxcode!='NULL':
                if taxcode in factory_fine_list:
                    factory_fine_list[taxcode]['record'].append(row)
                    factory_fine_list[taxcode]['record_count']+=1
                    factory_fine_list[taxcode]['money_amount']+=int(row['penalty_money'])
                else:
                    factory_fine_list[taxcode]={"record_count":1, "money_amount":int(row['penalty_money']), "record":[row]}
            else:
                name=row['facility_name']  
                if name in inv_taxcode:
                    taxcode=inv_taxcode[name]
                    if taxcode in factory_fine_list:
                        factory_fine_list[taxcode]['record'].append(row)
                        factory_fine_list[taxcode]['record_count']+=1
                        factory_fine_list[taxcode]['money_amount']+=int(row['penalty_money'])
                    else:
                        factory_fine_list[taxcode]={"record_count":1, "money_amount":int(row['penalty_money']), "record":[row]}        
        
        print(factory_fine_list)
        file_path=os.path.join(self.config['factory_folder'],'fine_corp.json')
        output_handler=open(file_path, 'w')
        output_handler.write(json.dumps(factory_fine_list, ensure_ascii=False))
        output_handler.close()              

    def generate_taxdiscount_list(self):
        '''
        transform xlsx to json 
        '''
        file_path=os.path.join(self.config['taxdiscount_folder'], '104discount.xlsx')
        input_handler=load_workbook(file_path)
        sheet_name_list=input_handler.get_sheet_names()

        for sheet in sheet_name_list:
            taxdiscount=set()
            sheet_content=input_handler.get_sheet_by_name(sheet)
            row_count=sheet_content.max_row
            for index in range(2, row_count):
                taxcode=sheet_content.cell(row=index, column=3).value
                taxdiscount.add(taxcode)

            sheet=int(sheet)+1911
            filename='{}_discount.json'.format(sheet)
            output_path=os.path.join(self.config['taxdiscount_folder'], filename)
            output_handler=open(output_path, 'w')
            output_handler.write(json.dumps(list(taxdiscount),ensure_ascii=False))
            output_handler.close()
            
    def parse_violate_rule(self, filename):
        input_handler=open(filename, 'r')
        reader=csv.DictReader(input_handler)

    def generate_group_list(self):
        file_name="groupdata.taxcode.{}.csv".format(self.config['start'])
        file_path=os.path.join(self.company_group, file_name)
        input_handler=open(file_path, 'r')
        reader=csv.DictReader(input_handler)

        #taxcode map which generated from ronny data
        taxcode_input=open(self.taxcode_list, 'r')
        taxcode_map=json.load(taxcode_input)

        #stock map which combine otc, pub, rotc, sii
        stock_input=open(self.config['stock_map'])
        stock_map=json.load(stock_input)
        inv_stock={v:k for k, v in stock_map.items()}

        #fine_corp record not related with year
        file_path=os.path.join(self.config['factory_folder'],'fine_corp.json')
        fine_handler=open(file_path, 'r')
        factory_fine_list=json.load(fine_handler)

        taxdiscount_file="{}_discount.json".format(self.config['start'])
        taxdiscount_path=os.path.join(self.config['taxdiscount_folder'], taxdiscount_file)
        taxdiscount_handler=open(taxdiscount_path, 'r')
        taxdiscount_list=json.load(taxdiscount_handler)

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
            has_fine_record=False
            has_discount=False
            fine_money_amount=0
            fine_record_count=0
            company_list=list(group_company_list[group_no])
            updated_company_list=[]
            for company_name in company_list:
                taxcode=taxcode_map[company_name]
                item={"name":company_name, "taxcode":taxcode, "fine_record":{}, "taxdiscount":False}
                
                if taxcode!='NA' and len(taxcode) and int(taxcode) in taxdiscount_list:
                    item["taxdiscount"]=True
                    has_discount=True
                if taxcode in factory_fine_list:
                    item['fine_record']=factory_fine_list[taxcode]
                    fine_money_amount+=factory_fine_list[taxcode]['money_amount']
                    fine_record_count+=factory_fine_list[taxcode]['record_count']
                    has_fine_record=True 
                updated_company_list.append(item)

            group_company_list[group_no]={"company_list":updated_company_list, "has_record":has_fine_record, "has_discount":has_discount, "fine_money_amount":fine_money_amount, "fine_record_count":fine_record_count}
        
        group_info_list=[]
        group_name_list={}
        for group_no in group_company_list:

            group_info_item={"group_no":group_no, "company_list":group_company_list[group_no]['company_list'], 
                "has_fine_record":group_company_list[group_no]['has_record'], 
                "has_discount":group_company_list[group_no]['has_discount'], 
                "fine_money_amount":group_company_list[group_no]['fine_money_amount'], "fine_record_count":group_company_list[group_no]['fine_record_count']}
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

    def generate_group_company_folder(self, folder_path):
        group_name_year={}
        for dirPath, dirNames, fileNames in os.walk(folder_path):        
                for f in fileNames:
                    if '.csv' in f:
                        sub_f=f[:-4]
                        file_info=sub_f.split('_')
                        group_name=file_info[0]
                        year=file_info[1]
                        file_path=os.path.join(dirPath, f)
                        groupname_list=self.generate_group_company_list(file_path, group_name, year)
                        item={"group_no":group_name, "group_name_list":groupname_list}
                        if year in group_name_year:
                            group_name_year[year].append(item)
                        else:
                            group_name_year[year]=[item]

        for key in group_name_year:   
            filename="groupName_{}.json".format(key)  
            file_path=os.path.join(self.config['company_folder'], filename)
            output_handler=open(file_path, 'w')
            output_handler.write(json.dumps(group_name_year[key], ensure_ascii=False))
            output_handler.close()        


    def generate_group_company_list(self, file_path, group_name, year):
        input_handler=open(file_path, 'r')
        reader=csv.DictReader(input_handler)
        
        #stock map which combine otc, pub, rotc, sii
        stock_input=open(self.config['stock_map'])
        stock_map=json.load(stock_input)
        inv_stock={v:k for k, v in stock_map.items()}

        group_company_list=[]
        company_set=set()
        edgelist=[]
        nodelist=[]
        group_name_set=set()
        for row in reader:
            if row['sublist.holder']=='NA':
                row['sublist.holder']=0
            item={"source":row['source'],"target":row['target'], "taxcode_source":row['taxcode.source'], "taxcode_target":row['taxcode.target'], "holder":row['sublist.holder']}    
            group_company_list.append(item) 
            if row['source'] not in company_set:
                company_set.add(row['source'])
                nodelist.append({"name":row['source']})
            if row['target'] not in company_set:
                company_set.add(row['target'])
                nodelist.append({"name":row['target']})

            stock=int(row['stock'])
            if stock in inv_stock:
                group_name_set.add(inv_stock[stock])    

        node_idx= {nodelist[i]['name']:i for i in range(len(nodelist))}
        for info in group_company_list:
            target_idx=node_idx[info['target']]   
            source_idx=node_idx[info['source']]
            owner_holder='%06f'%(float(info['holder'])*100)
            item={"source":source_idx, "target":target_idx, "holder":owner_holder}
            edgelist.append(item)

        file_name="{}_{}_list.json".format(group_name, year)
        file_path=os.path.join(self.config['company_folder'], group_name, file_name)
        output_handler=open(file_path, 'w')
        output_handler.write(json.dumps(group_company_list, ensure_ascii=False))
        output_handler.close()      

        reparsed_content={"y":year, "nodes":nodelist, "edges":edgelist}
        file_name="{}_{}_graph.json".format(group_name, year)
        file_path=os.path.join(self.config['company_folder'], group_name, file_name)
        output_handler=open(file_path, "w")
        output_handler.write(json.dumps(reparsed_content, ensure_ascii=False))
        output_handler.close()

        return list(group_name_set)
    
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
    elif task=='generate_taxcode_ronny':
        analysis.generate_taxcode_ronny()
    elif task=='parse_factory_fine':
        analysis.generate_factory_fine_list()
    elif task=='generate_taxdiscount_list':
        analysis.generate_taxdiscount_list()
    elif task=='generate_group_company_list':
        file_name="G1101_2013.csv"
        file_path=os.path.join(project_config['company_folder'], 'G1101', file_name)
        analysis.generate_group_company_list(file_name)    
    elif task=='generate_group_company_folder':
        analysis.generate_group_company_folder(project_config['company_folder'])
    else:
        print("no match task")        