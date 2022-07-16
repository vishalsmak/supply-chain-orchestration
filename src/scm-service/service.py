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
    event_file_name = os.path.join(os.path.dirname(__file__), 'events.txt')
    print(f"attempting to write all queue events to file {event_file_name}")
    event_file = open(event_file_name, 'a')
except Exception as e:
    print (f"Failed to start service : {e}")

def des():
    try:
        event_file.close()
    except Exception as e:
        print (f"Failed to stop service : {e}")

def on_message(ch, method, properties, body):
    print (f'Got message {body}')
    event_file.write(f'{body}\n')
    event_file.flush()
    database.save(body)

def start_subscribe():
    try:
        queue.subscribe(on_message = on_message)
    except Exception as e:
        print (f"ending subscription : {e}")

if __name__ == '__main__':
    start_subscribe()
    des()