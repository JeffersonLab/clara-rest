'''
Created on 06-03-2015

@author: royarzun
'''
from ClaraWebREST import celery_app
from xsys.xMsgFE import xMsgFE
from time import sleep

@celery_app.task()
def UploadTask(message):

    # Update the state. The meta data is available in task.info dictionary
    # The meta data is useful to store relevant information to the task
    # Here we are storing the upload progress in the meta. 

    UploadTask.update_state(state='PROGRESS', meta={'progress': 0})
    sleep(30)
    UploadTask.update_state(state='PROGRESS', meta={'progress': 30})
    sleep(30)
    return message


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
    FE = xMsgFE()
    print "FrontEnd has been deployed"
    StartNodeDPETask.update_state(state='SUCCESS', meta={'progress': 100})
    sleep(100)
    return "Servicio Lanzado"
    