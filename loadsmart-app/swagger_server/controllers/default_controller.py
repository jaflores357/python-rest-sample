import connexion
import six
import boto3

from swagger_server.models.machine_id import MachineId  # noqa: E501
from swagger_server.models.machine_info import MachineInfo  # noqa: E501
from swagger_server import util


def attach_instance(elbName, machineId=None):  # noqa: E501
    """attach_instance

    Attach an instance on the load balancer # noqa: E501

    :param elbName: pass the load balancer name
    :type elbName: str
    :param machineId: instance identifier
    :type machineId: dict | bytes

    :rtype: MachineInfo
    """
    if connexion.request.is_json:
        machineId = MachineId.from_dict(connexion.request.get_json())  # noqa: E501

    client = boto3.client('elb')
    response = client.register_instances_with_load_balancer(
       LoadBalancerName=elbName,
       Instances=[
          {
            'InstanceId': machineId.instance_id
          },
       ]
    )

    return response

def elb_elb_name_delete(elbName, machineId=None):  # noqa: E501
    """elb_elb_name_delete

    Detach an instance from the load balancer # noqa: E501

    :param elbName: pass the load balancer name
    :type elbName: str
    :param machineId: instance identifier
    :type machineId: dict | bytes

    :rtype: MachineInfo
    """
    if connexion.request.is_json:
        machineId = MachineId.from_dict(connexion.request.get_json())  # noqa: E501
    
    client = boto3.client('elb')
    response = client.deregister_instances_from_load_balancer(
       LoadBalancerName=elbName,
       Instances=[
          {
            'InstanceId': machineId.instance_id
          },
       ]
    )

    return response

def healthcheck_get():  # noqa: E501
    """healthcheck_get

    API health check # noqa: E501


    :rtype: None
    """
    return 'true'


def list_machines_elb(elbName):  # noqa: E501
    """list_machines_elb

    List machines attached to a particular load balancer # noqa: E501

    :param elbName: pass the load balancer name
    :type elbName: str

    :rtype: List[MachineInfo]
    """
    client = boto3.client('elb')

    response = client.describe_load_balancers(
       LoadBalancerNames=[elbName,],
    )

    instances = []
    for instance in response['LoadBalancerDescriptions'][0]['Instances']:
       instances.append(MachineId(instance['InstanceId']))
   
    return instances

