import sqlite3
 
def sqlite_create_table(table_name):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    query_create = """
        CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            fullname TEXT NOT NULL
        )
    """.format(table_name)
    cursor.execute(query_create)

    conn.commit()
    conn.close()




def sqlite_insert_data(table_name, data):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # if table_name == "calibrator":
    #     insert_query = """
    #         INSERT INTO {} (name, manufacture, country, version)
    #         VALUES (?, ?, ?, ?)
    #     """.format(table_name)
    #     my_data = (data["name"], data["manufacture"], data["country"], data["version"])
    #     cursor.execute(insert_query, my_data)
    insert_query = """
        INSERT INTO {} (name, fullname)
        VALUES (?, ?)
    """.format(table_name)
    my_data = (data["name"], data["fullname"])
    cursor.execute(insert_query, my_data)
        
    conn.commit()
    conn.close()

def sqlite_read_table(table_name):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM {}'.format(table_name))
    rows = cursor.fetchall()

    for row in rows:
        print(row)
    conn.close()

def sqlite_list_all_table():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        print(table)
    conn.close()

def sqlite_drop_table(table_name):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    conn.commit()
    conn.close()

calibrator_data = {
    # "name": "HVPD pC Calibrator",
    # "manufacture": "HVPD",
    # "country": "UK",
    # "version": "v2",
    # "name": "Tetex pC Calibrator",
    # "manufacture": "Haefely",
    # "country": "Swiss",
    # "version": "v1",
    "name": "Tetex pC Calibrator",
    "manufacture": "Haefely",
    "country": "Swiss",
    "version": "v1",
}
# sqlite_create_table("calibrator")
# sqlite_insert_data("calibrator", calibrator_data)
# sqlite_read_table("calibrator")

sensor_data = {
    # "name": "HFCT-HVPD",
    # "manufacture": "HVPD",
    # "country": "UK",
    # "model": "small",
    # "version": "v1"
    "name": "TTATs",
    "manufacture": "TTAT-ITB",
    "country": "Indonesia",
    "model": "diy",
    "version": "v2"
}
# sqlite_create_table("sensor")
# sqlite_insert_data("sensor", sensor_data)
# sqlite_read_table("sensor")

material_data = {
    # "name": "EPR",
    # "fullname": "Ethylene Propylene Rubber"
    # "name": "XLPE",
    # "fullname": "Cross-Linked Polyethylene"
    "name": "Silicon Rubber",
    "fullname": "Silicon Rubber"
}
# sqlite_create_table("material")
# sqlite_insert_data("material", material_data)
# sqlite_read_table("material")



# create table pake nama timestamp, jadi unique


# conn = sqlite3.connect('inventory.db')
# cursor = conn.cursor()

# cursor.execute('''
# DELETE FROM voltage_option
# WHERE id = (SELECT id FROM voltage_option ORDER BY id DESC LIMIT 1)
# ''')

# query_create = """
#     CREATE TABLE IF NOT EXISTS {} (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         phase TEXT NOT NULL
#     )
# """.format("phase_option")
# cursor.execute(query_create)

# conn.commit()

# insert_query = """
#     INSERT INTO {} (phase)
#     VALUES (?)
# """.format("phase_option")
# my_data = ("Phase T",)
# cursor.execute(insert_query, my_data)

# conn.commit()
# conn.close()
# sqlite_read_table("voltage_option")

# conn.close()

sqlite_list_all_table()