"""Reusable data-cleaning logic extracted from the Day 3 notebook."""

from __future__ import annotations

import pandas as pd


TEXT_COLUMNS = [
    "home_country",
    "source_currency",
    "dest_currency",
    "channel",
    "ip_country",
    "kyc_tier",
]

NUMERIC_COLUMNS = [
    "amount_src",
    "amount_usd",
    "fee",
    "exchange_rate_src_to_dest",
    "ip_risk_score",
    "account_age_days",
    "device_trust_score",
    "chargeback_history_count",
    "risk_score_internal",
    "txn_velocity_1h",
    "txn_velocity_24h",
    "corridor_risk",
]


def convert_bool_like(series: pd.Series) -> pd.Series:
    """Convert common boolean-like strings into pandas nullable booleans."""

    if pd.api.types.is_bool_dtype(series):
        return series.astype("boolean")

    mapping = {
        "true": True,
        "false": False,
        "1": True,
        "0": False,
        "yes": True,
        "no": False,
        "y": True,
        "n": False,
        "t": True,
        "f": False,
    }
    return series.astype("string").str.strip().str.lower().map(mapping).astype("boolean")


def clean_transactions(df_raw: pd.DataFrame, now_utc: pd.Timestamp | None = None) -> pd.DataFrame:
    """Clean raw NovaPay transactions while preserving label integrity."""

    if "is_fraud" not in df_raw.columns:
        raise KeyError("Required target column is_fraud is missing.")

    df = df_raw.copy()
    df["is_fraud"] = pd.to_numeric(df["is_fraud"], errors="coerce")
    df = df.dropna(subset=["is_fraud"]).copy()
    df["is_fraud"] = df["is_fraud"].astype(int)

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df.dropna(subset=["timestamp"]).copy()
    now_utc = now_utc or pd.Timestamp.now(tz="UTC")
    df = df.loc[df["timestamp"] <= now_utc].copy()

    for column in TEXT_COLUMNS:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip().str.lower()

    if "channel" in df.columns:
        df["channel"] = (
            df["channel"]
            .str.replace(r"\s+", " ", regex=True)
            .replace({"moblie": "mobile", "mobille": "mobile", "weeb": "web"})
        )

    if "kyc_tier" in df.columns:
        df["kyc_tier"] = df["kyc_tier"].replace({"standrd": "standard", "enhancd": "enhanced"})

    for column in ["home_country", "source_currency", "dest_currency", "ip_country"]:
        if column in df.columns:
            df[column] = df[column].str.upper()

    df = df.drop_duplicates().copy()

    for column in ["new_device", "location_mismatch"]:
        if column in df.columns:
            df[column] = convert_bool_like(df[column])

    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    negative_mask = pd.Series(False, index=df.index)
    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            negative_mask = negative_mask | (df[column] < 0).fillna(False)
    df = df.loc[~negative_mask].copy()

    missing_tokens = {"", "unknown", "nan", "none", "null", "na", "n/a", "<na>"}
    for column in TEXT_COLUMNS:
        if column in df.columns:
            missing_like = df[column].astype("string").str.strip().str.lower().isin(missing_tokens)
            df.loc[missing_like, column] = pd.NA
            df[column] = df[column].fillna("Unknown")

    return df
