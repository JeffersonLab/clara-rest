#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo Oyarzun
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#
import simplejson as json
from math import floor
from urllib2 import urlopen, HTTPError

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response

from Nodes.models import Node

D_URL = '/dpes/'
C_URL = '/containers/'
S_URL = '/services/'
JSON_SUFFIX = '?format=json'
JSONR_SUFFIX = '?format=json&runtime=all'


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer,))
def DpeList(request, format=None):
    data = {'nodes': Node.objects.all()}
    return Response(data, template_name='dpe/dpes.html')


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer,))
def DpeDetail(request, DPE_id, format=None):
    try:
        dpe_reg_url = "http://" + request.get_host() + D_URL + DPE_id
        dpe_run_url = dpe_reg_url + JSONR_SUFFIX
        con_reg_url = dpe_reg_url + C_URL

        d_reg_data = json.load(urlopen(dpe_reg_url))
        d_run_data = json.load(urlopen(dpe_run_url))
        c_reg_data = json.load(urlopen(con_reg_url))

        dpe_name = d_reg_data['hostname'] + "_" + d_reg_data['language']
        cpu_ratio = float(d_run_data['cpu_usage'])*100
        mem_size = 32000# int(d_reg_data['memory_size'])
        mem_usage = d_run_data['memory_usage']
        mem_ratio = (mem_size/mem_usage)*100

        data = {'dpe_name': dpe_name,
                'dpe_id': d_reg_data['node_id'],
                'cpu_ratio': cpu_ratio,
                'mem_ratio': mem_ratio,
                'mem_size': mem_size,
                'mem_usage': mem_usage,
                'containers': c_reg_data}

        return render_to_response('dpe/dpe.html', data)

    except HTTPError:
        return HttpResponseNotFound()


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer,))
def ServiceDetail(request, DPE_id, cont_id, service_id, format=None):
    try:
        dpe_reg_url = "http://" + request.get_host() + D_URL + DPE_id
        con_reg_url = dpe_reg_url + C_URL
        ser_reg_url = con_reg_url + cont_id + S_URL + service_id
        ser_run_url = ser_reg_url + JSONR_SUFFIX

        d_reg_data = json.load(urlopen(dpe_reg_url))
        c_reg_data = json.load(urlopen(con_reg_url))
        s_reg_data = json.load(urlopen(ser_reg_url))
        s_run_data = json.load(urlopen(ser_run_url))

        dpe_name = d_reg_data['hostname'] + "_" + d_reg_data['language']
#         cpu_ratio = float(d_run_data['cpu_usage'])
        mem_size = int(d_reg_data['memory_size'])
#         mem_usage = d_run_data['mem_usage']
#         mem_ratio = floor(mem_size/mem_usage)

        data = {'dpe_name': dpe_name,
                'dpe_id': d_reg_data['node_id'],
                'container_id': cont_id,
                'service_id': service_id,
                'service_run': s_run_data,
                'service_name': s_reg_data['engine_name'],
                'service_class_name': s_reg_data['class_name'],
                'author': s_reg_data['engine_name'],
                'service_reg': s_reg_data}

        return render_to_response('service/service.html', data)

    except HTTPError:
        return HttpResponseNotFound()
