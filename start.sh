#!/bin/bash

docker build -t cc-backend-user:latest ./user-management
docker build -t cc-backend-product:latest ./product-management
docker build -t cc-backend-order:latest ./order-management
docker build -t cc-backend-review:latest ./review-management
docker build -t cc-frontend:latest ./frontend

docker tag cc-backend-user:latest abhayjo/cc-backend-user:latest
docker tag cc-backend-product:latest abhayjo/cc-backend-product:latest
docker tag cc-backend-order:latest abhayjo/cc-backend-order:latest
docker tag cc-backend-review:latest abhayjo/cc-backend-review:latest
docker tag cc-frontend:latest abhayjo/cc-frontend:latest

docker push abhayjo/cc-backend-user:latest
docker push abhayjo/cc-backend-product:latest
docker push abhayjo/cc-backend-order:latest
docker push abhayjo/cc-backend-review:latest
docker push abhayjo/cc-frontend:latest


kubectl apply -f ./mongodb/db-deployment.yaml
kubectl apply -f ./user-management/user-deployment.yaml
kubectl apply -f ./product-management/product-deployment.yaml
kubectl apply -f ./order-management/order-deployment.yaml
kubectl apply -f ./review-management/review-deployment.yaml
kubectl apply -f ./frontend/frontend-deployment.yaml

kubectl apply -f ./mongodb/db-service.yaml
kubectl apply -f ./user-management/user-service.yaml
kubectl apply -f ./product-management/product-service.yaml
kubectl apply -f ./order-management/order-service.yaml
kubectl apply -f ./review-management/review-service.yaml
kubectl apply -f ./frontend/frontend-service.yaml

