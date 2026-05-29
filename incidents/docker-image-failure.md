# P1 Incident Report - Failed Docker Deployment

## Incident ID
P1-2025-003

## Severity
P1 - Critical

## Service
Production API Platform

## Situation
A new deployment introduced a corrupted Docker image. The application failed immediately after deployment, causing widespread service disruption.

## Symptoms
- Pods entered CrashLoopBackOff state.
- API requests returned HTTP 503 errors.
- Load balancer health checks failed.
- Users could not access the platform.

## Downtime
32 Minutes

## Error Messages

```bash
CrashLoopBackOff
```

```bash
Back-off restarting failed container
```

```bash
exec format error
```

```text
503 Service Unavailable
```

## Root Cause
The CI/CD pipeline built the Docker image using ARM64 architecture while production worker nodes required AMD64 images.

## Resolution

### Inspect Pod Failures

```bash
kubectl describe pod api-prod-xyz
```

### Verify Image Architecture

```bash
docker inspect myapp:latest
```

### Rebuild Correct Image

```bash
docker buildx build \
  --platform linux/amd64 \
  -t myapp:latest .
```

### Roll Back Deployment

```bash
kubectl rollout undo deployment/api
```

### Verify Recovery

```bash
kubectl rollout status deployment/api
```

## Preventive Actions
- Validate image architecture during CI builds.
- Add deployment smoke tests.
- Configure automatic rollback policies.
- Standardize build environments.

## Status
Resolved