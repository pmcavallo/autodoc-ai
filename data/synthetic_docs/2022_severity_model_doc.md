---
title: "Personal Auto Bodily Injury Severity Model"
model_type: "severity"
technique: "GLM"
product: "personal_auto"
coverage: "bodily_injury"
year: 2022
status: "production"
---

# Personal Auto Bodily Injury Severity Model - Documentation

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes. No real insurance data, customer information, proprietary methodologies, or confidential information from any insurance company or financial institution is used or simulated.

All names, addresses, policy numbers, claim amounts, and company information are fictional. Any resemblance to actual persons, organizations, or data is purely coincidental.

This project showcases AI agent capabilities for automated documentation generation and is not intended for production use with real data or models.

---

## Executive Summary

ABC Insurance Company developed this Generalized Linear Model (GLM) to predict the average cost per bodily injury (BI) claim in its personal auto insurance portfolio. The severity model works in conjunction with the frequency model to produce total loss cost predictions (frequency × severity) for accurate premium calculations.

The model addresses the business need for improved severity cost predictions in a period of rapidly escalating medical costs and increasing litigation expenses. Between 2018 and 2021, average BI severity increased 24% (from $18,500 to $22,900 per claim), driven by medical inflation, attorney representation rates, and changing injury patterns.

This severity model uses a GLM with Gamma distribution and log link function, incorporating 14 predictor variables including claim characteristics, policy features, and injury indicators. The model was developed on closed claim data from accident years 2018-2020, representing approximately 36,500 closed BI claims with at least 24 months of development.

**Key Results:**
- R-squared: 0.38 (validation set)
- Mean Absolute Percentage Error (MAPE): 28.5%
- Root Mean Squared Error (RMSE): $8,420
- Top decile average severity: $58,400 vs. overall average $22,900 (2.55x)
- Implementation: Q3 2022 (deployed July 15, 2022 alongside frequency model)
- Expected annual premium impact: $9M improvement in rate adequacy

The model has been reviewed and approved by the Model Risk Governance Committee and complies with NAIC Model Audit Rule and relevant Actuarial Standards of Practice.

---

## 1. Business Context & Objectives

### 1.1 Background

ABC Insurance Company's bodily injury coverage has experienced significant severity trend over the past four years, substantially outpacing general inflation and creating rate adequacy challenges:

**Historical Severity Trends:**
- 2018: Average paid severity $18,500
- 2019: Average paid severity $19,800 (+7.0%)
- 2020: Average paid severity $21,200 (+7.1%)
- 2021: Average paid severity $22,900 (+8.0%)
- Cumulative increase 2018-2021: +23.8%
- General inflation (CPI) same period: +10.2%
- Medical inflation (CPI-Medical): +12.4%

**Severity Drivers:**
- Medical cost inflation exceeding general inflation
- Increasing complexity of treatments and longer recovery times
- Higher attorney representation rates (54% in 2021 vs. 42% in 2018)
- Emergence of higher-severity injury types
- Increased litigation and settlement costs
- Third-party legal funding affecting settlement dynamics

The existing severity model, deployed in 2017, failed to adequately capture these dynamics and systematically underestimated costs for high-severity claims. This led to rate inadequacy, particularly in segments with higher injury severity (e.g., younger drivers, urban territories).

### 1.2 Business Problem

The primary business challenges addressed by the severity model redevelopment include:

1. **Rate Inadequacy**: Underestimation of high-severity claims leading to insufficient premiums
   - Loss ratio for claims >$50K was 92% (vs. target 65%)
   - High-severity claims represent 8% of count but 42% of total cost
   - Inadequate reserves for ongoing claims

2. **Insufficient Segmentation**: Limited ability to differentiate severity across risk factors
   - Existing model used only 5 predictors
   - Large within-segment variation (coefficient of variation >2.0)
   - Poor prediction for attorney-represented claims

3. **Trend Capture**: Model did not adequately capture severity inflation
   - Annual re-calibration required manual adjustments
   - Lagging indicator approach caused reactive pricing
   - Missed emerging severity patterns

4. **Medical Cost Management**: Limited visibility into cost drivers
   - Unable to identify high-cost claim characteristics early
   - Insufficient differentiation of injury types
   - Weak integration with claims management strategy

### 1.3 Objectives

The severity model redevelopment project established the following objectives:

**Primary Objectives:**
- Achieve R-squared ≥ 0.35 on validation data (vs. 0.22 for existing model)
- Reduce MAPE to <30% (vs. 38% for existing model)
- Improve high-severity prediction (top decile MAPE <35%)
- Incorporate attorney representation and injury severity indicators

**Secondary Objectives:**
- Enable early identification of potentially high-cost claims
- Support claims department in severity management
- Provide transparency for reserves and pricing decisions
- Build framework for future incorporation of medical bill review data

**Business Impact Goals:**
- Improve loss cost adequacy by $9M annually
- Reduce reserve strengthening by 20% through better initial estimates
- Support $8M in targeted rate increases for high-severity segments
- Improve claims department severity triage accuracy by 30%

---

## 2. Regulatory Compliance Statement

This model has been developed in accordance with the following regulatory and professional standards:

### 2.1 NAIC Model Audit Rule (MAR)

The model complies with all aspects of the NAIC Model Audit Rule including comprehensive documentation, independent validation, ongoing monitoring procedures, and governance oversight. The model documentation includes detailed data specifications, methodology, assumptions, limitations, and validation results.

### 2.2 Actuarial Standards of Practice (ASOPs)

**ASOP No. 12 - Risk Classification:**
- Severity variables selected based on actuarial relevance and causal relationships
- All variables demonstrate statistically significant relationships with claim costs
- Variables comply with state insurance regulations and anti-discrimination laws

**ASOP No. 23 - Data Quality:**
- Comprehensive data quality assessment performed on claims data
- Claim development patterns analyzed to ensure data maturity
- Missing data and outliers addressed through systematic procedures
- Data quality limitations explicitly documented

**ASOP No. 41 - Actuarial Communications:**
- Model purpose, methodology, assumptions, and limitations clearly documented
- Intended use for pricing and reserving specified
- Uncertainty and limitations disclosed

**ASOP No. 56 - Modeling:**
- Model design appropriate for intended purpose
- Validation testing comprehensive and well-documented
- Limitations quantified and disclosed
- Ongoing monitoring plan established

**ASOP No. 43 - Property/Casualty Unpaid Claim Estimates:**
- Severity model supports reserve estimation
- Development patterns and reporting lags considered
- Uncertainty in estimates quantified

### 2.3 State Requirements

The model complies with rate filing requirements in all 15 states where ABC Insurance operates. State-specific loss cost multiplicatorsare applied where required by regulation. Rate filings incorporating the severity model were submitted in Q2 2022 and approved by June 30, 2022.

### 2.4 Internal Governance

**Model Approvals:**
- Model Risk Governance Committee: April 18, 2022
- Chief Actuary: April 22, 2022
- Chief Claims Officer: April 28, 2022
- Pricing Committee: May 5, 2022
- Executive Risk Committee: May 18, 2022

---

## 3. Data Environment

### 3.1 Data Sources

**Claims Transaction Data (Primary Source):**
- Source System: ClaimsVision 2.5
- Accident Years: 2018, 2019, 2020
- Evaluation Date: December 31, 2021 (24-36 months development)
- Closed Claims: 36,482 bodily injury claims
- Total Incurred: $835M in claim payments
- Data Elements: Payments, reserves, injury codes, attorney flags, settlement dates

**Policy Data:**
- Source System: PolicyMaster 3.0
- Linked via policy number to claims
- Elements: Coverage limits, deductibles, policy characteristics
- Match Rate: 99.4% of claims successfully linked to policy data

**Injury Coding Data:**
- Source: Internal claims coding system
- Injury Severity Scale: Minor, Moderate, Serious, Severe
- Body Part Injured: 12 categories
- Treatment Type: Outpatient, Inpatient, Surgery, Physical Therapy
- Coding Completeness: 94.2% of claims

**Attorney Representation Data:**
- Source: Claims notes and legal tracking system
- Attorney Involved Flag: Yes/No/Unknown
- Date of Attorney Representation
- Completeness: 98.7% of claims flagged

**Third-Party Data:**
- Medical Cost Index: Regional medical inflation factors
- Geographic Data: Territory risk scores from frequency model
- Economic Data: County-level income and employment statistics

### 3.2 Data Quality Procedures

**Development Maturity:**
- Claims selected with ≥24 months of development from accident date
- Closure rate analysis: 94% of selected claims closed
- Open claims excluded from training set (potential development bias)
- IBNR claims excluded (not yet reported)

**Payment Validation:**
- Total incurred = paid + case reserves (for open claims in validation)
- Cross-validation against financial reporting (99.7% match)
- Large claims (>$250K) individually reviewed for accuracy
- Duplicate payments identified and corrected (0.2% of claims)

**Outlier Treatment:**
- Claims >$500K reviewed individually (1.2% of claims, 8.4% of total cost)
- Excluded catastrophic injury claims >$2M (0.1% of claims, expert review needed)
- Claims <$100 excluded (likely administrative-only claims, 2.3% of claims)
- Final dataset: $500 ≤ severity ≤ $500,000

**Missing Data Patterns:**
- Injury code missing: 5.8% of claims (assigned "Unknown" category)
- Attorney flag unknown: 1.3% of claims (imputed based on claim characteristics)
- Policy data unmatched: 0.6% of claims (excluded from analysis)
- Treatment type missing: 7.2% (imputed based on severity and injury type)

**Consistency Checks:**
- Accident date before claim report date (100% pass)
- Claim report date before payment dates (99.9% pass, exceptions reviewed)
- Total payments equal to sum of individual transactions (100% match)
- Injury severity consistent with treatment type (98.4% consistency)

### 3.3 Variable Definitions

**Claim Characteristics:**
- `claim_age_days`: Days from accident to claim closure (continuous, 30-1095 days)
- `total_incurred`: Total incurred loss (paid + case reserves) in dollars
- `attorney_involved`: Attorney representation (Yes/No)
- `injury_severity`: Coded severity level (Minor, Moderate, Serious, Severe)
- `body_part`: Body part injured (Head, Neck, Back, Extremity, Multiple, Other)
- `treatment_type`: Medical treatment category (Outpatient, Inpatient, Surgery, PT)
- `claimant_age`: Age of injured party (continuous, 0-95)

**Policy Characteristics:**
- `coverage_limit`: BI liability limit ($100K/$300K, $250K/$500K, $500K/$1M, $1M/$2M)
- `at_fault_driver_age`: Age of at-fault driver (continuous, 16-90)
- `vehicle_type`: At-fault vehicle type (Sedan, SUV, Truck, Van, Sports Car)
- `policy_tenure`: Years with ABC Insurance (continuous, 0-25)

**Geographic Variables:**
- `territory`: Geographic zone (Zone 1-10, same as frequency model)
- `medical_cost_index`: Regional medical cost factor (continuous, 0.85-1.25)

**Temporal Variables:**
- `accident_year`: Year of accident (2018, 2019, 2020)
- `trend_factor`: Severity trend adjustment based on accident year

### 3.4 Data Exclusions

**Claim Exclusions:**
- Open/pending claims (insufficient development): 6,441 claims excluded
- Claims <24 months development: 3,892 claims excluded
- Catastrophic claims >$2M: 37 claims excluded (manual review process)
- Minimum claims <$500: 1,083 claims excluded (administrative)
- Data quality failures: 185 claims excluded
- Total excluded: 11,638 claims (24.2% of universe)

**Final Analysis Dataset:**
- Closed Claims: 36,482
- Average Severity: $22,900
- Median Severity: $14,200
- Standard Deviation: $29,400
- Coefficient of Variation: 1.28
- Severity Range: $500 - $500,000

---

## 4. Methodology

### 4.1 Model Type Selection

A Generalized Linear Model (GLM) with Gamma distribution was selected for severity modeling based on the following considerations:

**Statistical Properties:**
- Gamma distribution appropriate for positive continuous outcomes (claim costs)
- Right-skewed distribution matches severity distribution characteristics
- Log link ensures positive predictions
- Variance increases with mean (heteroskedasticity characteristic of severity data)

**Actuarial Standards:**
- GLMs widely accepted for insurance severity modeling
- Transparent and interpretable coefficients
- Multiplicative structure aligns with rating factor approach
- Compatible with frequency model for combined loss cost estimation

**Business Requirements:**
- Coefficients translate to severity relativities for rating
- Model integrates easily with existing systems
- Interpretability for claims management and reserving
- Regulatory acceptance and explainability

**Alternative Techniques Considered:**

**Log-Normal GLM:**
- Tested but Gamma distribution provided better fit
- AIC: Gamma 485,320 vs. Log-Normal 491,850
- Diagnostic plots favored Gamma distribution

**XGBoost/Random Forest:**
- Evaluated for potential predictive improvement
- R² improvement: only +0.04 vs. GLM
- Interpretability challenges outweighed small gain
- Considered for future Phase 2 model enhancement

**Neural Networks:**
- Rejected due to lack of interpretability
- Regulatory concerns about "black box" nature
- Insufficient training data for deep learning approaches

### 4.2 Mathematical Formulation

**Gamma Distribution Assumption:**
```
Y_i ~ Gamma(μ_i, φ)
```

Where:
- Y_i = severity (total incurred cost) for claim i
- μ_i = expected severity
- φ = shape parameter (constant across observations)

**Link Function:**
```
log(μ_i) = β_0 + β_1×X_1i + β_2×X_2i + ... + β_k×X_ki
```

**Equivalently:**
```
μ_i = exp(β_0 + Σ β_j×X_ji)
```

**Variance Function:**
```
Var(Y_i) = φ × μ_i²
```

This specification captures the property that severity variance increases with the mean.

**Severity Relativity Interpretation:**

For a categorical variable with baseline level b and level j:
```
Relativity_j = exp(β_j - β_b)
```

For continuous variable X with coefficient β:
```
Relativity for change Δ = exp(β × Δ)
```

**Example:**
If β_attorney = 0.52, then claims with attorney representation have expected severity:
```
Relativity = exp(0.52) = 1.68 (68% higher than non-represented claims)
```

**Combined Frequency-Severity:**

Total loss cost = Frequency × Severity
```
E[Loss Cost] = λ × μ = exp(β^freq + β^sev)
```

This multiplicative combination produces final premium indication.

### 4.3 Assumptions

**Key Model Assumptions:**

1. **Gamma Distribution**: Claim severity follows Gamma distribution
   - Validation: Q-Q plots and distribution fit tests performed
   - Alternative: Log-normal tested but Gamma provided superior fit

2. **Independent Observations**: Claim severities are independent
   - Justification: Geographic and temporal diversity
   - Limitation: May not hold for multi-claimant accidents (rare)

3. **Log-Linear Mean Function**: Log severity linear in predictors
   - Validation: Partial residual plots reviewed
   - Adjustment: Continuous variables capped/floored where appropriate

4. **Constant Shape Parameter**: Dispersion constant across predictions
   - Validation: Pearson residuals examined for heteroskedasticity
   - Result: Reasonable assumption, mild violations acceptable

5. **Full Development**: Claims sufficiently developed to maturity
   - Validation: Development triangles show 94% closure rate
   - Adjustment: 24-month minimum development requirement

6. **No Selection Bias**: Closed claims representative of universe
   - Risk: Early settlers may differ from late settlers
   - Mitigation: Development pattern analysis shows minimal bias

### 4.4 Limitations

**Known Limitations:**

1. **Development Uncertainty**: Claims may develop further after 24 months
   - Impact: May underestimate severity for slow-developing injuries
   - Mitigation: Tail development factors applied in reserving process

2. **Omitted Variables**: Some predictive factors not captured:
   - Pre-existing medical conditions (data privacy limitations)
   - Claimant employment and income (not consistently available)
   - Detailed medical billing information (future enhancement planned)

3. **Attorney Representation Timing**: Flag captures representation at any point
   - Issue: Early vs. late representation may have different severity impacts
   - Data limitation: Timing not consistently recorded

4. **Injury Coding Subjectivity**: Injury severity assigned by claims adjusters
   - Risk: Inter-rater reliability variations
   - Mitigation: Coding guidelines and training provided, 94% completeness

5. **Outlier Treatment**: Capping at $500K excludes highest-severity claims
   - Impact: Model may underpredict rare catastrophic claims
   - Mitigation: Separate large loss loading applied in pricing

6. **Temporal Trend**: Linear trend assumption may not capture acceleration
   - Risk: Underestimate future severity if trend accelerates
   - Monitoring: Quarterly trend analysis updates

7. **Geographic Granularity**: Medical cost index at territory level
   - Trade-off: Balance between precision and credibility
   - Limitation: Within-territory medical cost variation not captured

---

## 5. Model Development Process

### 5.1 Development Data

**Data Splitting Strategy:**

Claims dataset split temporally by accident year:

- **Training Set**: Accident years 2018-2019 (65% of data)
  - 23,713 closed claims
  - Total incurred: $543M
  - Average severity: $22,900
  - Used for model fitting and variable selection

- **Validation Set**: Accident year 2020 H1 (18% of data)
  - 6,567 closed claims
  - Total incurred: $151M
  - Average severity: $23,000
  - Used for hyperparameter tuning and model selection

- **Holdout Set**: Accident year 2020 H2 (17% of data)
  - 6,202 closed claims
  - Total incurred: $141M
  - Average severity: $22,700
  - Reserved for final model evaluation only

**Rationale:**
- Temporal split tests predictive power on future claims
- Avoids data leakage and overfitting
- Mimics production scenario (predict future from past)
- Ensures train/validation/holdout similarity in average severity

**Development Requirements:**
- All claims ≥24 months development from accident date
- Claims evaluated as of December 31, 2021
- Closed claims only (case reserves excluded)
- Payment data complete through evaluation date

### 5.2 Variable Selection

**Initial Variable Pool:**

Started with 28 potential predictor variables:

**Claim-Level (16 variables):**
- Injury severity, body part, treatment type, medical procedures
- Attorney involvement, litigation status, settlement type
- Claimant age, gender, prior claims history
- Claim report lag, claim closure duration

**Policy-Level (8 variables):**
- Coverage limit, policy tenure, at-fault driver age
- Vehicle type, vehicle age, territory
- Prior claims, insurance score

**Geographic/Temporal (4 variables):**
- Territory, medical cost index, accident year, accident quarter

**Selection Process:**

**Step 1: Univariate Analysis (All 28 Variables)**

Calculated severity relativities for each variable:
- Ranked by R² and F-statistic
- Eliminated 9 variables with weak relationships (p > 0.10)
- Remaining: 19 variables

**Step 2: Correlation Analysis**

Checked for multicollinearity:
- Injury severity and treatment type highly correlated (r = 0.72)
- Selected injury severity (stronger relationship)
- Claim closure duration and claim age correlated (r = 0.88)
- Selected claim age (better data quality)

**Step 3: Forward Selection**

- Started with intercept-only model
- Added variables iteratively based on AIC improvement
- Stopping criterion: ΔAIC < 5
- Result: 14 variables selected

**Step 4: Interaction Testing**

Tested two-way interactions:
- `attorney_involved × injury_severity`: Significant (p < 0.001), included
- `coverage_limit × injury_severity`: Not significant (p = 0.14), excluded
- `territory × medical_cost_index`: Collinear, excluded

**Final Variable Set (14 variables + 1 interaction):**

1. `attorney_involved` (binary)
2. `injury_severity` (4 levels)
3. `body_part` (6 categories)
4. `treatment_type` (4 categories)
5. `claimant_age` (continuous)
6. `coverage_limit` (4 categories)
7. `at_fault_driver_age` (continuous)
8. `vehicle_type` (5 categories)
9. `policy_tenure` (continuous)
10. `territory` (10 categories)
11. `medical_cost_index` (continuous)
12. `accident_year` (trend factor)
13. `claim_age_days` (continuous)
14. `multiple_claimants` (binary flag)
15. **Interaction:** `attorney_involved × injury_severity`

**Variable Selection Validation:**
- All variables significant at p < 0.05
- VIF (Variance Inflation Factor) < 5 for all variables
- Direction of coefficients aligned with actuarial judgment
- Stability across train/validation splits confirmed

### 5.3 Model Calibration

**Estimation Method:**
- Maximum likelihood estimation (MLE) for Gamma GLM
- Fisher scoring algorithm (IRLS variant)
- Convergence achieved in 15 iterations (tolerance = 1e-7)

**Continuous Variable Transformations:**

- `claimant_age`: Capped at 95 (sparse data beyond)
- `at_fault_driver_age`: Capped at 16-90
- `policy_tenure`: Capped at 25 years
- `claim_age_days`: Capped at 30-1095 days (1 month to 3 years)
- `medical_cost_index`: Bounded at 0.85-1.25 (reasonable range)

**Categorical Baseline Levels:**
- Attorney Involved: No (baseline)
- Injury Severity: Minor (baseline)
- Body Part: Extremity (most common, lowest severity)
- Treatment Type: Outpatient (baseline)
- Coverage Limit: $100K/$300K (most common)
- Vehicle Type: Sedan (baseline)
- Territory: Zone 5 (median risk)

**Handling Missing Data:**

- Injury severity missing (5.8%): Assigned "Unknown" category
- Attorney flag unknown (1.3%): Imputed using logistic regression based on claim characteristics
- Treatment type missing (7.2%): Imputed based on injury severity and payments
- Other variables: <1% missing, cases excluded

**Trend Adjustment:**

Annual severity trend incorporated via accident year coefficient:
- 2018: Baseline (trend factor = 1.00)
- 2019: +7.5% (trend factor = 1.075)
- 2020: +7.8% (trend factor = 1.075 × 1.078 = 1.159)

**Model Convergence Diagnostics:**
- Deviance: 892,450 (training set)
- Degrees of freedom: 23,672
- Pearson chi-square / df = 1.08 (acceptable dispersion)
- AIC: 485,320
- BIC: 485,890

**Coefficient Stability:**
- Bootstrap validation (1,000 iterations) shows tight confidence intervals
- Cross-validation (5-fold) confirms minimal overfitting
- Temporal stability tested: coefficients stable across 2018-2019 split

---

## 6. Model Performance & Validation

### 6.1 In-Sample Results

**Training Set Performance (Accident Years 2018-2019):**

**Goodness of Fit:**
- R-squared: 0.41
- Adjusted R-squared: 0.40
- Mean Absolute Error (MAE): $7,850
- Mean Absolute Percentage Error (MAPE): 26.8%
- Root Mean Squared Error (RMSE): $8,200

**Prediction Accuracy by Severity Decile:**

| Decile | Actual Avg | Predicted Avg | Ratio | Claim Count |
|--------|------------|---------------|-------|-------------|
| 1      | $2,100     | $2,050        | 1.02  | 2,371       |
| 2      | $4,800     | $4,750        | 1.01  | 2,371       |
| 3      | $7,200     | $7,350        | 0.98  | 2,371       |
| 4      | $10,400    | $10,550       | 0.99  | 2,371       |
| 5      | $14,200    | $14,100       | 1.01  | 2,371       |
| 6      | $18,500    | $18,650       | 0.99  | 2,371       |
| 7      | $24,800    | $24,600       | 1.01  | 2,371       |
| 8      | $34,200    | $34,500       | 0.99  | 2,371       |
| 9      | $50,100    | $49,800       | 1.01  | 2,372       |
| 10     | $62,700    | $63,000       | 1.00  | 2,371       |

**Overall:** Excellent calibration across severity spectrum, with <2% error in each decile.

**Calibration Statistics:**
- Mean predicted severity: $22,900
- Mean actual severity: $22,900
- Overall bias: 0.0%
- Correlation (actual vs. predicted): 0.71

### 6.2 Out-of-Sample Validation

**Validation Set Performance (Accident Year 2020 H1):**

**Goodness of Fit:**
- R-squared: 0.38
- Adjusted R-squared: 0.37
- Mean Absolute Error (MAE): $8,150
- Mean Absolute Percentage Error (MAPE): 28.5%
- Root Mean Squared Error (RMSE): $8,420

**Calibration:**
- Mean predicted severity: $23,200
- Mean actual severity: $23,000
- Overall bias: +0.9% (slight overprediction, acceptable)

**Holdout Set Performance (Accident Year 2020 H2):**

**Goodness of Fit:**
- R-squared: 0.37
- MAPE: 29.2%
- RMSE: $8,580

**Model Generalization:**
- R² decrease from training to holdout: 0.04 (minimal overfitting)
- MAPE increase: 2.4 percentage points (acceptable degradation)
- Model demonstrates strong generalization to unseen data

**High-Severity Performance:**

For claims in top severity quartile (>$32K):
- MAPE: 33.5% (vs. 42% for existing model)
- Correlation: 0.64 (vs. 0.48 for existing model)
- Significant improvement in high-severity prediction

### 6.3 Sensitivity Analysis

**Coefficient Confidence Intervals (Bootstrap, 1,000 iterations):**

| Variable                  | Coefficient | 95% CI             |
|---------------------------|-------------|--------------------|
| Attorney (Yes vs. No)     | 0.520       | [0.485, 0.555]     |
| Injury: Severe vs. Minor  | 1.280       | [1.225, 1.335]     |
| Injury: Serious vs. Minor | 0.740       | [0.695, 0.785]     |
| Treatment: Surgery        | 0.580       | [0.540, 0.620]     |
| Coverage: $1M vs. $100K   | 0.215       | [0.175, 0.255]     |
| Medical Cost Index        | 0.420       | [0.365, 0.475]     |

**Variable Importance (Permutation Analysis):**

Measured R² decrease when each variable is randomly permuted:

| Variable            | R² Drop | Importance Rank |
|---------------------|---------|-----------------|
| injury_severity     | 0.18    | 1               |
| attorney_involved   | 0.09    | 2               |
| treatment_type      | 0.07    | 3               |
| body_part           | 0.04    | 4               |
| medical_cost_index  | 0.03    | 5               |
| coverage_limit      | 0.02    | 6               |
| (remaining vars)    | <0.02   | 7-14            |

**Insight:** Injury severity is the dominant predictor, followed by attorney involvement and treatment type.

**Scenario Testing:**

**Scenario 1: Medical Inflation Acceleration**
- Assumption: Medical costs increase 12% annually (vs. historical 8%)
- Impact: Severity predictions increase 12% proportionally via medical cost index
- Action: Monitor actual vs. expected; recalibrate if trend persists

**Scenario 2: Attorney Representation Increase**
- Assumption: Attorney involvement rises from 54% to 65%
- Impact: Average severity increases $1,200 (5.2%)
- Action: Monitor attorney representation rates; adjust base severity if structural shift

**Scenario 3: Telematics Adoption**
- Assumption: Safer driving reduces serious injury rate by 15%
- Impact: Mix shift toward lower severity; average decreases $800 (3.5%)
- Action: Segment telematics policies separately when credible

---

## 7. Model Comparison & Selection

### 7.1 Champion Model (Existing 2017 Model)

**Current Production Severity Model:**

- Technique: GLM with Gamma distribution
- Variables: 5 predictors (injury severity, territory, coverage limit, claimant age, accident year)
- Validation Performance (2021 data):
  - R²: 0.22
  - MAPE: 38.0%
  - RMSE: $11,200
  - High-severity MAPE: 52% (poor performance)

**Known Deficiencies:**
- Missing attorney involvement flag (strong predictor)
- Outdated territory definitions
- Insufficient injury detail (2 categories vs. 4)
- No treatment type differentiation
- Poor high-severity prediction

### 7.2 Challenger Model (2022 GLM)

**Proposed Severity Model (Documented Here):**

- Technique: GLM with Gamma distribution and interaction term
- Variables: 14 predictors + 1 interaction
- Validation Performance (2020 data):
  - R²: 0.38
  - MAPE: 28.5%
  - RMSE: $8,420
  - High-severity MAPE: 33.5% (substantial improvement)

**Key Enhancements:**
- Attorney involvement incorporated (strongest predictor after injury)
- More granular injury severity coding (4 levels)
- Treatment type included (surgery, inpatient, etc.)
- Updated medical cost indices
- Interaction between attorney and injury severity

### 7.3 Comparison Results

**Performance Metrics Comparison:**

| Metric                | Champion | Challenger | Improvement |
|-----------------------|----------|------------|-------------|
| R² (validation)       | 0.22     | 0.38       | +72.7%      |
| MAPE                  | 38.0%    | 28.5%      | -25.0%      |
| RMSE                  | $11,200  | $8,420     | -24.8%      |
| High-severity MAPE    | 52.0%    | 33.5%      | -35.6%      |
| Variables             | 5        | 14         | +9          |
| Correlation (act/pred)| 0.54     | 0.71       | +31.5%      |

**Business Impact Assessment:**

Using 2021 validation year, estimated financial impact:

**Rate Adequacy:**
- High-severity segment: Rates increase 10-18% (currently underpriced by $3.2M)
- Attorney-represented claims: Rates increase 12% (currently underpriced by $2.8M)
- Low-severity segment: Rates decrease 3-5% (currently overpriced by $1.1M)
- Net premium change: +$4.9M annually

**Reserve Accuracy:**
- Improved initial case reserves reduce strengthening by 20%
- Estimated benefit: $2.1M annual reduction in reserve additions
- Better IBNR estimation through improved severity understanding

**Claims Management:**
- Early identification of high-severity potential improves triage
- Estimated medical management savings: $2.0M annually

**Total Estimated Annual Benefit: $9.0M**

### 7.4 Selection Rationale

**Decision: Deploy Challenger Model to Production**

The Model Risk Governance Committee approved the challenger severity model based on:

1. **Superior Predictive Accuracy**: 72% improvement in R² is highly material

2. **High-Severity Improvement**: 35.6% reduction in high-severity MAPE addresses critical business need

3. **Actuarially Sound**: All variables have strong theoretical basis and statistical significance

4. **Regulatory Compliance**: Enhanced documentation meets all NAIC and ASOP requirements

5. **Business Value**: $9M projected annual benefit vs. $1.8M implementation cost (5:1 ROI)

6. **Claims Integration**: Model provides actionable insights for claims severity management

7. **Stakeholder Support**: Claims, pricing, and finance departments support deployment

**Deployment Strategy:** Production deployment July 15, 2022, alongside frequency model for complete loss cost refresh.

---

## 8. Implementation Plan

### 8.1 Timeline

**Phase 1: Pre-Production Validation (June 1-30, 2022)**
- Parallel run in rating and reserving systems
- Claims department training on severity flags
- User acceptance testing
- Final governance approvals

**Phase 2: Production Deployment (July 1-15, 2022)**
- Deploy severity model to rating engine
- Activate for new business and renewals (coordinated with frequency model)
- Initialize monitoring dashboards
- Alert mechanisms activated

**Phase 3: Claims Integration (July 15-August 31, 2022)**
- Severity scoring added to new claims workflow
- High-severity alerts integrated with claims assignment system
- Training for claims adjusters on model outputs
- Reserve setting guidelines updated

**Phase 4: Monitoring Period (July 2022-December 2022)**
- Weekly monitoring during first month
- Monthly monitoring thereafter
- Quarterly validation reviews
- 6-month comprehensive model review (January 2023)

### 8.2 Integration

**Rating System:**
- Severity coefficients exported to rating tables
- Combined with frequency model for total loss cost
- API updated for real-time severity scoring
- Historical comparisons for renewals enabled

**Reserving System:**
- Severity predictions incorporated into initial case reserve recommendations
- Integrated with claims adjuster workflow
- Override capability with documentation requirements
- Monthly reserve adequacy reports

**Claims Management System:**
- Severity score added to claim record at FNOL (First Notice of Loss)
- High-severity flags trigger:
  - Senior adjuster assignment
  - Medical case management review
  - Early settlement evaluation
- Dashboard for claims management with severity distribution

**Data Warehouse:**
- Model version tracking
- Prediction logging for validation
- Actual vs. expected severity reports
- Trend analysis and monitoring metrics

### 8.3 Training

**Actuarial Staff (12 hours):**
- Technical model deep-dive (4 hours)
- Reserving applications (3 hours)
- Monitoring procedures and dashboards (2 hours)
- Model governance and documentation (3 hours)

**Claims Department (8 hours):**
- Overview of severity model (2 hours)
- Interpreting severity scores and flags (2 hours)
- Integration with claims workflow (2 hours)
- Case studies and examples (2 hours)

**Underwriting Staff (4 hours):**
- Model overview and rating impact (2 hours)
- Combined frequency-severity loss costs (1 hour)
- Customer communication strategies (1 hour)

**IT/Data Teams (6 hours):**
- Technical implementation (3 hours)
- Monitoring and alerting systems (2 hours)
- Troubleshooting procedures (1 hour)

**Training Completion Target:** June 25, 2022

---

## 9. Ongoing Monitoring & Governance

### 9.1 Monitoring Metrics

**Monthly KPIs:**
- Actual vs. Predicted Severity (overall and by segment)
- Prediction Bias (actual / predicted - 1)
- High-Severity Claim Rate (>$50K)
- Attorney Representation Rate
- Distribution of Severity Scores
- Reserve Development Patterns

**Quarterly Validation Metrics:**
- R² on rolling 12-month data
- MAPE overall and by severity band
- Coefficient stability (refit on recent data)
- Calibration testing (actual vs. predicted by decile)
- Variable importance rankings

**Annual Comprehensive Review:**
- Full model re-validation
- Assumption testing
- Competitive benchmarking
- Regulatory compliance review
- Model documentation update
- Enhancement opportunities assessment

**Real-Time Alerts:**

Triggered automatically if:
- Actual/Expected severity >1.15 or <0.85 for 2 consecutive months
- R² drops below 0.32
- High-severity claim rate increases >30% vs. prior year
- Any coefficient changes >25% when re-estimated
- Attorney representation rate changes >10 percentage points

### 9.2 Review Frequency

**Weekly Reviews (First Month Post-Deployment):**
- New claims severity scoring validation
- High-severity flag accuracy
- Claims department feedback
- Technical issues or anomalies

**Monthly Reviews (Pricing Analytics Team):**
- KPI dashboard review
- Investigate triggered alerts
- Document findings in monitoring log
- Escalate issues to Chief Actuary if material

**Quarterly Reviews (Chief Actuary):**
- Formal validation testing on recent data
- Statistical performance trends
- External environment scan (regulations, competitive, economic)
- Sign-off on model continuation or adjustment plan

**Annual Reviews (Model Risk Governance Committee):**
- Comprehensive validation report
- Model appropriateness assessment
- Limitations and assumptions review
- Decision: continue, recalibrate, or replace
- Update model documentation

### 9.3 Escalation Procedures

**Level 1: Minor Performance Variance (R² = 0.32-0.35)**
- Action: Enhanced monitoring and investigation
- Responsibility: Pricing Analytics Team
- Timeline: Document findings within 30 days
- Outcome: Continue with increased scrutiny or make minor adjustments

**Level 2: Material Performance Degradation (R² < 0.32 or MAPE > 35%)**
- Action: Root cause analysis and corrective action plan
- Responsibility: Chief Actuary
- Timeline: Initial assessment within 15 days, action plan within 45 days
- Outcome: Model recalibration or enhancement project

**Level 3: Critical Issues (Regulatory concerns, systematic bias, major data quality issues)**
- Action: Immediate investigation and remediation
- Responsibility: Model Risk Governance Committee
- Timeline: Response within 5 business days
- Outcome: Temporary model adjustments or reversion to previous model if necessary

**Model Replacement Triggers:**

Model will be replaced or substantially updated if:
- R² declines below 0.28 and cannot be restored through recalibration
- Systematic bias >10% emerges and persists
- Regulatory requirements change materially
- Major data environment changes (e.g., new injury coding system)
- Business strategy shifts (e.g., new products, states, or segments)
- Superior alternative methodology becomes available

**Expected Model Lifecycle:** 3-5 years before major update or replacement.

---

## Appendices

### Appendix A: Detailed Coefficient Tables

**Categorical Variables - Injury Severity:**

| Injury Level | Coefficient | Std Error | Relativity | Avg Severity |
|--------------|-------------|-----------|------------|--------------|
| Minor        | 0.000       | -         | 1.00       | $8,200       |
| Moderate     | 0.420       | 0.028     | 1.52       | $12,500      |
| Serious      | 0.740       | 0.032     | 2.10       | $17,200      |
| Severe       | 1.280       | 0.038     | 3.60       | $29,500      |

**Categorical Variables - Body Part:**

| Body Part   | Coefficient | Std Error | Relativity | Avg Severity |
|-------------|-------------|-----------|------------|--------------|
| Extremity   | 0.000       | -         | 1.00       | $14,800      |
| Neck        | 0.185       | 0.024     | 1.20       | $17,800      |
| Back        | 0.245       | 0.026     | 1.28       | $18,900      |
| Head        | 0.380       | 0.032     | 1.46       | $21,600      |
| Multiple    | 0.520       | 0.038     | 1.68       | $24,900      |
| Other       | 0.110       | 0.029     | 1.12       | $16,600      |

**Categorical Variables - Treatment Type:**

| Treatment Type | Coefficient | Std Error | Relativity | Avg Severity |
|----------------|-------------|-----------|------------|--------------|
| Outpatient     | 0.000       | -         | 1.00       | $9,400       |
| Inpatient      | 0.385       | 0.028     | 1.47       | $13,800      |
| Surgery        | 0.580       | 0.035     | 1.79       | $16,800      |
| Physical Ther. | 0.125       | 0.022     | 1.13       | $10,600      |

**Binary Variables:**

| Variable                | Coefficient | Std Error | Relativity | Impact     |
|-------------------------|-------------|-----------|------------|------------|
| Attorney (Yes vs. No)   | 0.520       | 0.022     | 1.68       | +68%       |
| Multiple Claimants      | 0.295       | 0.048     | 1.34       | +34%       |

**Continuous Variables:**

| Variable            | Coefficient | Std Error | Per-Unit Impact |
|---------------------|-------------|-----------|-----------------|
| claimant_age        | -0.0035     | 0.0008    | -0.35% per year |
| at_fault_driver_age | -0.0025     | 0.0007    | -0.25% per year |
| policy_tenure       | -0.0120     | 0.0022    | -1.2% per year  |
| claim_age_days      | 0.0003      | 0.0001    | +0.03% per day  |
| medical_cost_index  | 0.420       | 0.055     | +42% per unit   |

**Interaction Term:**

| Interaction                      | Coefficient | Std Error | Effect                          |
|----------------------------------|-------------|-----------|---------------------------------|
| Attorney × Injury Severe         | 0.220       | 0.045     | Additional +25% for severe cases |
| Attorney × Injury Serious        | 0.140       | 0.038     | Additional +15% for serious cases|

### Appendix B: Model Diagnostics

**Residual Analysis:**

- Pearson residuals approximately normally distributed (Q-Q plot)
- No systematic patterns in residuals vs. fitted values
- Mild heteroskedasticity acceptable for Gamma GLM
- No influential outliers (Cook's distance < 0.5 for all claims)

**Distribution Fit:**

- Gamma distribution provides good fit to severity data
- Anderson-Darling test: p-value = 0.08 (fail to reject Gamma)
- Alternative log-normal: p-value = 0.02 (rejected)

**Multicollinearity Check:**

All VIF (Variance Inflation Factor) values < 5:
- Highest VIF: injury_severity (3.2)
- medical_cost_index and territory correlated but VIF = 2.8 (acceptable)

### Appendix C: Severity Distribution Summary

**Overall Severity Distribution:**

- Mean: $22,900
- Median: $14,200
- Standard Deviation: $29,400
- Skewness: 2.85 (right-skewed)
- Kurtosis: 12.4 (heavy-tailed)

**Severity by Key Segments:**

| Segment              | Mean Severity | Median | Std Dev | Count  |
|----------------------|---------------|--------|---------|--------|
| No Attorney          | $14,200       | $9,800 | $15,400 | 16,782 |
| With Attorney        | $33,800       | $24,600| $38,200 | 19,700 |
| Minor Injury         | $8,200        | $6,400 | $7,900  | 12,450 |
| Moderate Injury      | $12,500       | $10,200| $11,800 | 14,320 |
| Serious Injury       | $17,200       | $14,800| $15,600 | 7,240  |
| Severe Injury        | $29,500       | $26,100| $32,400 | 2,472  |

---

## Document Control

**Version:** 1.0
**Date:** June 2, 2022
**Last Updated:** June 2, 2022

**Prepared by:**
Michael Chen, FCAS, MAAA
Senior Actuary, Claims Analytics
ABC Insurance Company

**Reviewed by:**
Robert Johnson, FCAS, MAAA
Chief Actuary
ABC Insurance Company

**Reviewed by:**
Patricia Davis
Chief Claims Officer
ABC Insurance Company

**Approved by:**
Sarah Williams
Model Risk Officer
ABC Insurance Company

**Distribution:**
- Model Risk Governance Committee
- Pricing Committee
- Claims Department Leadership
- State Insurance Department Filings
- Internal Audit Department
- Corporate Actuarial Library

**Next Review Date:** June 1, 2023

**Model ID:** PAUTO-SEV-GLM-2022.1
**Documentation Reference:** DOC-2022-SEV-001

---

**End of Document**
