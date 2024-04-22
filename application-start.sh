#!/bin/bash

docker build -t cc-backend-user:1.0 ./user-management
docker build -t cc-backend-product:1.0 ./product-management
docker build -t cc-backend-order:1.0 ./order-management
docker build -t cc-backend-review:1.0 ./review-management
docker build -t cc-frontend:1.0 ./frontend

docker tag cc-backend-user:1.0 akshar0909/cc-backend-user:1.0
docker tag cc-backend-product:1.0 akshar0909/cc-backend-product:1.0
docker tag cc-backend-order:1.0 akshar0909/cc-backend-order:1.0
docker tag cc-backend-review:1.0 akshar0909/cc-backend-review:1.0
docker tag cc-frontend:1.0 akshar0909/cc-frontend:1.0

docker push akshar0909/cc-backend-user:1.0
docker push akshar0909/cc-backend-product:1.0
docker push akshar0909/cc-backend-order:1.0
docker push akshar0909/cc-backend-review:1.0
docker push akshar0909/cc-frontend:1.0


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