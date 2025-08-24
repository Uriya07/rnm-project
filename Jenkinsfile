pipeline {
  agent any

  options {
    timestamps()
  }

  environment {
    DOCKERHUB_CREDS = credentials('dockerhub')
    IMAGE_NAME = 'uriya07/rnm-api'
    CHART_DIR  = 'helm/rnm-api'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker image') {
      steps {
        ansiColor('xterm') {
          sh '''
            docker build -t $IMAGE_NAME:$BUILD_NUMBER .
            docker tag $IMAGE_NAME:$BUILD_NUMBER $IMAGE_NAME:latest
          '''
        }
      }
    }

    stage('Login & Push') {
      steps {
        ansiColor('xterm') {
          sh '''
            echo "$DOCKERHUB_CREDS_PSW" | docker login -u "$DOCKERHUB_CREDS_USR" --password-stdin
            docker push $IMAGE_NAME:$BUILD_NUMBER
            docker push $IMAGE_NAME:latest
          '''
        }
      }
    }

    stage('Deploy to Minikube via Helm') {
      steps {
        ansiColor('xterm') {
          sh '''
            helm upgrade --install rnm-api $CHART_DIR \
              --set image.repository=$IMAGE_NAME \
              --set image.tag=$BUILD_NUMBER
          '''
        }
      }
    }
  }

  post {
    always {
      sh 'docker logout || true'
    }
  }
}

