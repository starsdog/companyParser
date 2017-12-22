# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import json
import requests
import argparse
import time
import csv
import traceback
import re
from lxml import etree
from lxml import html

class Stack:
  def __init__(self):
    self.__storage = []

  def isEmpty(self):
    return len(self.__storage) == 0

  def push(self,p):
    self.__storage.append(p)

  def pop(self):
    return self.__storage.pop()

class companyNode(object):
    def __init__(self, config_file):

        with open(config_file) as file:
            self.config = json.load(file)
            #for key in config.keys():
            #    setattr(self, key, config[key])
        kind=self.config['kind']
        
        self.xml_folder=self.config[kind]['xml_folder']
        self.board_folder=self.config[kind]['board_folder']
        self.mops_folder=self.config[kind]['mops_folder']
        self.zip_folder=self.config['zip_folder']
        self.check_board_list=self.config[kind]['check_board_list']
        self.missing_stock_list=self.config[kind]['stock_map_missing_list']

    def check_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
 
    def _convertText(self, textLine):
        new_string = textLine
        
        new_string = new_string.replace("Ａ", "A")
        new_string = new_string.replace("Ｂ", "B")
        new_string = new_string.replace("Ｃ", "C")
        new_string = new_string.replace("Ｄ", "D")
        new_string = new_string.replace("Ｅ", "E")
        new_string = new_string.replace("Ｆ", "F")
        new_string = new_string.replace("Ｇ", "G")
        new_string = new_string.replace("Ｈ", "H")
        new_string = new_string.replace("Ｉ", "I")
        new_string = new_string.replace("Ｊ", "J")
        new_string = new_string.replace("Ｋ", "K")
        new_string = new_string.replace("Ｌ", "L")
        new_string = new_string.replace("Ｍ", "M")
        new_string = new_string.replace("Ｎ", "N")
        new_string = new_string.replace("Ｏ", "O")
        new_string = new_string.replace("Ｐ", "P")
        new_string = new_string.replace("Ｑ", "Q")
        new_string = new_string.replace("Ｒ", "R")
        new_string = new_string.replace("Ｓ", "S")
        new_string = new_string.replace("Ｔ", "T")
        new_string = new_string.replace("Ｕ", "U")
        new_string = new_string.replace("Ｖ", "V")
        new_string = new_string.replace("Ｗ", "W")
        new_string = new_string.replace("Ｘ", "X")
        new_string = new_string.replace("Ｙ", "Y")
        new_string = new_string.replace("Ｚ", "Z")
        new_string = new_string.replace("ａ", "a")
        new_string = new_string.replace("ｂ", "b")
        new_string = new_string.replace("ｃ", "c")
        new_string = new_string.replace("ｄ", "d")
        new_string = new_string.replace("ｅ", "e")
        new_string = new_string.replace("ｆ", "f")
        new_string = new_string.replace("ｇ", "g")
        new_string = new_string.replace("ｈ", "h")
        new_string = new_string.replace("ｉ", "i")
        new_string = new_string.replace("ｊ", "j")
        new_string = new_string.replace("ｋ", "k")
        new_string = new_string.replace("ｌ", "l")
        new_string = new_string.replace("ｍ", "m")
        new_string = new_string.replace("ｎ", "n")
        new_string = new_string.replace("ｏ", "o")
        new_string = new_string.replace("ｐ", "p")
        new_string = new_string.replace("ｑ", "q")
        new_string = new_string.replace("ｒ", "r")
        new_string = new_string.replace("ｓ", "s")
        new_string = new_string.replace("ｔ", "t")
        new_string = new_string.replace("ｕ", "u")
        new_string = new_string.replace("ｖ", "v")
        new_string = new_string.replace("ｗ", "w")
        new_string = new_string.replace("ｘ", "x")
        new_string = new_string.replace("ｙ", "y")
        new_string = new_string.replace("ｚ", "z")
        new_string = new_string.replace("（", "(")
        new_string = new_string.replace("）", ")")
        new_string = new_string.replace("〔", "(")
        new_string = new_string.replace("〕", ")")
        new_string = new_string.replace("【", "(")
        new_string = new_string.replace("】", ")")
        new_string = new_string.replace("　", " ")
        new_string = new_string.replace("．", ".")
        new_string = new_string.replace("，", ",")
        new_string = new_string.replace("\n",'')
        new_string = new_string.replace("  ",'')
        new_string = new_string.replace('1.','').replace('2.','').replace('3.','').replace('4.','').replace('5.','').replace('6.','')
        new_string = new_string.replace('7.','').replace('8.','').replace('9.','').replace('10.','').replace('11.','').replace('12.','')
        new_string = new_string.replace('(1)','').replace('(2)','').replace('(3)','').replace('(4)','').replace('(5)','').replace('(6)','')
        new_string = new_string.replace('(7)','').replace('(8)','').replace('(9)','').replace('(10)','').replace('(11)','').replace('(12)','')
        new_string = new_string.replace('(註一)','').replace('(註二)','').replace('(註三)','').replace('(註四)','').replace('(註五)','').replace('(註六)','')
        new_string = new_string.replace('(註七)','').replace('(註八)','').replace('(註九)','').replace('(註十)','').replace('(註十一)','').replace('(註十二)','')
        new_string = new_string.replace('(註1)','').replace('(註2)','').replace('(註3)','').replace('(註4)','').replace('(註5)','').replace('(註6)','')
        new_string = new_string.replace('(註7)','').replace('(註8)','').replace('(註9)','').replace('(註10)','').replace('(註11)','').replace('(註12)','')

        #print("{},{}".format(textLine, new_string))
        return new_string  

    def _check_name_list(self, ori_name, name_list):
        display_name=ori_name
        is_exist=False
        clean_name=ori_name.replace('股份','').replace('有限','').replace('公司','').replace('(股)','').replace('集團','').rstrip(' \n').lstrip('\n').rstrip(' ').lstrip(' ')
        for name_set in name_list:
            is_exist=False
            for name in name_set:
                if clean_name.replace(' ','') in name.replace(' ',''):
                    is_exist=True
                    break
            if is_exist:
                display_name=name_set[0]
                break
        
        #print("{},{},{},{}".format(ori_name, display_name, is_exist, name_list))
        return display_name, is_exist      

    def _find_bracket_pair(self, ori_name, separate_pair):
        left_bracket = Stack()
        index = 0
        string_pair=[]
        is_balance=True
        while index < len(ori_name):
            char = ori_name[index]
            if char == separate_pair[0]:
                left_bracket.push(index)
                #print("push, {}".format(index))
            elif char == separate_pair[1]:
                if left_bracket.isEmpty():
                    is_balance=False
                    #print("unbalance {}".format(ori_name[index]))
                    break
                else:
                    left_bracket_idx=left_bracket.pop()
                    string_pair.append([left_bracket_idx+1,index])
            index += 1

        #print("{},{}, {}".format(ori_name, separate_pair, string_pair))    
        if is_balance:
            return string_pair[-1], is_balance  
        else:
            return [], is_balance     

    def _update_display_name(self, display_name, name_part2, name_list):
        find_idx=-1
        new_name_list=name_list
        for idx in range(0, len(name_list)):
            is_exist=False
            for name in name_list[idx]:
                if name_part2 in name:
                    find_idx=idx
                    break

            if find_idx!=-1:
                break        
                    
        return find_idx
           
    def _insert_name_list(self, ori_name, name_list, unique_name_list):
        '''
        ori_name=台灣通運倉儲股份有限公司（台灣通運公司）
        display_name=台灣通運倉儲股份有限公司
        short_name=台灣通運公司
        name_list=[[['台灣通運倉儲股份有限公司', '台灣通運公司', '台灣通運'], ['金昌石礦股份有限公司', '金昌石礦']]
        unique_name_list=('台灣通運倉儲股份有限公司', '台灣通運公司', '台灣通運', '金昌石礦股份有限公司', '金昌石礦')
        '''
        #check full name exist or not
        display_name, is_exist=self._check_name_list(ori_name, name_list)
        if is_exist:
            return display_name
    
        full_name=ori_name
        display_name=ori_name
        name_set=[]
        separate_list=[['(',')']]
        is_separate_find=False
        for separate_pair in separate_list:
            if separate_pair[1] in full_name[-1]:
                index_pair, is_balance=self._find_bracket_pair(ori_name, separate_pair)
                if is_balance:
                    display_name=full_name[:index_pair[0]-1]
                    name_part2=full_name[index_pair[0]:index_pair[1]].replace("\"”", '').replace("以下稱", '').replace("簡稱", '').replace("以下", '')
                    if '，' in name_part2:  
                        #翔智科技股份有限公司(翔智，台灣)
                        index=name_part2.find('，') 
                        name_part2=name_part2[:index]
                    short_name=display_name.replace('股份','').replace('有限','').replace('公司','').replace('(股)','').replace('集團','').rstrip(' \n').lstrip('\n').rstrip(' ').lstrip(' ')
                    is_separate_find=True

                    #簡稱先出現
                    if display_name not in unique_name_list and name_part2 in unique_name_list:
                        unique_name_list.add(display_name)
                        unique_name_list.add(short_name)
                        old_idx=self._update_display_name(display_name, name_part2, name_list)
                        new_name_pair=name_list[old_idx]+[display_name, short_name]
                        #print(new_name_pair)
                        del name_list[old_idx]            
                        name_list.append(new_name_pair)   
                        display_name=name_part2    
                    
                    if display_name not in unique_name_list and short_name not in unique_name_list and name_part2 not in unique_name_list:
                        unique_name_list.add(display_name)
                        unique_name_list.add(short_name)
                        if name_part2.find('註')==-1:
                            unique_name_list.add(name_part2)
                            name_list.append([display_name, name_part2, short_name])
                        else:
                            name_list.append([display_name, short_name])  
                else:
                    is_separate_find=False 

        if is_separate_find==False:
            short_name=display_name.replace('股份','').replace('有限','').replace('公司','').replace('(股)','').rstrip(' \n')
            if display_name not in unique_name_list and short_name not in unique_name_list:
                unique_name_list.add(display_name)
                unique_name_list.add(short_name)      
                name_list.append([display_name, short_name])  
            else:
                display_name, is_exist=self._check_name_list(ori_name, name_list)           
        #print("{}, {}, {}".format(ori_name, display_name, name_list))
        return display_name       

    def _separate_company_list(self, ori_name, parent_name):
        multi_name_list=[]
        if '及' in parent_name and ori_name.find(parent_name)!=-1: #及成企業股份有限公司
            multi_name_list.append(ori_name)
            return multi_name_list

        if '及' in ori_name and '註' in ori_name: #CMAI N.A.(註2及3)
            multi_name_list.append(ori_name)
            return multi_name_list

        raw_multi_name_list=re.split('及|及其|、|/', ori_name)

        for raw_name in raw_multi_name_list:
            if '母公司' in raw_name.replace(' ',''):
                raw_name=parent_name
            elif '本公司' in raw_name.replace(' ',''):
                raw_name=parent_name    
            elif '子公司' in raw_name.replace(' ',''):
                continue
            multi_name_list.append(raw_name)
        return multi_name_list  

    def parse_xml(self, stock, year, name, filename=''):
        if len(filename)==0:
            filename='tifrs-fr1-m1-ci-cr-{}-{}Q4.xml'.format(str(stock), str(year))
        file_path=os.path.join(self.xml_folder, filename)
        tree=ET.parse(file_path)
        content=tree.getroot()
        if year==2016:
            if stock in [1538, 3570, 3662, 5309, 6497, 1587, 3603, 5262, 5299, 6288, 6581, 6625, 6640, 4767, 6661]:
                company_header='{http://www.xbrl.org/tifrs/notes/2017-03-31}'
            else:
                company_header='{http://www.xbrl.org/tifrs/notes/2015-03-31}'
        elif year==2013 and stock==2719:
            company_header='{http://www.xbrl.org/ifrs}'
        else:
            company_header='{http://www.xbrl.org/tifrs/notes/'+str(year)+'-03-31}'

        #table1: 列入合併財務報表之子公司
        target_element=company_header+'TheConsolidatedEntities'
        sublist=[]
        table1_name_list=[]
        unique_name_list=set()
        #insert full name into name_list
        self._insert_name_list(name, table1_name_list, unique_name_list)  
        #for item in content:
        #    print("{}".format(item.tag))

        target_list=content.findall(target_element)
        for target in target_list:
            for child in target:
                if 'CompanyNameOfTheInvestor' in child.tag:
                    multi_raw_source=[]
                    multi_raw_target=[]
                    multi_source=[]
                    multi_target=[]
                    source=child.text.rstrip(' ')
                    source=self._convertText(source)    
                    if '本公司' in source.replace(' ',''):
                        source=name
                    is_coreSource=0
                    if name in source:
                        is_coreSource=1
                    
                    multi_raw_source=self._separate_company_list(source, name)
                    if len(multi_raw_source):
                        for source in multi_raw_source:
                            try:
                                source=self._insert_name_list(source, table1_name_list, unique_name_list) 
                                multi_source.append(source)
                            except Exception as e:
                                print(multi_raw_source)    
                    else:            
                        source=self._insert_name_list(source, table1_name_list, unique_name_list) 
                        multi_source.append(source)        
                elif 'NameOfInvestee' in child.tag:
                    sub_source=child.text.rstrip(' ')
                    sub_source=self._convertText(sub_source)
                    
                    multi_raw_target=self._separate_company_list(sub_source, name)
                    if len(multi_raw_target):
                        for sub_source in multi_raw_target:
                            sub_source=self._insert_name_list(sub_source, table1_name_list, unique_name_list)
                            multi_target.append(sub_source)
                    else:        
                        sub_source=self._insert_name_list(sub_source, table1_name_list, unique_name_list)
                        multi_target.append(sub_source)
                elif 'PercentageOfOwnership3' in child.tag:
                    for invest_detail in child:
                        if 'AtTheEndOfThisPeriod' in invest_detail.tag:
                            owner_holder=invest_detail.text  
                elif 'AtTheEndOfThisPeriod' in child.tag:
                    owner_holder=child.text 
                elif 'PercentageOfOwnership4' in child.tag:
                    if str(year) in child.attrib['contextRef']:
                        owner_holder=child.text  
        
            for source in multi_source:
                for sub_source in multi_target:
                    if source in ['合計','合併'] or sub_source in ['合計','合併']:
                        continue
                    item={"source":source, "target":sub_source, "holder":owner_holder, "location":"不明", "is_coreSource":is_coreSource, "table_source1":1, "table_source2":0, "table_source3":0}
                    sublist.append(item) 
        
        #table2: 被投資公司名稱、所在地區
        company_element=company_header+'NamesLocationsAndRelatedInformationOfInvesteesOverWhichTheCompanyExercisesSignificantInfluence'
        company_list=content.findall(company_element)
        json_output={"year":str(year), "stock":stock}
        for company in company_list:
            for child in company:
                #print("{}, {}".format(child.tag, child.attrib))
                if 'CompanyNameOfTheInvestor' in child.tag:
                    multi_raw_source=[]
                    multi_raw_target=[]
                    multi_source=[]
                    multi_target=[]
                    source=child.text.rstrip(' ')
                    source=self._convertText(source)
                    if '本公司' in source.replace(' ',''):
                        source=name
                    is_coreSource=0
                    if name in source:
                        is_coreSource=1
                    multi_raw_source=self._separate_company_list(source, name)    
                    if len(multi_raw_source):
                        for source in multi_raw_source:
                            source=self._insert_name_list(source, table1_name_list, unique_name_list) 
                            multi_source.append(source)
                    else:
                        source=self._insert_name_list(source, table1_name_list, unique_name_list)  
                        multi_source.append(source)             
                elif 'CompanyNameOfTheInvestee' in child.tag:
                    sub_source=child.text.rstrip(' ')
                    sub_source=self._convertText(sub_source)

                    multi_raw_target=self._separate_company_list(sub_source, name)
                    
                    if len(multi_raw_target):
                        for sub_source in multi_raw_target:
                            sub_source=self._insert_name_list(sub_source, table1_name_list, unique_name_list)
                            multi_target.append(sub_source)
                    else:        
                        sub_source=self._insert_name_list(sub_source, table1_name_list, unique_name_list)
                        multi_target.append(sub_source)
                elif 'Location' in child.tag:
                    location=child.text.replace('\n','').rstrip(' ')
                    #print("{}, {}".format(child.text, location))
                elif 'InvestmentsAtTheEndOfThePeriod' in child.tag:
                    for sub_invest in child:
                        if 'PercentageOfOwnership1' in sub_invest.tag:
                            owner_holder=sub_invest.text

            
            for sub_source in multi_target:
                sub_source, is_exist=self._check_name_list(sub_source, table1_name_list)
                #print("{}, {}".format(sub_source, is_exist))
                is_exist=0
                if sub_source in ['合計','合併']:
                    continue

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
                        if source in ['合計','合併']:
                            continue
                        item={"source":source, "target":sub_source, "holder":owner_holder, "location":location, "is_coreSource":is_coreSource, "table_source1":0, "table_source2":1, "table_source3":0}
                        sublist.append(item)
        #print(sublist)
        #print("sub_company_except_china={}".format(len(table2_list)))
            
        #table3: 轉投資大陸地區之事業相關資訊 
        table3_list=[]
        china_company_element=company_header+'InformationOfInvestmentInMainlandChina'
        china_list=content.findall(china_company_element)
        china_json={"year":str(year), "stock":stock}
        china_sublist=[]
        #print("china={}".format(len(china_list)))
        for china_company in china_list:
            sub_source_note=''
            method=-1
            for child in china_company:
                #print("china chila={}".format(child.tag))
                if 'CompanyNameOfTheInvesteeInMainlandChina' in child.tag:    
                    sub_source=child.text.rstrip(' ')
                    sub_source=self._convertText(sub_source)
                    sub_source=sub_source.replace('(註一)','').replace('(註二)','').replace('(註三)','').replace('(註四)','').replace('(註五)','').replace('(註六)','')
                    sub_source=sub_source.replace('(註七)','').replace('(註八)','').replace('(註九)','').replace('(註十)','').replace('(註十一)','').replace('(註十二)','')
                elif 'PercentageOfOwnershipThroughDirectAndIndirectInvestmentByTheCompany' in child.tag:
                    owner_holder=child.text
                elif 'MethodOfInvestment' in child.tag:
                    method=int(child.text)
                elif 'Note' in child.tag:
                    if child.text!=None:
                        sub_source_note=child.text.rstrip(' \n')

            sub_source, is_exist=self._check_name_list(sub_source, table1_name_list)
            is_exist=0
            for i in range(0, len(sublist)):
                if sub_source in sublist[i]['target']:
                    sublist[i]['location']='china'
                    sublist[i]['table_source3']=1
                    china_item={"target":sublist[i]['target'], "holder":sublist[i]['holder'], "note":sub_source_note, "method":method}
                    china_sublist.append(china_item)
                    is_exist=1  
                    break
            
            if is_exist==0:             
                source='再投資大陸公司'
                item={"source":source, "target":sub_source, "holder":owner_holder, "location":'china', "is_coreSource":0, "table_source1":0, "table_source2":0, "table_source3":1}
                china_item={"target":sub_source, "holder":owner_holder, "note":sub_source_note, "method":method}
                sublist.append(item)
                china_sublist.append(china_item)

        #table3備註
        china_note_element=company_header+'Note-InformationOfInvestmentInMainlandChina'
        china_note=[]
        china_note_list=content.findall(china_note_element)
        for note in china_note_list:
            if note.text!=None:
                china_note=note.text.split("\n")
            
        china_json['sublist']=china_sublist
        china_json['notelist']=china_note
        
        current_source=''
        current_target=''
        for sub in sublist:
            if '本集團' in sub['source']:
                sub['source']=name    
        
            if sub['source'] not in ['-', '"', '〃', '〞','－']:
                current_source=sub['source']

            if sub['target'] not in ['-', '"', '〃', '〞','－']:
                current_target=sub['target']

            if sub['source'] in ['-', '"', '〃', '〞','－']:
                sub['source']=current_source

            if sub['target'] in ['-', '"', '〃', '〞','－']:
                sub['target']=current_target
    
        check_result=self.check_parser_reuslt(sublist)
        if check_result==False:
            print("{}, {}".format(stock, check_result))

        json_output['sublist']=sublist
        output_folder=os.path.join(self.mops_folder, str(stock))
        #print(output_folder)
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

        name_map_filename='{}_{}_name.json'.format(str(stock), str(year))
        name_map_path=os.path.join(output_folder, name_map_filename)
        name_map_output=open(name_map_path,"w")
        name_map_output.write(json.dumps(table1_name_list, ensure_ascii=False))
        name_map_output.close()

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
        r=requests.post(url, data=payload)
        print("{}, {}".format(r.status_code, len(r.content)))
        filename='{}_{}.xml'.format(str(stock), str(year))
        output_folder=os.path.join(self.xml_folder, str(stock))
        self.check_folder(output_folder) 
        output_file=os.path.join(output_folder, filename)        
        output=open(output_file, "wb")
        output.write(r.content)
        output.close()

    def download_xml_by_category(self, year, kind):
        try:
            if kind=='pub':
                target_list=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','XX','97', '98','99' ]
            elif kind=='rotc':
                target_list=['02','03','04','05','06','07','08','10','11','14','15','16','17','18','20','21', '22','23', '24','25','26','27','28','29','30','31','32','33' ]
            elif kind=='otc':
                target_list=['02','03','04','05','06','07','08','10','11','14','15','16','17','18','20','21','22','23','24','25','26','27','28','29','30','31','32','33','80','91']
            elif kind=='sii':
                target_list=['01','02','03','04','05','06','07','08','09','10','11','12','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','91']
                
            for target in target_list:
                #payload='encodeURIComponent=1&step=1&firstin=true&MAR_KIND='+kind+'&CODE='+target+'&SYEAR='+str(year)+'&SSEASON=01&REPORT_ID=C'
                #url='http://mops.twse.com.tw/mops/web/ajax_t164sb02/server-java/FileDownLoad'
                #if year==2014 and kind=='pub':

                #payload='step=9&fileName='+filename+'&filePath=/home/html/nas/xbrl/'+str(year)+'/&firstin=true'
                #else:    
                filename='{}-04-{}-{}-C.zip'.format(str(year), kind, target)
                payload='step=9&fileName='+filename+'&filePath=/home/html/nas/ifrs/'+str(year)+'/&firstin=true'
                url='http://mops.twse.com.tw/server-java/FileDownLoad'
                r=requests.post(url, data=payload)
                if r.status_code==200:
                    filename='{}_{}_{}.zip'.format(kind, target, str(year))
                    output_folder=os.path.join(self.zip_folder, kind, str(year))
                    self.check_folder(output_folder)
                    output_file=os.path.join(output_folder, filename)
                    print(output_file)
                    output=open(output_file,"wb")
                    output.write(r.content)
                    output.close()
                time.sleep(10)    
        except Exception as e:
            raise 

    def download_board_xml(self, stock, year, check_exist=True):
        try:
            taiwan_year=year-1911 
            filename='{}_{}_board.html'.format(str(stock), str(year))
            output_folder=os.path.join(self.board_folder, str(stock))
            self.check_folder(output_folder) 
            output_file=os.path.join(output_folder, filename) 
            if (check_exist==True and not os.path.exists(output_file)) or check_exist==False:       
                payload='encodeURIComponent=1&step=1&firstin=1&off=1&keyword4=&code1=&TYPEK2=&checkbtn=&queryName=co_id&inpuType=co_id&TYPEK=all&isnew=false&co_id='+str(stock)+'&year='+str(taiwan_year)+'&month=12'
                url='http://mops.twse.com.tw/mops/web/ajax_stapap1'
                r=requests.post(url, data=payload)
                print("{}".format(filename))
                output=open(output_file, "wb")
                output.write(r.content)
                output.close()
                time.sleep(10)
        except Exception as e:
            raise    

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

    def parse_folder(self, stock_map):
        print("Now, we are paring {}".format(self.xml_folder))
        keyError_list=[]
        try:
            for dirPath, dirNames, fileNames in os.walk(self.xml_folder):        
                for f in fileNames:
                    if '.xml' in f:
                        filename="{}".format(os.path.join(dirPath, f))
                        f_parts=f.split('-')
                        stock=int(f_parts[5])
                        year=int(f_parts[6][:4])
                        try:
                            self.parse_xml(stock, year, stock_map[stock], filename)
                        except KeyError:
                            keyError_list.append(stock)
        except Exception as e:
            print(filename)
            print(traceback.format_exc())     

        if len(keyError_list):
            print("We can't find some stock in stock_map, missing stock={}".format(keyError_list))               

    def download_board(self, stock_map, year, check_exist=True):
        for stock in stock_map:
            try:
                self.download_board_xml(stock, year, check_exist)
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(120)    

    def parse_board(self, stock, year, name):
        filename="{}_{}_board.html".format(stock, year)
        file_path=os.path.join(self.board_folder, str(stock), filename)
        content=open(file_path).read()
        parser = etree.HTMLParser(encoding='utf-8')
        tree=etree.HTML(content, parser)
        target_list=tree.xpath("//table")
        total_board=0
        total_supervisor=0
        board_dict={}
        supervisor_dict={}
        prev_source=''
        result_list=[]
        if len(target_list)==0:
            return result_list, False

        for target in target_list:
            if target.attrib.get('class')=='hasBorder':
                for tr_info in target.iter('tr'):
                    if tr_info.attrib.get('class')=='odd' or tr_info.attrib.get('class')=='even':
                        td_list=[]
                        for td_info in tr_info.iter('td'):
                            td_list.append(td_info.text)
                        title=td_list[0].replace('\u3000','').rstrip(' \n')
                        source=td_list[1].replace('\u3000','').rstrip(' \n')
                        source=self._convertText(source)
                        if '法人代表人' in title and '董事' in title:
                            if prev_source in board_dict.keys():
                                board_dict[prev_source]+=1
                            else:
                                board_dict[prev_source]=1    
                        elif '法人代表人' in title and '監察' in title:
                            if prev_source in supervisor_dict.keys():
                                supervisor_dict[prev_source]+=1
                            else:
                                supervisor_dict[prev_source]=1        
                        elif '董事' in title and '本人' in title:
                            total_board +=1
                        elif '監察' in title and '本人' in title:
                            total_supervisor +=1    
                        prev_source=source   

        #json_output['totalboard']=total_board
        #json_output['totalsupervisor']=total_supervisor
        board_list=[{"source":k, "number":v} for k, v in board_dict.items()]
        supervisor_list=[{"source":k, "number":v} for k, v in supervisor_dict.items()]
        #json_output['boardlist']=board_list
        #json_output['supervisorlist']=supervisor_list
        for board in board_list:
            item={"stock":stock, "source":board['source'], "target":name, "totalboard":total_board, "boardnumber":board['number'], "totalsupervisor":total_supervisor, "supervisornumber":0}
            result_list.append(item)
        for supervisor in supervisor_list:
            item={"stock":stock, "source":supervisor['source'], "target":name, "totalboard":total_board, "boardnumber":0, "totalsupervisor":total_supervisor, "supervisornumber":supervisor['number']}
            result_list.append(item)
            
        #print(result_list)
        return result_list, True

    def parse_board_folder(self, stock_map):
        output_file=os.path.join(self.board_folder, 'board.csv')
        output_handler=open(output_file, 'w')
        writer=csv.DictWriter(output_handler, fieldnames=['stock','source','target','totalboard','boardnumber','totalsupervisor','supervisornumber'])
        writer.writeheader()
        fail_stock=[]
        for dirPath, dirNames, fileNames in os.walk(self.board_folder):        
            for f in fileNames:
                if '.html' in f:
                    filename="{}".format(os.path.join(dirPath, f))
                    f_parts=f.split('_')
                    stock=int(f_parts[0])
                    year=int(f_parts[1])
                    result_list, status=self.parse_board(stock, year, stock_map[stock])
                    if status==False:
                        fail_stock.append(stock)
                    else:
                        for item in result_list:
                            writer.writerow(item)
        output_handler.close()  
        print("parse_board_folder complete, fail_stock={}".format(fail_stock))              

    def check_board_status(self, stock_map):
        input_file=os.path.join(self.board_folder, 'board.csv')
        input_handler=open(input_file, 'r')
        reader=csv.DictReader(input_handler)
        done_stock=set()
        for row in reader:
            done_stock.add(int(row['stock']))

        target_stock=set(stock_map.keys())
        unfinished=target_stock-done_stock
        unfinished_json={k:stock_map[k] for k in unfinished}

        if len(unfinished):
            output_handler=open("board_missing.json", 'w')
            output_handler.write(json.dumps(unfinished_json, ensure_ascii=False))
            output_handler.close()
            print("There are some missing stock in board={}".format(unfinished_json))
        else:
            print("Every stock is finished!")    

    def check_board_fail_reason(self):
        no_data=[]
        no_publish=[]
        unknown=[]
        for item in self.check_board_list:
            filename="{}_{}_board.html".format(str(item), self.config['start'])
            file_path=os.path.join(self.board_folder, str(item), filename)
            content=open(file_path).read()
            parser = etree.HTMLParser(encoding='utf-8')
            tree=etree.HTML(content, parser)
            target_list=tree.xpath("//h2")
            if len(target_list):
                if '查無資料' in target_list[0].text:
                    no_data.append(item)
            
            print(filename)
            target_list=tree.xpath("//h3")
            if len(target_list):
                if '不繼續公開發行' in target_list[0].text:
                    no_publish.append(item)    
                if '已下市' in target_list[0].text: 
                    no_publish.append(item)      
        print("查無資料={}".format(no_data))
        print("不繼續公開發行={}".format(no_publish))
        unknown=list(set(self.check_board_list)-set(no_data)-set(no_publish))
        print("其他原因={}".format(unknown))          

    def parse_missing_stock_name(self, year):
        missing_stock_map={}
        for dirPath, dirNames, fileNames in os.walk(self.xml_folder):        
            for f in fileNames:
                if '.xml' in f:
                        filename="{}".format(os.path.join(dirPath, f))
                        f_parts=f.split('-')
                        stock=int(f_parts[5])

                        if stock in self.missing_stock_list:
                            tree=ET.parse(filename)
                            content=tree.getroot()
                            if year==2016:
                                if stock in [1538, 3570, 3662, 5309, 6497, 1587, 3603, 5262, 5299, 6288, 6581, 6625, 6640, 4767, 6661]:
                                    accounting_header='{http://www.xbrl.org/tifrs/ar/2017-03-31}'
                                else:
                                    accounting_header='{http://www.xbrl.org/tifrs/ar/2015-03-31}'
                            else:
                                accounting_header='{http://www.xbrl.org/tifrs/ar/'+str(year)+'-03-31}'

                            target_element=accounting_header+'AccountantsReportBody'
                            target_list=content.findall(target_element)
                            case=0
                            for target in target_list:
                                body=target.text
                                end_index=body.find('公鑒')
                                start_index=body.find('會計師查核報告')
                                case=1
                                if start_index==-1:
                                    start_index=body.find('會 計 師 查 核 報 告')
                                    case=2
                                if start_index==-1:
                                    case=3

                                if case==1:    
                                    name=body[start_index+7:end_index].replace('董事會','')
                                elif case==2:
                                    name=body[start_index+13:end_index].replace('董事會','')
                                elif case==3:
                                    name=body[:end_index].replace('董事會','')
                                
                                name=self._convertText(name).rstrip(' ').lstrip(' ')
                                missing_stock_map[stock]=name
        
        return missing_stock_map
        
    def parse_stock_name(self, inv_stock, year):
        fail_stock=[]

        for key in inv_stock.keys():
            filename="{}_{}_board.html".format(str(key), str(year))
            filepath=os.path.join(self.board_folder, str(key), filename)
            if not os.path.exists(filepath):
                fail_stock.append(key)
                continue
            content=open(filepath).read()
            parser = etree.HTMLParser(encoding='utf-8')
            tree=etree.HTML(content, parser)
            fullname=tree.xpath("//td[@class='compName']")
            if len(fullname):   
                name=fullname[0].text.replace(str(key),'').replace('臺','台').replace(' ','').replace('　','')
                name=self._convertText(name)
                inv_stock[key]=name
            else:
                fail_stock.append(key)
        
        if len(fail_stock):
            print("parse_stock_name fail={}".format(fail_stock))
        return inv_stock

    def parse_stock_list(self):
        stock_list={}
        for dirPath, dirNames, fileNames in os.walk(self.xml_folder):        
            for f in fileNames:
                if '.xml' in f:
                    f_parts=f.split('-')
                    stock=int(f_parts[5])     
                    stock_list[stock]=""
        
        return stock_list   

    def check_parser_reuslt(self, sublist):
        fail_item=[]
        check_result=True
        
        for item in sublist:
            source=item['source']
            target=item['target']
            check_result=True

            if source in ["及", "及其", "、", "/", "合計", '子公司', '母公司', '本公司', '本集團', '-', '"', '〃', '〞','－'] :
                check_result=False
            if target in ["及", "及其", "、", "/", "合併", '子公司', '母公司', '本公司', '本集團', '-', '"', '〃', '〞','－'] :    
                check_result=False

            if check_result==False:
                fail_item.append(item)
        
        if check_result==False:
            print(fail_item)

        if len(sublist)==0:
            check_result=False

        return check_result             
        
if __name__=="__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--task', metavar='parse', type=str, nargs=1, required=True,
        help='Specify a task to do. (parse)')
    arg_parser.add_argument('-c', '--config', metavar='config.json', type=str, nargs=1, required=True,
        help='Specify a config file')

    args = arg_parser.parse_args()

    if args.task!=None:
        task=args.task[0]

    if args.config!=None:
        config_name=args.config[0]  
    else:
        config_name='config.json'      

    project_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = project_dir + '/project_config/'+ config_name  
    
    with open(config_file) as file:
        project_config=json.load(file)
        
    kind=project_config['kind']
    kind_list=project_config['kind_list']
    
    with open(project_config[kind]['stock_map_json']) as file:
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
    parser=companyNode(config_file) 
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
        parser.parse_folder(inv_stock)
    elif task=='download_board':
        file_path=os.path.join(project_config[kind]['board_folder'], 'stock_list.json')
        with open(file_path) as file:
            inv_stock = json.load(file)
        parser.download_board(inv_stock, project_config['start'])    
    elif task=='parse_board':
        result_list=parser.parse_board(1592, 2016, inv_stock[1592])
        print(result_list)
    elif task=='parse_board_folder':
        parser.download_board(inv_stock, project_config['start'])
        parser.parse_board_folder(inv_stock)   
    elif task=='check_board_status':
        parser.check_board_status(inv_stock)
    elif task=='check_board_fail_reason':
        parser.check_board_fail_reason()    
    elif task=='download_missing_board':
        parser.download_board(project_config[kind]['board_missing_list'], project_config['start'], check_exist=False)
    elif task=='parse_stock_name':
        file_path=os.path.join(project_config[kind]['board_folder'], 'stock_list.json')
        with open(file_path) as file:
            inv_stock = json.load(file)
        new_inv_stock=parser.parse_stock_name(inv_stock, project_config['start'])
        new_stock={v:int(k) for k, v in new_inv_stock.items()}  
        output_handler=open(project_config[kind]['stock_map_json'], 'w')
        output_handler.write(json.dumps(new_stock, ensure_ascii=False))
        output_handler.close()
    elif task=='download_category_xml': 
        for kind in kind_list:
            parser.download_xml_by_category(project_config['start'],kind)
    elif task=='parse_stock_list':
        stock_list=parser.parse_stock_list()

        file_path=os.path.join(project_config[kind]['board_folder'], 'stock_list.json')
        output_handler=open(file_path, 'w')
        output_handler.write(json.dumps(stock_list, ensure_ascii=False))
        output_handler.close()
    elif task=='parse_missing_stock_name':
        missing_stock_map=parser.parse_missing_stock_name(project_config['start'])   
        inv_stock={v:k for k, v in missing_stock_map.items()}  
        output_handler=open(project_config[kind]['missing_stock_map_json'], 'w')
        output_handler.write(json.dumps(inv_stock, ensure_ascii=False))
        output_handler.close() 
    else:
        print("no match job!")
