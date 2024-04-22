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
                    withCredentials([file(credentialsId: 'kubernetes-credentials', variable: 'KUBECONFIG_PATH')]) {
                        sh "kubectl --kubeconfig=${KUBECONFIG_PATH} apply -f ./user-management/user-deployment.yaml"
                        sh "kubectl --kubeconfig=${KUBECONFIG_PATH} apply -f ./mongodb/db-deployment.yaml"
                        sh "kubectl --kubeconfig=${KUBECONFIG_PATH} apply -f ./product-management/product-deployment.yaml"
                        sh "kubectl --kubeconfig=${KUBECONFIG_PATH} apply -f ./order-management/order-deployment.yaml"
                        sh "kubectl --kubeconfig=${KUBECONFIG_PATH} apply -f ./review-management/review-deployment.yaml"
                        sh "kubectl --kubeconfig=${KUBECONFIG_PATH} apply -f ./frontend/frontend-deployment.yaml"

                        sh "kubectl --kubeconfig=${KUBECONFIG_PATH} apply -f ./mongodb/db-service.yaml"
                        sh "kubectl --kubeconfig=${KUBECONFIG_PATH} apply -f ./user-management/user-service.yaml"
                        sh "kubectl --kubeconfig=${KUBECONFIG_PATH} apply -f ./product-management/product-service.yaml"
                        sh "kubectl --kubeconfig=${KUBECONFIG_PATH} apply -f ./order-management/order-service.yaml"
                        sh "kubectl --kubeconfig=${KUBECONFIG_PATH} apply -f ./review-management/review-service.yaml"
                        sh "kubectl --kubeconfig=${KUBECONFIG_PATH} apply -f ./frontend/frontend-service.yaml"
                    }
                }
            }
        }
    }
}
