pipeline {
    agent { docker { image 'docker' } }
    stages {
        stage('test') {
            steps {
                sh 'echo test start'
                sh 'docker run hello-world'
                sh 'echo test stop'
            }
        }
    }
}