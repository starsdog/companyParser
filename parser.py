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
    
    
    def parse_xml(self, stock, year, name):
        filename='{}_{}.xml'.format(str(stock), str(year))
        file_path=os.path.join(self.xml_folder, str(stock), filename)
        tree=ET.parse(file_path)
        content=tree.getroot()
        company_header='{http://www.xbrl.org/tifrs/notes/'+str(year)+'-03-31}'
        company_element=company_header+'NamesLocationsAndRelatedInformationOfInvesteesOverWhichTheCompanyExercisesSignificantInfluence'
        company_list=content.findall(company_element)
        json_output={"y":str(year)}
        sublist=[]
        for company in company_list:
            for child in company:
                #print("{}, {}".format(child.tag, child.attrib))
                if 'CompanyNameOfTheInvestor' in child.tag:
                    source=child.text
                    if '本公司' in source:
                        source=name
                elif 'CompanyNameOfTheInvestee' in child.tag:
                    sub_source=child.text
                elif 'InvestmentsAtTheEndOfThePeriod' in child.tag:
                    for sub_invest in child:
                        if 'PercentageOfOwnership1' in sub_invest.tag:
                            owner_holder=sub_invest.text
            item={"source":source, "sub_source":sub_source, "holder":owner_holder}
            sublist.append(item)
        print("sub_company_except_china={}".format(len(sublist)))
            
        china_sublist=[]
        china_company_element=company_header+'InformationOfInvestmentInMainlandChina'
        china_list=content.findall(china_company_element)
        print("china={}".format(len(china_list)))
        for china_company in china_list:
            for child in china_company:
                #print("china chila={}".format(child.tag))
                source=''
                if 'CompanyNameOfTheInvesteeInMainlandChina' in child.tag:    
                    sub_source=child.text
                elif 'PercentageOfOwnershipThroughDirectAndIndirectInvestmentByTheCompany' in child.tag:
                    owner_holder=child.text
            item={"source":source, "sub_source":sub_source, "holder":owner_holder}
            china_sublist.append(item)
         
        json_output['sublist']=sublist
        json_output['china_sublist']=china_sublist
        filename='{}_{}.json'.format(str(stock), str(year))
        file_path=os.path.join(self.json_folder, filename)
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
        output_file=os.path.join(self.xml_folder, str(stock), filename)
        output=open(output_file, "wb")
        output.write(r.content)
        output.close()

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

    target_list=project_config['target']
    stock_dict={}
    for t in target_list:
        if t in stock.keys():
            stock_dict[t]=stock[t]
        else:
            print("can't find stock number of {}".format(t))

    parser=companyNode('config.json') 
    if task=='parse':
        for key in stock_dict.keys():
            parser.parse_xml(stock_dict[key], 2014, key)
    elif task=='download':
        for key in stock_dict.keys():
            parser.download_xml(stock_dict[key], 2014)
    else:
        print("no match job!")
