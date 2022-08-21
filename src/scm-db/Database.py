import os, pymongo

class Database:
    db_service_name = 'SCM_DB_SERVICE'
    db_host_var_name = f'{db_service_name}_HOST'
    db_port_var_name = f'{db_service_name}_PORT'
    db_username = 'smak'
    db_password = 'smak'
    db_name = 'scm-database'

    def __init__(self):
        try:
            self.db_host = os.environ.get(self.db_host_var_name, 'localhost')
            self.db_port = os.environ.get(self.db_port_var_name, 27017)
            self.connection_string = f'mongodb://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}'
            print(f'Connecting to mongo db using : {self.connection_string}')
            self.client = pymongo.MongoClient(self.connection_string)
            self.db = self.client["scm-db"]
            self.category_collection = self.db["category_collection"]
            self.dropped_collection = self.db["dropped_collection"]
            self.delivery_rist_collection = self.db["risk_collection"]
        except Exception as e:
            print (f"Failed to connect to mongo db : {e}")
    
    def __del__(self):
        try:
            self.client.close()
        except Exception as e:
            print (f"Failed to disconnect from mongo db : {e}")

    def save_category_list(self, data):
        try:
            self.category_collection.insert_many(data)
        except Exception as e:
            print (f"Failed to save to mongo db : {e}")
    
    def save_dropped_data(self, data):
        try:
            self.dropped_collection.insert_many(data)
        except Exception as e:
            print (f"Failed to save to mongo db : {e}")

    def save_delivery_risk_mean(self, data):
        try:
            self.delivery_rist_collection.inset_many(data)
        except Exception as e:
            print (f"Failed to save to mongo db : {e}")

    def fetch(self):
        try:
            return list(self.category_collection.find())
        except Exception as e:
            print (f"Failed to read from mongo db : {e}")
            return str(e)