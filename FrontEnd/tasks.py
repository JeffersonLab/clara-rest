'''
Created on 06-03-2015

@author: royarzun
'''
from ClaraWebREST import celery_app
from src.sys.Platform import Platform
from celery.task.control import revoke
import json


def get_task_status(task_id):
    task = start_fe_task.AsyncResult(task_id)
    status = task.status
    progress = 0

    if status == u'SUCCESS':
        progress = 100
    elif status == u'FAILURE':
        progress = -1
    elif status == 'PROGRESS':
        progress = task.info['progress']

    data = json.dumps({'pid': task_id,
                       'status': status,
                       'progress': progress
                       },
                      sort_keys=True,
                      separators=(',', ': '),
                      indent=4
                      )
    return data


def revoke_task(feid):
    revoke(feid, terminate=True)


@celery_app.task()
def start_fe_task(message):
    print "FrontEnd about to be deployed"
    start_fe_task.update_state(state='PROGRESS', meta={'progress': 0})
    try:
        platform = Platform()
        platform.start()
    except ValueError:
        print "Oopsss..... Seems like the ip has been already taken"
        start_fe_task.update_state(state='FAILURE', meta={'progress': -1})
        return False

    start_fe_task.update_state(state='SUCCESS', meta={'progress': 100})
    print "FrontEnd has been deployed"
    return True
