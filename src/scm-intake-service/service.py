import os, sys

# import file from sibling directory
api_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.dirname(api_dir)
queue_dir = os.path.join(app_dir, 'scm-queue')
db_dir = os.path.join(app_dir, 'scm-db')
sys.path.append(queue_dir)
sys.path.append(db_dir)
from EventQueue import EventQueue
from Database import Database

try:
    queue = EventQueue()
    database = Database()
except Exception as e:
    print (f"Failed to start service : {e}")

def on_message(ch, method, properties, body):
    database.save(body)

def start_subscribe():
    try:
        queue.subscribe(on_message = on_message)
    except Exception as e:
        print (f"ending subscription : {e}")

if __name__ == '__main__':
    start_subscribe()