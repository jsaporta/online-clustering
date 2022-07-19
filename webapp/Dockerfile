FROM python:3.6.15
RUN pip install --upgrade pip
RUN pip install bokeh confluent-kafka numpy scikit-learn
COPY webapp.py .
CMD ["python", "./webapp.py"]
