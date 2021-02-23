FROM gcr.io/ddd-model-gap/recsys/tf-serving-base

# Copy the exporter models. Directory pattern should be /<model>/<version>
# Only the latest version is run by the tensorflow serving
# Take care of the number of model in exporter directory, can grow your container.
COPY model /models/tf_models

# Serve the model on REST API port define by Cloud Run
CMD tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=vae_cf --model_base_path=/models/tf_models