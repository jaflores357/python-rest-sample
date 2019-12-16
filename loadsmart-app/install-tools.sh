#!/bin/bash

## Install python3 and pip
yum -y install python3
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

## Install Tox - test tool
python3 -m pip install tox

## Install Locust - load tool
python3 -m pip install locust