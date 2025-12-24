---
title: "2023 Homeowners Wind/Hail Severity Model Documentation"
model_id: "HO-SEV-WIND-2023"
model_type: "severity"
portfolio: "homeowners"
peril: "wind_hail"
company: "ABC Insurance Company"
version: "1.5"
effective_date: "2023-07-01"
status: "production"
owner: "Property Actuarial Team"
---

# 2023 Homeowners Wind/Hail Severity Model
## Model Documentation

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes.

---

## Executive Summary

### Model Purpose

The 2023 Homeowners Wind/Hail Severity Model predicts the average cost per wind or hail claim for ABC Insurance Company's homeowners portfolio. This model covers non-catastrophe wind and hail events; large CAT events are modeled separately using third-party catastrophe models.

### Key Results

- **Model Type:** Generalized Linear Model (Gamma with log link)
- **Training Period:** 2018-2022 accident years
- **Validation R²:** 0.31
- **Average Severity:** $12,450 per claim
- **Key Predictors:** Roof age, roof type, Coverage A limit, deductible, construction type

### Business Impact

- Enables accurate pricing of wind/hail exposure
- Supports roof age underwriting guidelines
- Informs deductible selection recommendations

---

## Section 1: Business Context

### 1.1 Model Objectives

1. **Pricing:** Develop severity factors for wind/hail loss costs
2. **Underwriting:** Support roof condition guidelines
3. **Reinsurance:** Provide non-CAT wind/hail severity for treaty analysis
4. **Claims:** Benchmark claim settlements against expected severity

### 1.2 Model Scope

**In Scope:**
- Non-catastrophe wind claims (thunderstorms, isolated hail)
- Roof damage, siding damage, fence damage, tree damage
- Coverage A and Coverage B losses
- Claims with incurred >$500 (excludes glass-only)

**Out of Scope:**
- Catastrophe-designated events (separate CAT model)
- Hurricane and tropical storm claims
- Tornado claims (unless non-CAT)
- Contents-only claims (modeled separately)

### 1.3 CAT vs. Non-CAT Definition

**CAT Designation Criteria:**
- PCS (Property Claim Services) designated event
- Industry losses >$25 million
- Named tropical systems

**This Model:** Non-CAT only (CAT events removed from training data)

---

## Section 2: Data Sources

### 2.1 Claims Data

**Source:** ClaimsVision Claims Management System
**Extraction Date:** February 1, 2023
**Maturity:** 18+ months from loss date (development complete)

**Key Fields:**
- Claim number, date of loss
- Cause of loss: Wind (130), Hail (131)
- Total incurred (paid + reserve)
- Coverage allocation (A, B, C)
- Deductible applied
- CAT flag (excluded if Y)

**Claim Count:** 18,456 non-CAT wind/hail claims
**Average Severity:** $12,450

**Severity Distribution:**

| Percentile | Severity |
|------------|----------|
| 10th | $2,100 |
| 25th | $4,500 |
| 50th (Median) | $8,200 |
| 75th | $15,400 |
| 90th | $28,700 |
| 95th | $42,500 |
| 99th | $85,200 |

---

### 2.2 Policy Data

**Source:** PropertyMaster (linked by policy number)

**Key Fields:**
- Coverage A limit
- Deductible (all-peril and wind/hail specific)
- Roof age (years since installation/replacement)
- Roof type (asphalt shingle, tile, metal, slate)
- Construction type
- Year built
- Territory

**Data Quality:**
- Roof age available: 62% of policies (imputed for remainder)
- Roof type available: 78% of policies

---

### 2.3 Third-Party Data

**Roof Condition Scores (Aerial Imagery):**
- Partner: EagleView / Verisk
- Coverage: 45% of portfolio
- Used for validation, not model input

**Replacement Cost Data:**
- CoreLogic replacement cost estimates
- Used to validate Coverage A limits

---

## Section 3: Feature Engineering

### 3.1 Severity Calculation

```
Gross Severity = Total Incurred (Paid + Reserve)
Net Severity = Gross Severity - Deductible Applied

Model Target: Gross Severity (deductible modeled separately)
```

**Development Adjustment:**
- Claims developed to ultimate using 18-month factors
- Development factor: 1.02 average

---

### 3.2 Roof Age

**Transformation:**
```python
roof_age = current_year - roof_install_year
roof_age_capped = min(roof_age, 30)  # Cap at 30 years

# Imputation for missing
roof_age_imputed = where(roof_age.isna(), 
                         property_age * 0.6,  # Assume roof replaced at 60% of property age
                         roof_age)
```

**Actuarial Basis:**
- Older roofs more susceptible to damage
- Granule loss, brittleness increase with age
- Repair vs. replace decision affected by age

**Severity Relativities:**

| Roof Age | Relativity | Basis |
|----------|------------|-------|
| 0-5 years | 0.75 | New roofs more resilient |
| 6-10 years | 0.90 | Good condition |
| 11-15 years | 1.00 (base) | Average |
| 16-20 years | 1.20 | Aging, more repair needed |
| 21-25 years | 1.45 | Often requires replacement |
| 26+ years | 1.75 | Full replacement likely |

---

### 3.3 Roof Type

**Categories:**

| Roof Type | Relativity | Notes |
|-----------|------------|-------|
| Asphalt 3-tab | 1.15 | Most common, moderate durability |
| Asphalt architectural | 1.00 (base) | Better impact resistance |
| Metal | 0.80 | Highly resistant to hail |
| Tile (clay/concrete) | 0.90 | Good resistance, expensive repair |
| Slate | 0.85 | Very durable |
| Wood shake | 1.35 | Higher damage susceptibility |

**Impact Resistance Classes:**
- Class 4 (highest): Metal, some architectural shingles
- Class 3: Quality architectural shingles
- Class 1-2: Standard 3-tab, wood shake

---

### 3.4 Coverage A Limit

**Transformation:**
```python
cov_a_log = np.log(coverage_a_limit)

# Or banded
cov_a_band = pd.cut(coverage_a_limit, 
                    bins=[0, 150000, 250000, 400000, 600000, np.inf],
                    labels=['<$150K', '$150-250K', '$250-400K', '$400-600K', '>$600K'])
```

**Rationale:** Higher-value homes have higher repair costs (better materials, larger structures).

---

### 3.5 Deductible

**Deductible Types:**
- Flat deductible: $500, $1,000, $2,500, $5,000
- Percentage deductible: 1%, 2%, 5% of Coverage A (wind/hail specific)

**Treatment:**
- Model gross severity
- Apply deductible factor separately in loss cost calculation
- Account for "disappearing deductible" effect at higher severities

---

## Section 4: Model Specification

### 4.1 Model Structure

**Distribution:** Gamma
**Link Function:** Log
**Weight:** None (each claim equally weighted)

**Formula:**
```
log(E[Severity]) = β₀ + β₁×Roof_Age + β₂×Roof_Type + β₃×log(Cov_A) 
                   + β₄×Construction + β₅×Territory
```

### 4.2 Distribution Selection

**Tested Distributions:**

| Distribution | AIC | Residual Pattern |
|--------------|-----|------------------|
| Gamma | 215,420 | Good fit |
| Lognormal | 216,890 | Slight underfit at tail |
| Inverse Gaussian | 218,450 | Overfit at tail |
| Tweedie (p=1.5) | 215,680 | Similar to Gamma |

**Selection:** Gamma chosen for balance of fit and parsimony.

---

### 4.3 Coefficient Table

| Variable | Level | Coefficient | Std Error | p-value | Relativity |
|----------|-------|-------------|-----------|---------|------------|
| Intercept | - | 7.824 | 0.156 | <0.001 | - |
| Roof Age | Per 5 years | 0.095 | 0.012 | <0.001 | 1.10 |
| Roof Type | Asphalt 3-tab | 0.140 | 0.028 | <0.001 | 1.15 |
| Roof Type | Asphalt arch | 0.000 | - | - | 1.00 |
| Roof Type | Metal | -0.223 | 0.052 | <0.001 | 0.80 |
| Roof Type | Tile | -0.105 | 0.045 | 0.020 | 0.90 |
| Roof Type | Wood shake | 0.300 | 0.068 | <0.001 | 1.35 |
| log(Cov A) | Per unit | 0.412 | 0.024 | <0.001 | varies |
| Construction | Frame | 0.095 | 0.022 | <0.001 | 1.10 |
| Construction | Masonry | 0.000 | - | - | 1.00 |

---

## Section 5: Model Validation

### 5.1 Train/Validation/Holdout Split

| Dataset | Period | Claims | Avg Severity | Purpose |
|---------|--------|--------|--------------|---------|
| Train | 2018-2020 | 11,074 | $11,850 | Model fitting |
| Validation | 2021 | 3,691 | $12,640 | Tuning |
| Holdout | 2022 | 3,691 | $13,180 | Final evaluation |

*Note: 2022 severity higher due to inflation*

### 5.2 Performance Metrics

| Metric | Train | Validation | Holdout |
|--------|-------|------------|---------|
| R² | 0.34 | 0.31 | 0.29 |
| MAE | $4,250 | $4,580 | $4,820 |
| MAPE | 38% | 41% | 43% |
| Gini | 0.42 | 0.39 | 0.38 |

### 5.3 Actual vs. Expected by Segment

**By Roof Age:**

| Roof Age | Expected Avg | Actual Avg | Ratio |
|----------|--------------|------------|-------|
| 0-5 | $9,340 | $9,120 | 0.98 |
| 6-10 | $11,200 | $11,450 | 1.02 |
| 11-15 | $12,450 | $12,380 | 0.99 |
| 16-20 | $14,940 | $15,280 | 1.02 |
| 21+ | $18,240 | $17,850 | 0.98 |

**By Roof Type:**

| Roof Type | Expected Avg | Actual Avg | Ratio |
|-----------|--------------|------------|-------|
| Asphalt 3-tab | $13,450 | $13,680 | 1.02 |
| Asphalt arch | $11,700 | $11,580 | 0.99 |
| Metal | $9,360 | $9,150 | 0.98 |
| Tile | $10,530 | $10,820 | 1.03 |

### 5.4 Large Loss Analysis

**Large Loss Definition:** Claims >$50,000

| Segment | Large Loss % | Expected | Actual |
|---------|--------------|----------|--------|
| Roof 0-10 years | 2.8% | 3.0% | 2.6% |
| Roof 11-20 years | 5.2% | 5.0% | 5.4% |
| Roof 21+ years | 8.5% | 8.2% | 8.8% |

**Finding:** Older roofs have disproportionate large loss frequency (often full roof replacement).

---

## Section 6: Trend Analysis

### 6.1 Historical Severity Trend

| Year | Avg Severity | YoY Change |
|------|--------------|------------|
| 2018 | $10,250 | - |
| 2019 | $10,890 | +6.2% |
| 2020 | $11,420 | +4.9% |
| 2021 | $12,180 | +6.7% |
| 2022 | $13,180 | +8.2% |

**5-Year Average Trend:** 6.5% annual

### 6.2 Trend Drivers

1. **Material Costs:** Roofing materials +8-10% annually (2021-2022)
2. **Labor Costs:** Contractor rates +5-7% annually
3. **Matching Requirements:** Insurance-to-code requirements increasing
4. **Demand Surge:** Local events create contractor shortages

### 6.3 Prospective Trend Assumption

**Selected Trend:** 6.0% annual (moderated from recent highs)

---

## Section 7: Model Limitations

### 7.1 Known Limitations

1. **Roof Age Data:** 38% imputed, may reduce accuracy
2. **CAT Threshold:** Non-CAT/CAT boundary may shift claim mix
3. **Geographic Concentration:** Some territories lack credibility
4. **Material Costs:** Rapid inflation may outpace model
5. **Depreciation:** Model does not address actual cash value vs. replacement cost

### 7.2 Assumptions

1. Gamma distribution appropriate for claim severity
2. Roof age has linear effect on log-severity
3. Non-CAT and CAT events have similar severity drivers
4. Coverage limit is proxy for property quality

---

## Section 8: Implementation and Monitoring

### 8.1 Monitoring Plan

**Monthly:**
- Average severity vs. expected
- Large loss counts
- Material cost indices

**Quarterly:**
- A/E by roof age band
- Severity trend update
- CAT vs. non-CAT mix

**Annual:**
- Full re-validation
- Roof age factor recalibration
- Trend assumption review

### 8.2 Trigger for Refresh

- A/E ratio outside 0.90-1.10 for 2 quarters
- Material cost inflation >10% deviation from assumption
- Significant change in roof technology or building codes

---

## Document Approval

**Prepared by:** Emily Chen, FCAS | Property Actuarial Team
**Reviewed by:** Sarah Mitchell, FCAS | Chief Actuary - Property
**Approved by:** Model Risk Governance Committee

**Approval Date:** June 1, 2023

---

**End of Document**
