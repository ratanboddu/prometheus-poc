#!/usr/bin/env python3

from flask import Flask, Response
from prometheus_client import Counter, Gauge, generate_latest, Summary, Histogram, start_http_server, make_wsgi_app,  start_wsgi_server


import time


app = Flask("__name__")


my_counter = Counter('my_counter', 'Testing counter')

my_gauge = Gauge('my_gauge', 'Testing gauge')

my_summary = Summary('response_latency_seconds', 'Response latency (seconds)')
obv_summary = Summary('request_size_bytes', 'Request size (bytes)')

my_histogram = Histogram('response_latency_seconds_his', 'Response latency (seconds)')
obv_histogram = Histogram('request_size_bytes_his', 'Request size (bytes)')


@app.route("/counter")
def counter():
    my_counter.inc()
    return "Testing Counter"


@app.route("/gauge-inc")
def gauge_inc():
    my_gauge.inc()
    return "Testing gauge inc"


@app.route("/gauge-dec")
def gauge_dec():
    my_gauge.dec()
    return "Testing gauge dec"


@my_summary.time()
def sleep_function():
    """A dummy function"""
    time.sleep(5)
    return "Testing Summary"


@my_histogram.time()
def sleep_function_histogram():
    """A dummy function"""
    time.sleep(2)
    return "Testing Histogram"


@app.route("/summary")
def summary():
    return sleep_function()


@app.route("/summary-observe")
def summary_observe():
    obv_summary.observe(102)
    return "Testing summary-observe"


@app.route("/histogram")
def histogram():
    return sleep_function_histogram()


@app.route("/histogram-observe")
def histogram_observe():
    obv_histogram.observe(102)
    return "Testing histogram-observe"


@app.route("/metrics")
def metrics():
    content = generate_latest()
    return Response(content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9898, debug=True)



# docker network create prometheus
# docker run --publish 5000:5000 --network prometheus --name flask-app --detach akhilputhiry/flask-app:1.0.0
# docker run --publish 9090:9090 --network prometheus --name prometheus --volume /Users/akhillawrence/personal/metrics/prometheus.yml:/etc/prometheus/prometheus.yml --detach prom/prometheus:latest
