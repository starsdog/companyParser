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
        separate_list=[['（', '）'], ['(',')']]
        is_separate_find=False
        for separate_pair in separate_list:
            if separate_pair[1] in full_name[-1]:
                last_index=full_name.rfind(separate_pair[0])
                if last_index!=-1:
                    display_name=full_name[:last_index].rstrip(' \n')
                    name_part2=full_name[last_index+1:-1].replace("\"”以下稱", '').rstrip(' \n')
                    short_name=display_name.replace('股份','').replace('有限','').replace('公司','').replace('(股)','').rstrip(' \n')
                    is_separate_find=True
                    if display_name not in unique_name_list and short_name not in unique_name_list and name_part2 not in unique_name_list:
                        unique_name_list.add(display_name)
                        unique_name_list.add(short_name)
                        if name_part2.find('註')==-1:
                            unique_name_list.add(name_part2)
                            name_list.append([display_name, name_part2, short_name])
                        else:
                            name_list.append([display_name, short_name])        

        if is_separate_find==False:
            short_name=display_name.replace('股份','').replace('有限','').replace('公司','').replace('(股)','').rstrip(' \n')
            if display_name not in unique_name_list and short_name not in unique_name_list:
                unique_name_list.add(display_name)
                unique_name_list.add(short_name)      
                name_list.append([display_name, short_name])        
        #print("{}, {}".format(ori_name, name_list))
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
                    multi_raw_source=[]
                    multi_source=[]
                    source=child.text.rstrip(' \n')
                    if '本公司' in source.replace(' ',''):
                        source=name
                    is_coreSource=0
                    if name in source:
                        is_coreSource=1
                    source=self._insert_name_list(source, table1_name_list, unique_name_list) 
                    and_index=source.find('及')
                    if and_index!=-1:
                        multi_raw_source=source.split('及')
                        for source in multi_raw_source:
                            source=self._insert_name_list(source, table1_name_list, unique_name_list) 
                            multi_source.append(source)
                    else:
                        multi_source.append(source)        
                elif 'NameOfInvestee' in child.tag:
                    sub_source=child.text.rstrip(' \n')
                    sub_source=self._insert_name_list(sub_source, table1_name_list, unique_name_list)
                elif 'PercentageOfOwnership4' in child.tag:
                    if str(year) in child.attrib['contextRef']:
                        owner_holder=child.text  
                    
            for source in multi_source:
                item={"source":source, "target":sub_source, "holder":owner_holder, "location":"不明", "is_coreSource":is_coreSource, "table_source1":1, "table_source2":0, "table_source3":0}
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
                    multi_raw_source=[]
                    multi_source=[]
                    if '本公司' in source.replace(' ',''):
                        source=name
                    is_coreSource=0
                    if name in source:
                        is_coreSource=1
                    source=self._check_name_list(source, table1_name_list)  
                    and_index=source.find('及')
                    if and_index!=-1:
                        multi_raw_source=source.split('及')
                        for source in multi_raw_source:
                            source=self._insert_name_list(source, table1_name_list, unique_name_list) 
                            multi_source.append(source)
                    else:
                        multi_source.append(source)             
                elif 'CompanyNameOfTheInvestee' in child.tag:
                    sub_source=child.text.rstrip(' \n')
                    sub_source=self._insert_name_list(sub_source, table1_name_list, unique_name_list)
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
                    sublist[i]['table_source2']=1
                    is_exist=1
                    break      

            if is_exist==0:
                for source in multi_source:
                    item={"source":source, "target":sub_source, "holder":owner_holder, "location":location, "is_coreSource":is_coreSource, "table_source1":0, "table_source2":1, "table_source3":0}
                    sublist.append(item)
        #print("sub_company_except_china={}".format(len(table2_list)))
            
        #table3: 轉投資大陸地區之事業相關資訊 
        table3_list=[]
        china_company_element=company_header+'InformationOfInvestmentInMainlandChina'
        china_list=content.findall(china_company_element)
        china_json={"year":str(year), "stock":stock}
        china_sublist=[]
        #print("china={}".format(len(china_list)))
        for china_company in china_list:
            for child in china_company:
                #print("china chila={}".format(child.tag))
                sub_source_note=''
                if 'CompanyNameOfTheInvesteeInMainlandChina' in child.tag:    
                    sub_source=child.text.rstrip(' \n')
                    sub_source=sub_source.replace('（註一）','').replace('（註二）','').replace('（註三）','').replace('（註四）','').replace('（註五）','').replace('（註六）','')
                    sub_source=sub_source.replace('（註七）','').replace('（註八）','').replace('（註九）','').replace('（註十）','').replace('（註十一）','').replace('（註十二）','')
                    sub_source=self._insert_name_list(sub_source, table1_name_list, unique_name_list)
                elif 'PercentageOfOwnershipThroughDirectAndIndirectInvestmentByTheCompany' in child.tag:
                    owner_holder=child.text
                elif 'Note' in child.tag:
                    if child.text!=None:
                        sub_source_note=child.text.rstrip(' \n')

            sub_source=self._check_name_list(sub_source, table1_name_list)
            is_exist=0
            for i in range(0, len(sublist)):
                if sub_source in sublist[i]['target']:
                    sublist[i]['location']='china'
                    sublist[i]['table_source3']=1
                    china_item={"target":sublist[i]['target'], "holder":sublist[i]['holder'], "note":sub_source_note}
                    china_sublist.append(china_item)
                    is_exist=1  
                    break
            
            if is_exist==0:             
                source='再投資大陸公司'
                item={"source":source, "target":sub_source, "holder":owner_holder, "location":'china', "is_coreSource":0, "table_source1":0, "table_source2":0, "table_source3":1}
                china_item={"target":sublist[i]['target'], "holder":sublist[i]['holder'], "note":sub_source_note}
                sublist.append(item)
                china_sublist.append(china_item)

        #table3備註
        china_note_element=company_header+'Note-InformationOfInvestmentInMainlandChina'
        china_note=[]
        note_separate=['註一', '註二', '註三', '註四', '註五', '註六', '註七', '註八', '註九', '註十', '註十一', '註十二', '註十三', '註十四']
        note_separate=note_separate+['註1', '註2', '註3', '註4', '註5', '註6', '註7', '註8', '註9', '註10', '註11', '註12', '註13', '註14']
        sub_note_separate=['(1)', '(2)', '(3)', '(4)', '(5)', '(6)', '(7)', '(8)', '(9)', '(10)', '(11)', '(12)', '(13)', '(14)']
        china_note_list=content.findall(china_note_element)
        for note in china_note_list:
            for i in range(0, len(note_separate)):
                current_note_list=self.parse_content_by_separate(note.text, note_separate)

            if len(current_note_list):
                for note_content in current_note_list:
                    current_note=note_content
                    sub_note_list=self.parse_content_by_separate(current_note, sub_note_separate)
                    if len(sub_note_list):
                        current_note=[sub_note_list]
                    china_note.append(current_note)
                
        china_json['sublist']=china_sublist
        china_json['notelist']=china_note
        
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
        
        china_filename='{}_{}_china.json'.format(str(stock), str(year))
        china_path=os.path.join(output_folder, china_filename)
        china_output=open(china_path, "w")
        china_output.write(json.dumps(china_json, ensure_ascii=False))
        china_output.close()

    def parse_content_by_separate(self, content, separate_list):
        result_list=[]
        for i in range(0, len(separate_list)):
            separate=separate_list[i]
            result=''
            separate_start_idx=content.find(separate)
            if separate_start_idx!=-1:
                if i!=(len(separate_list)-1):
                    next_separate=separate_list[i+1]
                    separate_end_idx=content.find(next_separate)
                    if separate_end_idx!=-1:
                        result=content[separate_start_idx:separate_end_idx]
                    else:
                        result=content[separate_start_idx:]   
                else:
                    result=content[separate_start_idx:]    
            if len(result):
                result_list.append(result)

        return result_list                 

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
