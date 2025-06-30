from tinydb import TinyDB, Query
# /Users/deny/proty02/assets/db/app_data.db

db = TinyDB('/Users/deny/proty02/assets/db/background.json')
db.insert({'int': 1, 'char': 'a'})
db.insert({'int': 1, 'char': 'b'})