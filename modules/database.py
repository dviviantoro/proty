import os, sys
from tinydb import TinyDB, Query
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *

db_app_path = temp_dir / "app.json"
db = TinyDB(db_app_path)

def tinydb_insert_dict(category, dict_data):
    table = db.table(category)
    table.insert(dict_data)
    logger.info(f"tinydb record {category} data: {dict_data}")

def tinydb_read(category):
    table = db.table(category)
    return table.all()

def tinydb_check_existence(category, name):
    table = db.table(category)
    return True if table.search(Query().name == name) != [] else False

def tinydb_append_xy(category, project, xy):
    table = db.table(category)
    current_project = table.search(Query().name == project)
    try:
        current_project[0]["xy"].append(xy)
        table.update({'xy': current_project[0]["xy"]}, Query().name == project)
    except Exception as e:
        print(e)
        table.update({'xy': [xy]}, Query().name == project)

def tinydb_change_phase(phase):
    table = db.table("general")
    table.update({"phase": phase})
    return table.all()

def tinydb_update_temp(key, value):
    tbl = db.table("temp")
    tbl.update({key: value})
    return tbl.all()
