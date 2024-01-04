FROM python:3.7-slim

WORKDIR /usr/src/healthCheck

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "healthCheck.py"]

