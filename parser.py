# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import json
import requests
import argparse

class companyNode(object):
    def __init__(self, config_file):

        with open(config_file) as file:
            config = json.load(file)
            for key in config.keys():
                setattr(self, key, config[key])

    def check_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
 
    def _check_name_list(self, ori_name, name_list):
        display_name=ori_name
        clean_name=ori_name.replace('股份','').replace('有限','').replace('公司','').replace('(股)','')
        for name_set in name_list:
            is_exist=False
            for name in name_set:
                if clean_name in name:
                    is_exist=True
                    break
            if is_exist:
                display_name=name_set[0]
                break
        
        return display_name        

    def _insert_name_list(self, ori_name, name_list, unique_name_list):
        '''
        ori_name=台灣通運倉儲股份有限公司（台灣通運公司）
        display_name=台灣通運倉儲股份有限公司
        short_name=台灣通運公司
        name_list=[[['台灣通運倉儲股份有限公司', '台灣通運公司', '台灣通運'], ['金昌石礦股份有限公司', '金昌石礦']]
        unique_name_list=('台灣通運倉儲股份有限公司', '台灣通運公司', '台灣通運', '金昌石礦股份有限公司', '金昌石礦')
        '''
        full_name=ori_name
        display_name=ori_name
        name_set=[]
        if '）' in full_name[-1]:
            last_index=full_name.rfind('（')
            if last_index!=-1:
                display_name=full_name[:last_index]
                name_part2=full_name[last_index+1:-1]
                short_name=display_name.replace('股份','').replace('有限','').replace('公司','').replace('(股)','')
                if display_name not in unique_name_list and short_name not in unique_name_list and name_part2 not in unique_name_list:
                    unique_name_list.add(display_name)
                    unique_name_list.add(name_part2)
                    unique_name_list.add(short_name)
                    name_list.append([display_name, name_part2, short_name])
        else:
            short_name=display_name.replace('股份','').replace('有限','').replace('公司','').replace('(股)','')
            if display_name not in unique_name_list and short_name not in unique_name_list:
                unique_name_list.add(display_name)
                unique_name_list.add(short_name)       
                name_list.append([display_name, short_name])
            else:
                display_name=self._check_name_list(ori_name, name_list)    
        print("{}, {}".format(ori_name, name_list))
        return display_name       

    def parse_xml(self, stock, year, name, filename=''):
        if len(filename)==0:
            filename='tifrs-fr1-m1-ci-cr-{}-{}Q4.xml'.format(str(stock), str(year))
        file_path=os.path.join(self.xml_folder, filename)
        tree=ET.parse(file_path)
        content=tree.getroot()
        company_header='{http://www.xbrl.org/tifrs/notes/'+str(year-1)+'-03-31}'
        
        #table1: 列入合併財務報表之子公司
        target_element=company_header+'TheConsolidatedEntities'
        sublist=[]
        table1_name_list=[]
        unique_name_list=set()
        target_list=content.findall(target_element)
        for target in target_list:
            for child in target:
                if 'CompanyNameOfTheInvestor' in child.tag:
                    source=child.text.rstrip(' \n')
                    if '本公司' in source.replace(' ',''):
                        source=name
                    is_coreSource=0
                    if name in source:
                        is_coreSource=1
                    source=self._insert_name_list(source, table1_name_list, unique_name_list)   
                elif 'NameOfInvestee' in child.tag:
                    sub_source=child.text.rstrip(' \n')
                    sub_source=self._insert_name_list(sub_source, table1_name_list, unique_name_list)
                elif 'PercentageOfOwnership4' in child.tag:
                    if str(year) in child.attrib['contextRef']:
                        owner_holder=child.text  
                    
            item={"source":source, "target":sub_source, "holder":owner_holder, "location":"不明", "is_coreSource":is_coreSource, "table_source":1}
            sublist.append(item)  
        #print(table1_name_list)      

        #table2: 被投資公司名稱、所在地區
        company_element=company_header+'NamesLocationsAndRelatedInformationOfInvesteesOverWhichTheCompanyExercisesSignificantInfluence'
        company_list=content.findall(company_element)
        json_output={"year":str(year), "stock":stock}
        for company in company_list:
            for child in company:
                #print("{}, {}".format(child.tag, child.attrib))
                if 'CompanyNameOfTheInvestor' in child.tag:
                    source=child.text.rstrip(' \n')
                    if '本公司' in source.replace(' ',''):
                        source=name
                    is_coreSource=0
                    if name in source:
                        is_coreSource=1
                    source=self._check_name_list(source, table1_name_list)       
                elif 'CompanyNameOfTheInvestee' in child.tag:
                    sub_source=child.text.rstrip(' \n')
                elif 'Location' in child.tag:
                    location=child.text.rstrip(' \n')
                elif 'InvestmentsAtTheEndOfThePeriod' in child.tag:
                    for sub_invest in child:
                        if 'PercentageOfOwnership1' in sub_invest.tag:
                            owner_holder=sub_invest.text

            sub_source=self._check_name_list(sub_source, table1_name_list)
            #print("{}, {}".format(source, sub_source))
            is_exist=0
            for i in range(0, len(sublist)):
                if source in sublist[i]['source'] and sub_source in sublist[i]['target']:
                    sublist[i]['location']=location 
                    is_exist=1
                    break
                if '本集團' in sublist[i]['source'].replace(' ','') and sub_source in sublist[i]['target']:  
                    if '本公司' in source.replace(' ','') or '本集團' in source.replace(' ',''):
                        source=name
                    sublist[i]['source']=source
                    sublist[i]['location']=location
                    is_exist=1
                    break      

            if is_exist==0:
                item={"source":source, "target":sub_source, "holder":owner_holder, "location":location, "is_coreSource":is_coreSource, "table_source":2}
                sublist.append(item)
        #print("sub_company_except_china={}".format(len(table2_list)))
            
        #table3: 轉投資大陸地區之事業相關資訊 
        table3_list=[]
        china_company_element=company_header+'InformationOfInvestmentInMainlandChina'
        china_list=content.findall(china_company_element)
        print("china={}".format(len(china_list)))
        for china_company in china_list:
            for child in china_company:
                #print("china chila={}".format(child.tag))
                if 'CompanyNameOfTheInvesteeInMainlandChina' in child.tag:    
                    sub_source=child.text.rstrip(' \n')
                    sub_source=sub_source.replace('（註一）','').replace('（註二）','').replace('（註三）','').replace('（註四）','').replace('（註五）','').replace('（註六）','')
                    sub_source=sub_source.replace('（註七）','').replace('（註八）','').replace('（註九）','').replace('（註十）','').replace('（註十一）','').replace('（註十二）','')
                elif 'PercentageOfOwnershipThroughDirectAndIndirectInvestmentByTheCompany' in child.tag:
                    owner_holder=child.text
                
            sub_source=self._check_name_list(sub_source, table1_name_list)
            is_exist=0
            for i in range(0, len(sublist)):
                if sub_source in sublist[i]['target']:
                    sublist[i]['location']='china'
                    is_exist=1  
                    break
            
            if is_exist==0:             
                source='再投資大陸公司'
                item={"source":source, "target":sub_source, "holder":owner_holder, "location":'china', "is_coreSource":0, "table_source":3}
                sublist.append(item)
    
        print(len(sublist))
        for sub in sublist:
            if '本集團' in sub['source']:
                sub['source']=name    
        
        json_output['sublist']=sublist
        output_folder=os.path.join(self.mops_folder, str(stock))
        self.check_folder(output_folder)
        filename='{}_{}.json'.format(str(stock), str(year))
        file_path=os.path.join(output_folder, filename)
        output=open(file_path, "w")
        output.write(json.dumps(json_output, ensure_ascii=False))
        output.close()

    def download_xml(self, stock, year):
        payload='step=9&functionName=t164sb01&report_id=C&co_id='+str(stock)+'&year='+str(year)+'&season=4'
        url='http://mops.twse.com.tw/server-java/FileDownLoad'
        cookie={}
        r=requests.post(url, data=payload)
        print("{}, {}".format(r.status_code, len(r.content)))
        filename='{}_{}.xml'.format(str(stock), str(year))
        output_folder=os.path.join(self.xml_folder, str(stock))
        self.check_folder(output_folder) 
        output_file=os.path.join(output_folder, filename)        
        output=open(output_file, "wb")
        output.write(r.content)
        output.close()

    def parse_mops(self, stock, year):        
        filename='{}_{}.json'.format(str(stock), str(year))
        file_path=os.path.join(self.mops_folder, str(stock), filename)
        input_handler=open(file_path)
        content=json.load(input_handler)
        edgelist=[]
        nodes=set()
        nodelist=[]
        for info in content['sublist']:
            if info['source'] not in nodes:
                nodes.add(info['source'])
                nodelist.append({"name":info['source']})
            if info['sub_source'] not in nodes:
                nodes.add(info['sub_source'])
                nodelist.append({"name":info['sub_source']})
        
        node_idx= {nodelist[i]['name']:i for i in range(len(nodelist))}
        for info in content['sublist']:
            sub_source_idx=node_idx[info['sub_source']]
            source_idx=node_idx[info['source']]
            owner_holder=info['holder']*100
            item={"source":source_idx, "target":sub_source_idx, "holder":owner_holder}
            edgelist.append(item)
        
        reparsed_content={"y":year, "nodes":nodelist, "edges":edgelist}
        folder_path=os.path.join(self.show_mops_folder, str(stock))
        self.check_folder(folder_path)
        file_path=os.path.join(folder_path, filename)
        output=open(file_path, "w")
        output.write(json.dumps(reparsed_content, ensure_ascii=False))
        output.close()

    def parse_credit(self, stock, year):
        filename='{}_{}.json'.format(str(stock), str(year))
        file_path=os.path.join(self.credit_folder, str(stock), filename)
        input_handler=open(file_path)
        content=json.load(input_handler)
        edgelist=[]
        nodes=set()
        nodelist=[]
        for info in content['subinfo']:
            if len(info['tblHolder']):
                sub_source=info['name']
                if sub_source not in nodes:
                    nodes.add(sub_source)
                    nodelist.append({"name":sub_source})
                for holder_idx in range(1, len(info['tblHolder'])):
                    source=info['tblHolder'][holder_idx][0]
                    if source not in nodes:
                        nodes.add(source)
                        nodelist.append({"name":source})
    
        node_idx= {nodelist[i]['name']:i for i in range(len(nodelist))}
        for info in content['subinfo']:
            if len(info['tblHolder']):
                sub_source_idx=node_idx[info['name']]
                for holder_idx in range(1, len(info['tblHolder'])):
                    source_idx=node_idx[info['tblHolder'][holder_idx][0]]
                    owner_holder=info['tblHolder'][holder_idx][1]
                    item={"source":source_idx, "target":sub_source_idx, "holder":owner_holder}
                    edgelist.append(item)
         
        reparsed_content={"y":year, "nodes":nodelist, "edges":edgelist}
        folder_path=os.path.join(self.show_credit_folder, str(stock))
        self.check_folder(folder_path)
        file_path=os.path.join(folder_path, filename)
        output=open(file_path, "w")
        output.write(json.dumps(reparsed_content, ensure_ascii=False))
        output.close()

    def parse_folder(self, folder_path, stock_map):
        for dirPath, dirNames, fileNames in os.walk(folder_path):        
            for f in fileNames:
                if '.xml' in f:
                    filename="{}".format(os.path.join(dirPath, f))
                    f_parts=f.split('-')
                    stock=int(f_parts[5])
                    year=int(f_parts[6][:4])
                    self.parse_xml(stock, year, stock_map[stock], filename)

if __name__=="__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--task', metavar='parse', type=str, nargs=1, required=True,
        help='Specify a task to do. (parse)')

    args = arg_parser.parse_args()

    if args.task!=None:
        task=args.task[0]

    with open('config.json') as file:
        project_config=json.load(file)
        
    with open('stock_map.json') as file:
        stock = json.load(file)

    inv_stock={v:k for k, v in stock.items()}            
    target_list=project_config['target']
    stock_dict={}
    for t in target_list:
        if t in stock.keys():
            stock_dict[t]=stock[t]
        else:
            print("can't find stock number of {}".format(t))

    year=project_config['start']
    parser=companyNode('config.json') 
    if task=='parse':
        for key in stock_dict.keys():
            parser.parse_xml(stock_dict[key], 2014, key)
    elif task=='download':
        for key in stock_dict.keys():
            parser.download_xml(stock_dict[key], 2014)
    elif task=='reparse_credit':
        for key in stock_dict.keys():
            parser.parse_credit(stock_dict[key], year)
    elif task=='reparse_mops':
        for key in stock_dict.keys():
            parser.parse_mops(stock_dict[key], year)
    elif task=='parse_folder':
        parser.parse_folder(project_config['xml_folder'], inv_stock)
    else:
        print("no match job!")
