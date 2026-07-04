# Contributing

Thanks for improving NovaPay Fraud Detection.

## Local setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux, activate with `source .venv/bin/activate`.

## Development workflow

1. Create a focused branch for the change.
2. Keep notebooks as reproducible research artifacts.
3. Move reusable logic into `src/novapay/` or `api/` when it is used more than once.
4. Add or update tests for API scoring, feature engineering, or model-loading changes.
5. Run `pytest` before opening a pull request.

## Data and model artifacts

The small sample project artifacts in this repository are included for portfolio reproducibility. If a future dataset or model becomes too large for GitHub, store it externally and document the download path in `README.md`.

## Pull request checklist

- The project runs from the repository root.
- New paths are relative, not machine-specific.
- Generated files are saved under `reports/`, `models/`, or `data/processed/`.
- Secrets, API keys, and private customer data are not committed.
