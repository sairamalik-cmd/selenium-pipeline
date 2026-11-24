pipeline {
  agent any
  environment {
    IMAGE = 'lab11-site'
    NET   = 'lab11-net'
  }
  stages {
    stage('Build') {
      steps {
        sh '''
          rm -rf build && mkdir -p build
          cp -r src/* build/
          echo "Build ${BUILD_NUMBER}" > build/build.txt
        '''
      }
    }
    stage('Package') {
      steps {
        sh 'docker build -t ${IMAGE}:${BUILD_NUMBER} -t ${IMAGE}:latest .'
      }
    }
    stage('Start Staging') {
      steps {
        sh '''
          docker network create ${NET} || true
          docker rm -f lab11-staging || true
          docker run -d --name lab11-staging --network ${NET} ${IMAGE}:${BUILD_NUMBER}
          sleep 3
        '''
      }
    }
    stage('Test') {
      agent {
        docker {
          image 'selenium-test-agent'
          args '--network lab11-net --shm-size=1g -e HOME=/tmp'
          reuseNode true
        }
      }
      environment { BASE_URL = 'http://lab11-staging' }
      steps {
        sh 'pytest -v --junitxml=results.xml tests'
      }
      post {
        always {
          junit 'results.xml'
          archiveArtifacts artifacts: 'screenshot.png', allowEmptyArchive: true
        }
      }
    }
  }
  post {
    always {
      sh 'docker rm -f lab11-staging || true'
    }
  }
}
