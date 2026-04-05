# backend/metrics/metrics.py

def log_metric(name: str, value):
    """
    Logs a metric. Currently prints to stdout, 
    can be extended to push to Prometheus, Grafana, or other monitoring.
    """
    print(f"[METRIC] {name}: {value}")