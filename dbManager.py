# -*- coding: utf-8 -*-
import json
import pymysql

class dbManager(object):
    def __init__(self, config):
        self.host = config['host']
        self.user = config['user']
        self.passwd = config['password']
        self.db = config['database']
        self.port= config['port']

        self.charset = "utf8mb4"
        self.cursorclass = pymysql.cursors.DictCursor

        self.connection=None
        self.cursor=None

    def connect(self):
        if self.connection is None:
            self.connection= pymysql.connect(host=self.host,
                    user=self.user,
                    passwd=self.passwd,
                    port=self.port,
                    db=self.db,
                    charset=self.charset,
                    cursorclass=self.cursorclass,
                    autocommit=True)
            self.cursor=self.connection.cursor()        

    def close(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.connection:
            self.connection.close()
            self.connection = None        

    def insert_company(self, item):
        self.connect()
        try:
            field_list=list()
            param_list=list()
            for key in item:
                #if type(book_attr[key])==list and len(book_attr[key])==0:
                #    continue
                if key=='group':
                    field_list.append('`{}`'.format(key))
                else:    
                    field_list.append(key)
                param_list.append('%('+key+')s')

            insert_sql="insert into factory_group ("+",".join(field_list)+") VALUES ("+ ",".join(param_list)+")"
            sql = self.cursor.mogrify(insert_sql, item)
            self.cursor.execute(insert_sql, item)
        except pymysql.InternalError as e:
            print(item)
            raise
        except pymysql.IntegrityError as e:
            if e.args[0]=='1062':
                print("duplicate key")
        finally:
            self.close()   

    def query_parent(self, company_name):
        self.connect()
        try:
            query_sql="select * from company_info where company_name like '%%{company_name}%%'".format(company_name=company_name)
            self.cursor.execute(query_sql)
            parent_info=self.cursor.fetchone()
            return parent_info
        except Exception as e:
            raise
        finally: 
            self.close()           
     
    def query_fine_record_by_taxcode(self, taxcode):
        self.connect()
        try:
            query_sql="select factory_fine.penalty_money, factory_corp.registration_no from factory_fine, factory_corp where factory_corp.corp_id=%(taxcode)s and factory_corp.registration_no=factory_fine.registration_no"
            #print("{}, {}".format(query_sql, taxcode))
            self.cursor.execute(query_sql, {"taxcode":taxcode})
            fine_record_list=self.cursor.fetchall()
            penalty_money=0
            has_fine=False
            if len(fine_record_list):
                has_fine=True
                for record in fine_record_list:
                    penalty_money+=int(record['penalty_money'])
            return has_fine, penalty_money, len(fine_record_list)
        except Exception as e:
            raise
        finally: 
            self.close()            

