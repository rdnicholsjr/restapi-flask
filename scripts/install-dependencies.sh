#!/bin/bash

yum update -y && yum upgrade -y
pip install pylint
pip install flask
pip install flask-HTTPAuth
pip install flask-Cors
pip install werkzeug

