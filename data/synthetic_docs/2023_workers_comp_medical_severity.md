---
title: "2023 Workers Compensation Medical Severity Model Documentation"
model_id: "WC-MED-SEV-2023"
portfolio: "workers_comp"
type: "model_documentation"
company: "ABC Insurance Company"
version: "1.0"
model_owner: "David Chen, FCAS"
effective_date: "2023-10-01"
status: "active"
---

# 2023 Workers Compensation Medical Severity Model

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes.

---

## Executive Summary

### Model Purpose

The 2023 Workers Compensation Medical Severity Model predicts the expected medical cost per claim based on injury characteristics, claimant demographics, and state factors.

### Key Findings

- Injury type and body part are strongest predictors
- Medical costs increased 6% annually (2018-2022)
- State fee schedules create 40% variation across states
- Model achieves R-squared of 0.42 on holdout data

---

## Data Sources

### Internal Data

| Source | Description | Records | Date Range |
|--------|-------------|---------|------------|
| WCClaims | Claim-level medical payments | 28,400 | 2018-2022 |
| MedicalDetail | Treatment transactions | 425,000 | 2018-2022 |

### External Data

| Source | Description | Usage |
|--------|-------------|-------|
| NCCI | Medical benchmarks | Benchmark |
| WCRI | State medical studies | Validation |

---

## Feature Engineering

### Injury Type Categories

- Strain/Sprain (42% of claims)
- Contusion/Bruise (15%)
- Laceration/Cut (12%)
- Fracture (10%)
- Burn (3%)
- Cumulative Trauma (8%)
- Other (10%)

### Body Part Categories

- Back/Spine (28% of claims)
- Upper Extremity - Shoulder/Arm (18%)
- Upper Extremity - Hand/Wrist (15%)
- Lower Extremity - Knee/Leg (16%)
- Lower Extremity - Foot/Ankle (8%)
- Head/Neck (7%)
- Multiple/Other (8%)

### State Fee Schedule Index

Relative to Medicare baseline (1.0):
- California: 1.35
- New York: 1.28
- Texas: 0.95
- Florida: 0.92

---

## Methodology

**Approach:** GLM with Gamma distribution, Log link

### Model Specification

```
log(E[medical]) = intercept + injury_type + body_part + age + state_fee_index
```

---

## Model Results

### Injury Type Relativities

| Injury Type | Relativity | Avg Medical |
|-------------|------------|-------------|
| Strain/Sprain | 1.00 | $15,200 |
| Contusion | 0.78 | $11,900 |
| Laceration | 0.70 | $10,600 |
| Fracture | 1.73 | $26,300 |
| Burn | 2.05 | $31,200 |
| Cumulative | 2.34 | $35,600 |

### Age Relativities

| Age Band | Relativity |
|----------|------------|
| 16-29 | 1.00 |
| 30-44 | 1.11 |
| 45-54 | 1.25 |
| 55-64 | 1.42 |
| 65+ | 1.62 |

### Model Fit

| Metric | Value |
|--------|-------|
| R-squared | 0.42 |
| RMSE | $13,800 |
| Dispersion | 1.35 |

---

## Validation

### Holdout Performance

| Metric | Training | Holdout |
|--------|----------|---------|
| R-squared | 0.46 | 0.42 |
| MAE | $7,200 | $7,900 |

### Segment Validation

All segments within 5% A/E tolerance.

---

## Model Limitations

1. Development uncertainty in ultimate medical
2. Fee schedule changes may outpace model
3. Medical management impact not directly modeled
4. Pharmacy cost volatility

---

## Medical Trend

| Year | Avg Medical | Trend |
|------|-------------|-------|
| 2018 | $15,200 | - |
| 2019 | $16,100 | +5.9% |
| 2020 | $16,800 | +4.3% |
| 2021 | $17,600 | +4.8% |
| 2022 | $18,500 | +5.1% |

**5-Year CAGR: 5.1%**

---

## Body Part Relativities

| Body Part | Coefficient | Std Error | Relativity | Avg Medical |
|-----------|-------------|-----------|------------|-------------|
| Back/Spine | 0.000 | - | 1.00 | $18,200 |
| Upper Ext - Shoulder | 0.125 | 0.032 | 1.13 | $20,600 |
| Upper Ext - Hand/Wrist | -0.185 | 0.028 | 0.83 | $15,100 |
| Lower Ext - Knee/Leg | 0.095 | 0.030 | 1.10 | $20,000 |
| Lower Ext - Foot/Ankle | -0.145 | 0.034 | 0.87 | $15,800 |
| Head/Neck | 0.285 | 0.038 | 1.33 | $24,200 |
| Multiple Body Parts | 0.425 | 0.042 | 1.53 | $27,800 |

---

## State Fee Schedule Relativities

| State Group | Fee Index | Coefficient | Relativity | Avg Medical |
|-------------|-----------|-------------|------------|-------------|
| Low Fee (TX, FL, IN) | 0.90 | -0.18 | 0.84 | $15,200 |
| Medium Fee (OH, PA, IL) | 1.00 | 0.00 | 1.00 | $18,100 |
| High Fee (CA, NY, NJ) | 1.25 | 0.22 | 1.25 | $22,600 |
| Very High Fee (WA, MA) | 1.35 | 0.32 | 1.38 | $24,900 |

---

## Continuous Variable Effects

### Claimant Age

```
Coefficient: 0.012 per year above 40
Standard Error: 0.002
P-value: <0.001

Age Effect:
- Age 25: 0.85x baseline
- Age 40: 1.00x baseline (reference)
- Age 55: 1.20x baseline
- Age 65: 1.35x baseline
```

### Claim Duration

```
Coefficient: 0.0008 per day
Standard Error: 0.0001
P-value: <0.001

Duration Effect (days to MMI):
- 30 days: 0.90x baseline
- 90 days: 1.00x baseline (reference)
- 180 days: 1.08x baseline
- 365 days: 1.25x baseline
```

---

## Model Validation

### Holdout Performance

**Data Split:**
- Training: 70% (2018-2021 accident years)
- Holdout: 30% (2022 accident year)

**Performance Metrics:**

| Metric | Training | Holdout | Degradation |
|--------|----------|---------|-------------|
| R-squared | 0.46 | 0.42 | -0.04 |
| RMSE | $12,400 | $13,800 | +$1,400 |
| MAE | $6,800 | $7,900 | +$1,100 |
| MAPE | 28.5% | 31.2% | +2.7% |

**Assessment:** Model shows acceptable generalization with minimal overfitting.

### Actual vs Expected by Segment

**By Injury Type:**

| Injury Type | Expected | Actual | A/E Ratio |
|-------------|----------|--------|-----------|
| Strain/Sprain | $15,400 | $15,200 | 0.99 |
| Contusion | $11,700 | $11,900 | 1.02 |
| Laceration | $10,800 | $10,600 | 0.98 |
| Fracture | $25,800 | $26,300 | 1.02 |
| Burn | $30,500 | $31,200 | 1.02 |
| Cumulative Trauma | $34,900 | $35,600 | 1.02 |

**By Age Band:**

| Age Band | Expected | Actual | A/E Ratio |
|----------|----------|--------|-----------|
| 16-29 | $14,200 | $14,100 | 0.99 |
| 30-44 | $16,100 | $16,400 | 1.02 |
| 45-54 | $18,600 | $18,200 | 0.98 |
| 55-64 | $21,800 | $22,400 | 1.03 |
| 65+ | $25,200 | $24,600 | 0.98 |

**By State Fee Group:**

| State Group | Expected | Actual | A/E Ratio |
|-------------|----------|--------|-----------|
| Low Fee | $15,000 | $15,200 | 1.01 |
| Medium Fee | $18,200 | $18,100 | 1.00 |
| High Fee | $22,400 | $22,600 | 1.01 |
| Very High Fee | $25,200 | $24,900 | 0.99 |

### Lift Analysis

| Decile | Predicted Avg | Actual Avg | Lift vs Random |
|--------|---------------|------------|----------------|
| 1 (lowest) | $6,200 | $6,400 | 0.35x |
| 2 | $9,100 | $9,300 | 0.51x |
| 3 | $11,800 | $11,600 | 0.64x |
| 4 | $14,200 | $14,500 | 0.80x |
| 5 | $16,400 | $16,200 | 0.89x |
| 6 | $18,800 | $19,100 | 1.05x |
| 7 | $21,500 | $21,200 | 1.17x |
| 8 | $25,400 | $25,800 | 1.42x |
| 9 | $31,200 | $30,800 | 1.70x |
| 10 (highest) | $45,600 | $46,200 | 2.54x |

**Top Decile Lift: 2.54x** demonstrates strong model discrimination.

---

## Implementation

### Production Scoring

**Medical Severity Factor Calculation:**

```python
def calculate_wc_medical_severity_factor(claim):
    """
    Calculate expected medical severity for a WC claim.
    Returns severity factor relative to baseline.
    """
    base_severity = 18100  # Overall average medical severity
    factor = 1.0

    # Injury type factor
    injury_factors = {
        'strain_sprain': 1.00,
        'contusion': 0.78,
        'laceration': 0.70,
        'fracture': 1.73,
        'burn': 2.05,
        'cumulative_trauma': 2.34,
        'other': 0.95
    }
    factor *= injury_factors.get(claim.injury_type, 1.0)

    # Body part factor
    body_factors = {
        'back_spine': 1.00,
        'shoulder_arm': 1.13,
        'hand_wrist': 0.83,
        'knee_leg': 1.10,
        'foot_ankle': 0.87,
        'head_neck': 1.33,
        'multiple': 1.53
    }
    factor *= body_factors.get(claim.body_part, 1.0)

    # Age factor (relative to age 40)
    age_factor = math.exp(0.012 * (claim.claimant_age - 40))
    factor *= max(0.75, min(age_factor, 1.50))  # Cap at reasonable bounds

    # State fee schedule factor
    state_fee_factors = {
        'low': 0.84,
        'medium': 1.00,
        'high': 1.25,
        'very_high': 1.38
    }
    factor *= state_fee_factors.get(claim.state_fee_tier, 1.0)

    return base_severity * factor
```

### Reserve Setting Integration

**Initial Case Reserve:**
```python
def set_initial_medical_reserve(claim):
    """
    Set initial medical case reserve based on model prediction.
    """
    predicted_severity = calculate_wc_medical_severity_factor(claim)

    # Apply development factor for claim age
    development_factor = get_medical_development_factor(claim.days_since_injury)

    # Calculate ultimate expected medical
    ultimate_medical = predicted_severity * development_factor

    # Initial reserve = ultimate minus paid to date
    initial_reserve = ultimate_medical - claim.medical_paid_to_date

    return max(initial_reserve, 0)
```

### System Integration

**Data Flow:**
1. Claim receives injury coding at FNOL or adjuster review
2. Medical severity model scores claim within 24 hours
3. Score stored in ClaimsVision for case management
4. Reserve recommendations generated for adjuster review
5. High-severity alerts trigger medical management review

**API Endpoint:**
```
POST /api/v1/wc/medical-severity-score
Input: claim_id, injury_type, body_part, claimant_age, state
Output: predicted_severity, confidence_interval, risk_tier
```

---

## Monitoring Plan

### Key Performance Indicators

**Monthly Monitoring:**

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| A/E Ratio (Overall) | 0.95-1.05 | <0.90 or >1.10 |
| MAPE | <35% | >40% |
| High Severity Rate | 8-12% | >15% |
| Reserve Adequacy | 98-102% | <95% or >108% |

**Quarterly Monitoring:**

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| R-squared (rolling 12mo) | >0.38 | <0.35 |
| Lift Ratio (top decile) | >2.2x | <1.8x |
| Coefficient Stability | Within 15% | >20% change |
| Medical Trend | 4-7% | >10% |

### Monitoring Dashboard

**Weekly Alerts:**
- Claims with actual severity >2x predicted
- Claims with predicted severity >$75,000
- Unusual injury type/body part combinations
- State-level A/E deviations >15%

**Monthly Reports:**
- A/E by injury type, body part, age, state
- Medical cost trend emergence
- Reserve adequacy by cohort
- Model score distribution

### Model Refresh Schedule

| Activity | Frequency | Responsibility |
|----------|-----------|----------------|
| KPI Review | Monthly | Actuarial Analyst |
| Full Validation | Quarterly | Senior Actuary |
| Coefficient Recalibration | Annual | Model Owner |
| Major Revision | 3-5 years | Model Risk Committee |

### Escalation Procedures

**Level 1 - Elevated Monitoring:**
- Trigger: A/E ratio 1.05-1.10 for 2 consecutive months
- Action: Enhanced monitoring, root cause investigation
- Owner: Actuarial Analyst

**Level 2 - Model Review:**
- Trigger: A/E ratio >1.10 or R² <0.38
- Action: Full model review, coefficient analysis
- Owner: Senior Actuary / Model Owner

**Level 3 - Model Override:**
- Trigger: A/E ratio >1.15 or systematic bias identified
- Action: Temporary adjustments, expedited recalibration
- Owner: Chief Actuary / Model Risk Committee

---

## Appendices

### Appendix A: Full Coefficient Table

**Model Specification:**
```
log(E[Medical_Severity]) = β₀ + Σ βᵢ × Xᵢ

Distribution: Gamma
Link: Log
Dispersion: 1.35
```

**Complete Coefficient Estimates:**

| Variable | Level | Coefficient | Std Error | P-value | Relativity |
|----------|-------|-------------|-----------|---------|------------|
| Intercept | - | 9.52 | 0.08 | <0.001 | - |
| Injury Type | Strain/Sprain (base) | 0.000 | - | - | 1.00 |
| Injury Type | Contusion | -0.248 | 0.035 | <0.001 | 0.78 |
| Injury Type | Laceration | -0.357 | 0.042 | <0.001 | 0.70 |
| Injury Type | Fracture | 0.548 | 0.038 | <0.001 | 1.73 |
| Injury Type | Burn | 0.718 | 0.058 | <0.001 | 2.05 |
| Injury Type | Cumulative Trauma | 0.850 | 0.045 | <0.001 | 2.34 |
| Body Part | Back/Spine (base) | 0.000 | - | - | 1.00 |
| Body Part | Shoulder/Arm | 0.125 | 0.032 | <0.001 | 1.13 |
| Body Part | Hand/Wrist | -0.185 | 0.028 | <0.001 | 0.83 |
| Body Part | Knee/Leg | 0.095 | 0.030 | 0.002 | 1.10 |
| Body Part | Foot/Ankle | -0.145 | 0.034 | <0.001 | 0.87 |
| Body Part | Head/Neck | 0.285 | 0.038 | <0.001 | 1.33 |
| Body Part | Multiple | 0.425 | 0.042 | <0.001 | 1.53 |
| Age | Per year above 40 | 0.012 | 0.002 | <0.001 | 1.012 |
| State Fee Index | Per 0.1 unit | 0.088 | 0.018 | <0.001 | 1.09 |
| Claim Duration | Per 30 days | 0.024 | 0.004 | <0.001 | 1.02 |

### Appendix B: Data Dictionary

| Field | Description | Source | Format |
|-------|-------------|--------|--------|
| claim_id | Unique claim identifier | WCClaims | VARCHAR(20) |
| injury_type | NCCI injury nature code | WCClaims | VARCHAR(2) |
| body_part | NCCI body part code | WCClaims | VARCHAR(2) |
| claimant_age | Age at date of injury | WCClaims | INTEGER |
| state_code | State of jurisdiction | WCClaims | VARCHAR(2) |
| medical_paid | Total medical payments | WCClaims | DECIMAL(12,2) |
| medical_reserve | Medical case reserve | WCClaims | DECIMAL(12,2) |
| medical_incurred | Paid + Reserve | Calculated | DECIMAL(12,2) |
| days_to_mmi | Days from DOI to MMI | WCClaims | INTEGER |
| surgery_flag | Indicator for surgery | MedicalDetail | BOOLEAN |
| fee_schedule_index | State fee relativity | Reference | DECIMAL(4,2) |

### Appendix C: SQL Data Extraction

```sql
-- Medical Severity Model Training Data Extract
SELECT
    c.claim_id,
    c.accident_date,
    c.injury_type_code,
    c.body_part_code,
    DATEDIFF(year, cl.birth_date, c.accident_date) as claimant_age,
    c.state_code,
    s.fee_schedule_index,
    c.medical_paid_total,
    c.medical_reserve_total,
    c.medical_paid_total + c.medical_reserve_total as medical_incurred,
    DATEDIFF(day, c.accident_date, c.mmi_date) as days_to_mmi,
    CASE WHEN m.surgery_count > 0 THEN 1 ELSE 0 END as surgery_flag
FROM wc_claims c
INNER JOIN claimants cl ON c.claimant_id = cl.claimant_id
INNER JOIN state_fee_schedule s ON c.state_code = s.state_code
LEFT JOIN (
    SELECT claim_id, COUNT(*) as surgery_count
    FROM medical_transactions
    WHERE procedure_type = 'SURGERY'
    GROUP BY claim_id
) m ON c.claim_id = m.claim_id
WHERE c.accident_date BETWEEN '2018-01-01' AND '2022-12-31'
  AND c.claim_status = 'CLOSED'
  AND c.medical_incurred >= 500
  AND c.medical_incurred <= 500000;
```

### Appendix D: Model Training Code

```python
"""
Workers Compensation Medical Severity Model
Training Script
Model ID: WC-MED-SEV-2023
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from statsmodels.genmod.generalized_linear_model import GLM
from statsmodels.genmod import families

def prepare_features(df):
    """Prepare features for medical severity model."""

    # Create dummy variables for categorical features
    injury_dummies = pd.get_dummies(df['injury_type'], prefix='injury')
    body_dummies = pd.get_dummies(df['body_part'], prefix='body')

    # Continuous variable transformations
    df['age_centered'] = df['claimant_age'] - 40
    df['age_centered'] = df['age_centered'].clip(-20, 30)

    # Log transform claim duration
    df['log_duration'] = np.log(df['days_to_mmi'].clip(30, 1095))

    # Combine features
    X = pd.concat([
        injury_dummies.drop('injury_strain_sprain', axis=1),
        body_dummies.drop('body_back_spine', axis=1),
        df[['age_centered', 'fee_schedule_index', 'log_duration']]
    ], axis=1)

    return X

def train_severity_model(df):
    """Train Gamma GLM for medical severity."""

    # Prepare features and target
    X = prepare_features(df)
    X = sm.add_constant(X)
    y = df['medical_incurred']

    # Fit Gamma GLM with log link
    model = GLM(
        y, X,
        family=families.Gamma(link=families.links.Log())
    )

    results = model.fit()

    return results

def validate_model(model, X_test, y_test):
    """Calculate validation metrics."""

    predictions = model.predict(X_test)

    # R-squared (pseudo)
    ss_res = np.sum((y_test - predictions) ** 2)
    ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # RMSE
    rmse = np.sqrt(np.mean((y_test - predictions) ** 2))

    # MAE
    mae = np.mean(np.abs(y_test - predictions))

    # MAPE
    mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100

    return {
        'r_squared': r_squared,
        'rmse': rmse,
        'mae': mae,
        'mape': mape
    }

if __name__ == "__main__":
    # Load data
    df = pd.read_csv("wc_medical_severity_data.csv")

    # Train-test split (temporal)
    train_df = df[df['accident_year'] <= 2021]
    test_df = df[df['accident_year'] == 2022]

    # Train model
    model = train_severity_model(train_df)

    # Validate
    X_test = sm.add_constant(prepare_features(test_df))
    metrics = validate_model(model, X_test, test_df['medical_incurred'])

    print("Model Summary:")
    print(model.summary())
    print("\nValidation Metrics:")
    print(metrics)
```

---

## Document Control

**Version:** 1.0
**Effective Date:** October 1, 2023
**Model Owner:** David Chen, FCAS
**Last Validated:** September 2023
**Next Review:** September 2024

**Approvals:**
- David Chen, FCAS - Model Owner
- Independent Validation: Lisa Park, FCAS
- Model Risk Committee: Approved September 20, 2023

---

**End of Document**
