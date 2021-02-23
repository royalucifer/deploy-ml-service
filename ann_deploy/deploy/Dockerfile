FROM gcr.io/ddd-model-gap/recsys/ann-index-base:latest

# Copy the annoy index.
COPY AnnSearch /opt/workdir/AnnSearch
WORKDIR /opt/workdir

# Serve the Annoy on REST API port define by Cloud Run
# CMD ["python3", "main.py"]
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 main:app