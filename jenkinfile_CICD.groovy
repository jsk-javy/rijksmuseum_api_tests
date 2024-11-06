pipeline {
    agent any

    environment {
        PYTHON_ENV = 'venv'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'master', url: '<repository-url>'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh 'python -m venv ${PYTHON_ENV}'
                sh '. ${PYTHON_ENV}/bin/activate && pip install -r requirement.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. ${PYTHON_ENV}/bin/activate && pytest Tests/'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/test-reports/*.xml', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
