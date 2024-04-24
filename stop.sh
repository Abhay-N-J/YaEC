#!/bin/bash

kubectl delete service user-service
kubectl delete service product-service
kubectl delete service order-service
kubectl delete service review-service
kubectl delete service frontend-service
# kubectl delete service mongodb-service

kubectl delete deployment user-deployment
kubectl delete deployment product-deployment
kubectl delete deployment order-deployment
kubectl delete deployment review-deployment
kubectl delete deployment frontend-deployment
# kubectl delete deployment mongodb

# sudo -u jenkins kubectl delete service user-service
# sudo -u jenkins kubectl delete service product-service
# sudo -u jenkins kubectl delete service order-service
# sudo -u jenkins kubectl delete service review-service
# sudo -u jenkins kubectl delete service frontend-service
# sudo -u jenkins kubectl delete service mongodb-service

# sudo -u jenkins kubectl delete deployment user-deployment
# sudo -u jenkins kubectl delete deployment product-deployment
# sudo -u jenkins kubectl delete deployment order-deployment
# sudo -u jenkins kubectl delete deployment review-deployment
# sudo -u jenkins kubectl delete deployment frontend-deployment
# sudo -u jenkins kubectl delete deployment mongodb

docker rmi abhayjo/cc-backend-user:latest
docker rmi abhayjo/cc-backend-product:latest
docker rmi abhayjo/cc-backend-order:latest
docker rmi abhayjo/cc-backend-review:latest
docker rmi abhayjo/cc-frontend:latest

docker rmi cc-backend-user:latest
docker rmi cc-backend-product:latest
docker rmi cc-backend-order:latest
docker rmi cc-backend-review:latest
docker rmi cc-frontend:latest
