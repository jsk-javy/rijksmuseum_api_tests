pipeline {
    agent any

    environment {
        // Specify Python version or virtual environment
        VENV_DIR = "p312env"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Install dependencies if needed
                script {
                    if (!fileExists("${VENV_DIR}/bin/activate")) {
                        sh "python3 -m venv ${VENV_DIR}"
                    }
                    sh """
                    . ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt || echo "requirements.txt not found, skipping..."
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                // Run pytest and output results in JUnit XML format
                script {
                    sh """
                    . ${VENV_DIR}/bin/activate
                    pytest --junitxml=report.xml
                    """
                }
            }
        }

        stage('Publish Test Report') {
            steps {
                // Publish the JUnit test report
                junit 'report.xml'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/report.xml', allowEmptyArchive: true
        }
        cleanup {
            cleanWs()
        }
    }
}
