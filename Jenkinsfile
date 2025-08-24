pipeline {
  agent any
  environment {
    REGISTRY = "docker.io"
    IMAGE    = "uriya07/rnm-api"
    TAG      = "${env.BUILD_NUMBER}"
    RELEASE  = "rnm-api"
    NAMESPACE = "rnm"
    CHART_PATH = "helm/rnm-api" // התאם לנתיב הצ׳ארט אצלך
  }
  options { timestamps() }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Build & Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'DOCKERHUB_CREDS', usernameVariable: 'DU', passwordVariable: 'DP')]) {
          sh '''
            echo "$DP" | docker login -u "$DU" --password-stdin
            docker build -t $IMAGE:$TAG .
            docker tag $IMAGE:$TAG $REGISTRY/$IMAGE:$TAG
            docker push $REGISTRY/$IMAGE:$TAG
          '''
        }
      }
    }
    stage('Deploy (Helm)') {
      steps {
        sh '''
          export KUBECONFIG=/root/.kube/config
          kubectl create ns $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
          helm upgrade -i $RELEASE $CHART_PATH \
            -n $NAMESPACE \
            --set image.repository=$REGISTRY/$IMAGE \
            --set image.tag=$TAG \
            --wait --timeout 5m
          kubectl get pods -n $NAMESPACE -o wide
        '''
      }
    }
  }
}

