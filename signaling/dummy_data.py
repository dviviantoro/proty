import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *
from modules.database import tinydb_read, tinydb_change_phase, tinydb_change_value
import json

print(tinydb_read("temp"))
tinydb_change_value("temp", "sensor", False)
print(tinydb_read("temp"))

# print(tinydb_read("general")[0])
# tinydb_change_phase(5)
# print(tinydb_read("general")[0])

# my_list = [[9, -3], [5, -10], [4, -10], [5, -4], [7, -1], [5, -6]]
# tinydb_append_xy("background_sampling", "ngopi", my_list)


# my_dict = {
#     'operator': 'aa',
#     'name': 'aaa',
#     'location': 'aaaaa',
#     'sensor': 'HFCT TTAT',
#     'timestamp': '2025-06-19 12:28:57',
#     'xy': [1, 2]
#     }

# serialized_dict = {}
# for field, value in my_dict.items():
#     if isinstance(value, (list, dict)):
#         # If the value is a list or dict, dump it to a JSON string
#         serialized_dict[field] = json.dumps(value)
#     else:
#         # Otherwise, use the value as is
#         serialized_dict[field] = value


#     redis_hset("dummy", serialized_dict)

# print(redis_hgetall("dummy"))