#!/bin/bash

echo "Tagging server"

docker tag inventoryserver:latest 938957839258.dkr.ecr.us-east-2.amazonaws.com/inventoryserver:latest

echo "done"

echo "Pushing server to ECR"

docker push 938957839258.dkr.ecr.us-east-2.amazonaws.com/inventoryserver:latest

echo "done"
