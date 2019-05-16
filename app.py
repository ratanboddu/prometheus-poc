from flask import Flask, Response
from prometheus_client import Counter, Gauge, generate_latest


app = Flask("__name__")


my_counter = Counter('my_counter', 'Testing counter')
my_gauge = Gauge('my_gauge', 'Testing gauge')


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


@app.route("/metrics")
def metrics():
    content = generate_latest()
    return Response(content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


# docker network create prometheus
# docker run --publish 5000:5000 --network prometheus --name flask-app --detach akhilputhiry/flask-app:1.0.0
# docker run --publish 9090:9090 --network prometheus --name prometheus --volume /Users/akhillawrence/personal/metrics/prometheus.yml:/etc/prometheus/prometheus.yml --detach prom/prometheus:latest
