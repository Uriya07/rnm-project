# Kubernetes (Minikube) Guide

This guide shows how to run the **Rick & Morty Filter API** on a local Kubernetes cluster using **Minikube**.

> All commands are intended to be run from the repository root (where `Dockerfile` and `k8s/` live).

---

## 1) Prerequisites
- Docker Desktop installed and running
- Minikube installed
- kubectl available (Minikube installs it)

Verify:
```bash
docker --version
minikube version
kubectl version --client
```

---

## 2) Start Minikube
```bash
minikube start --driver=docker
kubectl get nodes
```
You should see a single node named `minikube` in `Ready` state.

---

## 3) Build the Docker image *inside* Minikube
Minikube uses its own Docker daemon. Point your shell to it, then build:

```bash
# Use Minikube's Docker
eval $(minikube docker-env)

# Build the image for the API
docker build -t rnm-api:latest .

# Optional: confirm it's there
docker images | grep rnm-api
```

> If you forget `eval $(minikube docker-env)` the cluster won't see your local image
> and Pods may fail with `ImagePullBackOff`.

---

## 4) Deploy to Kubernetes
Apply the Deployment and Service manifests:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Watch until Pods are Ready
kubectl get pods -w -l app=rnm-api   # Ctrl+C to exit
```

---

## 5) Access the service
Easiest way:
```bash
minikube service rnm-api
```
This opens a browser or prints a URL you can use (usually a localhost URL).

Useful endpoints:
- `/`          – landing JSON message
- `/health`    – health check (should return `{"ok": true}`)
- `/characters`– filtered characters as JSON
- `/csv`       – downloads `out.csv`

Alternatively, use the NodePort manually:
```bash
minikube ip
# Suppose it returns 192.168.49.2
# Then browse: http://192.168.49.2:30080/health
```

> On Windows/WSL with Docker driver, the localhost URL printed by `minikube service` is usually the most reliable.

---

## 6) Typical dev loop (code → image → rollout)
Whenever you change code:
```bash
# 1) Make sure shell points to Minikube Docker
eval $(minikube docker-env)

# 2) Rebuild image
docker build -t rnm-api:latest .

# 3) Restart rollout
kubectl rollout restart deployment/rnm-api

# 4) Wait until new Pods are Ready
kubectl rollout status deployment/rnm-api
```

---

## 7) Scaling (replicas)
Change the number of Pods on the fly:
```bash
kubectl scale deployment/rnm-api --replicas=4
kubectl get deploy rnm-api
kubectl get pods -l app=rnm-api
```

---

## 8) Logs & troubleshooting
```bash
# Logs from all Pods
kubectl logs -l app=rnm-api --tail=100

# Describe resources for details
kubectl describe deploy rnm-api
kubectl describe svc rnm-api

# Common issue: ImagePullBackOff
# Fix: rebuild image *inside* Minikube Docker and restart the rollout:
eval $(minikube docker-env)
docker build -t rnm-api:latest .
kubectl rollout restart deployment/rnm-api
kubectl rollout status deployment/rnm-api
```

---

## 9) Cleanup
```bash
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
# or remove the entire cluster:
minikube delete
```

---

## Notes
- The manifests use `readinessProbe` and `livenessProbe` on `/health` to ensure Pods are healthy.
- `Service` is `NodePort` on `30080` for easy local access.
- For production, consider using a `LoadBalancer` Service type (with `minikube tunnel`) or an Ingress.
