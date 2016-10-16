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
import math

phi = (math.sqrt(5)+1)/2.0

SECRET = "DADA"

# PATH = "/Users/kurner/Documents/classroom_labs/session10"
PATH = "/Users/kurner/Documents/workspace/TinyFlaskApp/src"
DB1 = os.path.join(PATH, 'periodic_table.db')
DB2 = os.path.join(PATH, 'glossary.db')
DB3 = os.path.join(PATH, 'polyhedrons.db')

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
            print("Not connecting to", db.db_name)
            raise
    db.conn.close()

class elemsDB:
    
    def __init__(self, db_name):
        self.db_name = db_name

    def _create_table(self):
        # used outside of web serving mode
        # https://www.sqlite.org/lang_droptable.html
        self.curs.execute("""DROP TABLE IF EXISTS Elements""")
        self.curs.execute("""CREATE TABLE Elements
            (elem_protons int PRIMARY KEY,
             elem_symbol text,
             elem_long_name text,
             elem_mass float,
             elem_series text,
             updated_at int,
             updated_by text)""")
             
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

    def update(self, the_data):
        if self.conn and the_data["secret"] == SECRET:
            d = {}
            # might be a form, might be some kind of dict
            try:
                d.update(the_data.to_dict(flat=True)) # the_data is immutable
            except AttributeError:
                d.update(the_data)
            d["initials"]="KTU"
            d["right_now"]=mod_date()
            query = ("UPDATE Elements "
            "SET elem_protons = {protons}, elem_long_name = '{long_name}', "  
            "elem_mass = {mass}, elem_series = '{series}', "
            "updated_at = {right_now}, updated_by = '{initials}' WHERE elem_symbol = '{symbol}'")
            query = query.format(**d)
            print(query)
            self.curs.execute(query)
            self.conn.commit()
            return "UPDATE SUCCESSFUL"
        else:
            print("NO CONNECTION")
        return "NOT FOUND"
         
    def save(self, the_data):
        elem = the_data["symbol"]
        if self.conn and the_data["secret"] == SECRET:
            query = ("SELECT * FROM Elements "
            "WHERE elem_symbol = '{}'".format(elem))
            self.curs.execute(query)
            result = self.curs.fetchone()
            if result:
                return "ALREADY IN DB"
            else:
                d = {}
                # might be a form, might be some kind of dict
                try:
                    d.update(the_data.to_dict(flat=True)) # the_data is immutable
                except AttributeError:
                    d.update(the_data)
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

    def _create_table(self):
        # used outside of web serving mode
        # https://www.sqlite.org/lang_droptable.html
        self.curs.execute("""DROP TABLE IF EXISTS Glossary""")
        self.curs.execute("""CREATE TABLE Glossary
            (gl_term text PRIMARY KEY,
             gl_definition text,
             updated_at int,
             updated_by text)""")
             
    def seek(self, term):
        if self.conn:
            if term != "all":
                query = ("SELECT * FROM Glossary "
                "WHERE gl_term = '{}'".format(term))
                self.curs.execute(query)
                result = self.curs.fetchone()
                if result:
                    return json.dumps(list(result))
            else:
                query = "SELECT * FROM Glossary ORDER BY gl_term"
                self.curs.execute(query)
                result={}
                for row in self.curs.fetchall():
                    result[row[1]] = list(row)
                return json.dumps(result)                
        return "NOT FOUND"

    def update(self, the_data):
        if self.conn and the_data["secret"] == SECRET:
            d = {}
            # might be a form, might be some kind of dict
            try:
                d.update(the_data.to_dict(flat=True)) # the_data is immutable
            except AttributeError:
                d.update(the_data)
            d["initials"]="KTU"
            d["right_now"]=mod_date()
            query = ("UPDATE Glossary "
            "SET gl_definition = '{gl_definition}', "  
            "updated_at = {right_now}, updated_by = '{initials}' WHERE gl_term = '{gl_term}'")
            query = query.format(**d)
            print(query)
            self.curs.execute(query)
            self.conn.commit()
            return "UPDATE SUCCESSFUL"
        else:
            print("NO CONNECTION")
        return "NOT FOUND"
        
    def save(self, the_data):
        term = the_data["gl_term"]
        print("save glossary term...")
        if self.conn and the_data["secret"] == SECRET:
            query = ("SELECT * FROM Glossary "
            "WHERE gl_term = '{}'".format(term))
            self.curs.execute(query)
            result = self.curs.fetchone()
            if result:
                return "ALREADY IN DB"
            else:
                d = {}
                # might be a form, might be some kind of dict
                try:
                    d.update(the_data.to_dict(flat=True)) # the_data is immutable
                except AttributeError:
                    d.update(the_data)
                d["initials"]="KTU"
                d["right_now"]=mod_date()
                query = ("INSERT INTO Glossary "
                "(gl_term, gl_definition, "
                "updated_at, updated_by) "
                "VALUES ('{gl_term}', '{gl_definition}', {right_now}, '{initials}')")
                query = query.format(**d)
                print(query)
                self.curs.execute(query)
                self.conn.commit()
                return "POST SUCCESSFUL"
        return "NOT FOUND"
    
class shapesDB:
    
    def __init__(self, db_name):
        self.db_name = db_name

    def _create_table(self):
        # used outside of web serving mode
        # https://www.sqlite.org/lang_droptable.html
        self.curs.execute("""DROP TABLE IF EXISTS Shapes""")
        self.curs.execute("""CREATE TABLE Shapes
                (shape_id int PRIMARY KEY, 
                shape text, 
                abbrev text,
                shape_v int, 
                shape_f int, 
                shape_e int, 
                shape_dual_id int, 
                shape_volume float, 
                updated_at int, 
                updated_by text)""")
        
    def _load_data(self):
        """
        Tetravolumes per Synergetics 1 & 2
        http://controlroom.blogspot.com/2010/02/getting-phi-in-game.html
        """
        tetrahedron = dict(shape_id=1, shape="tetrahedron", abbrev = "tetra",
                   shape_v = 4, shape_f = 4, shape_e = 6, shape_dual_id=1, 
                   shape_volume = 1)
        octahedron = dict(shape_id=2, shape="octahedron", abbrev = "octa",
                   shape_v = 6, shape_f = 8, shape_e = 12, shape_dual_id=3, 
                   shape_volume = 4)
        cube = dict(shape_id=3, shape="cube", abbrev = "cube",
                   shape_v = 8, shape_f = 6, shape_e = 12, shape_dual_id=2, 
                   shape_volume = 3)
        RD = dict(shape_id=6, shape="rhombic dodecahedron", abbrev = "RD",
                   shape_v = 14, shape_f = 12, shape_e = 24, shape_dual_id=8, 
                   shape_volume = 6)    
        cuboctahedron = dict(shape_id=8, shape="cuboctahedron", abbrev = "cubocta",
                   shape_v = 12, shape_f = 14, shape_e = 24, shape_dual_id=6, 
                   shape_volume = 20)    
        icosahedron = dict(shape_id=4, shape="icosahedron", abbrev = "icosa",
                   shape_v = 12, shape_f = 20, shape_e = 30, shape_dual_id=5, 
                   shape_volume = 5 * math.sqrt(2) * phi**2)
        dodecahedron = dict(shape_id=5, shape="pentagonal dodecahedron", abbrev = "PD",
                   shape_v = 20, shape_f = 12, shape_e = 30, shape_dual_id=4, 
                   shape_volume = (phi**2 + 1) * 3 * math.sqrt(2))
        RT = dict(shape_id=7, shape="rhombic triacontahedron", abbrev = "RT",
                   shape_v = 24, shape_f = 30, shape_e = 52, shape_dual_id=9, 
                   shape_volume = 15 * math.sqrt(2))
        
        self.save(tetrahedron)
        self.save(octahedron)
        self.save(icosahedron)
        self.save(dodecahedron)
        self.save(cube)
        self.save(RD)
        self.save(RT)
        self.save(cuboctahedron)
                  
    def seek(self, abbrev):
        if self.conn:
            if abbrev != "all":
                query = ("SELECT * FROM Shapes "
                "WHERE abbrev = '{}'".format(abbrev))
                self.curs.execute(query)
                result = self.curs.fetchone()
                if result:
                    return json.dumps(list(result))
            else:
                query = "SELECT * FROM Shapes ORDER BY shape_id"
                self.curs.execute(query)
                result={}
                for row in self.curs.fetchall():
                    result[row[1]] = list(row)
                return json.dumps(result)                
        return "NOT FOUND"

    def update(self, the_data):
        if self.conn and the_data["secret"] == SECRET:
            d = {}
            # might be a form, might be some kind of dict
            try:
                d.update(the_data.to_dict(flat=True)) # the_data is immutable
            except AttributeError:
                d.update(the_data)
            d["initials"]="KTU"
            d["right_now"]=mod_date()
            query = ("UPDATE Shapes "
            "SET shape = '{shape}', abbrev = '{abbrev}', shape_v = {shape_v}, shape_e = {shape_e}, "
            "shape_f = {shape_f}, shape_volume = {shape_volume}, "  
            "updated_at = {right_now}, updated_by = '{initials}' WHERE shape_id = {shape_id}")
            query = query.format(**d)
            print(query)
            self.curs.execute(query)
            self.conn.commit()
            return "UPDATE SUCCESSFUL"
        else:
            print("NO CONNECTION")
        return "NOT FOUND"
        
    def save(self, the_data):
        term = the_data["abbrev"]
        if self.conn and the_data["secret"] == SECRET:
            query = ("SELECT * FROM Shapes "
            "WHERE abbrev = '{}'".format(term))
            self.curs.execute(query)
            result = self.curs.fetchone()
            if result:
                return "ALREADY IN DB"
            else:
                d = {}
                # might be a form, might be some kind of dict
                try:
                    d.update(the_data.to_dict(flat=True)) # the_data is immutable
                except AttributeError:
                    d.update(the_data)
                d["initials"]="KTU"
                d["right_now"]=mod_date()
                query = ("INSERT INTO Shapes "
                "(shape_id, shape, abbrev, shape_v, shape_f, shape_e, "
                "shape_dual_id, shape_volume, "
                "updated_at, updated_by) "
                "VALUES ({shape_id}, '{shape}', '{abbrev}', "
                "{shape_v}, {shape_f}, {shape_e}, "
                "{shape_dual_id}, {shape_volume}, "
                "{right_now}, '{initials}')")
                query = query.format(**d)
                print(query)
                self.curs.execute(query)
                self.conn.commit()
                return "POST SUCCESSFUL"
        return "NOT FOUND"