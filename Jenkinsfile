
pipeline {
    agent any

    stages {
        stage('Git Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python, Pytest & Evidently') {
            steps {
                sh '''
                    docker run --rm \
                    --volumes-from jenkins \
                    -w "$WORKSPACE" \
                    python:3.12-slim \
                    bash -c "
                        set -e

                        echo '===== Python Environment ====='
                        python --version

                        echo '===== Checking Workspace ====='
                        ls -la
                        test -f requirements.txt

                        echo '===== Installing Dependencies ====='
                        pip install -r requirements.txt

                        mkdir -p reports data
                        rm -f data/current.csv

                        echo '===== Running Pytest ====='
                        pytest -v --junitxml=reports/test-results.xml

                        echo '===== Generating API Data ====='
                        python monitoring/generate_current.py

                        echo '===== Running Evidently Monitoring ====='
                        python -u monitoring/evidently_monitor.py

                        echo '===== Pipeline Completed ====='
                    "
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true,
                          testResults: 'reports/test-results.xml'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**',
                             allowEmptyArchive: true

            echo 'Addition MLOps Pipeline Finished'
        }
    }
}
