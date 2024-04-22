pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/AKSHAR-0909/YaEC']]
                ])
            }
        }

        stage('Build') {
            steps {
                script {
                    dir('user-management') {
                        sh "docker build -t akshar0909/cc-backend-user:1.0 ."
                    }
                    dir('product-management') {
                        sh "docker build -t akshar0909/cc-backend-product:1.0 ."
                    }
                    dir('order-management') {
                        sh "docker build -t akshar0909/cc-backend-order:1.0 ."
                    }
                    dir('review-management') {
                        sh "docker build -t akshar0909/cc-backend-review:1.0 ."
                    }
                    dir('frontend') {
                        sh "docker build -t akshar0909/cc-frontend:1.0 ."
                    }
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    dir('user-management') {
                        withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                            def registry_url = "docker.io"
                            sh "docker login -u $USER -p $PASSWORD ${registry_url}"
                            sh "docker push akshar0909/cc-backend-user:1.0"
                        }
                    }
                    dir('product-management') {
                        withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                            def registry_url = "docker.io"
                            sh "docker login -u $USER -p $PASSWORD ${registry_url}"
                            sh "docker push akshar0909/cc-backend-product:1.0"
                        }
                    }
                    dir('order-management') {
                        withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                            def registry_url = "docker.io"
                            sh "docker login -u $USER -p $PASSWORD ${registry_url}"
                            sh "docker push akshar0909/cc-backend-order:1.0"
                        }
                    }
                    dir('review-management') {
                        withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                            def registry_url = "docker.io"
                            sh "docker login -u $USER -p $PASSWORD ${registry_url}"
                            sh "docker push akshar0909/cc-backend-review:1.0"
                        }
                    }
                    dir('frontend') {
                        withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                            def registry_url = "docker.io"
                            sh "docker login -u $USER -p $PASSWORD ${registry_url}"
                            sh "docker push akshar0909/cc-frontend:1.0"
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubernetes-credentials', variable: 'KUBECONFIG_FILE')]) {
                        sh """
                        echo ${KUBECONFIG_FILE}
                        export KUBECONFIG=${KUBECONFIG_FILE}
                        kubectl apply -f ./user-management/user-deployment.yaml
                        kubectl apply -f ./mongodb/db-deployment.yaml
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
                        """
                    }
                }
            }
        }

    }
}
