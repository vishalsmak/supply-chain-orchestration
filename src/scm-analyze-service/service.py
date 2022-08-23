import os, sys

# import file from sibling directory
api_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.dirname(api_dir)
queue_dir = os.path.join(app_dir, 'scm-queue')
db_dir = os.path.join(app_dir, 'scm-db')
cmn_dir = os.path.join(app_dir, 'scm-common')
sys.path.append(queue_dir)
sys.path.append(db_dir)
sys.path.append(cmn_dir)
from EventQueue import EventQueue
from Database import Database
from UploadDir import get_upload_dir
from extractor import DataExtractor

queue = None
upload_folder = None
database = None

def on_message(ch, method, properties, body):
    try:
        process_file(os.path.join(upload_folder, body.decode('utf-8')))
    except Exception as e:
        print (f"Failure while handling event : {str(e)}")

def process_file(filename):
    de = DataExtractor(os.path.join(upload_folder, filename))
    database.save_category_list(de.get_category_list())
    database.save_dropped_data(de.get_dropped_data().to_dict('records'))
    database.save_delivery_risk_mean(de.get_delivery_risk_mean().to_dict('records'))

if __name__ == '__main__':
    try:
        queue = EventQueue()
        upload_folder = get_upload_dir()
        database = Database()
        queue.subscribe(on_message = on_message)
    except Exception as e:
        print (f"Failure in service : {e}")