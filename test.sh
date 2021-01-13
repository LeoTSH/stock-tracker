#!/bin/bash

# SRC="937fae72dc8a:/var/jenkins_home/workspace/Testing pipeline/test_dag.py"
SRC="/var/jenkins_home/workspace/Testing pipeline/test_dag.py"
echo ${SRC}
cp ${SRC} /var/airflow/dags
# docker cp "${SRC}" /var