# Helm Chart

This chart deploys the RNM API service to Kubernetes.

## Files

- `Chart.yaml`
- `values.yaml`
- `templates/` (deployment, service, ingress)

## Quick install

```bash
# From repo root (or cd helm)
helm upgrade --install rnm-api ./helm   --namespace default --create-namespace   --set image.repository=uriya077/myapp   --set image.tag=latest
```

Verify:
```bash
kubectl get pods,svc,ing -n default
```

## Common overrides

```bash
helm upgrade --install rnm-api ./helm   --namespace default --create-namespace   --set image.repository=uriya077/myapp   --set image.tag=latest   --set service.type=ClusterIP   --set resources.limits.cpu=500m   --set resources.limits.memory=256Mi
```

If you want NodePort for quick testing:
```bash
helm upgrade --install rnm-api ./helm   --set service.type=NodePort   --set service.nodePort=30080
```

## Uninstall

```bash
helm uninstall rnm-api -n default
```

## Notes

- Ensure your Kubernetes context points to your Minikube cluster:
  ```bash
  kubectl config use-context minikube
  kubectl get nodes -o wide
  ```
- If you’re on WSL and see connection issues to `127.0.0.1:xxxx`, fix kubeconfig with your Minikube IP (see main README).

