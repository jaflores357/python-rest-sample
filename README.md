# APP

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

**EnvironmentTag**: Tag fo environment 

**SetupTag**: Tag of application

**KeyName**: The key used to access the machines

**InstanceType**: The instance type used to create the ec2 instances

**S3Bucket**: Bucket name that contain the application 

**S3Key**: The application in ZIP format

**SNSEmail**: Emails used to receive the alerts

**SSHLocation**: IP address to allow SSH to ec2 instances

**LatestAmiId**: AMI ID used to create the ec2 instances 

**VpcNet**: Network range of VPC

**CidrBlockPublicSubnet1A**: Network range of public subnet


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

