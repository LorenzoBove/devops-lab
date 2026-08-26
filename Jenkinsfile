pipeline {
    agent any

    environment {
        CI_NETWORK = 'devops-lab-ci'
        MONGO_CONTAINER = 'devops-lab-mongodb-ci'

        REGISTRY = 'ghcr.io'
        IMAGE_NAME = 'ghcr.io/lorenzobove/devops-lab-api'
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
        stage('Image Metadata') {
            steps {
                script {
                    env.GIT_SHORT_SHA = sh(
                        script: 'git rev-parse --short=7 HEAD',
                        returnStdout: true
                    ).trim()

                    env.IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_SHORT_SHA}"
                }

                sh '''
                    echo "Build number: $BUILD_NUMBER"
                    echo "Git commit:   $GIT_COMMIT"
                    echo "Short SHA:    $GIT_SHORT_SHA"
                    echo "Image tag:    $IMAGE_TAG"
                    echo "Image:        $IMAGE_NAME:$IMAGE_TAG"
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                echo 'Building FastAPI Docker image'

                sh '''
                    docker build \
                        --label org.opencontainers.image.source=https://github.com/LorenzoBove/devops-lab \
                        --label org.opencontainers.image.revision=$GIT_COMMIT \
                        -t $IMAGE_NAME:$IMAGE_TAG \
                        -t $IMAGE_NAME:sha-$GIT_SHORT_SHA \
                        -t $IMAGE_NAME:latest \
                        .
                '''
            }
        }
        stage('Login to GHCR') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-ghcr',
                        usernameVariable: 'GHCR_USERNAME',
                        passwordVariable: 'GHCR_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$GHCR_TOKEN" | \
                            docker login ghcr.io \
                            -u "$GHCR_USERNAME" \
                            --password-stdin
                    '''
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                echo 'Publishing Docker image to GHCR'

                sh '''
                    docker push $IMAGE_NAME:$IMAGE_TAG
                    docker push $IMAGE_NAME:sha-$GIT_SHORT_SHA
                    docker push $IMAGE_NAME:latest
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
                docker logout ghcr.io 2>/dev/null || true
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