---
title: "2023 Commercial Auto Liability Severity Model Documentation"
model_id: "CA-SEV-2023-001"
portfolio: "commercial_auto"
type: "model_documentation"
company: "ABC Insurance Company"
version: "1.0"
model_owner: "Jennifer Martinez, FCAS"
effective_date: "2023-07-01"
status: "active"
---

# 2023 Commercial Auto Liability Severity Model

**SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes. No real insurance data, customer information, proprietary methodologies, or confidential information from any insurance company or financial institution is used or simulated.

All names, addresses, policy numbers, claim amounts, and company information are fictional. Any resemblance to actual persons, organizations, or data is purely coincidental.

This project showcases AI agent capabilities for automated documentation generation and is not intended for production use with real data or models.

---

## Executive Summary

### Model Purpose

The 2023 Commercial Auto Liability Severity Model predicts the expected cost per liability claim for commercial auto fleets. This model works in conjunction with the frequency model to produce total loss cost predictions for accurate premium calculations and reserve setting.

### Key Findings

- Injury severity and attorney involvement are the strongest predictors
- Vehicle weight class significantly impacts severity (heavy trucks 1.4x multiplier)
- Jurisdiction tier creates substantial severity variation (2.1x between favorable and nuclear jurisdictions)
- Social inflation trend running at 8% annually (vs. 5% medical-only)
- Model achieves R-squared of 0.35 on holdout data (log-transformed severity)

### Business Impact

- Supports claim-level reserve setting
- Enables jurisdiction-specific rate adjustments
- Identifies high-severity potential claims early
- Improves large loss management through early detection
- Expected annual impact: $6.2M improvement in rate adequacy

---

## 1. Business Context & Objectives

### 1.1 Background

Commercial auto liability severity has experienced significant trend acceleration driven by social inflation, nuclear verdicts, and third-party litigation funding. ABC Insurance Company's commercial auto liability portfolio faces unique challenges:

**Historical Severity Trends:**
- 2018: Average BI severity $48,200
- 2019: Average BI severity $52,400 (+8.7%)
- 2020: Average BI severity $55,800 (+6.5%, COVID-dampened)
- 2021: Average BI severity $62,100 (+11.3%)
- 2022: Average BI severity $68,500 (+10.3%)
- 5-Year CAGR: 9.2% (significantly exceeding medical inflation)

**Severity Drivers:**
- Nuclear verdicts: Verdicts exceeding $10M increased 300% since 2018
- Attorney involvement: 62% of BI claims in 2022 vs. 48% in 2018
- Third-party litigation funding: Enabling longer litigation, higher demands
- Reptile theory litigation tactics: Increasing jury awards
- Social media jury pool influence: More plaintiff-favorable jurors

### 1.2 Business Problem

The primary challenges addressed by this severity model include:

1. **Underestimation of Large Losses**: Prior model significantly underestimated claims >$250K, leading to reserve inadequacy

2. **Jurisdiction Blindness**: Prior model did not adequately capture jurisdiction-level severity variation

3. **Social Inflation Lag**: Traditional trend selection methods lagged actual severity emergence

4. **Attorney Impact**: Attorney involvement multiplier underestimated true impact

5. **Heavy Vehicle Exposure**: Heavy truck claims not adequately differentiated from light vehicle claims

### 1.3 Objectives

**Primary Objectives:**
- Achieve R-squared >= 0.32 on log-transformed severity
- Capture jurisdiction tier effects with 4-level classification
- Incorporate social inflation trend explicitly
- Model attorney involvement with interaction effects
- Apply appropriate large loss treatment ($500K cap)

**Secondary Objectives:**
- Support early identification of potentially nuclear claims
- Enable jurisdiction-specific pricing adjustments
- Improve initial case reserve accuracy
- Provide claims department with severity risk scores

---

## 2. Regulatory Compliance Statement

### 2.1 NAIC Model Audit Rule (MAR)

This model documentation complies with NAIC Model Audit Rule requirements including comprehensive documentation, independent validation, ongoing monitoring procedures, and governance oversight.

### 2.2 Actuarial Standards of Practice (ASOPs)

**ASOP No. 12 - Risk Classification:**
- Severity variables selected based on actuarial relevance
- All variables demonstrate statistically significant relationships
- Jurisdiction tier based on objective litigation environment metrics

**ASOP No. 23 - Data Quality:**
- Claim data quality assessment performed
- Development patterns analyzed to ensure data maturity
- Large loss treatment documented

**ASOP No. 43 - Property/Casualty Unpaid Claim Estimates:**
- Severity model supports reserve estimation
- Development patterns and trends considered
- Large loss loading methodology documented

**ASOP No. 56 - Modeling:**
- Lognormal distribution selection justified
- Validation testing comprehensive
- Social inflation trend assumptions documented

### 2.3 State Requirements

The model complies with commercial auto rating requirements in all 35 states where ABC Insurance operates. Large loss treatment and social inflation trend assumptions documented for rate filing support.

### 2.4 Internal Governance

**Model Approvals:**
- Model Risk Governance Committee: June 12, 2023
- Chief Actuary: June 15, 2023
- Chief Claims Officer: June 16, 2023
- Pricing Committee: June 22, 2023

---

## 3. Data Sources

### 3.1 Internal Data Sources

**ClaimsVision CA - Commercial Auto Claims**

| Data Type | Description | Records | Date Range |
|-----------|-------------|---------|------------|
| Liability BI Claims | Bodily injury claims | 18,400 | 2017-2022 |
| Closed Claims | Fully settled claims | 15,200 | 2017-2022 |
| Large Losses (>$100K) | High severity claims | 2,850 | 2017-2022 |
| Nuclear Verdicts (>$1M) | Extreme outcomes | 124 | 2017-2022 |

**Key Data Elements:**
- Claim identifiers: Claim number, policy number, vehicle
- Injury details: Severity code, body part, treatment type
- Attorney data: Representation flag, law firm tier, filing date
- Financials: Paid indemnity, paid expense, case reserves
- Jurisdiction: Accident state, venue county

**Data Quality:**
- Closed claim rate at 24 months: 82%
- Attorney flag accuracy: 98%
- Injury severity coding: 94% complete

---

**Litigation Tracking System**

| Data Type | Description | Coverage |
|-----------|-------------|----------|
| Suit Filed Flag | Litigation indicator | 100% of claims |
| Law Firm | Plaintiff attorney firm | 95% of litigated |
| Venue | Court jurisdiction | 98% of litigated |
| Demand History | Settlement demands | 88% of litigated |

---

**Vehicle Data (from FleetMaster)**

| Data Type | Description | Coverage |
|-----------|-------------|----------|
| Vehicle Weight Class | GVW-based classification | 98% |
| Vehicle Type | Truck, van, service | 100% |
| At-Fault Vehicle ID | Vehicle causing accident | 92% |

---

### 3.2 External Data Sources

**Jurisdiction Risk Database**

| Source | Description | Usage |
|--------|-------------|-------|
| ATRA Judicial Hellholes | Litigation environment rankings | Tier assignment |
| Verdict Analytics | Nuclear verdict tracking | Trend analysis |
| State Tort Reform Status | Damage cap information | Severity cap modeling |

**Jurisdiction Tier Assignment:**

| Tier | Definition | % of Claims | Characteristics |
|------|------------|-------------|-----------------|
| Favorable | Strong tort reform, conservative | 22% | TX rural, OH, IN |
| Neutral | Average litigation environment | 45% | Most states |
| Unfavorable | Plaintiff-friendly | 25% | CA, NY, NJ urban |
| Nuclear | Extreme verdict risk | 8% | Cook County, LA, FL tri-county |

---

### 3.3 Data Quality Assessment

**Claim Development:**
- Claims evaluated at 24+ months development
- Open claims excluded (development uncertainty)
- IBNR not included in training data

**Large Loss Treatment:**
- Claims capped at $500K for model training
- Excess load calculated separately (12% of capped losses)
- 124 claims >$1M reviewed individually

**Attorney Flag Validation:**
```
Comparison: Litigation tracking vs. ClaimsVision attorney flag
- Agreement rate: 97.2%
- Discrepancies reviewed and resolved
```

---

## 4. Feature Engineering

### 4.1 Injury Severity Classification

**Severity Categories:**

| Category | Definition | % of Claims | Avg Severity |
|----------|------------|-------------|--------------|
| Minor | Soft tissue, no lost time | 35% | $18,200 |
| Moderate | Fractures, moderate soft tissue | 38% | $42,500 |
| Serious | Significant injury, surgery | 19% | $98,400 |
| Severe/Catastrophic | Permanent impairment, death | 8% | $285,600 |

**Injury Severity Score:**
```python
def classify_injury_severity(claim):
    """
    Classify injury severity based on claim characteristics.
    """
    if claim.death_flag:
        return 'severe_catastrophic'
    elif claim.surgery_flag or claim.hospitalization_days > 7:
        return 'serious'
    elif claim.fracture_flag or claim.hospitalization_days > 0:
        return 'moderate'
    else:
        return 'minor'
```

---

### 4.2 Attorney Involvement

**Attorney Categories:**

| Category | Definition | % of Claims | Severity Multiplier |
|----------|------------|-------------|---------------------|
| No Attorney | Unrepresented claimant | 38% | 1.00 (baseline) |
| Standard Attorney | Typical PI firm | 48% | 2.20 |
| Billboard/TV Firm | High-volume plaintiff firm | 11% | 2.65 |
| Nuclear Firm | Known for large verdicts | 3% | 3.80 |

**Attorney Tier Assignment:**
```python
def classify_attorney_tier(claim):
    """
    Classify attorney tier based on firm characteristics.
    """
    if not claim.attorney_involved:
        return 'no_attorney'
    elif claim.law_firm in NUCLEAR_FIRM_LIST:
        return 'nuclear_firm'
    elif claim.law_firm in BILLBOARD_FIRM_LIST:
        return 'billboard_firm'
    else:
        return 'standard_attorney'
```

---

### 4.3 Vehicle Weight Class

**Weight Categories:**

| Class | GVW (lbs) | % of Claims | Severity Impact |
|-------|-----------|-------------|-----------------|
| Light (<10K) | <10,000 | 42% | 1.00 (baseline) |
| Medium (10-26K) | 10,001-26,000 | 31% | 1.18 |
| Heavy (>26K) | >26,000 | 27% | 1.40 |

**Rationale:** Heavier vehicles cause more damage in collisions, leading to more severe injuries.

---

### 4.4 Jurisdiction Tier

**Tier Definitions:**

| Tier | Criteria | Example Jurisdictions |
|------|----------|----------------------|
| Favorable | Damage caps, conservative juries | TX rural, OH, IN, WI |
| Neutral | Average tort environment | Most suburban/rural areas |
| Unfavorable | No caps, plaintiff-friendly | CA urban, NY, NJ |
| Nuclear | Extreme verdict risk, reptile tactics | Cook County IL, St. Louis, LA parishes |

**Jurisdiction Scoring:**
```python
jurisdiction_tier = {
    'cook_county_il': 'nuclear',
    'st_louis_mo': 'nuclear',
    'los_angeles_ca': 'unfavorable',
    'harris_county_tx': 'neutral',
    'franklin_county_oh': 'favorable',
    # ... additional mappings
}
```

---

### 4.5 Policy Limit

**Limit Categories:**

| Limit | % of Policies | Avg Severity | Impact |
|-------|---------------|--------------|--------|
| $100K CSL | 8% | $38,200 | Baseline |
| $300K CSL | 22% | $48,500 | 1.08 |
| $500K CSL | 35% | $56,800 | 1.15 |
| $1M CSL | 28% | $72,400 | 1.28 |
| $2M+ CSL | 7% | $95,200 | 1.42 |

**Note:** Higher limits correlate with higher severity due to:
- Selection effect (higher-risk fleets buy more coverage)
- Settlement anchoring (demands anchored to available limits)

---

## 5. Methodology

### 5.1 Model Selection

**Approach:** Generalized Linear Model (GLM)
**Distribution:** Lognormal
**Link Function:** Log (identity on log scale)

**Rationale for Lognormal:**

Commercial auto liability severity exhibits heavier tails than personal auto due to:
- Higher damage potential (heavy vehicles)
- Commercial policy limits (higher available recovery)
- Nuclear verdict exposure
- Third-party litigation funding enabling longer litigation

**Distribution Comparison:**

| Distribution | AIC | BIC | Q-Q Plot Fit |
|--------------|-----|-----|--------------|
| Gamma | 285,420 | 285,890 | Poor tail fit |
| Lognormal | 282,150 | 282,620 | Good tail fit |
| Inverse Gaussian | 286,800 | 287,270 | Poor overall fit |

**Selection:** Lognormal provides superior fit, especially in the tail.

### 5.2 Model Specification

```
log(severity) = β₀ + β₁(injury_severity) + β₂(attorney_tier)
                + β₃(vehicle_weight) + β₄(jurisdiction_tier)
                + β₅(policy_limit) + β₆(claimant_age)
                + β₇(injury × attorney_interaction) + ε

Where ε ~ Normal(0, σ²)
```

**Variable Definitions:**

| Variable | Type | Levels/Range | Selection Rationale |
|----------|------|--------------|---------------------|
| Injury Severity | Categorical | 4 levels | Primary cost driver |
| Attorney Tier | Categorical | 4 levels | Litigation impact |
| Vehicle Weight | Categorical | 3 levels | Damage potential |
| Jurisdiction Tier | Categorical | 4 levels | Litigation environment |
| Policy Limit | Categorical | 5 levels | Settlement anchoring |
| Claimant Age | Continuous | 0-90 | Economic damages |
| Injury × Attorney | Interaction | 16 combinations | Non-additive effect |

### 5.3 Large Loss Treatment

**Cap and Load Approach:**

```python
def apply_large_loss_treatment(severity):
    """
    Cap severity at $500K, calculate excess load separately.
    """
    CAP_THRESHOLD = 500000

    capped_severity = min(severity, CAP_THRESHOLD)
    excess_severity = max(0, severity - CAP_THRESHOLD)

    return capped_severity, excess_severity

# Excess load calculation
total_excess = sum(excess_severities)
total_capped = sum(capped_severities)
excess_load_factor = total_excess / total_capped  # ~12%
```

**Rationale for $500K Cap:**
- Commercial auto limits typically $1M+, higher than personal auto
- 12% of claims exceed $100K, 3% exceed $500K
- Large loss volatility distorts GLM coefficients
- Separate excess load provides more stable indication

### 5.4 Social Inflation Trend

**Trend Assumption:**

| Component | Annual Trend | Source |
|-----------|--------------|--------|
| Medical Inflation | 5.0% | CPI-Medical |
| Social Inflation | 3.0% | Verdict analysis |
| **Total BI Trend** | **8.0%** | Combined |

**Social Inflation Indicators:**
- Nuclear verdict frequency: +25% annually
- Attorney involvement rate: +2% annually
- Average verdict amount: +12% annually
- Average settlement amount: +9% annually

**Trend Selection Rationale:**
```
Traditional medical trend alone (5%) insufficient
Verdict and settlement data suggest 8-10% total trend
Selected 8% as supported by industry studies
```

### 5.5 Assumptions

**Key Model Assumptions:**

1. **Lognormal Distribution**: Log-severity approximately normal
   - Validation: Q-Q plot and Shapiro-Wilk test on residuals
   - Result: Acceptable fit, slight heavy tail in extreme cases

2. **Constant Variance**: Homoskedasticity on log scale
   - Validation: Breusch-Pagan test
   - Result: Mild heteroskedasticity acceptable

3. **Full Development**: Claims sufficiently developed
   - Validation: 24-month minimum, 82% closure rate
   - Adjustment: Open claims excluded

4. **No Selection Bias**: Closed claims representative
   - Risk: High-severity claims settle later
   - Mitigation: Development pattern analysis

### 5.6 Limitations

**Known Limitations:**

1. **Nuclear Verdict Uncertainty**: Model capped at $500K; extreme outcomes unpredictable

2. **Jurisdiction Classification Lag**: Nuclear jurisdictions evolve; tier assignments require annual review

3. **Attorney Strategy Changes**: Plaintiff bar tactics evolve (e.g., reptile theory spread)

4. **Third-Party Funding**: Impact of litigation funding not directly modeled

5. **COVID Development**: 2020-2021 claims may have atypical development

6. **Economic Damages**: Claimant income/occupation not captured (data limitations)

---

## 6. Model Results

### 6.1 Coefficient Summary

**Injury Severity:**

| Level | Coefficient | Std Error | P-value | Relativity | Avg Severity |
|-------|-------------|-----------|---------|------------|--------------|
| Minor | 0.000 | - | - | 1.00 | $18,200 |
| Moderate | 0.848 | 0.045 | <0.001 | 2.33 | $42,500 |
| Serious | 1.688 | 0.058 | <0.001 | 5.41 | $98,400 |
| Severe/Catastrophic | 2.752 | 0.082 | <0.001 | 15.68 | $285,600 |

**Attorney Tier:**

| Level | Coefficient | Std Error | P-value | Relativity | Avg Severity |
|-------|-------------|-----------|---------|------------|--------------|
| No Attorney | 0.000 | - | - | 1.00 | $28,400 |
| Standard Attorney | 0.788 | 0.038 | <0.001 | 2.20 | $62,500 |
| Billboard/TV Firm | 0.975 | 0.052 | <0.001 | 2.65 | $75,300 |
| Nuclear Firm | 1.335 | 0.085 | <0.001 | 3.80 | $107,900 |

**Vehicle Weight Class:**

| Level | Coefficient | Std Error | P-value | Relativity | Avg Severity |
|-------|-------------|-----------|---------|------------|--------------|
| Light (<10K) | 0.000 | - | - | 1.00 | $48,200 |
| Medium (10-26K) | 0.166 | 0.032 | <0.001 | 1.18 | $56,900 |
| Heavy (>26K) | 0.336 | 0.038 | <0.001 | 1.40 | $67,500 |

**Jurisdiction Tier:**

| Level | Coefficient | Std Error | P-value | Relativity | Avg Severity |
|-------|-------------|-----------|---------|------------|--------------|
| Favorable | -0.223 | 0.042 | <0.001 | 0.80 | $43,500 |
| Neutral | 0.000 | - | - | 1.00 | $54,400 |
| Unfavorable | 0.336 | 0.038 | <0.001 | 1.40 | $76,200 |
| Nuclear | 0.742 | 0.065 | <0.001 | 2.10 | $114,200 |

**Policy Limit:**

| Level | Coefficient | Std Error | P-value | Relativity | Avg Severity |
|-------|-------------|-----------|---------|------------|--------------|
| $100K CSL | 0.000 | - | - | 1.00 | $38,200 |
| $300K CSL | 0.077 | 0.048 | 0.109 | 1.08 | $41,300 |
| $500K CSL | 0.140 | 0.045 | 0.002 | 1.15 | $43,900 |
| $1M CSL | 0.247 | 0.048 | <0.001 | 1.28 | $48,900 |
| $2M+ CSL | 0.351 | 0.062 | <0.001 | 1.42 | $54,200 |

**Continuous Variables:**

| Variable | Coefficient | Std Error | P-value | Effect |
|----------|-------------|-----------|---------|--------|
| Claimant Age | -0.006 | 0.001 | <0.001 | -0.6% per year |

**Note:** Younger claimants have higher economic damages (lost wages), but older claimants have higher medical costs. Net effect is mild negative relationship.

### 6.2 Interaction Effects

**Attorney × Injury Severity Interaction:**

| Injury Level | No Attorney | Standard | Billboard | Nuclear |
|--------------|-------------|----------|-----------|---------|
| Minor | 1.00 | 1.85 | 2.10 | 2.80 |
| Moderate | 2.33 | 5.12 | 6.17 | 8.86 |
| Serious | 5.41 | 13.52 | 17.57 | 27.04 |
| Severe | 15.68 | 43.90 | 58.87 | 94.56 |

**Interpretation:** Attorney impact is amplified for severe injuries. Nuclear attorneys on severe injuries show 6x multiplier vs. non-attorney baseline.

### 6.3 Model Fit Statistics

| Metric | Value |
|--------|-------|
| R-squared (training) | 0.38 |
| R-squared (holdout) | 0.35 |
| RMSE (log scale) | 0.82 |
| MAE (log scale) | 0.65 |
| MAPE | 42.5% |

**Note:** R-squared of 0.35 on severity is strong given inherent unpredictability of individual claim outcomes.

---

## 7. Model Validation

### 7.1 Data Split

**Temporal Split:**
- Training: 2017-2021 (80% of claims)
- Holdout: 2022 (20% of claims)

**Training Set:**
- Claims: 12,160
- Average Severity: $52,400
- Median Severity: $32,800

**Holdout Set:**
- Claims: 3,040
- Average Severity: $68,500
- Median Severity: $42,100

### 7.2 Holdout Performance

| Metric | Training | Holdout | Degradation |
|--------|----------|---------|-------------|
| R-squared | 0.38 | 0.35 | -0.03 |
| RMSE (log) | 0.78 | 0.82 | +0.04 |
| MAE (log) | 0.62 | 0.65 | +0.03 |
| MAPE | 40.2% | 42.5% | +2.3% |

**Assessment:** Acceptable generalization with minimal overfitting.

### 7.3 Actual vs Expected by Segment

**By Injury Severity:**

| Level | Expected | Actual | A/E Ratio |
|-------|----------|--------|-----------|
| Minor | $18,400 | $18,200 | 0.99 |
| Moderate | $41,800 | $42,500 | 1.02 |
| Serious | $96,200 | $98,400 | 1.02 |
| Severe | $278,400 | $285,600 | 1.03 |

**By Attorney Tier:**

| Tier | Expected | Actual | A/E Ratio |
|------|----------|--------|-----------|
| No Attorney | $27,800 | $28,400 | 1.02 |
| Standard | $61,200 | $62,500 | 1.02 |
| Billboard | $73,800 | $75,300 | 1.02 |
| Nuclear | $105,400 | $107,900 | 1.02 |

**By Jurisdiction Tier:**

| Tier | Expected | Actual | A/E Ratio |
|------|----------|--------|-----------|
| Favorable | $44,200 | $43,500 | 0.98 |
| Neutral | $53,800 | $54,400 | 1.01 |
| Unfavorable | $74,800 | $76,200 | 1.02 |
| Nuclear | $111,200 | $114,200 | 1.03 |

**By Vehicle Weight:**

| Class | Expected | Actual | A/E Ratio |
|-------|----------|--------|-----------|
| Light | $47,400 | $48,200 | 1.02 |
| Medium | $55,800 | $56,900 | 1.02 |
| Heavy | $66,200 | $67,500 | 1.02 |

### 7.4 Large Loss Validation

**Claims >$100K:**

| Predicted Band | Count | Avg Predicted | Avg Actual | A/E |
|----------------|-------|---------------|------------|-----|
| $100K-$150K | 420 | $118,200 | $122,400 | 1.04 |
| $150K-$250K | 285 | $182,400 | $188,600 | 1.03 |
| $250K-$500K | 148 | $328,500 | $342,200 | 1.04 |
| >$500K (capped) | 92 | $500,000 | $845,200 | 1.69* |

*Excess load captures this difference (12% loading applied to capped losses)

### 7.5 Lift Analysis

| Decile | Predicted Avg | Actual Avg | Lift vs Random |
|--------|---------------|------------|----------------|
| 1 (lowest) | $14,200 | $13,800 | 0.25x |
| 2 | $22,400 | $23,100 | 0.42x |
| 3 | $32,600 | $31,800 | 0.58x |
| 4 | $42,800 | $44,200 | 0.80x |
| 5 | $52,400 | $51,600 | 0.94x |
| 6 | $62,800 | $64,500 | 1.17x |
| 7 | $78,400 | $76,200 | 1.38x |
| 8 | $98,600 | $102,400 | 1.86x |
| 9 | $132,400 | $128,600 | 2.33x |
| 10 (highest) | $198,200 | $208,400 | 3.78x |

**Top Decile Lift: 3.78x** demonstrates strong severity discrimination.

---

## 8. Implementation

### 8.1 Production Scoring

**Severity Factor Calculation:**

```python
def calculate_liability_severity_factor(claim):
    """
    Calculate expected liability severity for a commercial auto claim.
    Returns expected severity in dollars.
    """
    base_severity = 54400  # Overall average severity
    factor = 1.0

    # Injury severity factor
    injury_factors = {
        'minor': 1.00,
        'moderate': 2.33,
        'serious': 5.41,
        'severe_catastrophic': 15.68
    }
    injury_factor = injury_factors.get(claim.injury_severity, 1.0)

    # Attorney tier factor
    attorney_factors = {
        'no_attorney': 1.00,
        'standard_attorney': 2.20,
        'billboard_firm': 2.65,
        'nuclear_firm': 3.80
    }
    attorney_factor = attorney_factors.get(claim.attorney_tier, 1.0)

    # Interaction adjustment
    interaction = get_interaction_adjustment(
        claim.injury_severity,
        claim.attorney_tier
    )

    # Vehicle weight factor
    weight_factors = {
        'light': 1.00,
        'medium': 1.18,
        'heavy': 1.40
    }
    weight_factor = weight_factors.get(claim.vehicle_weight_class, 1.0)

    # Jurisdiction tier factor
    jurisdiction_factors = {
        'favorable': 0.80,
        'neutral': 1.00,
        'unfavorable': 1.40,
        'nuclear': 2.10
    }
    jurisdiction_factor = jurisdiction_factors.get(claim.jurisdiction_tier, 1.0)

    # Policy limit factor
    limit_factors = {
        '100k': 1.00,
        '300k': 1.08,
        '500k': 1.15,
        '1m': 1.28,
        '2m_plus': 1.42
    }
    limit_factor = limit_factors.get(claim.policy_limit_tier, 1.0)

    # Claimant age factor
    age_factor = math.exp(-0.006 * (claim.claimant_age - 40))

    # Combine factors
    factor = (injury_factor * interaction * weight_factor *
              jurisdiction_factor * limit_factor * age_factor)

    # Apply trend to accident date
    years_from_base = (claim.accident_date - BASE_DATE).days / 365.25
    trend_factor = (1.08) ** years_from_base

    return base_severity * factor * trend_factor
```

### 8.2 Reserve Setting Integration

**Initial Case Reserve:**
```python
def set_initial_liability_reserve(claim):
    """
    Set initial liability case reserve based on model prediction.
    """
    predicted_severity = calculate_liability_severity_factor(claim)

    # Apply development factor based on claim age
    development_factor = get_liability_development_factor(
        claim.days_since_accident
    )

    # Calculate ultimate expected severity
    ultimate_severity = predicted_severity * development_factor

    # Apply large loss loading for high predictions
    if predicted_severity > 100000:
        ultimate_severity *= 1.12  # 12% excess load

    # Initial reserve = ultimate minus paid to date
    initial_reserve = ultimate_severity - claim.indemnity_paid_to_date

    return max(initial_reserve, 0)
```

### 8.3 High-Severity Alert System

**Alert Triggers:**
```python
def evaluate_severity_alerts(claim):
    """
    Generate alerts for high-severity potential claims.
    """
    predicted = calculate_liability_severity_factor(claim)
    alerts = []

    # Tier 1: Nuclear potential
    if predicted > 500000:
        alerts.append({
            'level': 'CRITICAL',
            'message': 'Nuclear verdict potential',
            'action': 'Escalate to senior claims counsel'
        })

    # Tier 2: High severity
    elif predicted > 250000:
        alerts.append({
            'level': 'HIGH',
            'message': 'High severity potential',
            'action': 'Assign to experienced adjuster'
        })

    # Tier 3: Elevated severity
    elif predicted > 100000:
        alerts.append({
            'level': 'ELEVATED',
            'message': 'Elevated severity potential',
            'action': 'Enhanced monitoring'
        })

    return alerts
```

### 8.4 System Integration

**Data Flow:**
1. Claim created at FNOL with initial injury coding
2. Attorney involvement flagged as identified
3. Jurisdiction tier assigned based on accident location
4. Severity model scores claim within 24 hours
5. Alerts generated for high-severity predictions
6. Reserves adjusted based on model output
7. Re-scoring triggered when key variables change

**API Endpoint:**
```
POST /api/v1/commercial-auto/severity-score
Input: claim_id, injury_severity, attorney_tier, vehicle_weight,
       jurisdiction, policy_limit, claimant_age
Output: predicted_severity, confidence_interval, risk_tier, alerts
```

---

## 9. Monitoring Plan

### 9.1 Key Performance Indicators

**Monthly Monitoring:**

| Metric | Target | Yellow Alert | Red Alert |
|--------|--------|--------------|-----------|
| A/E Ratio (Overall) | 0.95-1.05 | 0.90-0.95 or 1.05-1.10 | <0.90 or >1.10 |
| Large Loss A/E (>$100K) | 0.90-1.10 | 0.85-1.15 | <0.85 or >1.15 |
| Nuclear Jurisdiction A/E | 0.90-1.10 | 0.85-1.15 | <0.85 or >1.15 |
| Reserve Adequacy | 98-102% | 95-105% | <95% or >105% |

**Quarterly Monitoring:**

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| R-squared (rolling 12mo) | >0.32 | <0.28 |
| Top Decile Lift | >3.0x | <2.5x |
| Social Inflation Trend | 7-9% | <5% or >12% |
| Coefficient Stability | Within 20% | >25% change |

### 9.2 Social Inflation Tracking

**Quarterly Social Inflation Report:**

| Indicator | Current | Prior Year | Change |
|-----------|---------|------------|--------|
| Nuclear Verdict Count | TBD | TBD | TBD% |
| Average Verdict Amount | TBD | TBD | TBD% |
| Attorney Involvement Rate | TBD | TBD | TBD% |
| Average Time to Settlement | TBD | TBD | TBD% |

**Trend Adjustment Protocol:**
- If social inflation exceeds 10% for 2 consecutive quarters, escalate to Chief Actuary
- Consider trend assumption revision at annual model review
- Document trend emergence in monitoring log

### 9.3 Monitoring Dashboard

**Weekly Alerts:**
- Claims with predicted severity >$250K
- Nuclear jurisdiction claims with attorney involvement
- Severity predictions >2x initial reserve
- New nuclear firm involvement

**Monthly Reports:**
- A/E by injury severity, attorney tier, jurisdiction, vehicle weight
- Severity trend emergence by accident quarter
- Reserve adequacy by cohort
- Model score distribution

### 9.4 Model Refresh Schedule

| Activity | Frequency | Responsibility |
|----------|-----------|----------------|
| KPI Review | Monthly | Actuarial Analyst |
| Full Validation | Quarterly | Senior Actuary |
| Social Inflation Review | Quarterly | Model Owner |
| Coefficient Update | Annual | Model Owner |
| Jurisdiction Tier Review | Annual | Model Risk Committee |
| Major Revision | 3-5 years | Model Risk Committee |

### 9.5 Escalation Procedures

**Level 1 - Elevated Monitoring:**
- Trigger: A/E 1.05-1.10 for 2 consecutive months
- Action: Enhanced monitoring, segment deep-dive
- Owner: Actuarial Analyst

**Level 2 - Model Review:**
- Trigger: A/E >1.10 or R² <0.30
- Action: Full model review, trend analysis
- Owner: Model Owner / Senior Actuary

**Level 3 - Model Override:**
- Trigger: A/E >1.15 or systematic bias identified
- Action: Temporary trend adjustment, expedited revision
- Owner: Chief Actuary / Model Risk Committee

---

## Appendices

### Appendix A: Full Coefficient Table

**Model Specification:**
```
log(severity) = β₀ + Σ βᵢ × Xᵢ + ε
ε ~ Normal(0, σ²)

Distribution: Lognormal
σ (residual std): 0.82
```

**Complete Coefficient Estimates:**

| Variable | Level | Coefficient | Std Error | P-value | Relativity |
|----------|-------|-------------|-----------|---------|------------|
| Intercept | - | 10.52 | 0.08 | <0.001 | - |
| Injury | Minor (base) | 0.000 | - | - | 1.00 |
| Injury | Moderate | 0.848 | 0.045 | <0.001 | 2.33 |
| Injury | Serious | 1.688 | 0.058 | <0.001 | 5.41 |
| Injury | Severe | 2.752 | 0.082 | <0.001 | 15.68 |
| Attorney | None (base) | 0.000 | - | - | 1.00 |
| Attorney | Standard | 0.788 | 0.038 | <0.001 | 2.20 |
| Attorney | Billboard | 0.975 | 0.052 | <0.001 | 2.65 |
| Attorney | Nuclear | 1.335 | 0.085 | <0.001 | 3.80 |
| Weight | Light (base) | 0.000 | - | - | 1.00 |
| Weight | Medium | 0.166 | 0.032 | <0.001 | 1.18 |
| Weight | Heavy | 0.336 | 0.038 | <0.001 | 1.40 |
| Jurisdiction | Favorable | -0.223 | 0.042 | <0.001 | 0.80 |
| Jurisdiction | Neutral (base) | 0.000 | - | - | 1.00 |
| Jurisdiction | Unfavorable | 0.336 | 0.038 | <0.001 | 1.40 |
| Jurisdiction | Nuclear | 0.742 | 0.065 | <0.001 | 2.10 |
| Limit | $100K (base) | 0.000 | - | - | 1.00 |
| Limit | $300K | 0.077 | 0.048 | 0.109 | 1.08 |
| Limit | $500K | 0.140 | 0.045 | 0.002 | 1.15 |
| Limit | $1M | 0.247 | 0.048 | <0.001 | 1.28 |
| Limit | $2M+ | 0.351 | 0.062 | <0.001 | 1.42 |
| Claimant Age | Per year | -0.006 | 0.001 | <0.001 | 0.994 |

### Appendix B: Jurisdiction Tier Mapping

**Nuclear Jurisdictions:**

| Jurisdiction | State | Characteristics |
|--------------|-------|-----------------|
| Cook County | IL | Reptile theory, high verdicts |
| St. Louis City | MO | Plaintiff-friendly, no caps |
| St. Clair County | IL | Madison County alternative |
| Orleans Parish | LA | High verdicts, no caps |
| Miami-Dade | FL | Nuclear verdict hotspot |
| Broward County | FL | High attorney involvement |
| Palm Beach | FL | Large verdicts |
| Los Angeles | CA | High costs, no caps |

### Appendix C: Data Dictionary

| Field | Description | Source | Format |
|-------|-------------|--------|--------|
| claim_id | Unique claim identifier | ClaimsVision | VARCHAR(20) |
| accident_date | Date of accident | ClaimsVision | DATE |
| injury_severity | Severity classification | ClaimsVision | VARCHAR(20) |
| attorney_tier | Attorney firm tier | Litigation Tracking | VARCHAR(20) |
| vehicle_weight_class | GVW-based class | FleetMaster | VARCHAR(15) |
| jurisdiction_tier | Litigation environment | Reference | VARCHAR(15) |
| policy_limit | Policy limit tier | PolicyAdmin | VARCHAR(10) |
| claimant_age | Claimant age at accident | ClaimsVision | INTEGER |
| indemnity_paid | Total indemnity paid | ClaimsVision | DECIMAL(12,2) |
| indemnity_reserve | Indemnity case reserve | ClaimsVision | DECIMAL(12,2) |
| total_incurred | Paid + Reserve | Calculated | DECIMAL(12,2) |

### Appendix D: SQL Data Extraction

```sql
-- Commercial Auto Liability Severity Model Training Data
SELECT
    c.claim_id,
    c.accident_date,
    c.injury_severity_code,
    CASE
        WHEN l.law_firm_id IN (SELECT firm_id FROM nuclear_firms) THEN 'nuclear_firm'
        WHEN l.law_firm_id IN (SELECT firm_id FROM billboard_firms) THEN 'billboard_firm'
        WHEN l.attorney_involved = 1 THEN 'standard_attorney'
        ELSE 'no_attorney'
    END as attorney_tier,
    v.gvw_class as vehicle_weight_class,
    j.jurisdiction_tier,
    p.limit_tier as policy_limit,
    DATEDIFF(year, cl.birth_date, c.accident_date) as claimant_age,
    c.indemnity_paid + c.indemnity_reserve as total_incurred
FROM ca_claims c
INNER JOIN litigation_tracking l ON c.claim_id = l.claim_id
INNER JOIN vehicles v ON c.vehicle_id = v.vehicle_id
INNER JOIN jurisdiction_tiers j ON c.venue_county = j.county_code
INNER JOIN policies p ON c.policy_number = p.policy_number
LEFT JOIN claimants cl ON c.claimant_id = cl.claimant_id
WHERE c.accident_date BETWEEN '2017-01-01' AND '2022-12-31'
  AND c.claim_status = 'CLOSED'
  AND c.coverage_type = 'LIABILITY_BI'
  AND c.total_incurred >= 500
  AND c.total_incurred <= 500000;  -- Capped for training
```

### Appendix E: Model Training Code

```python
"""
Commercial Auto Liability Severity Model
Training Script
Model ID: CA-SEV-2023-001
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats

def prepare_features(df):
    """Prepare features for severity model."""

    # Create dummy variables
    injury_dummies = pd.get_dummies(df['injury_severity'], prefix='injury')
    attorney_dummies = pd.get_dummies(df['attorney_tier'], prefix='attorney')
    weight_dummies = pd.get_dummies(df['vehicle_weight_class'], prefix='weight')
    jurisdiction_dummies = pd.get_dummies(df['jurisdiction_tier'], prefix='jurisdiction')
    limit_dummies = pd.get_dummies(df['policy_limit'], prefix='limit')

    # Drop baseline categories
    injury_dummies = injury_dummies.drop('injury_minor', axis=1, errors='ignore')
    attorney_dummies = attorney_dummies.drop('attorney_no_attorney', axis=1, errors='ignore')
    weight_dummies = weight_dummies.drop('weight_light', axis=1, errors='ignore')
    jurisdiction_dummies = jurisdiction_dummies.drop('jurisdiction_neutral', axis=1, errors='ignore')
    limit_dummies = limit_dummies.drop('limit_100k', axis=1, errors='ignore')

    # Age transformation
    df['age_centered'] = df['claimant_age'] - 40

    # Interaction terms
    for inj in ['moderate', 'serious', 'severe']:
        for att in ['standard_attorney', 'billboard_firm', 'nuclear_firm']:
            col_name = f'interact_{inj}_{att}'
            df[col_name] = (
                (df['injury_severity'] == inj).astype(int) *
                (df['attorney_tier'] == att).astype(int)
            )

    # Combine features
    interaction_cols = [c for c in df.columns if c.startswith('interact_')]
    X = pd.concat([
        injury_dummies,
        attorney_dummies,
        weight_dummies,
        jurisdiction_dummies,
        limit_dummies,
        df[['age_centered'] + interaction_cols]
    ], axis=1)

    return X

def train_severity_model(df):
    """Train Lognormal GLM for liability severity."""

    # Prepare features and target
    X = prepare_features(df)
    X = sm.add_constant(X)
    y = np.log(df['total_incurred'])  # Log-transform for lognormal

    # Fit OLS on log scale (equivalent to lognormal GLM)
    model = sm.OLS(y, X)
    results = model.fit()

    return results

def calculate_r_squared(model, X, y):
    """Calculate R-squared on log scale."""
    predictions = model.predict(X)
    ss_res = np.sum((y - predictions) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - (ss_res / ss_tot)

if __name__ == "__main__":
    # Load data
    df = pd.read_csv("ca_severity_data.csv")

    # Train-test split (temporal)
    train_df = df[df['accident_year'] <= 2021]
    test_df = df[df['accident_year'] == 2022]

    # Train model
    model = train_severity_model(train_df)

    # Validate
    X_test = sm.add_constant(prepare_features(test_df))
    y_test = np.log(test_df['total_incurred'])
    r_squared = calculate_r_squared(model, X_test, y_test)

    print("Model Summary:")
    print(model.summary())
    print(f"\nHoldout R-squared: {r_squared:.3f}")
```

---

## Document Control

**Version:** 1.0
**Effective Date:** July 1, 2023
**Model Owner:** Jennifer Martinez, FCAS
**Last Validated:** June 2023
**Next Review:** June 2024

**Approvals:**
- Jennifer Martinez, FCAS - Model Owner
- Independent Validation: Thomas Wright, FCAS
- Chief Claims Officer: Patricia Davis
- Model Risk Committee: Approved June 22, 2023

---

**End of Document**
