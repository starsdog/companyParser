import xml.etree.ElementTree as ET
import json
import requests

class companyNode(object):
    def __init__(self, config_file):

        with open(config_file) as file:
            config = json.load(file)
            for key in config.keys():
                setattr(self, key, config[key])
    
    
    def parse_xml(self, file_name):
        content=ET.parse(file_name).getroot()
        company_list=content.findall('{http://www.xbrl.org/tifrs/notes/2013-03-31}NamesLocationsAndRelatedInformationOfInvesteesOverWhichTheCompanyExercisesSignificantInfluence')
        print(len(company_list))
        json_output={}
        for company in company_list:
            for child in company:
                #print("{}, {}".format(child.tag, child.attrib))
                if 'CompanyNameOfTheInvestor' in child.tag:
                    source=child.text
                elif 'CompanyNameOfTheInvestee' in child.tag:
                    sub_source=child.text
                elif 'InvestmentsAtTheEndOfThePeriod' in child.tag:
                    for sub_invest in child:
                        if 'PercentageOfOwnership1' in sub_invest.tag:
                            owner_pert=sub_invest.text
            print("{}, {}, {}".format(source, sub_source, owner_pert))           

    def download_xml(self):
        payload={"step": 9, "functionName":"t164sb01", "report_id":"C", "co_id":2311, "year": 2013, "season":1}
        url='http://mops.twse.com.tw/server-java/FileDownLoad'
        r=requests.post(url, data=json.dumps(payload))
        print("{}".format(r.status_code))


if __name__=="__main__":
    parser=companyNode('config.json')
    #parser.parse_xml('2311.xml')
    parser.download_xml()
