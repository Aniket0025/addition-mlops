
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
                    -v "$WORKSPACE:/workspace" \
                    -w /workspace \
                    python:3.12-slim \
                    bash -c "
                        set -e

                        echo '===== Python Environment ====='
                        python --version

                        echo '===== Installing Dependencies ====='
                        pip install -r requirements.txt

                        mkdir -p reports data
                        rm -f data/current.csv

                        echo '===== Running Pytest ====='
                        pytest -v --junitxml=reports/test-results.xml

                        echo '===== Generating API Data ====='
                        python -c 'from fastapi.testclient import TestClient; from app.main import app; c=TestClient(app); [c.post(\"/add\", json={\"num1\": i*10, \"num2\": i*5}).raise_for_status() for i in range(1,31)]; print(\"Generated 30 API records\")'

                        echo '===== Running Evidently Monitoring ====='
                        python -u monitoring/evidently_monitor.py

                        echo '===== Pipeline Tasks Completed ====='
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
