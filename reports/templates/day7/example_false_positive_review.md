# NovaPay Fraud Alert Review Template

## Transaction Summary
- Transaction ID: FP_EXAMPLE_FROM_DAY7
- Review Date: 2026-07-03
- Analyst: Fraud Operations Analyst
- Model Version: Day 6 best advanced model
- Prediction: Fraud alert
- Fraud Probability: Populate from `false_positive_explanation.csv`
- Confidence Score: Populate from `false_positive_explanation.csv`
- Actual Outcome if known: Legitimate transaction, false positive

## Reason Codes
| Rank | Reason Code | Feature | Contribution Direction | Analyst Interpretation |
|------|-------------|---------|------------------------|------------------------|
| 1 | High transaction activity in the last 24 hours increased fraud risk. | txn_velocity_24h | Increased fraud risk | Customer activity resembled known rapid-transfer fraud behaviour. |
| 2 | The transaction amount was unusual compared with the customer's normal behaviour. | amount_to_customer_avg | Increased fraud risk | Amount pattern looked unusual but may reflect a genuine urgent payment. |
| 3 | Low device trust increased fraud risk. | device_trust_score | Increased fraud risk | Customer may have recently changed phone or browser. |

## Customer and Transaction Context
- Amount: Populate from transaction row
- Channel: Populate from transaction row
- Home Country: Populate from transaction row
- IP Country: Populate from transaction row
- KYC Tier: Populate from transaction row
- Device Trust: Populate from transaction row
- Transaction Velocity 1h: Populate from transaction row
- Transaction Velocity 24h: Populate from transaction row
- Chargeback History: Populate from transaction row

## Analyst Decision
- [ ] Approve transaction
- [x] Manual review
- [ ] Temporarily hold
- [ ] Escalate to fraud investigation

## Analyst Notes
This alert should be reviewed as a likely false positive if customer identity, device ownership, and payment intent are confirmed. The reason codes are meaningful risk signals, but they can also occur during legitimate travel, device replacement, urgent family transfers, or repeated payments.

## Recommended Follow-up
- [x] Contact customer
- [x] Verify device
- [ ] Request additional KYC
- [x] Monitor account
- [ ] Close alert as false positive
