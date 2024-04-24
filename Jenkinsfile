pipeline {
    agent any

    environment {
        KUBECONFIG = '/home/abhayjo/.kube/config'
    }

    stages {
        stage('Clone') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/joshi']],
                    userRemoteConfigs: [[url: 'https://github.com/Abhay-N-J/YaEC']]
                ])
            }
        }

        stage('Build') {
            steps {
                script {
                    dir('user-management') {
                        sh "docker build -t cc-backend-user:latest ."
                        sh "docker tag cc-backend-user:latest abhayjo/cc-backend-user:latest"
                    }
                    dir('product-management') {
                        sh "docker build -t cc-backend-product:latest ."
                        sh "docker tag cc-backend-product:latest abhayjo/cc-backend-product:latest"
                    }
                    dir('order-management') {
                        sh "docker build -t cc-backend-order:latest ."
                        sh "docker tag cc-backend-order:latest abhayjo/cc-backend-order:latest"
                    }
                    dir('review-management') {
                        sh "docker build -t cc-backend-review:latest ."
                        sh "docker tag cc-backend-review:latest abhayjo/cc-backend-review:latest"
                    }
                    dir('frontend') {
                        sh "docker build -t cc-frontend:latest ."
                        sh "docker tag cc-frontend:latest abhayjo/cc-frontend:latest"
                    }
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    sh """sudo -u jenkins docker images | awk '$1 != "python" && $1 != "gcr.io/k8s-minikube/kicbase" {print $3}' | xargs -r sudo -u jenkins docker rmi -f """

                    dir('user-management') {
                        withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                            def registry_url = "docker.io"
                            sh "echo '${PASSWORD}' | docker login --username '${USER}' --password-stdin"
                            sh "docker push abhayjo/cc-backend-user:latest"
                        }
                    }
                    dir('product-management') {
                        withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                            def registry_url = "docker.io"
                            sh "echo '${PASSWORD}' | docker login --username '${USER}' --password-stdin"
                            sh "docker push abhayjo/cc-backend-product:latest"
                        }
                    }
                    dir('order-management') {
                        withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                            def registry_url = "docker.io"
                            sh "echo '${PASSWORD}' | docker login --username '${USER}' --password-stdin"
                            sh "docker push abhayjo/cc-backend-order:latest"
                        }
                    }
                    dir('review-management') {
                        withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                            def registry_url = "docker.io"
                            sh "echo '${PASSWORD}' | docker login --username '${USER}' --password-stdin"
                            sh "docker push abhayjo/cc-backend-review:latest"
                        }
                    }
                    dir('frontend') {
                        withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                            def registry_url = "docker.io"
                            sh "echo '${PASSWORD}' | docker login --username '${USER}' --password-stdin"
                            sh "docker push abhayjo/cc-frontend:latest"
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh """
                    sudo -u jenkins kubectl version
                    sudo -u jenkins kubectl apply -f ./mongodb/db-deployment.yaml --context minikube
                    sudo -u jenkins kubectl apply -f ./user-management/user-deployment.yaml --context minikube
                    sudo -u jenkins kubectl apply -f ./product-management/product-deployment.yaml --context minikube
                    sudo -u jenkins kubectl apply -f ./order-management/order-deployment.yaml --context minikube
                    sudo -u jenkins kubectl apply -f ./review-management/review-deployment.yaml --context minikube
                    sudo -u jenkins kubectl apply -f ./frontend/frontend-deployment.yaml --context minikube
                    sudo -u jenkins kubectl apply -f ./mongodb/db-service.yaml --context minikube
                    sudo -u jenkins kubectl apply -f ./user-management/user-service.yaml --context minikube
                    sudo -u jenkins kubectl apply -f ./product-management/product-service.yaml --context minikube
                    sudo -u jenkins kubectl apply -f ./order-management/order-service.yaml --context minikube
                    sudo -u jenkins kubectl apply -f ./review-management/review-service.yaml --context minikube
                    sudo -u jenkins kubectl apply -f ./frontend/frontend-service.yaml --context minikube
                    """
                }
            }
        }
        stage('Expose Service') {
            steps {
                script {
                    sh "sudo -u jenkins minikube tunnel &"
                    sleep 10

                    def frontendIP = sh(script: "sudo -u jenkins kubectl get svc frontend-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'", returnStdout: true).trim()

                    if (frontendIP) {
                        echo "External IP of frontend service: ${frontendIP}"
                        // sh "sudo -u jenkins ngrok http ${frontendIP}:8004 &"
                    } else {
                        echo "Error: External IP of frontend service not found"
                    }
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
