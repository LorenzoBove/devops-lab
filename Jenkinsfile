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

                    echo "Operating system:"
                    uname -a

                    echo "Python:"
                    python3 --version || true

                    echo "Pip:"
                    pip3 --version || true

                    echo "Docker:"
                    docker --version || true
                '''
            }
        }
    }
}
