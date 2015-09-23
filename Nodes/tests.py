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

from mockito import *
import unittest
from rest_framework import status
from rest_framework.test import APITestCase

from claraweb.orchestrators.orchestrator import WebOrchestrator


class DPENodeTests(APITestCase):
    fixtures = ['tests/fixtures/Nodes.yaml', ]
    url = '/dpes/'
    url_del = url+'2'
    initial_data = {'DPEInfo': 2, 'hostname': '129.57.114.94',
                    'language': '_java', 'n_cores': 8}

    def test_create_node(self):
        """
        We must ensure that the DPE node instance gets created
        correctly into the database
        """
        response = self.client.post(self.url, self.initial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_node(self):
        """
        We must ensure that the DPE node instance gets deleted
        correctly into the database under delete request
        """
        response = self.client.delete(self.url_del, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrchestratorTests(unittest.TestCase):

    def setUp(self):
        self.orchestrator = WebOrchestrator()
        when(self.orchestrator.base).generic_send().thenReturn(True)

    def test_exit_dpe_returns_negative_ping(self):
        self.orchestrator.dpe_exit("some_dpe_name")

    def test_deploy_container(self):
        self.orchestrator.deploy_container("129.57.114.94_java:container_name")

    def test_remove_container(self):
        self.orchestrator.remove_container("129.57.114.94_java:container_name")
