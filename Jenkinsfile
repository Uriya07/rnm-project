pipeline {
  agent any

  environment {
    // Docker Hub image name. Change to your Docker Hub username/repo.
    DOCKER_IMAGE = "uriya07/rnm-api"
    // Short git commit for tagging
    GIT_SHORT_SHA = "${env.GIT_COMMIT?.take(7)}"
    // Kubernetes namespace
    K8S_NAMESPACE = "default"
    // Helm release name (must match templates if used as app label)
    RELEASE = "rnm-api"
    // Path to the Helm chart in this repo
    CHART = "helm/rnm-api"
  }

  options {
    timestamps()
    ansiColor('xterm')
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker image') {
      steps {
        sh '''
          set -e
          docker version
          echo "Building image: $DOCKER_IMAGE:$GIT_SHORT_SHA"
          docker build -t $DOCKER_IMAGE:$GIT_SHORT_SHA .
          docker tag $DOCKER_IMAGE:$GIT_SHORT_SHA $DOCKER_IMAGE:latest
        '''
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh '''
            set -e
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push $DOCKER_IMAGE:$GIT_SHORT_SHA
            docker push $DOCKER_IMAGE:latest
          '''
        }
      }
    }

    stage('Deploy to Minikube with Helm') {
      steps {
        sh '''
          set -e
          kubectl version --client
          helm version
          kubectl config current-context

          # Deploy/upgrade with dynamic image tag
          helm upgrade --install $RELEASE $CHART \
            --namespace $K8S_NAMESPACE --create-namespace \
            --set image.repository=$DOCKER_IMAGE \
            --set image.tag=$GIT_SHORT_SHA

          echo "Waiting for rollout..."
          kubectl rollout status deploy/$RELEASE -n $K8S_NAMESPACE --timeout=120s
          echo "Services:"
          kubectl get svc -n $K8S_NAMESPACE
          echo "Pods:"
          kubectl get pods -n $K8S_NAMESPACE -l app.kubernetes.io/name=$RELEASE -o wide
        '''
      }
    }
  }

  post {
    always {
      sh 'docker logout || true'
      archiveArtifacts artifacts: '**/helm/**', onlyIfSuccessful: false
    }
  }
}
