from flask import request
from prometheus_client import Counter, Histogram
import time
import sys

FLASK_REQUEST_COUNT = Counter( __name__.replace('.', '_') + '_request_count', 'App Request Count', ['app_name', 'method', 'endpoint', 'http_status'])
FLASK_REQUEST_LATENCY = Histogram(__name__.replace('.', '_') + '_request_latency_seconds', 'Flask Request Latency', ['app_name', 'endpoint'])

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    FLASK_REQUEST_LATENCY.labels('webapp', request.path).observe(resp_time)
    return response

def record_request_data(response):
    FLASK_REQUEST_COUNT.labels('webapp', request.method, request.path,
            response.status_code).inc()
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(record_request_data)
    app.after_request(stop_timer)
