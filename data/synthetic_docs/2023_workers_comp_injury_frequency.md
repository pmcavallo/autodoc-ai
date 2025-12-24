---
title: "2023 Workers Compensation Injury Frequency Model Documentation"
model_id: "WC-INJ-FREQ-2023"
portfolio: "workers_comp"
type: "model_documentation"
company: "ABC Insurance Company"
version: "1.0"
model_owner: "David Chen, FCAS"
effective_date: "2023-10-01"
status: "active"
---

# 2023 Workers Compensation Injury Frequency Model

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes.

---

## Executive Summary

### Model Purpose

The 2023 Workers Compensation Injury Frequency Model predicts the expected claim frequency per $100 of payroll by classification code, employer characteristics, and state. This model supports loss cost development, experience rating, and underwriting risk assessment.

### Key Findings

- NCCI class code is the dominant predictor of frequency
- Employer size (payroll) shows significant frequency benefit
- Model achieves AUC of 0.68 on holdout data
- Frequency declined 2% from prior model (safety improvements)

### Business Impact

- Supports class code loss cost relativities
- Enables experience modification validation
- Improves small account underwriting
- Informs safety program ROI analysis

---

## Model Scope and Objectives

### Scope

**In Scope:**
- All workers compensation indemnity claims
- Medical-only claims (for total frequency)
- Claims across all NCCI and independent bureau states

**Out of Scope:**
- Monopolistic state experience (OH, WA, WY, ND)
- Claims with $0 ultimate incurred
- Fraudulent claims (excluded post-investigation)

### Objectives

1. Predict annual claim frequency by payroll exposure
2. Validate NCCI class code relativities
3. Identify employer-level risk factors
4. Support loss cost filings

---

## Data Sources

### Internal Data

| Source | Description | Records | Date Range |
|--------|-------------|---------|------------|
| WCPolicy | Policy and employer data | 85,000 policies | 2018-2022 |
| WCClaims | Indemnity and medical claims | 28,400 | 2018-2022 |
| PayrollAudit | Audited payroll by class | 72,000 | 2018-2022 |

### External Data

| Source | Description | Usage |
|--------|-------------|-------|
| NCCI | Class code definitions, loss costs | Benchmark |
| BLS | Industry injury rates | Validation |
| D&B | Employer firmographics | Enrichment |

### Data Quality

**Payroll Accuracy:**
- 88% of policies have audited payroll
- Estimated-to-audit ratio: Mean 0.98, Std Dev 0.18
- Class code corrections at audit: 12%

**Claim Data:**
- Indemnity claims: 18,200
- Medical-only claims: 10,200
- Average lag to report: 8 days

---

## Feature Engineering

### Classification

**NCCI Class Code Grouping:**
```python
# 600+ class codes grouped into 25 hazard groups
class_group = ncci_class_to_hazard_group[class_code]

Hazard Groups:
- Clerical/Professional (8810, 8820): Lowest risk
- Manufacturing-Light (3681, 3632): Low-Medium
- Construction-Light (5403, 5183): Medium
- Healthcare (8832, 8833): Medium
- Construction-Heavy (5022, 5213): High
- Trucking (7219, 7228): Highest
```

**Governing Class:**
```python
governing_class = class_with_max_payroll(policy)

# Exclude standard exceptions
excluded = ['8810', '8742', '8803']  # Clerical, outside sales, auditors
```

### Employer Characteristics

**Employer Size (Payroll):**
```python
total_payroll = sum(audited_payroll_by_class)

size_tier = pd.cut(total_payroll, 
                   bins=[0, 100000, 500000, 2000000, 10000000, float('inf')],
                   labels=['Micro', 'Small', 'Medium', 'Large', 'Jumbo'])
```

**Years in Business:**
```python
years_in_business = current_year - business_start_year

# Capped at 25 years
years_capped = min(years_in_business, 25)
```

**Experience Modification:**
```python
# Prior experience mod (if experience-rated)
prior_mod = experience_mod_prior_term

# New business has no mod (assigned 1.0 for modeling)
```

### State Factors

**State Benefit Index:**
```
Relative benefit generosity by state
Base = 1.0 (median state)

High benefit states: CA (1.25), NY (1.20), NJ (1.15)
Low benefit states: TX (0.85), FL (0.90), IN (0.92)
```

---

## Methodology

### Model Selection

**Approach:** Generalized Linear Model (GLM)
**Distribution:** Poisson
**Link Function:** Log
**Offset:** Log(payroll / 100)

**Rationale:**
- Poisson appropriate for claim counts
- Payroll exposure in offset
- Aligns with NCCI loss cost methodology

### Model Specification

```
log(E[claims]) = β₀ + β₁(hazard_group) + β₂(employer_size) 
                 + β₃(years_in_business) + β₄(state_benefit_index)
                 + β₅(prior_experience_mod) + log(payroll/100)
```

### Variable Selection

**Final Model Variables:**
| Variable | Type | Levels | Selection Rationale |
|----------|------|--------|---------------------|
| Hazard Group | Categorical | 25 | Industry risk differences |
| Employer Size | Categorical | 5 | Safety resources, selection |
| Years in Business | Continuous | Capped 25 | Experience, stability |
| State Benefit Index | Continuous | - | Claim filing propensity |
| Prior Experience Mod | Continuous | - | Historical loss indicator |

---

## Model Results

### Coefficient Summary

| Variable | Level | Coefficient | Std Error | Relativity |
|----------|-------|-------------|-----------|------------|
| Intercept | - | -6.12 | 0.08 | - |
| Hazard Group | Clerical (base) | 0.00 | - | 1.00 |
| Hazard Group | Mfg-Light | 0.65 | 0.06 | 1.92 |
| Hazard Group | Healthcare | 0.82 | 0.07 | 2.27 |
| Hazard Group | Constr-Light | 1.05 | 0.06 | 2.86 |
| Hazard Group | Constr-Heavy | 1.45 | 0.08 | 4.26 |
| Hazard Group | Trucking | 1.62 | 0.10 | 5.05 |
| Employer Size | Micro (base) | 0.00 | - | 1.00 |
| Employer Size | Small | -0.08 | 0.04 | 0.92 |
| Employer Size | Medium | -0.18 | 0.05 | 0.84 |
| Employer Size | Large | -0.28 | 0.06 | 0.76 |
| Employer Size | Jumbo | -0.35 | 0.08 | 0.70 |
| Years in Business | Per 5 years | -0.05 | 0.02 | 0.95 |
| State Benefit Index | Per 0.1 unit | 0.08 | 0.03 | 1.08 |
| Prior Exp Mod | Per 0.1 unit | 0.12 | 0.02 | 1.13 |

### Hazard Group Detail

| Hazard Group | Expected Freq | Relativity | Claims/100 Payroll |
|--------------|---------------|------------|-------------------|
| 1 - Clerical | 0.18 | 1.00 | 0.0018 |
| 5 - Mfg-Light | 0.35 | 1.92 | 0.0035 |
| 10 - Healthcare | 0.41 | 2.27 | 0.0041 |
| 15 - Constr-Light | 0.52 | 2.86 | 0.0052 |
| 20 - Constr-Heavy | 0.77 | 4.26 | 0.0077 |
| 25 - Trucking | 0.91 | 5.05 | 0.0091 |

### Model Fit Statistics

| Metric | Value |
|--------|-------|
| Deviance | 18,420 |
| Pearson Chi-Square | 17,890 |
| Degrees of Freedom | 18,350 |
| Dispersion | 0.98 |
| AIC | 42,100 |

---

## Validation

### Holdout Performance

**Data Split:**
- Training: 70% (2018-2021)
- Holdout: 30% (2022)

**Discrimination:**
| Metric | Training | Holdout |
|--------|----------|---------|
| AUC | 0.71 | 0.68 |
| Gini | 0.42 | 0.36 |

**Calibration:**
| Decile | Expected | Actual | A/E |
|--------|----------|--------|-----|
| 1 (lowest risk) | 185 | 172 | 0.93 |
| 2 | 245 | 251 | 1.02 |
| 3 | 298 | 289 | 0.97 |
| 4 | 352 | 361 | 1.03 |
| 5 | 412 | 405 | 0.98 |
| 6 | 478 | 488 | 1.02 |
| 7 | 558 | 545 | 0.98 |
| 8 | 662 | 678 | 1.02 |
| 9 | 812 | 798 | 0.98 |
| 10 (highest risk) | 1,198 | 1,213 | 1.01 |

### Segment Validation

**By State Group:**
| State Group | Expected | Actual | A/E |
|-------------|----------|--------|-----|
| High Benefit | 1,850 | 1,890 | 1.02 |
| Medium Benefit | 2,420 | 2,380 | 0.98 |
| Low Benefit | 930 | 930 | 1.00 |

**By Employer Size:**
| Size | Expected | Actual | A/E |
|------|----------|--------|-----|
| Micro | 1,420 | 1,480 | 1.04 |
| Small | 1,680 | 1,650 | 0.98 |
| Medium | 1,250 | 1,220 | 0.98 |
| Large | 650 | 640 | 0.98 |
| Jumbo | 200 | 210 | 1.05 |

---

## Model Limitations

### Known Limitations

1. **Class Code Accuracy:** 12% of policies have class code corrections at audit; model uses as-written codes
2. **Experience Mod Timing:** Prior mod may not reflect most recent year's experience
3. **State Variation:** Model uses benefit index rather than state fixed effects; some state-specific factors not captured
4. **COVID Impact:** 2020-2021 experience affected by pandemic; frequency artificially depressed

### Uncertainty Quantification

**Parameter Uncertainty:**
- Hazard group coefficients stable (narrow CIs)
- State benefit index coefficient has wider uncertainty

**Prediction Uncertainty:**
- Individual employer predictions have +/- 30% standard error
- Portfolio-level predictions stable within +/- 5%

---

## Implementation

### Production Deployment

**Frequency Factor Calculation:**
```python
def calculate_wc_frequency_factor(policy):
    base_frequency = 0.003  # Per $100 payroll
    factor = 1.0
    
    # Hazard group
    hazard_factors = get_hazard_group_factors()
    factor *= hazard_factors[policy.hazard_group]
    
    # Employer size
    size_factors = {'Micro': 1.0, 'Small': 0.92, 'Medium': 0.84,
                   'Large': 0.76, 'Jumbo': 0.70}
    factor *= size_factors[policy.size_tier]
    
    # Years in business
    years = min(policy.years_in_business, 25)
    factor *= 0.95 ** (years / 5)
    
    # State benefit
    factor *= 1.08 ** ((policy.state_benefit_index - 1.0) / 0.1)
    
    # Prior experience mod
    factor *= 1.13 ** ((policy.prior_mod - 1.0) / 0.1)
    
    return base_frequency * factor
```

### Loss Cost Filing Support

**Class Code Loss Cost Validation:**
```
Compare model-implied frequency to NCCI published loss costs
- Correlation: 0.94
- Mean absolute deviation: 8%
- Supports company loss cost multiplier
```

---

## Regulatory Compliance

### ASOP Compliance

- **ASOP 12:** Hazard group classification documented
- **ASOP 23:** Data quality (class code accuracy) disclosed
- **ASOP 25:** Credibility by class group addressed
- **ASOP 56:** Model validation completed

### NCCI Alignment

- Model frequency relativities correlate 0.94 with NCCI loss costs
- Supports use of NCCI class codes as rating basis
- Experience rating validation supports NCCI plan

---

## Appendices

### Appendix A: Full Hazard Group Relativities

[25 hazard group factors with confidence intervals]

### Appendix B: State Benefit Index Values

[State-by-state benefit index with methodology]

### Appendix C: Comparison to NCCI

| Hazard Group | Model Relativity | NCCI Relativity | Ratio |
|--------------|------------------|-----------------|-------|
| Clerical | 1.00 | 1.00 | 1.00 |
| Healthcare | 2.27 | 2.35 | 0.97 |
| Construction | 2.86 | 2.95 | 0.97 |
| Trucking | 5.05 | 5.20 | 0.97 |

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
