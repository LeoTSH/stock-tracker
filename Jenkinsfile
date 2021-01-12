pipeline {
    agent { docker { image 'docker' } }
    stages {
        stage('test') {
            steps {
                sh 'docker run hello-world'
                sh 'echo done'
            }
        }
    }
}