import time

from celery import Celery
from flask_socketio import SocketIO

app = Celery('bbd_tasks', backend='rpc://', borker='pyamqp://guest@localhost//')
socketio = SocketIO(message_queue='amqp:///socketio')

class CeleryTasks():

    @app.task
    def long_task(n):
        print 'This task will take {0} seconds'.format(n)
        for i in range(n):
            print i
            time.sleep(1)

    @app.task
    def send_message(message, delay):
        print 'This task will send \'{0}\' after {1} seconds'.format(message, delay)
        for i in range(delay):
            print i
            time.sleep(1)
        socketio.emit('event', message, namespace='/namespace')
        print 'Sent: \'{0}\''.format(message)
