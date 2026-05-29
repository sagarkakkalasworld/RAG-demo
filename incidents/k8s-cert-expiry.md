# P1 Incident Report - Kubernetes Certificate Expiry

## Incident ID
P1-2025-001

## Severity
P1 - Critical

## Service
Production Kubernetes Cluster

## Situation
The production Kubernetes cluster became inaccessible during business hours. Engineers could not deploy new releases, scale applications, or manage workloads.

## Symptoms
- Applications became unavailable.
- New pods could not be scheduled.
- CI/CD deployments failed.
- Monitoring dashboards reported API server connectivity issues.

## Downtime
47 Minutes

## Error Messages

```bash
Unable to connect to the server: x509: certificate has expired or is not yet valid
```

```bash
kubectl get nodes
Error from server (InternalError)
```

```bash
TLS handshake timeout
```

## Root Cause
The Kubernetes API server certificate expired. No certificate expiration monitoring or alerting mechanism was configured.

## Resolution

### Verify Certificate Expiry

```bash
kubeadm certs check-expiration
```

### Renew Certificates

```bash
kubeadm certs renew all
```

### Restart Kubernetes Components

```bash
systemctl restart kubelet
```

### Validate Cluster Health

```bash
kubectl get nodes
kubectl get pods -A
```

## Preventive Actions
- Configure certificate expiry monitoring.
- Create alerts for 30, 15, and 7 days before expiry.
- Automate certificate renewal procedures.

## Status
Resolved