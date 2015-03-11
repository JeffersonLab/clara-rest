'''
Created on 06-03-2015

@author: royarzun
'''
from ClaraWebREST import celery_app
from src.sys.Dpe import Dpe
from time import sleep


def get_task_status(task_id):

    # If you have a task_id, this is how you query that task 
    task = start_node_task.AsyncResult(task_id)
    status = task.status
    progress = 0

    if status == u'SUCCESS':
        progress = 100
    elif status == u'FAILURE':
        progress = 0
    elif status == 'PROGRESS':
        progress = task.info['progress']

    return {'pid':task_id, 'status': status, 'progress': progress}

@celery_app.task()
def start_node_task(message):
    print "Node about to be deployed"
    start_node_task.update_state(state='PROGRESS', meta={'progress': 0})
    try:
        DPE_node = Dpe()
        DPE_node.start()
    except ValueError:
        print "Oopsss..... Seems like the ip has been already taken"
        start_node_task.update_state(state='FAILURE', meta={'progress': -1})
        return False
    
    print "Este el PID"
    print "..."
    start_node_task.update_state(state='SUCCESS', meta={'progress': 100})
    print "Node has been deployed (sleeping now!!!)"
    sleep(100)
    return True