#!/bin/bash

kubectl delete service user-service
kubectl delete service product-service
kubectl delete service order-service
kubectl delete service review-service
kubectl delete service frontend-service

kubectl delete deployment user-deployment
kubectl delete deployment product-deployment
kubectl delete deployment order-deployment
kubectl delete deployment review-deployment
kubectl delete deployment frontend-deployment

docker rmi akshar0909/cc-backend-user:1.0
docker rmi akshar0909/cc-backend-product:1.0
docker rmi akshar0909/cc-backend-order:1.0
docker rmi akshar0909/cc-backend-review:1.0
docker rmi akshar0909/cc-frontend:1.0

docker rmi cc-backend-user:1.0
docker rmi cc-backend-product:1.0
docker rmi cc-backend-order:1.0
docker rmi cc-backend-review:1.0
docker rmi cc-frontend:1.0
