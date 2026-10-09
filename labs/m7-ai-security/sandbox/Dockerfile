# Offline, scripted AI-assistant sandbox for the M7 prompt-injection lab.
# No model, no network egress — pure stdlib rule-based stub.
FROM python:3.12-alpine
COPY app.py /app/app.py
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["python3", "app.py"]
