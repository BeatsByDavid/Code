import time

from celery import Celery
from flask_socketio import SocketIO

from UploadingQueries import UploadingQueries

app = Celery('bbd_tasks', backend='rpc://', borker='pyamqp://guest@localhost//')
socketio = SocketIO(message_queue='amqp:///socketio')

class CeleryTasks:

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

    def upload_new_data(**kwargs):
        CeleryTasks.upload_new_data.delay(**kwargs)
        return "OK"

    @app.task
    def upload_new_data_cel(**kwargs):
        u = UploadingQueries()
        new = u.add_data(**kwargs)
        socketio.emit('new_data', new.to_json(), '/namespace')
        print 'Added new data via celery task!'
