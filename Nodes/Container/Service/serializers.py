#
# Copyright (C) 2015. Jefferson Lab, Clara framework (JLAB). All Rights Reserved.
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

from rest_framework import serializers

from models import ServiceEngine


class ServiceEngineSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceEngine
        fields = ('service_id', 'container', 'engine_name', 'class_name',
                  'author', 'version', 'language', 'description',)
        read_only_fields = ('service_id', 'container',)


class ServiceEngineNestedSerializer(serializers.ModelSerializer):
    parent_id = None
    parent_dpe_id = None
    
    def __init__(self, *args, **kwargs):
        self.parent_id = kwargs.pop('container', None)
        super(ServiceEngineNestedSerializer, self).__init__(*args, **kwargs)
    
    class Meta:
        model = ServiceEngine
        fields = ('container', 'engine_name', 'class_name', 'author',
                  'version', 'language', 'description',)
        read_only_fields = ('container',)
        
    def create(self, validated_data):
        service = ServiceEngine(engine_name=validated_data['engine_name'],
                                class_name=validated_data['class_name'],
                                author=validated_data['author'],
                                version=validated_data['version'],
                                language=validated_data['language'],
                                description=validated_data['description'],)    
        return service
