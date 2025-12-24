---
title: "2023 Homeowners Fire Frequency Model Documentation"
model_id: "HO-FREQ-FIRE-2023"
model_type: "frequency"
portfolio: "homeowners"
peril: "fire"
company: "ABC Insurance Company"
version: "2.0"
effective_date: "2023-07-01"
status: "production"
owner: "Property Actuarial Team"
---

# 2023 Homeowners Fire Frequency Model
## Model Documentation

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes.

---

## Executive Summary

### Model Purpose

The 2023 Homeowners Fire Frequency Model predicts the expected number of fire-related claims per policy-year for ABC Insurance Company's homeowners portfolio. Fire claims include structural fires, cooking fires, electrical fires, and heating equipment fires, but exclude wildfire (modeled separately via catastrophe models).

### Key Results

- **Model Type:** Generalized Linear Model (Poisson with log link)
- **Training Period:** 2018-2022 policy years
- **Validation R²:** 0.24 (acceptable for frequency models)
- **Overall Fire Frequency:** 2.8 claims per 1,000 policy-years
- **Key Predictors:** Protection class, year built, construction type, heating type

### Business Impact

- Enables risk-based pricing differentiation by fire risk characteristics
- Supports underwriting guidelines for high-risk properties
- Provides loss cost estimates for rate filings

---

## Section 1: Business Context

### 1.1 Model Objectives

This model serves multiple business objectives:

1. **Pricing:** Develop fire frequency relativities for rating plan
2. **Underwriting:** Identify high-risk properties for review
3. **Loss Prevention:** Target safety programs at highest-risk segments
4. **Reserving:** Provide frequency component for loss projections

### 1.2 Model Scope

**In Scope:**
- Non-weather fire claims (dwelling fires)
- Fire claims under Coverage A (dwelling) and Coverage C (contents)
- All homeowners policy forms (HO-3, HO-5)
- 15 operating states

**Out of Scope:**
- Wildfire (catastrophe model)
- Lightning-only claims (no resulting fire)
- Arson/fraud (separate model)

### 1.3 Prior Model Comparison

| Metric | Prior Model (2020) | Current Model (2023) |
|--------|-------------------|---------------------|
| Variables | 8 | 12 |
| R² (Validation) | 0.19 | 0.24 |
| Overall Frequency | 3.1 per 1,000 | 2.8 per 1,000 |
| Lift (Top/Bottom Decile) | 2.8x | 3.2x |

**Key Changes from Prior Model:**
- Added heating type as predictor
- Refined protection class treatment
- Updated territory definitions
- Incorporated 3 additional years of data

---

## Section 2: Data Sources

### 2.1 Policy Data

**Source:** PropertyMaster Policy Administration System
**Extraction Date:** January 15, 2023
**Period:** Policy years 2018-2022

**Key Fields:**
- Policy number, effective date, expiration date
- Property address and geocoded location
- Year built, square footage, number of stories
- Construction type (frame, masonry, superior)
- Protection class (1-10)
- Heating type (gas, electric, oil, wood)
- Coverage A limit
- Territory

**Record Count:** 2,847,000 policy-years

**Data Quality:**
- Completeness: 98.2% for required fields
- Year built missing: 2.8% (imputed using territory median)
- Heating type missing: 8.5% (imputed using construction era)

---

### 2.2 Claims Data

**Source:** ClaimsVision Claims Management System
**Extraction Date:** January 15, 2023
**Maturity:** 12+ months from loss date

**Key Fields:**
- Claim number, policy number
- Date of loss, cause of loss code
- Incurred loss (paid + reserve)
- Claim status (open/closed)

**Fire Cause of Loss Codes:**
- 110: Fire - cooking
- 111: Fire - electrical
- 112: Fire - heating equipment
- 113: Fire - smoking
- 114: Fire - other/unknown

**Claim Count:** 7,891 fire claims
**Overall Frequency:** 2.77 per 1,000 policy-years

---

### 2.3 External Data

**ISO Protection Class:**
- Public Protection Classification ratings
- Updated annually
- Matched by address

**Fire Department Data:**
- Distance to nearest fire station
- Fire department capability score
- Water source availability

---

## Section 3: Feature Engineering

### 3.1 Exposure Calculation

```
Exposure (policy-years) = (Policy_End - Policy_Start) / 365.25

Rules:
- Earned exposure used (not written)
- Minimum exposure: 30 days
- Mid-term cancellations prorated
```

### 3.2 Property Age

**Transformation:**
```python
property_age = 2023 - year_built
property_age_capped = min(property_age, 75)

# Age bands for analysis
age_band = pd.cut(property_age, bins=[0, 10, 25, 50, 75, 100],
                   labels=['0-10', '11-25', '26-50', '51-75', '75+'])
```

**Rationale:** Older properties have higher fire frequency due to aging electrical systems, outdated heating equipment, and degraded materials.

---

### 3.3 Protection Class

**ISO PPC Ratings:**

| PPC | Description | Frequency Relativity |
|-----|-------------|---------------------|
| 1-2 | Excellent fire protection | 0.70 |
| 3-4 | Good fire protection | 0.85 |
| 5-6 | Average fire protection | 1.00 (base) |
| 7-8 | Below average | 1.25 |
| 9 | Limited protection | 1.60 |
| 10 | No recognized protection | 2.20 |

**Treatment:**
- Grouped into tiers for credibility
- Linear trend within tiers validated

---

### 3.4 Construction Type

**Categories:**

| Construction | Description | Frequency Relativity |
|--------------|-------------|---------------------|
| Frame | Wood frame construction | 1.15 |
| Masonry | Brick/concrete | 1.00 (base) |
| Superior | Fire-resistive | 0.75 |

**Actuarial Basis:** Frame construction has higher combustibility and fire spread risk.

---

### 3.5 Heating Type

**Categories:**

| Heating Type | Frequency Relativity | Notes |
|--------------|---------------------|-------|
| Electric | 0.85 | Lowest fire risk |
| Gas (forced air) | 1.00 (base) | Standard |
| Gas (radiant) | 1.10 | Slightly higher |
| Oil | 1.25 | Higher fuel risk |
| Wood/pellet | 1.60 | Highest risk |

**Actuarial Basis:** Heating equipment is leading cause of home fires; risk varies by fuel type.

---

## Section 4: Model Specification

### 4.1 Model Structure

**Distribution:** Poisson
**Link Function:** Log
**Offset:** Log(exposure)

**Formula:**
```
log(E[Claims]) = β₀ + β₁×Protection_Class + β₂×Property_Age 
                 + β₃×Construction + β₄×Heating_Type 
                 + β₅×Territory + log(Exposure)
```

### 4.2 Variable Selection Process

**Initial Candidates:** 25 variables
**Final Variables:** 12 variables

**Selection Criteria:**
1. Statistical significance (p < 0.05)
2. Actuarial reasonableness
3. Coefficient stability across folds
4. Lift improvement

**Variables Tested but Rejected:**

| Variable | Reason for Rejection |
|----------|---------------------|
| Square footage | Not significant after controlling for value |
| Number of stories | Correlated with age; age preferred |
| Fireplace indicator | Data quality issues |
| Alarm discount | Selection bias concerns |

---

### 4.3 Coefficient Table

| Variable | Level | Coefficient | Std Error | p-value | Relativity |
|----------|-------|-------------|-----------|---------|------------|
| Intercept | - | -6.142 | 0.089 | <0.001 | - |
| Protection Class | 1-2 | -0.357 | 0.052 | <0.001 | 0.70 |
| Protection Class | 3-4 | -0.163 | 0.038 | <0.001 | 0.85 |
| Protection Class | 5-6 | 0.000 | - | - | 1.00 |
| Protection Class | 7-8 | 0.223 | 0.041 | <0.001 | 1.25 |
| Protection Class | 9-10 | 0.531 | 0.068 | <0.001 | 1.70 |
| Property Age | Per 10 years | 0.042 | 0.008 | <0.001 | 1.04 |
| Construction | Frame | 0.140 | 0.029 | <0.001 | 1.15 |
| Construction | Masonry | 0.000 | - | - | 1.00 |
| Construction | Superior | -0.288 | 0.065 | <0.001 | 0.75 |
| Heating Type | Electric | -0.163 | 0.035 | <0.001 | 0.85 |
| Heating Type | Gas | 0.000 | - | - | 1.00 |
| Heating Type | Oil | 0.223 | 0.048 | <0.001 | 1.25 |
| Heating Type | Wood | 0.470 | 0.072 | <0.001 | 1.60 |

---

## Section 5: Model Validation

### 5.1 Train/Validation/Holdout Split

| Dataset | Period | Policy-Years | Claims | Purpose |
|---------|--------|--------------|--------|---------|
| Train | 2018-2020 | 1,708,000 | 4,892 | Model fitting |
| Validation | 2021 | 569,000 | 1,524 | Hyperparameter tuning |
| Holdout | 2022 | 570,000 | 1,475 | Final evaluation |

### 5.2 Performance Metrics

| Metric | Train | Validation | Holdout |
|--------|-------|------------|---------|
| Deviance R² | 0.26 | 0.24 | 0.23 |
| Pearson χ²/df | 1.02 | 1.04 | 1.03 |
| AIC | 28,450 | 9,520 | 9,380 |
| Top Decile Lift | 3.4x | 3.2x | 3.1x |

### 5.3 Actual vs. Expected by Segment

**By Protection Class:**

| PPC Group | Expected | Actual | A/E Ratio |
|-----------|----------|--------|-----------|
| 1-2 | 412 | 398 | 0.97 |
| 3-4 | 583 | 601 | 1.03 |
| 5-6 | 489 | 485 | 0.99 |
| 7-8 | 298 | 312 | 1.05 |
| 9-10 | 218 | 204 | 0.94 |

**By Property Age:**

| Age Band | Expected | Actual | A/E Ratio |
|----------|----------|--------|-----------|
| 0-10 years | 285 | 271 | 0.95 |
| 11-25 years | 412 | 425 | 1.03 |
| 26-50 years | 498 | 492 | 0.99 |
| 51-75 years | 380 | 387 | 1.02 |
| 75+ years | 425 | 425 | 1.00 |

### 5.4 Calibration Plot

Model calibration tested via decile analysis on holdout set:

| Decile | Predicted Frequency | Actual Frequency | Ratio |
|--------|---------------------|------------------|-------|
| 1 (lowest) | 1.2 per 1,000 | 1.1 per 1,000 | 0.92 |
| 2 | 1.8 per 1,000 | 1.9 per 1,000 | 1.06 |
| 3 | 2.1 per 1,000 | 2.0 per 1,000 | 0.95 |
| 4 | 2.4 per 1,000 | 2.5 per 1,000 | 1.04 |
| 5 | 2.7 per 1,000 | 2.6 per 1,000 | 0.96 |
| 6 | 2.9 per 1,000 | 3.0 per 1,000 | 1.03 |
| 7 | 3.2 per 1,000 | 3.1 per 1,000 | 0.97 |
| 8 | 3.5 per 1,000 | 3.6 per 1,000 | 1.03 |
| 9 | 4.0 per 1,000 | 3.9 per 1,000 | 0.98 |
| 10 (highest) | 4.8 per 1,000 | 5.0 per 1,000 | 1.04 |

---

## Section 6: Model Limitations

### 6.1 Known Limitations

1. **Data Quality:** Year built and heating type have missing values requiring imputation
2. **Trend:** Fire frequency declining over time; model may need recalibration
3. **Arson:** Model does not distinguish accidental from intentional fires
4. **Geographic:** Limited data in some territories reduces credibility
5. **Emerging Risks:** Lithium battery fires not separately modeled

### 6.2 Assumptions

1. Past fire frequency patterns predictive of future
2. Protection class accurately reflects fire response capability
3. Policy characteristics accurately reported
4. No significant change in building codes or fire safety technology

---

## Section 7: Implementation and Monitoring

### 7.1 Implementation Plan

- **Effective Date:** July 1, 2023
- **Rate Filing:** Filed in all 15 states by May 15, 2023
- **System Integration:** Relativities loaded to rating engine
- **Training:** Underwriter training completed June 2023

### 7.2 Monitoring Plan

**Monthly:**
- Fire claim counts vs. expected
- Large fire loss review

**Quarterly:**
- A/E ratios by segment
- Protection class distribution shifts
- New construction mix

**Annual:**
- Full model re-validation
- Coefficient stability check
- Champion/challenger analysis

### 7.3 Trigger for Model Refresh

Model refresh required if:
- A/E ratio outside 0.90-1.10 for 2 consecutive quarters
- R² declines by more than 0.03
- Significant regulatory or market change
- Protection class definitions change

---

## Document Approval

**Prepared by:** David Park, FCAS | Property Actuarial Team
**Reviewed by:** Sarah Mitchell, FCAS | Chief Actuary - Property
**Approved by:** Model Risk Governance Committee

**Approval Date:** June 1, 2023

---

## Appendix A: ASOP Compliance

| ASOP | Section | Compliance Reference |
|------|---------|---------------------|
| ASOP 12 | Risk Classification | Section 3 (variables), Section 4 (coefficients) |
| ASOP 23 | Data Quality | Section 2 (data sources, quality metrics) |
| ASOP 41 | Communications | All sections (clear documentation) |
| ASOP 56 | Modeling | Sections 4-5 (methodology, validation) |

---

**End of Document**
