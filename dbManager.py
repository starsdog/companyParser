# -*- coding: utf-8 -*-
import json
import pymysql

class dbManager(object):
    def __init__(self, config):
        self.host = config['host']
        self.user = config['user']
        self.passwd = config['password']
        self.db = config['database']

        self.charset = "utf8mb4"
        self.cursorclass = pymysql.cursors.DictCursor

        self.connection=None
        self.cursor=None

    def connect(self):
        if self.connection is None:
            self.connection= pymysql.connect(host=self.host,
                    user=self.user,
                    passwd=self.passwd,
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
                field_list.append(key)
                param_list.append('%('+key+')s')

            insert_sql="insert into company_info ("+",".join(field_list)+") VALUES ("+ ",".join(param_list)+")"
            
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
            

