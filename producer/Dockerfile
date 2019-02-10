FROM python:latest
RUN pip install --upgrade pip
RUN pip install confluent-kafka scipy
COPY producer.py .
CMD ["python", "./producer.py"]
