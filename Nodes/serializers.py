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

from django.core.exceptions import ValidationError
from rest_framework import serializers

from utils.Validators import limit_validator
from Nodes.models import Node


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = ('node_id', 'hostname', 'language', 'canonical_name',
                  'created', 'modified')
        write_only_fields = ('hostname', 'language')
        read_only_fields = ('node_id', 'created', 'modified',
                            'canonical_name')

    def create(self, validated_data):
        # TODO: Need to rethink about parameters for creation.
        # TODO: Figure who is in charge of assign the DPE Resources
        node = Node(hostname=validated_data['hostname'],
                    language=validated_data['language'])
        node.save()
        return node


class NodeDeployerSerializer(serializers.Serializer):
    # TODO: Maybe we should think about bounds?
    DPEInfo = serializers.IntegerField(default=1, validators=[limit_validator])
    hostname = serializers.CharField(max_length=40)
