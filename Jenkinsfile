pipeline {
    agent any
    stages {
        stage('test') {
            steps {
                sh 'EXPORT src="937fae72dc8a:/var/jenkins_home/workspace/Testing pipeline/test_dag.py"'
                sh 'echo stage test start'
                sh 'docker cp $src ~/airflow/dags' 
                sh 'airflow dags backfill test_dag --start-date 2021-01-10 --end-date 2021-01-13'
                sh 'echo stage test stop'
            }
        }
    }
}