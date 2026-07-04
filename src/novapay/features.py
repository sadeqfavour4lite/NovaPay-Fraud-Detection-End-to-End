"""Reusable feature engineering helpers extracted from Days 4 and 8."""

from __future__ import annotations

import numpy as np
import pandas as pd


def add_transaction_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Create model-ready transaction features used by notebooks and API scoring."""

    df = frame.copy()
    timestamp = pd.to_datetime(df["timestamp"])

    df["transaction_hour"] = timestamp.dt.hour
    df["weekday"] = timestamp.dt.weekday
    df["is_weekend"] = df["weekday"].isin([5, 6]).astype(int)
    df["is_night_transaction"] = df["transaction_hour"].between(0, 5).astype(int)
    df["country_mismatch_flag"] = (df["home_country"] != df["ip_country"]).astype(int)
    df["corridor"] = df["source_currency"].astype(str) + "_to_" + df["dest_currency"].astype(str)

    df["corridor_risk_band"] = pd.cut(
        df["corridor_risk"],
        bins=[-np.inf, 0.33, 0.66, np.inf],
        labels=["low", "medium", "high"],
    ).astype(str)

    df["chargeback_group"] = pd.cut(
        df["chargeback_history_count"],
        bins=[-np.inf, 0, 2, np.inf],
        labels=["none", "some", "high"],
    ).astype(str)

    df["high_velocity_1h_flag"] = (df["txn_velocity_1h"] >= 5).astype(int)
    df["high_velocity_24h_flag"] = (df["txn_velocity_24h"] >= 20).astype(int)
    df["any_velocity_risk_flag"] = (
        (df["high_velocity_1h_flag"] == 1) | (df["high_velocity_24h_flag"] == 1)
    ).astype(int)
    df["high_ip_risk_flag"] = (df["ip_risk_score"] >= 0.75).astype(int)
    df["low_device_trust_flag"] = (df["device_trust_score"] <= 0.30).astype(int)

    df["device_trust_band"] = pd.cut(
        df["device_trust_score"],
        bins=[-np.inf, 0.30, 0.70, np.inf],
        labels=["low", "medium", "high"],
    ).astype(str)

    return df


def add_customer_device_history_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Add historical customer and device aggregates for batch modelling."""

    df = frame.copy()
    if "customer_id" in df.columns:
        customer_group = df.groupby("customer_id")["amount_usd"]
        df["customer_transaction_count"] = customer_group.transform("count")
        df["customer_total_amount"] = customer_group.transform("sum")
        df["customer_avg_amount"] = customer_group.transform("mean")
        df["customer_max_amount"] = customer_group.transform("max")
        df["customer_amount_std"] = customer_group.transform("std").fillna(0)
        df["amount_to_customer_avg"] = df["amount_usd"] / df["customer_avg_amount"].replace(0, 1)

    if {"customer_id", "timestamp"}.issubset(df.columns):
        df = df.sort_values(["customer_id", "timestamp"]).copy()
        previous_timestamp = df.groupby("customer_id")["timestamp"].shift(1)
        df["customer_recency_days"] = (
            pd.to_datetime(df["timestamp"]) - pd.to_datetime(previous_timestamp)
        ).dt.total_seconds().div(86400)
        df["customer_recency_days"] = df["customer_recency_days"].fillna(df["account_age_days"])

    if "device_id" in df.columns:
        device_group = df.groupby("device_id")["device_trust_score"]
        df["device_transaction_count"] = device_group.transform("count")
        df["device_avg_trust_score"] = device_group.transform("mean")

    return df


def build_feature_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Apply the full reusable feature pipeline to cleaned transactions."""

    return add_customer_device_history_features(add_transaction_features(frame))
