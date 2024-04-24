#!/bin/bash

sudo -u jenkins kubectl delete service user-service
sudo -u jenkins kubectl delete service product-service
sudo -u jenkins kubectl delete service order-service
sudo -u jenkins kubectl delete service review-service
sudo -u jenkins kubectl delete service frontend-service

sudo -u jenkins kubectl delete deployment user-deployment
sudo -u jenkins kubectl delete deployment product-deployment
sudo -u jenkins kubectl delete deployment order-deployment
sudo -u jenkins kubectl delete deployment review-deployment
sudo -u jenkins kubectl delete deployment frontend-deployment

# docker rmi akshar0909/cc-backend-user:1.0
# docker rmi akshar0909/cc-backend-product:1.0
# docker rmi akshar0909/cc-backend-order:1.0
# docker rmi akshar0909/cc-backend-review:1.0
# docker rmi akshar0909/cc-frontend:1.0

# docker rmi cc-backend-user:1.0
# docker rmi cc-backend-product:1.0
# docker rmi cc-backend-order:1.0
# docker rmi cc-backend-review:1.0
# docker rmi cc-frontend:1.0
