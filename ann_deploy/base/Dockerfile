FROM python:3.8-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
COPY . /opt/workdir

# Install gcc for annoy
RUN apt-get update -qqy && \
    apt-get install -qqy --no-install-recommends gcc && \
    apt-get install g++ -qqy && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install production dependencies.
RUN pip3 install --no-cache-dir numpy && \
    pip3 install --no-cache-dir annoy && \
    pip3 install --no-cache-dir nmslib && \
    pip3 install --no-cache-dir flask && \
    pip3 install --no-cache-dir gunicorn

RUN apt-get purge -qqy --auto-remove gcc g++