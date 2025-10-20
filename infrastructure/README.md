# Smart AI - Infrastructure

Infrastructure as Code (IaC) and deployment configurations for Smart AI.

## Overview

This directory contains:
- Kubernetes manifests for production deployment
- Docker configurations for local development
- Deployment scripts and automation
- CI/CD pipeline configurations

## Directory Structure

```
infrastructure/
├── kubernetes/             # Kubernetes manifests
│   ├── backend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── hpa.yaml
│   │   └── configmap.yaml
│   ├── database/
│   │   ├── postgresql-statefulset.yaml
│   │   ├── weaviate-statefulset.yaml
│   │   └── redis-deployment.yaml
│   ├── ingress/
│   │   ├── ingress.yaml
│   │   └── tls-secret.yaml
│   └── monitoring/
│       ├── prometheus.yaml
│       └── grafana.yaml
├── docker/
│   ├── docker-compose.dev.yml
│   ├── docker-compose.prod.yml
│   └── .env.example
└── scripts/
    ├── deploy.sh
    ├── rollback.sh
    └── health-check.sh
```

## Local Development with Docker

### Quick Start

```bash
cd infrastructure/docker

# Copy environment file
cp .env.example .env

# Start all services
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop all services
docker-compose -f docker-compose.dev.yml down
```

### Services

The development environment includes:
- PostgreSQL (port 5432)
- Weaviate (port 8080)
- Redis (port 6379)
- Adminer (port 8081) - Database management UI

### Configuration

Edit `.env` file:
```env
POSTGRES_DB=seva_ai
POSTGRES_USER=seva_user
POSTGRES_PASSWORD=seva_password

WEAVIATE_VERSION=1.22.4

REDIS_PASSWORD=redis_password
```

## Production Deployment with Kubernetes

### Prerequisites

- Kubernetes cluster (EKS, GKE, AKS, or self-hosted)
- kubectl configured
- Helm (optional, for easier deployments)

### Setup

1. **Create namespace**
   ```bash
   kubectl create namespace seva-ai
   ```

2. **Create secrets**
   ```bash
   kubectl create secret generic seva-secrets \
     --from-literal=database-url='postgresql://...' \
     --from-literal=claude-api-key='sk-...' \
     --from-literal=openai-api-key='sk-...' \
     --namespace seva-ai
   ```

3. **Deploy PostgreSQL**
   ```bash
   kubectl apply -f kubernetes/database/postgresql-statefulset.yaml
   ```

4. **Deploy Weaviate**
   ```bash
   kubectl apply -f kubernetes/database/weaviate-statefulset.yaml
   ```

5. **Deploy Backend**
   ```bash
   kubectl apply -f kubernetes/backend/
   ```

6. **Deploy Ingress**
   ```bash
   kubectl apply -f kubernetes/ingress/
   ```

### Deployment Script

Use automated deployment script:

```bash
./scripts/deploy.sh production
```

### Monitoring

Deploy monitoring stack:

```bash
kubectl apply -f kubernetes/monitoring/
```

Access Grafana:
```bash
kubectl port-forward -n seva-ai svc/grafana 3000:3000
```

## Kubernetes Manifests

### Backend Deployment

```yaml
# kubernetes/backend/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: seva-backend
  namespace: seva-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: seva-backend
  template:
    metadata:
      labels:
        app: seva-backend
    spec:
      containers:
      - name: backend
        image: seva-ai/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: seva-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Horizontal Pod Autoscaler

```yaml
# kubernetes/backend/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: seva-backend-hpa
  namespace: seva-ai
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: seva-backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### PostgreSQL StatefulSet

```yaml
# kubernetes/database/postgresql-statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql
  namespace: seva-ai
spec:
  serviceName: postgresql
  replicas: 1
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
      - name: postgresql
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: "seva_ai"
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: seva-secrets
              key: postgres-user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: seva-secrets
              key: postgres-password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 50Gi
```

## CI/CD Pipeline

### GitHub Actions

Located in `../.github/workflows/`

**Backend CI:**
```yaml
name: Backend CI

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'backend/**'
  pull_request:
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: |
          cd backend
          docker build -t seva-ai/backend:${{ github.sha }} .

      - name: Push to registry
        if: github.ref == 'refs/heads/main'
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push seva-ai/backend:${{ github.sha }}
```

**Deploy to Production:**
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Configure kubectl
        run: |
          echo ${{ secrets.KUBECONFIG }} | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/seva-backend \
            backend=seva-ai/backend:${{ github.sha }} \
            --namespace seva-ai

          kubectl rollout status deployment/seva-backend --namespace seva-ai
```

## Deployment Scripts

### Deploy Script

```bash
#!/bin/bash
# scripts/deploy.sh

set -e

ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
  echo "Usage: ./deploy.sh <environment>"
  echo "Environments: development, staging, production"
  exit 1
fi

echo "Deploying to $ENVIRONMENT..."

# Apply Kubernetes manifests
kubectl apply -f kubernetes/database/ --namespace seva-ai-$ENVIRONMENT
kubectl apply -f kubernetes/backend/ --namespace seva-ai-$ENVIRONMENT
kubectl apply -f kubernetes/ingress/ --namespace seva-ai-$ENVIRONMENT

# Wait for rollout
kubectl rollout status deployment/seva-backend --namespace seva-ai-$ENVIRONMENT

echo "Deployment complete!"
```

### Rollback Script

```bash
#!/bin/bash
# scripts/rollback.sh

set -e

ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
  echo "Usage: ./rollback.sh <environment>"
  exit 1
fi

echo "Rolling back $ENVIRONMENT deployment..."

kubectl rollout undo deployment/seva-backend --namespace seva-ai-$ENVIRONMENT

kubectl rollout status deployment/seva-backend --namespace seva-ai-$ENVIRONMENT

echo "Rollback complete!"
```

### Health Check Script

```bash
#!/bin/bash
# scripts/health-check.sh

ENVIRONMENT=$1
NAMESPACE="seva-ai-$ENVIRONMENT"

echo "Checking health of $ENVIRONMENT environment..."

# Check pod status
kubectl get pods -n $NAMESPACE

# Check backend health
kubectl exec -n $NAMESPACE deployment/seva-backend -- curl -f http://localhost:8000/health || exit 1

# Check database connection
kubectl exec -n $NAMESPACE deployment/seva-backend -- curl -f http://localhost:8000/health/ready || exit 1

echo "Health check passed!"
```

## Monitoring & Logging

### Prometheus

Scrape metrics from backend:

```yaml
# kubernetes/monitoring/prometheus.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: seva-ai
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'seva-backend'
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names:
                - seva-ai
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_label_app]
            action: keep
            regex: seva-backend
```

### Grafana Dashboards

Import dashboards for:
- API request metrics
- Database performance
- Claude API usage
- Error rates
- Resource utilization

## Security

### Network Policies

Restrict traffic between pods:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
  namespace: seva-ai
spec:
  podSelector:
    matchLabels:
      app: seva-backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgresql
    ports:
    - protocol: TCP
      port: 5432
```

### TLS Configuration

Use cert-manager for automatic certificate management:

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

## Cost Optimization

### Resource Limits

Set appropriate resource limits to avoid over-provisioning:
- Backend: 512Mi-1Gi memory, 500m-1000m CPU
- PostgreSQL: 1-2Gi memory, 500m-1000m CPU
- Weaviate: 2-4Gi memory, 1000m-2000m CPU

### Autoscaling

Use HPA to scale based on actual load, not estimated peak.

### Reserved Instances

For production, use reserved instances or savings plans for 30-40% cost reduction.

## Troubleshooting

### Pod not starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n seva-ai

# Check logs
kubectl logs <pod-name> -n seva-ai

# Check events
kubectl get events -n seva-ai --sort-by='.lastTimestamp'
```

### Service not accessible

```bash
# Check service
kubectl get svc -n seva-ai

# Test service internally
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://seva-backend:8000/health
```

### Database connection issues

```bash
# Check PostgreSQL pod
kubectl logs -n seva-ai statefulset/postgresql

# Test connection
kubectl exec -it -n seva-ai statefulset/postgresql -- psql -U seva_user -d seva_ai
```

## Contributing

See main repository [CONTRIBUTING.md](../CONTRIBUTING.md)

## License

MIT License - see LICENSE file for details
