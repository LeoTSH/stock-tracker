pipeline {
    agent { docker { image 'docker' } }
    stages {
        stage('test') {
            steps {
                sh 'echo test start'
                sh 'echo test 123'
                sh 'echo test stop'
            }
        }
    }
}