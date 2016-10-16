# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 11:28:57 2016

@author: Kirby Urner
"""
from flask import Flask, request, render_template
from connectors2 import Connector, elemsDB, glossaryDB, shapesDB
from connectors2 import DB1, DB2, DB3
import json
import collections

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/elements")
def elements():
    return render_template("elements.html")

@app.route("/elements/<symbol>", methods=['GET', 'POST'])
def element_page(symbol):

    if request.method == "POST":
        with Connector(elemsDB(DB1)) as dbx:
            result = dbx.update(request.form) 
            print(result)
                                           
    with Connector(elemsDB(DB1)) as dbx:
        result = dbx.seek(symbol)
    if "NOT FOUND" != result:
        if symbol != 'all':
            data = json.loads(result)
            return render_template("elem_page.html", 
                                protons=data[0],
                                elem=data[1], 
                                long_name=data[2],
                                mass=data[3],
                                series=data[4])
        else:
            data = json.loads(result)
            data = collections.OrderedDict(sorted(data.items(), 
                                            key=lambda k: k[1][0]))
            return render_template("all_elems.html", the_data=data)

    return render_template("elements.html")

@app.route("/api/elements", methods=['GET', 'POST'])
def get_elements():
    if request.method == "GET":
        elem = request.args.get('elem')
        result="NOT FOUND"
        with Connector(elemsDB(DB1)) as dbx:
            result = dbx.seek(elem) 
        if result != "NOT FOUND":
            return result
        return render_template("elements.html")
    if request.method == "POST":
        if request.form["secret"]=="DADA":
            with Connector(elemsDB(DB1)) as dbx:
                result = dbx.save(request.form)
            return result
        return "Oooo, you tried to post!"

#--------------------------------------------------
        
@app.route("/glossary")
def glossary():
    return render_template("glossary.html")

@app.route("/glossary/<term>",  methods=['GET', 'POST'])
def get_glossary(term):
    if request.method == "POST":
        print("POSTING DATA!!")
        with Connector(glossaryDB(DB2)) as dbx:
            result = dbx.update(request.form) 
            print(result)
            
    with Connector(glossaryDB(DB2)) as dbx:
        result = dbx.seek(term)
    if "NOT FOUND" != result:
        if term != 'all':
            data = json.loads(result)
            return render_template("term_page.html", 
                                the_term = data[0],
                                the_definition = data[1])
        else:
            data = json.loads(result)
            data = collections.OrderedDict(sorted(data.items(), 
                                            key=lambda k: k[1][0]))
            return render_template("all_terms.html", the_data=data)
        
    return render_template("glossary.html")

@app.route("/api/glossary", methods=['GET', 'POST'])
def get_terms():
    if request.method == "GET":
        term = request.args.get('term')
        result="NOT FOUND"
        with Connector(glossaryDB(DB2)) as dbx:
            result = dbx.seek(term) 
        if result != "NOT FOUND":
            return result
        return render_template("terms.html")
    if request.method == "POST":
        print("Posting to glossary")
        if request.form["secret"]=="DADA":
            with Connector(glossaryDB(DB2)) as dbx:
                result = dbx.save(request.form)
            return result
        return "Oooo, you tried to post!"
    
#--------------------------------------------------  

@app.route("/shapes")
def shapes():
    return render_template("shapes.html")

@app.route("/shapes/<abbrev>",  methods=['GET', 'POST'])
def get_polyhedrons(abbrev):
    if request.method == "POST":
        print("POSTING DATA!!")
        with Connector(shapesDB(DB3)) as dbx:
            result = dbx.update(request.form) 
            print(result)
            
    with Connector(shapesDB(DB3)) as dbx:
        result = dbx.seek(abbrev)
        
    if "NOT FOUND" != result:
        if abbrev != 'all':
            data = json.loads(result)
            return render_template("shape_page.html", 
                                shape_id = data[0],
                                shape = data[1],
                                abbrev = data[2],
                                shape_v = data[3],
                                shape_f = data[4],
                                shape_e = data[5],
                                shape_dual_id = data[6],
                                shape_volume = data[7])
        else:
            data = json.loads(result)
            data = collections.OrderedDict(sorted(data.items(), 
                                            key=lambda k: k[1][0]))
            return render_template("all_shapes.html", the_data=data)
        
    return render_template("shapes.html")

@app.route("/api/shapes", methods=['GET', 'POST'])
def get_shapes():
    if request.method == "GET":
        term = request.args.get('shape')
        result="NOT FOUND"
        with Connector(shapesDB(DB3)) as dbx:
            result = dbx.seek(term) 
        if result != "NOT FOUND":
            return result
        return render_template("shapes.html")
    if request.method == "POST":
        if request.form["secret"]=="DADA":
            with Connector(shapesDB(DB3)) as dbx:
                result = dbx.save(request.form)
            return result
        return "Oooo, you tried to post!"

@app.errorhandler(404)
def page_not_found(e):
    return render_template("home.html")
          
if __name__ == '__main__':
    app.run(port=5000, debug=True)

