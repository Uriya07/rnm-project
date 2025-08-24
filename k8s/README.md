# k8s Manifests

This folder contains raw Kubernetes manifests for running the app on a local Minikube cluster:

- `deployment.yaml`
- `service.yaml`
- `ingress.yaml` (optional but recommended with Minikube ingress addon)

## Prerequisites

- Docker Desktop or Docker Engine
- Minikube
- kubectl

## Deploy

```bash
minikube start

# On WSL/Windows users: fix kubeconfig server endpoint (first run only)
MINIKUBE_IP=$(minikube ip)
sed -Ei 's#https://127\.0\.0\.1:[0-9]+#https://'"$MINIKUBE_IP"':8443#g' "$HOME/.kube/config"

# If using ingress (recommended):
minikube addons enable ingress

# Apply resources
kubectl apply -f .
```

## Verify

```bash
kubectl get deploy,svc,ing -n default
kubectl logs deploy/rnm-api -n default
```

If you used an Ingress, obtain the Minikube IP and browse to the host configured in `ingress.yaml` (or use `curl`):
```bash
minikube ip
```

## Cleanup

```bash
kubectl delete -f .
```

## Notes

- Make sure the `image: uriya077/myapp:latest` in manifests matches your Docker Hub repository and tag.
- For NodePort service testing without ingress:
  ```bash
  kubectl get svc
  # then: curl http://$(minikube ip):<nodePort>/healthcheck
  ```
