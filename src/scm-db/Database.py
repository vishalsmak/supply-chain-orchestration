import os, pymongo

class Database:
    db_service_name = 'SCM_DB_SERVICE'
    db_host_var_name = f'{db_service_name}_HOST'
    db_port_var_name = f'{db_service_name}_PORT'
    db_name = 'scm-database'

    def __init__(self):
        try:
            self.db_host = os.environ.get(self.db_host_var_name, 'localhost')
            self.db_port = os.environ.get(self.db_port_var_name, 27017)
            print(f'Connecting to mongo db on : {self.db_host}:{self.db_port}')
            
        except Exception as e:
            print (f"Failed to connect to mongo db : {e}")
    
    def save(self, data):
        print('TODO')
