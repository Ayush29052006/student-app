pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Ayush29052006/student-app.git'
            }
        }

        stage('Build and Test') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pytest
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t kanadeayush29/studentapp:${BUILD_NUMBER} ."
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh "docker push kanadeayush29/studentapp:${BUILD_NUMBER}"
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                sed -i "s|studentapp:v1|studentapp:${BUILD_NUMBER}|" k8s/deployment.yaml
                kubectl apply -f k8s/
                kubectl rollout status deployment/studentapp-deployment
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                kubectl get pods
                kubectl get deployment
                kubectl get svc
                '''
            }
        }
    }
}
