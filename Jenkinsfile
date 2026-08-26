pipeline {
    agent any

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

        stage('Tests') {
            agent {
                docker {
                    image 'python:3.11-slim'
                }
            }

            environment {
                MONGODB_DATABASE = 'devops_lab_test'
            }

            steps {
                echo 'Creating Python virtual environment'

                sh '''
                    python --version

                    python -m venv .venv

                    .venv/bin/python -m pip install --upgrade pip

                    .venv/bin/pip install --no-cache-dir -r requirements.txt
                '''

                echo 'Running pytest'

                sh '''
                    .venv/bin/pytest -v
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }

        failure {
            echo 'Pipeline failed'
        }
    }
}