FROM ubuntu:xenial

# Install manually TensorflowServing
RUN apt-get update -qqy && \
    apt-get install -qqy curl && \
    echo "deb http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | tee /etc/apt/sources.list.d/tensorflow-serving.list && \
    curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | apt-key add - && \
    apt-get update && \
    apt-get install tensorflow-model-server
