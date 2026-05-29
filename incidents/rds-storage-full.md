# P1 Incident Report - AWS RDS Storage Full

## Incident ID
P1-2025-002

## Severity
P1 - Critical

## Service
Production MySQL Database (AWS RDS)

## Situation
The production database became unavailable because the allocated storage volume reached 100% utilization.

## Symptoms
- User login failures.
- Checkout process failures.
- API timeouts.
- Database write operations stopped.

## Downtime
1 Hour 12 Minutes

## Error Messages

```sql
ERROR 1114 (HY000): The table is full
```

```text
No space left on device
```

```text
RDS FreeStorageSpace = 0
```

## Root Cause
Unexpected growth of database logs consumed all available storage. CloudWatch alarms were configured with incorrect thresholds and failed to trigger alerts.

## Resolution

### Verify Storage Metrics

```bash
aws cloudwatch get-metric-statistics
```

### Increase Database Storage

```bash
aws rds modify-db-instance \
  --db-instance-identifier prod-db \
  --allocated-storage 500 \
  --apply-immediately
```

### Clean Old Logs

```sql
PURGE BINARY LOGS BEFORE NOW() - INTERVAL 7 DAY;
```

### Enable Storage Autoscaling

```bash
aws rds modify-db-instance \
  --max-allocated-storage 1000
```

## Preventive Actions
- Enable RDS storage autoscaling.
- Improve CloudWatch alert thresholds.
- Review database growth monthly.
- Implement log retention policies.

## Status
Resolved