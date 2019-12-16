#!/bin/bash
## Delete AWS loadsmart stack
echo "Delete stack..."
aws cloudformation delete-stack \
--region sa-east-1 \
--stack-name tst-loadsmart 

aws cloudformation wait stack-delete-complete \
--region sa-east-1 \
--stack-name tst-loadsmart 

## Delete key pair
echo "Delete key pair..."
aws ec2 delete-key-pair \
--region sa-east-1 \
--key-name loadsmart-key 

## Delete bucket
echo "Delete bucket.."
aws s3 rm s3://loadsmart-app-bucket \
--region sa-east-1 \
--recursive 

aws s3api delete-bucket \
--bucket loadsmart-app-bucket \
--region sa-east-1 

echo "done!"
