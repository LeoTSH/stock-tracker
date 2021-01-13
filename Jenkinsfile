pipeline {
    agent any
    stages {
        stage('test') {
            steps {
                sh 'echo stage test start'
                sh 'airflow dags backfill test_dag --start-date 2021-01-10 --end-date 2021-01-13'
                sh 'echo stage test stop'
            }
        }
    }
}