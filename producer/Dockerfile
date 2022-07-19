FROM python:3.6.15
RUN pip install --upgrade pip
RUN pip install confluent-kafka scipy
COPY producer.py .
CMD ["python", "./producer.py"]
