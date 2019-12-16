# Loadsmart APP

## Overview
Create an AWS environment with:
    - 1 key pair
    - 1 s3 bucket
    - 1 VPC
    - 1 public subnet 
    - 1 Auto Scalling Group 
        - create 2 instances
    - 1 Internet Gateway
    - 1 Classic loabalancer
    - 2 Alarms

* Cloudwatch Alarms

- CPU > 60% for 2 minutes: 

    When instances from ASG reach 60% for more than 2 minutes send an email to SNSEmail  (specified in parameters.json)

- Unhealthy host

    When an instance attached into balancer became unhealthy send an email to SNSEmail (specified in parameters.json)

## Requirements
AWS account with permissions
aws cli installed into local machine

## Usage

# File parameters.json

EnvironmentTag.........: Tag fo environment 
SetupTag...............: Tag of application 
KeyName................: The key used to access the machines
InstanceType...........: The instance type used to create the ec2 instances
S3Bucket...............: Bucket name that contain the application 
S3Key..................: The application in ZIP format
SNSEmail...............: Emails used to receive the alerts
SSHLocation............: IP address to allow SSH to ec2 instances
LatestAmiId............: AMI ID used to create the ec2 instances 
VpcNet.................: Network range of VPC
CidrBlockPublicSubnet1A: Network range of public subnet


# Create stack:

```
./create-stack.sh
```

# Delete stack:

```
./delete-stack.sh
```


# EC2 instances

```
aws ec2 describe-instances \
--region sa-east-1 \
--filters "Name=tag:Name,Values=spo-tst-loadsmart-app"
```

```
ssh ec2-user@<ec2 public IP> -i ~/.ssh/loadsmart-key
```


# Application:

-   After create stack you get an output like this:
    ...
    "Outputs": [
        {
            "Description": "Load Balancer DNS Name", 
            "ExportName": "LoadBalancerDNSName", 
            "OutputKey": "LoadBalancerDNSName", 
            "OutputValue": "<name>.elb.amazonaws.com"
        }
    ], 

    use OutputValue to reach the API

* Healthckeck 

```
curl -XGET http://<name>.elb.amazonaws.com/heathcheck
```

* List instances

```
curl -XGET http://<name>.elb.amazonaws.com/elb/default-elb
```

*  Remove instance from balance

```
curl -XDELETE \
-H "Content-Type: application/json" \
-d '{"instanceId": "i-0f11dd974b7379bf6"}' \
http://<name>.elb.amazonaws.com/elb/default-elb
```

* Add instance into balance

```
curl -XPOST \
-H "Content-Type: application/json" \
-d '{"instanceId": "i-0f11dd974b7379bf6"}' \
http://<name>.elb.amazonaws.com/elb/default-elb
```

# Load and unitary tests:

```
cd /opt/loadsmart-app/
./install-tools.sh
```

* Unitary testes

```
tox
```

* Load tests

```
export LOCUST_MACHINEID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
locust -f locust_files/loadsmart.py \
--no-web \
-c 30 \
-r 5 \
-t 1m \
--host http://<name>.elb.amazonaws.com/
```

- Best Result with no errors with 30 concurrent connections 

 Name                                                          # reqs      # fails     Avg     Min     Max  |  Median   req/s failures/s
--------------------------------------------------------------------------------------------------------------------------------------------
 DELETE /elb/default-elb                                          122     0(0.00%)      81      50     554  |      71    2.00    0.00
 GET /elb/default-elb                                             132     0(0.00%)     103      67     166  |      89    2.17    0.00
 POST /elb/default-elb                                            117     0(0.00%)      88      47     210  |      76    1.92    0.00
 GET /healthcheck                                                 139     0(0.00%)       5       4      14  |       5    2.28    0.00
--------------------------------------------------------------------------------------------------------------------------------------------
 Aggregated                                                       510     0(0.00%)      68       4     554  |      71    8.37    0.00

Percentage of the requests completed within given times
 Type                 Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100%
------------------------------------------------------------------------------------------------------------------------------------------------------
 DELETE               /elb/default-elb                                                  122     71     78     86     94    120    130    140    200    550    550    550
 GET                  /elb/default-elb                                                  132     90    120    130    140    150    150    160    160    170    170    170
 POST                 /elb/default-elb                                                  117     76     92    110    120    150    160    180    190    210    210    210
 GET                  /healthcheck                                                      139      5      5      5      5      6      7      9     10     14     14     14
------------------------------------------------------------------------------------------------------------------------------------------------------
 None                 Aggregated                                                        510     71     81     91    100    140    150    160    170    550    550    550

