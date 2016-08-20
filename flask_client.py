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
   term_page.html
   shapes.html
   shape_page.html
"""

import requests

def web_post(the_url, data):
    r = requests.post(the_url, data=data)
    print(r.status_code)
    print(r.content)

def web_post_element():
    data = {}
    data["protons"]=30
    data["symbol"]="Zn"
    data["long_name"]="Zinc"
    data["mass"]=65.38
    data["series"]="Transition metal"
    data["secret"]="DANyoob" # <--- primitive authentication
    url = 'http://localhost:5000/api/elements'
    # url = 'http://thekirbster.pythonanywhere.com/api/elements'
    web_post(url, data)
        
def web_post_shape(data):
    url = 'http://localhost:5000/api/elements'
    # url = 'http://thekirbster.pythonanywhere.com/api/elements'
    web_post(url, data)

# Platonics
tetrahedron = dict(shape_id=1, shape="tetrahedron", abbrev = "tetra",
                   shape_v = 4, shape_f = 4, shape_e = 6, shape_dual_id=1, 
                   shape_volume = 1)

octahedron = dict(shape_id=2, shape="octahedron", abbrev = "octa",
                   shape_v = 6, shape_f = 8, shape_e = 12, shape_dual_id=3, 
                   shape_volume = 4)

cube = dict(shape_id=3, shape="cube", abbrev = "cube",
                   shape_v = 8, shape_f = 6, shape_e = 12, shape_dual_id=2, 
                   shape_volume = 3)

icosahedron = dict(shape_id=4, shape="icosahedron", abbrev = "icosa",
                   shape_v = 12, shape_f = 20, shape_e = 30, shape_dual_id=5, 
                   shape_volume = 18.51)

dodecahedron = dict(shape_id=5, shape="pentagonal dodecahedron", abbrev = "PD",
                   shape_v = 20, shape_f = 12, shape_e = 30, shape_dual_id=4, 
                   shape_volume = 15.21)

web_post_shape(tetrahedron)
