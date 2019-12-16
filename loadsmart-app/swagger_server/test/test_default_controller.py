# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.machine_id import MachineId  # noqa: E501
from swagger_server.models.machine_info import MachineInfo  # noqa: E501
from swagger_server.test import BaseTestCase
from moto import mock_elb
import boto3


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    @mock_elb
    def create_elb(self):
        client = boto3.client('elb')
        response = client.create_load_balancer(
            LoadBalancerName='elbName',
            Listeners=[
                {
                    'Protocol': 'string',
                    'LoadBalancerPort': 123,
                    'InstanceProtocol': 'string',
                    'InstancePort': 123,
                    'SSLCertificateId': 'string'
                },
            ],
            AvailabilityZones=[
                'sa-east-1a'
            ],
            Tags=[
                {
                    'Key': 'name',
                    'Value': 'elbName'
                },
            ]
        )

    @mock_elb
    def test_attach_instance(self):
        """Test case for attach_instance

        
        """
        self.create_elb()
        machineId = MachineId('i-5203422c')
        response = self.client.open(
            '/elb/{elbName}'.format(elbName='elbName'),
            method='POST',
            data=json.dumps(machineId),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @mock_elb
    def test_elb_elb_name_delete(self):
        """Test case for elb_elb_name_delete

        
        """
        self.create_elb()
        machineId = MachineId('i-5203422c')
        response = self.client.open(
            '/elb/{elbName}'.format(elbName='elbName'),
            method='DELETE',
            data=json.dumps(machineId),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @mock_elb
    def test_healthcheck_get(self):
        """Test case for healthcheck_get

        
        """
        self.create_elb()
        response = self.client.open(
            '/healthcheck',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @mock_elb
    def test_list_machines_elb(self):
        """Test case for list_machines_elb

        
        """
        self.create_elb()
        response = self.client.open(
            '/elb/{elbName}'.format(elbName='elbName'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
