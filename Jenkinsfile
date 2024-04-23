pipeline {
    agent any

    environment {
        KUBECONFIG = '/home/akshar/.kube/config'
    }

    stages {
        stage('Clone') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/AKSHAR-0909/YaEC']]
                ])
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh """
                    kubectl version --kubeconfig $KUBECONFIG
                    kubectl apply -f ./mongodb/db-deployment.yaml --context minikube --kubeconfig $KUBECONFIG
                    // kubectl apply -f ./user-management/user-deployment.yaml --context minikube --kubeconfig $KUBECONFIG
                    // kubectl apply -f ./product-management/product-deployment.yaml --context minikube --kubeconfig $KUBECONFIG
                    // kubectl apply -f ./order-management/order-deployment.yaml --context minikube --kubeconfig $KUBECONFIG
                    // kubectl apply -f ./review-management/review-deployment.yaml --context minikube --kubeconfig $KUBECONFIG
                    // kubectl apply -f ./frontend/frontend-deployment.yaml --context minikube --kubeconfig $KUBECONFIG
                    // kubectl apply -f ./mongodb/db-service.yaml --context minikube --kubeconfig $KUBECONFIG
                    // kubectl apply -f ./user-management/user-service.yaml --context minikube --kubeconfig $KUBECONFIG
                    // kubectl apply -f ./product-management/product-service.yaml --context minikube --kubeconfig $KUBECONFIG
                    // kubectl apply -f ./order-management/order-service.yaml --context minikube --kubeconfig $KUBECONFIG
                    // kubectl apply -f ./review-management/review-service.yaml --context minikube --kubeconfig $KUBECONFIG
                    // kubectl apply -f ./frontend/frontend-service.yaml --context minikube --kubeconfig $KUBECONFIG
                    """
                }
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed'
        }
    }
}
