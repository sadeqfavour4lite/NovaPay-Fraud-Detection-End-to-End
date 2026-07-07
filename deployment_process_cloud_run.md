# NovaPay Fraud Detection API Deployment Process

## FastAPI + Docker + Google Cloud Run

This deployment guide documents the full Windows CMD workflow for moving the NovaPay Fraud Detection API from a local FastAPI project into a Google Cloud Run service. It is intended for analysts who need to reproduce, validate, or interact with the deployed API.

## 1. Install Google Cloud CLI

Download and install the Google Cloud SDK from the official Google Cloud documentation.

After installation, verify from CMD:

```cmd
gcloud --version
```

Expected result:

```text
Google Cloud SDK installed successfully
```

## 2. Authenticate Google Cloud Account

Login from CMD:

```cmd
gcloud auth login
```

A browser window opens. Complete Google authentication, then verify the active account:

```cmd
gcloud auth list
```

## 3. Initialise Google Cloud Configuration

Run:

```cmd
gcloud init
```

Select or create the Google Cloud project.

Project used:

```text
linear-elf-470513-j1
```

Confirm the active project:

```cmd
gcloud config get-value project
```

## 4. Navigate to NovaPay Project Directory

Move into the project folder:

```cmd
cd %USERPROFILE%\Downloads\NovaPay_Day8_API_Pipeline
```

Confirm files:

```cmd
dir
```

Expected project structure:

```text
NovaPay_Day8_API_Pipeline
|
|-- api
|   |-- main.py
|   |-- model_loader.py
|   `-- requirements.txt
|
|-- models
|   `-- day6
|       `-- best_advanced_model.joblib
|
`-- Dockerfile
```

The trained model must be available at:

```text
models\day6\best_advanced_model.joblib
```

## 5. Prepare Python Dependencies

Open requirements:

```cmd
notepad api\requirements.txt
```

Final requirements:

```text
fastapi==0.115.6
uvicorn[standard]==0.34.0
pandas==2.2.3
numpy==2.2.1
scikit-learn==1.6.0
joblib==1.4.2
imbalanced-learn==0.13.0
xgboost
```

Verify:

```cmd
type api\requirements.txt
```

## 6. Create Dockerfile

Open:

```cmd
notepad Dockerfile
```

Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY api/requirements.txt /app/api/requirements.txt

RUN pip install --no-cache-dir -r /app/api/requirements.txt

COPY api /app/api

COPY models /app/models

EXPOSE 8080

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

Cloud Run expects the container to listen on the runtime port. This deployment uses port `8080`.

## 7. Enable Google Cloud Services

Enable required services:

```cmd
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

Successful response:

```text
Operation finished successfully
```

## 8. Deploy FastAPI ML Application

Deploy to Cloud Run:

```cmd
gcloud run deploy novapay-fraud-api --source . --region europe-west2 --allow-unauthenticated
```

Confirm the prompt:

```text
Do you want to continue (Y/n)?
```

Input:

```text
Y
```

## 9. Google Cloud Build Process

Google Cloud automatically performs the following steps:

1. Builds the Docker container.
2. Installs Python dependencies.
3. Installs API and ML packages:
   - `fastapi`
   - `uvicorn`
   - `pandas`
   - `numpy`
   - `scikit-learn`
   - `imbalanced-learn`
   - `xgboost`
4. Uploads the container image.
5. Creates the Cloud Run revision.
6. Routes traffic to the deployed service.

## 10. Successful Deployment Output

Expected deployment result:

```text
Done.

Service [novapay-fraud-api] revision deployed
and serving 100 percent of traffic
```

Live API:

```text
https://novapay-fraud-api-731328327272.europe-west2.run.app
```

Swagger documentation:

```text
https://novapay-fraud-api-731328327272.europe-west2.run.app/docs
```

## 11. Validate API Health Endpoint

Open:

```text
GET /health
```

Expected response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

If the model is missing, copy the trained Day 6 artifact into:

```text
models\day6\best_advanced_model.joblib
```

Then redeploy the Cloud Run service.

## 12. Test Fraud Prediction Endpoint

Endpoint:

```text
POST /score
```

Example response:

```json
{
  "prediction": "legitimate",
  "fraud_probability": 0.2075,
  "confidence_score": 0.7925,
  "decision": "approve",
  "reason": "Transaction flagged for high IP risk score, location mismatch",
  "model_version": "day6_best_advanced_model"
}
```

Analysts can also interact with the API through Swagger:

```text
https://novapay-fraud-api-731328327272.europe-west2.run.app/docs
```

## Analyst Interaction Guide

Analysts can validate the live deployment without running the project locally.

Health check from CMD:

```cmd
curl https://novapay-fraud-api-731328327272.europe-west2.run.app/health
```

Open Swagger UI in a browser:

```text
https://novapay-fraud-api-731328327272.europe-west2.run.app/docs
```

In Swagger, select `POST /score`, choose **Try it out**, paste a valid transaction JSON payload, and execute the request. The API returns:

- `prediction`: fraud classification label.
- `fraud_probability`: model probability for fraud.
- `confidence_score`: confidence in the returned prediction.
- `decision`: operational action such as `approve`, `manual_review`, or `hold_and_investigate`.
- `reason`: analyst-readable explanation of the main risk signals.
- `model_version`: model artifact version used for scoring.

## Final Deployment Architecture

```text
User Transaction Request
        |
        v
Google Cloud Run
        |
        v
Docker Container
        |
        v
FastAPI REST API
        |
        v
Model Loader
        |
        v
XGBoost Fraud Model
        |
        v
Fraud Score + Explanation
```

## Outcome

The NovaPay machine learning model was successfully converted from a notebook experiment into a cloud-hosted production fraud detection service using FastAPI, Docker, Google Cloud Run, an XGBoost fraud model, and REST API architecture.

