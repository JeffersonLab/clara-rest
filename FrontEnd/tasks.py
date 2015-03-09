'''
Created on 06-03-2015

@author: royarzun
'''
from ClaraWebREST import celery_app
from src.sys.Dpe import Dpe
from time import sleep


def get_task_status(task_id):

    # If you have a task_id, this is how you query that task 
    task = StartNodeDPETask.AsyncResult(task_id)
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
def StartNodeDPETask(message):
    print "FrontEnd about to be deployed"
    StartNodeDPETask.update_state(state='PROGRESS', meta={'progress': 0})
    try:
        DPE_node = Dpe()
        DPE_node.start()
    except ValueError:
        print "Oopsss..... Seems like the ip has been already taken"
        pass
        
    print "FrontEnd has been deployed"
    StartNodeDPETask.update_state(state='SUCCESS', meta={'progress': 100})
    sleep(100)
    return "Servicio Lanzado"
    