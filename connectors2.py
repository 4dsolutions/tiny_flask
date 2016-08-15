# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 12:47:19 2016

@author: kurner
"""
import sqlite3 as sql
import os.path
import json
import time
from contextlib import contextmanager

# PATH = "/Users/kurner/Documents/classroom_labs/session10"
PATH = "."
DB1 = os.path.join(PATH, 'periodic_table.db')
DB2 = os.path.join(PATH, 'glossary.db')

def mod_date():
    return time.mktime(time.gmtime())  # GMT time

@contextmanager        
def Connector(db):
    try:
        db.conn = sql.connect(db.db_name)  # connection
        db.curs = db.conn.cursor()   # cursor
        yield db       
    except Exception as oops:
        if oops:
            raise
    db.conn.close()

class elemsDB:
    
    def __init__(self, db_name):
        self.db_name = db_name
     
    def seek(self, elem):
        if self.conn:
            if elem != "all":
                query = ("SELECT * FROM Elements "
                "WHERE elem_symbol = '{}'".format(elem))
                self.curs.execute(query)
                result = self.curs.fetchone()
                if result:
                    return json.dumps(list(result))
            else:
                query = "SELECT * FROM Elements ORDER BY elem_protons"
                self.curs.execute(query)
                result={}
                for row in self.curs.fetchall():
                    result[row[1]] = list(row)
                return json.dumps(result)                
        return "NOT FOUND"
     
    def save(self, the_data):
        elem = the_data["symbol"]
        if self.conn:
            query = ("SELECT * FROM Elements "
            "WHERE elem_symbol = '{}'".format(elem))
            self.curs.execute(query)
            result = self.curs.fetchone()
            if result:
                return "ALREADY IN DB"
            else:
                d = {}
                d.update(the_data.to_dict(flat=True)) # the_data is immutable
                print("Type:",type(the_data))
                d["initials"]="KTU"
                d["right_now"]=mod_date()
                query = ("INSERT INTO Elements "
                "(elem_protons, elem_symbol, elem_long_name, elem_mass, elem_series,"
                "updated_at, updated_by) "
                "VALUES ({protons}, '{symbol}', '{long_name}', "
                "{mass}, '{series}', {right_now}, '{initials}')")
                query = query.format(**d)
                print(query)
                self.curs.execute(query)
                self.conn.commit()
                return "POST SUCCESSFUL"
        return "NOT FOUND"
    
class glossaryDB:
    
    def __init__(self, db_name):
        self.db_name = db_name
     
    def seek(self, term):
        if self.conn:
            query = ("SELECT * FROM Glossary "
            "WHERE gl_term = '{}'".format(term))
            self.curs.execute(query)
            result = self.curs.fetchone()
            if result:
                return json.dumps(list(result))
        return "NOT FOUND"