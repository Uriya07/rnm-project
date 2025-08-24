# Rick & Morty Characters Filter - DevOps Project

## Project Goal
This project connects to the public [Rick & Morty API](https://rickandmortyapi.com/), fetches characters, filters them based on specific conditions, and outputs the result into a CSV file.  
Later, the project was containerized with Docker, deployed locally with Minikube (Kubernetes), and automated using GitHub Actions CI/CD.

---

## Filter Conditions
- **species** == "Human"
- **status** == "Alive"
- **origin** contains "Earth"

---

## Output
- A CSV file (`out.csv`) with the following columns:
  - **Name**
  - **Location**
  - **Image**

---

## Steps Completed ✅
1. **Setup**
   - Installed Python and virtual environment (venv).
   - Installed the `requests` library.

2. **Core Logic**
   - Implemented data fetching from API.
   - Implemented filtering logic.
   - Implemented CSV export (`out.csv`).

3. **Dockerization**
   - Added `Dockerfile` to containerize the application.
   - Verified build and run with `docker build` & `docker run`.

4. **Kubernetes**
   - Created Kubernetes manifests (`Deployment.yaml`, `Service.yaml`, `Ingress.yaml`).
   - Deployed application locally using **Minikube**.

5. **Helm**
   - Packaged the Kubernetes manifests into a **Helm chart**.
   - Verified deployment with Helm.

6. **GitHub Actions (CI/CD)**
   - Configured GitHub Actions workflow (`.github/workflows/ci.yml`).
   - Workflow builds Docker image, pushes it to **DockerHub**, and runs tests.
   - Secrets managed in GitHub for DockerHub credentials.

---

## Current Status 📌
- Core logic complete (Fetch → Pagination → Filter → CSV).
- Docker image successfully built and pushed to DockerHub.
- Application deployed on Minikube using Kubernetes & Helm.
- GitHub Actions CI/CD workflow is live and tested.

---

## How to Run (Locally)
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python app.py
```
Result will be saved in `out.csv`.

---

## How to Run with Docker
```bash
docker build -t uriya07/myapp .
docker run uriya07/myapp
```

---

## How to Deploy on Kubernetes (Minikube)
```bash
kubectl apply -f k8s/
```

---

## How to Deploy with Helm
```bash
helm install myapp helm/
```

---

## CI/CD with GitHub Actions
- Workflow file: `.github/workflows/ci.yml`
- Runs automatically on every push to main branch.
- Steps:
  1. Checkout repository
  2. Build Docker image
  3. Push image to DockerHub
  4. Deploy/test
