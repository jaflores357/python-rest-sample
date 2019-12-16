#!/bin/bash
## Create key pair
echo "Create key pair..."
aws ec2 create-key-pair \
--region sa-east-1 \
--key-name loadsmart-key \
--query 'KeyMaterial' \
--output text > ~/.ssh/loadsmart-key

chmod 600 ~/.ssh/loadsmart-key
 
## Create bucket 
echo "Create bucket..."
aws s3api create-bucket \
--bucket loadsmart-app-bucket \
--region sa-east-1 \
--create-bucket-configuration LocationConstraint=sa-east-1

## Send app to s3
echo "Upload loadsmart-app..."
cd loadsmart-app && zip -r ../loadsmart-app.1.zip . && cd ..
aws s3 cp loadsmart-app.1.zip s3://loadsmart-app-bucket/

## Create AWS loadsmart stack
echo "Create stack..."
aws cloudformation create-stack \
--region sa-east-1 \
--stack-name tst-loadsmart \
--template-body file://cf-loadsmart-app.yaml \
--parameters file://parameters.json \
--capabilities CAPABILITY_NAMED_IAM

aws cloudformation wait  stack-create-complete \
--region sa-east-1 \
--stack-name tst-loadsmart

echo "Describe stack..."
aws cloudformation describe-stacks \
--region sa-east-1 \
--stack-name tst-loadsmart 
