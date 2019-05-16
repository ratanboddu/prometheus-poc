FROM python:3.6-alpine
RUN pip install flask prometheus_client
COPY app.py /app.py
ENTRYPOINT ["python", "/app.py"]
EXPOSE 5000