pipeline {
    agent any

    environment {
        CI_NETWORK = 'devops-lab-ci'
        MONGO_CONTAINER = 'devops-lab-mongodb-ci'
    }

    stages {

        stage('Environment') {
            steps {
                echo 'Checking Jenkins execution environment'

                sh '''
                    echo "Current directory:"
                    pwd

                    echo "User:"
                    whoami

                    echo "Docker:"
                    docker --version
                '''
            }
        }

        stage('Start MongoDB') {
            steps {
                echo 'Creating CI Docker network and starting MongoDB'

                sh '''
                    docker rm -f $MONGO_CONTAINER 2>/dev/null || true
                    docker network rm $CI_NETWORK 2>/dev/null || true

                    docker network create $CI_NETWORK

                    docker run -d \
                        --name $MONGO_CONTAINER \
                        --network $CI_NETWORK \
                        mongo:7
                '''
            }
        }

        stage('Tests') {
            agent {
                docker {
                    image 'python:3.11-slim'

                    args '--network devops-lab-ci'
                }
            }

            environment {
                MONGODB_URL = 'mongodb://devops-lab-mongodb-ci:27017'
                MONGODB_DATABASE = 'devops_lab_test'
            }

            steps {

                echo 'Creating Python virtual environment'

                sh '''
                    python --version

                    python -m venv .venv

                    .venv/bin/python -m pip install --upgrade pip

                    .venv/bin/pip install \
                        --no-cache-dir \
                        -r requirements.txt
                '''

                echo 'Running pytest'

                sh '''
                    .venv/bin/pytest -v
                '''
            }
        }
    }

    post {

        always {
            echo 'Cleaning CI environment'

            sh '''
                docker rm -f $MONGO_CONTAINER 2>/dev/null || true
                docker network rm $CI_NETWORK 2>/dev/null || true
            '''
        }

        success {
            echo 'Pipeline completed successfully'
        }

        failure {
            echo 'Pipeline failed'
        }
    }
}