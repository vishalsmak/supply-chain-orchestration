import os, sys, time

# import file from sibling directory
api_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.dirname(api_dir)
db_dir = os.path.join(app_dir, 'scm-db')
sys.path.append(db_dir)
from Database import Database

try:
    database = Database()
except Exception as e:
    print (f"Failed to start service : {e}")

def start_analysis():
    try:
        while(True):
            print(database.fetch())
            time.sleep(10)
    except Exception as e:
        print (f"Failed to analyze data : {e}")

if __name__ == '__main__':
    start_analysis()