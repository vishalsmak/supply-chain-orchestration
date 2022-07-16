import os
import pika

class EventQueue:
    queue_service_name = 'SCM_QUEUE_SERVICE'
    queue_service_protocol = 'AMQP'
    queue_host_var_name = f'{queue_service_name}_HOST'
    queue_port_var_name = f'{queue_service_name}_PORT_{queue_service_protocol}'
    queue_name = 'scm-intake'

    def __init__(self):
        try:
            self.queue_host = os.environ.get(self.queue_host_var_name, 'localhost')
            self.queue_port = os.environ.get(self.queue_port_var_name, 5672)
            print(f'Connecting to Event Queue on : {self.queue_host}:{self.queue_port}')
            connection_parms = pika.ConnectionParameters(self.queue_host, self.queue_port, heartbeat=36000)
            self.connection = pika.BlockingConnection(connection_parms)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name)
        except Exception as e:
            print (f"Failed to connect to event queue : {e}")

    def __del__(self):
        try:
            self.connection.close()
        except Exception as e:
            print (f"Failed to disconnect from event queue : {e}")

    def publish(self, event_data):
        try:
            print(f"attempting to post {event_data}")
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=event_data)
            print("posted data to event queue")
        except Exception as e:
            print (f"Failed to post data to event queue : {e}")

    def subscribe(self, on_message):
        try:
            print("starting to subscribe to event queue")
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=on_message, auto_ack=True)
            self.channel.start_consuming()
        except Exception as e:
            print (f"Failed to subscribe to event queue : {e}")