FROM python:3.7-slim

WORKDIR /usr/src/healthCheck

COPY src/ .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "healthCheck.py", "--ifasync"]

