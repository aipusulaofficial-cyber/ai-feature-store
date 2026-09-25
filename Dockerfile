FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python","-c","from feature_store import FeatureStore; print('feature store ready')"]
