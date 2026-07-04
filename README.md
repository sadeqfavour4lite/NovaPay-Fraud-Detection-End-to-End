# NovaPay Fraud Detection

End-to-end machine learning project for detecting fraudulent digital money-transfer transactions. The project starts with raw transaction data, builds fraud-focused features, compares baseline and advanced models, explains model decisions, and packages the best model behind a FastAPI scoring service.

## Highlights

- Reproducible notebook workflow from cleaning through API packaging.
- Behavioural, velocity, geography, device, and corridor-risk feature engineering.
- Baseline and advanced model experiments with imbalanced-class handling.
- Explainability workflow for global SHAP-style insights, false-positive review, and stakeholder templates.
- Production-style FastAPI endpoint with request validation, model loading, health check, and Docker support.

## Repository Structure

```text
NovaPay_Fraud_Detection/
├── api/
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   ├── day5/
│   └── day6/
├── notebooks/
├── reports/
│   ├── artifacts/
│   ├── figures/
│   └── templates/
├── src/
│   └── novapay/
├── tests/
├── Dockerfile
├── PROJECT_SUMMARY.md
├── README.md
└── requirements.txt
```

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
uvicorn api.main:app --reload
```

Open:

- API health: `http://127.0.0.1:8000/health`
- Swagger docs: `http://127.0.0.1:8000/docs`

On macOS or Linux, activate with `source .venv/bin/activate`.

## Score a Transaction

```bash
curl -X POST "http://127.0.0.1:8000/score" \
  -H "Content-Type: application/json" \
  --data @reports/artifacts/day8/sample_request.json
```

The response includes:

- `prediction`
- `fraud_probability`
- `confidence_score`
- `decision`
- `reason`
- `model_version`

## Run With Docker

```bash
docker build -t novapay-fraud-api .
docker run --rm -p 8000:8000 novapay-fraud-api
```

## Notebook Workflow

Run notebooks from the repository root in this order:

1. `notebooks/03_cleaning.ipynb`
2. `notebooks/04_features_eda.ipynb`
3. `notebooks/05_baseline_models.ipynb`
4. `notebooks/06_advanced_models.ipynb`
5. `notebooks/07_explainability.ipynb`
6. `notebooks/08_api_pipeline.ipynb`

## File Placement Map

| File or artifact | GitHub location |
| --- | --- |
| `03_cleaning.ipynb` | `notebooks/03_cleaning.ipynb` |
| `04_features_eda.ipynb` | `notebooks/04_features_eda.ipynb` |
| `05_baseline_models.ipynb` | `notebooks/05_baseline_models.ipynb` |
| `06_advanced_models.ipynb` | `notebooks/06_advanced_models.ipynb` |
| `07_explainability.ipynb` | `notebooks/07_explainability.ipynb` |
| `08_api_pipeline.ipynb` | `notebooks/08_api_pipeline.ipynb` |
| `nova_pay_combined.csv` | `data/raw/nova_pay_combined.csv` |
| `cleaned_transactions.csv` | `data/processed/cleaned_transactions.csv` |
| `feature_engineered_transactions.csv` | `data/processed/feature_engineered_transactions.csv` after running Day 4 |
| Day 4 figures | `reports/figures/day4/` |
| Day 5 metrics and threshold CSVs | `reports/artifacts/day5/` |
| Day 5 best baseline model | `models/day5/day5_best_baseline_model.joblib` after running Day 5 |
| Day 6 experiment logs and summaries | `reports/artifacts/day6/` |
| Day 6 best advanced model | `models/day6/best_advanced_model.joblib` |
| Day 7 explainability reports | `reports/artifacts/day7/` |
| Day 7 review templates | `reports/templates/day7/` |
| Day 8 API samples and validation notes | `reports/artifacts/day8/` |
| FastAPI app | `api/` |
| Reusable cleaning and feature code | `src/novapay/` |

## GitHub Upload Checklist

- `api/__init__.py`
- `api/main.py`
- `api/model_loader.py`
- `api/schemas.py`
- `api/scoring.py`
- `data/raw/nova_pay_combined.csv`
- `data/processed/cleaned_transactions.csv`
- `models/day5/.gitkeep`
- `models/day6/best_advanced_model.joblib`
- `notebooks/03_cleaning.ipynb`
- `notebooks/04_features_eda.ipynb`
- `notebooks/05_baseline_models.ipynb`
- `notebooks/06_advanced_models.ipynb`
- `notebooks/07_explainability.ipynb`
- `notebooks/08_api_pipeline.ipynb`
- `reports/artifacts/.gitkeep`
- `reports/artifacts/day8/api_validation_notes.md`
- `reports/artifacts/day8/sample_request.json`
- `reports/artifacts/day8/sample_response.json`
- `reports/figures/.gitkeep`
- `reports/templates/day7/example_false_positive_review.md`
- `reports/templates/day7/stakeholder_review_template.md`
- `src/novapay/__init__.py`
- `src/novapay/data_cleaning.py`
- `src/novapay/features.py`
- `src/novapay/paths.py`
- `tests/conftest.py`
- `tests/test_api_scoring.py`
- `.dockerignore`
- `.gitignore`
- `CONTRIBUTING.md`
- `Dockerfile`
- `FILE_INVENTORY.md`
- `LICENSE`
- `PROJECT_SUMMARY.md`
- `README.md`
- `requirements.txt`

## Notes for Reviewers

This repository intentionally keeps the original notebooks as the project narrative and exposes reusable logic in `src/` and `api/` for maintainability. Generated figures and intermediate experiment outputs can be recreated by running the notebooks in order.
