
# Horizontal Pod Autoscaler (HPA) – Quick Guide

This document explains how HPA is configured for the `rnm-api` service and how to test scaling on Minikube.

---

## 1) Why HPA?
HPA automatically changes the number of Pods in a Deployment based on CPU utilization.  
Benefits: scalability during high load, cost/efficiency when idle, and improved availability.

---

## 2) Prerequisites
- Deployment has CPU requests/limits (so HPA can compute % utilization):
  ```yaml
  resources:
    requests:
      cpu: "100m"
      memory: "128Mi"
    limits:
      cpu: "500m"
      memory: "256Mi"
  ```
- Metrics Server enabled in Minikube:
  ```bash
  minikube addons enable metrics-server
  kubectl -n kube-system rollout status deploy/metrics-server
  ```

---

## 3) HPA Manifest
Create `k8s/hpa.yaml` with:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: rnm-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: rnm-api
  minReplicas: 2
  maxReplicas: 6
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```
Apply:
```bash
kubectl apply -f k8s/hpa.yaml
kubectl get hpa
```

---

## 4) Testing autoscaling
The default endpoints are mostly I/O-bound. Add a CPU endpoint to `main.py`:

```python
import time
from fastapi import Query

@app.get("/burn")
def burn(ms: int = Query(200, ge=1, le=20000)):
    end = time.perf_counter() + (ms / 1000.0)
    x = 0
    while time.perf_counter() < end:
        x = (x * 1664525 + 1013904223) % 2**32
    return {"burn_ms": ms, "checksum": x}
```

Rebuild & restart inside Minikube:
```bash
eval $(minikube docker-env)
docker build -t rnm-api:latest .
kubectl rollout restart deployment/rnm-api
kubectl rollout status deployment/rnm-api
```

Generate load (60s, 20 concurrent):
```bash
kubectl run hey --image=ghcr.io/rakyll/hey --restart=Never --   -z 60s -c 20 http://rnm-api:8000/burn?ms=200
```

Observe scaling:
```bash
watch -n 2 kubectl get hpa,deploy,po -l app=rnm-api
kubectl top pods -l app=rnm-api
```

Expected:
- HPA `TARGETS` rises above 50%.
- Deployment `REPLICAS` increases (up to 6).
- After the load pod is deleted, it scales down to 2.

---

## 5) Cleanup
```bash
kubectl delete pod hey --ignore-not-found
kubectl delete hpa rnm-api --ignore-not-found
```

---

## Notes
- For production (EKS), you can keep the same HPA manifest and use CloudWatch + Metrics Server or Prometheus.
- You can also autoscale on memory or custom metrics with `autoscaling/v2`.
