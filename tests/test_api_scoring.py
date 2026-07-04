from datetime import datetime, timezone

import pandas as pd

from api.schemas import TransactionPayload
from api.scoring import add_engineered_features, transaction_to_dataframe


def sample_payload() -> TransactionPayload:
    return TransactionPayload(
        transaction_id="TX12345",
        customer_id="CUST1001",
        timestamp=datetime(2026, 7, 3, 10, 15, tzinfo=timezone.utc),
        home_country="GB",
        source_currency="GBP",
        dest_currency="NGN",
        channel="mobile_app",
        amount_src=750.0,
        amount_usd=950.0,
        fee=8.5,
        exchange_rate_src_to_dest=1850.25,
        device_id="DEV-7788",
        new_device=True,
        ip_address="203.0.113.10",
        ip_country="NG",
        location_mismatch=True,
        ip_risk_score=0.86,
        kyc_tier="tier_2",
        account_age_days=24,
        device_trust_score=0.22,
        chargeback_history_count=1,
        risk_score_internal=0.84,
        txn_velocity_1h=6,
        txn_velocity_24h=26,
        corridor_risk=0.78,
    )


def test_transaction_to_dataframe_adds_model_features():
    frame = transaction_to_dataframe(sample_payload())

    expected_columns = {
        "transaction_hour",
        "weekday",
        "is_weekend",
        "is_night_transaction",
        "country_mismatch_flag",
        "corridor",
        "corridor_risk_band",
        "chargeback_group",
        "high_velocity_1h_flag",
        "high_velocity_24h_flag",
        "any_velocity_risk_flag",
        "high_ip_risk_flag",
        "low_device_trust_flag",
        "customer_transaction_count",
        "device_transaction_count",
        "device_trust_band",
    }

    assert expected_columns.issubset(frame.columns)
    assert frame.loc[0, "corridor"] == "GBP_to_NGN"
    assert frame.loc[0, "country_mismatch_flag"] == 1


def test_add_engineered_features_handles_low_risk_transaction():
    frame = pd.DataFrame(
        [
            {
                "timestamp": "2026-07-03T14:15:00Z",
                "home_country": "GB",
                "source_currency": "GBP",
                "dest_currency": "EUR",
                "ip_country": "GB",
                "amount_usd": 100.0,
                "account_age_days": 400,
                "device_trust_score": 0.92,
                "chargeback_history_count": 0,
                "txn_velocity_1h": 1,
                "txn_velocity_24h": 2,
                "ip_risk_score": 0.05,
                "corridor_risk": 0.1,
            }
        ]
    )

    engineered = add_engineered_features(frame)

    assert engineered.loc[0, "high_ip_risk_flag"] == 0
    assert engineered.loc[0, "low_device_trust_flag"] == 0
    assert engineered.loc[0, "device_trust_band"] == "high"
