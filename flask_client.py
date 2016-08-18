# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 17:35:58 2016

@author: Kirby Urner

Post a chemical element to the Periodic Table.
Goes into sqlite DB Periodic_table.Elements

API:

HTML views
/elements
/elements/H
/elements/Si
...
/elements/all

JSON output
/api/elements?elem=H
/api/elements?elem=O
...
/api/elements?elem=all

Requires:
flask_app.py  <--- uses flask (conda install flask)
connector.py

Databases (SQLite)  
glossary.db   <--- these may need to go in home dir
periodic_table.db

Jinja2 templates
/templates/
   home.html
   elements.html
   elem_page.html
   all_elems.html 
   glossary.html
   all_terms.html
   term_page.html
"""

import requests

data = {}
data["protons"]=30
data["symbol"]="Zn"
data["long_name"]="Zinc"
data["mass"]=65.38
data["series"]="Transition metal"
data["secret"]="***" # <--- primitive authentication

# the_url = 'http://localhost:5000/api/elements'
the_url = 'http://thekirbster.pythonanywhere.com/api/elements'
r = requests.post(the_url, data=data)
print(r.status_code)
print(r.content)
