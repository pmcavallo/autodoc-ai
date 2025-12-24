---
title: "Personal Auto Bodily Injury Frequency Model"
model_type: "frequency"
technique: "GLM"
product: "personal_auto"
coverage: "bodily_injury"
year: 2022
status: "production"
---

# Personal Auto Bodily Injury Frequency Model - Documentation

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes. No real insurance data, customer information, proprietary methodologies, or confidential information from any insurance company or financial institution is used or simulated.

All names, addresses, policy numbers, claim amounts, and company information are fictional. Any resemblance to actual persons, organizations, or data is purely coincidental.

This project showcases AI agent capabilities for automated documentation generation and is not intended for production use with real data or models.

---

## Executive Summary

ABC Insurance Company developed this Generalized Linear Model (GLM) to predict the frequency of bodily injury (BI) claims in its personal auto insurance portfolio. The model addresses the business need for more accurate risk segmentation and pricing precision in a competitive marketplace where loss ratios in the BI coverage had been trending upward from 2018-2020.

The frequency model uses a GLM with a Poisson distribution and log link function, incorporating 12 primary rating variables including driver age, vehicle characteristics, territory, and prior claims history. The model was developed on policy data from years 2019-2021, representing approximately 520,000 policies and 48,000 bodily injury claims.

**Key Results:**
- Model AUC: 0.72 (validation set)
- Gini coefficient: 0.44
- Top decile lift: 2.3x vs. random assignment
- Implementation: Q3 2022 (July 15, 2022 production deployment)
- Expected annual premium impact: $12M improvement in combined ratio
- Model validation period: 2022-2023

The model has been reviewed and approved by the Model Risk Governance Committee and meets all regulatory requirements under NAIC Model Audit Rule and relevant Actuarial Standards of Practice.

---

## 1. Business Context & Objectives

### 1.1 Background

ABC Insurance Company is a regional personal auto insurer operating in 15 states across the Midwest and Southern regions. The company writes approximately $850M in annual premium, with bodily injury liability representing 35% of total premium ($297M).

From 2018 to 2020, the company experienced adverse bodily injury loss ratio trends:
- 2018: 62% loss ratio
- 2019: 66% loss ratio
- 2020: 71% loss ratio

This deterioration was driven by:
- Increasing medical cost inflation (8-12% annually)
- Higher severity of injury claims
- Competitive market pressure limiting rate increases
- Insufficient risk segmentation in existing rating plan

The existing frequency model, deployed in 2016, showed declining predictive performance and was based on older statistical techniques that limited the company's ability to incorporate new data sources and interactions between variables.

### 1.2 Business Problem

The primary business problems addressed by this model development effort include:

1. **Inadequate Risk Segmentation**: The existing model used only 7 rating variables and did not capture important risk differentials, leading to adverse selection where lower-risk customers left for competitors while higher-risk customers remained.

2. **Pricing Precision**: Loss cost variation within rating cells was too high (coefficient of variation >1.5 in many cells), indicating insufficient granularity for competitive and actuarially sound pricing.

3. **Regulatory Compliance**: The existing model lacked comprehensive documentation and validation testing required under the NAIC Model Audit Rule, creating regulatory risk.

4. **Operational Efficiency**: The rating plan implementation was difficult to maintain and lacked transparency for underwriters and actuaries.

### 1.3 Objectives

The model development project had the following measurable objectives:

**Primary Objectives:**
- Achieve AUC ≥ 0.70 on out-of-sample validation data
- Improve top decile lift to >2.0x vs. random
- Reduce within-cell loss ratio variation by 20%
- Meet all NAIC and state regulatory requirements

**Secondary Objectives:**
- Incorporate territory refinements from concurrent geographic analysis
- Enable integration with telematics data in future iterations
- Provide transparency and interpretability for business stakeholders
- Reduce model deployment timeline from 6 months to 3 months

**Business Impact Goals:**
- Improve combined ratio by 2-3 points ($17M-25M annual benefit)
- Reduce quote-to-bind leakage by 15% through better pricing
- Maintain or improve customer retention rates
- Pass regulatory review without material findings

---

## 2. Regulatory Compliance Statement

This model has been developed in accordance with the following regulatory and professional standards:

### 2.1 NAIC Model Audit Rule (MAR)

The model documentation, governance, and validation procedures comply with the NAIC Model Audit Rule requirements including:
- Comprehensive documentation of data, methodology, assumptions, and limitations
- Independent validation by qualified professionals
- Ongoing monitoring procedures
- Model risk management framework
- Regular reviews by governance committees

### 2.2 Actuarial Standards of Practice (ASOPs)

This model adheres to the following Actuarial Standards of Practice:

**ASOP No. 12 - Risk Classification:**
- Variables selected based on actuarial principles of causality, objectivity, and practical feasibility
- All rating variables are demonstrably related to expected claim frequency
- Variables comply with state anti-discrimination laws
- Credibility standards applied to variable selection

**ASOP No. 23 - Data Quality:**
- Comprehensive data quality assessment performed
- Data sources documented with lineage tracking
- Missing data and outliers addressed systematically
- Data limitations disclosed and assessed for materiality

**ASOP No. 41 - Actuarial Communications:**
- Documentation includes scope, methodology, assumptions, and limitations
- Reliance on data and work of others disclosed
- Conflict of interest statement included
- Intended use and users clearly specified

**ASOP No. 56 - Modeling:**
- Model purpose and design clearly stated
- Model validation testing documented
- Limitations and uncertainty quantified
- Ongoing monitoring plan established

### 2.3 State Insurance Department Requirements

The model complies with rating variable approval requirements in all 15 states where ABC Insurance operates. Rate filings incorporating this model were submitted to state insurance departments in Q2 2022 and approved in all jurisdictions by June 30, 2022.

### 2.4 Internal Governance

The model was reviewed and approved by:
- Model Risk Governance Committee (April 15, 2022)
- Chief Actuary (April 20, 2022)
- Pricing Committee (May 5, 2022)
- Executive Risk Committee (May 18, 2022)

---

## 3. Data Environment

### 3.1 Data Sources

The model development utilized data from the following internal and external sources:

**Policy Data (Primary Source):**
- Source System: PolicyMaster 3.0 (core policy administration system)
- Time Period: Policies effective January 1, 2019 - December 31, 2021
- Extraction Date: February 15, 2022
- Records: 520,487 policy-years
- Data Elements: Policy characteristics, coverage selections, vehicle details, driver demographics

**Claims Data:**
- Source System: ClaimsVision 2.5 (claims management system)
- Time Period: Claims with accident dates January 1, 2019 - December 31, 2021
- Extraction Date: February 15, 2022 (with 90-day development lag)
- Records: 47,923 bodily injury claims
- Data Elements: Claim counts, accident details, injury descriptions, payment status

**Territory Data:**
- Source: Internal Geographic Analytics Team
- Territory Definition: 10-zone system based on ZIP code analysis
- Factors Considered: Population density, traffic volume, weather patterns, medical cost indices
- Last Update: January 2022

**Third-Party Data:**
- Vehicle Value Data: J.D. Power Vehicle Valuation Service
- Credit Score Data: LexisNexis Attract (where legally permissible, 8 states)
- Telematics Data: Not included in this model version (planned for 2024 update)

### 3.2 Data Quality Procedures

**Completeness Checks:**
- Policy-level completeness: 99.3% of required fields populated
- Claims-level completeness: 98.7% of required fields populated
- Missing data patterns analyzed; no systemic issues identified
- Records with >3 missing critical fields excluded (0.4% of data)

**Consistency Validation:**
- Cross-system reconciliation performed between policy and claims databases
- Claim counts matched within 0.1% between systems
- Premium amounts validated against financial reporting (99.8% match)
- Temporal consistency checks for policy effective dates and claim dates

**Outlier Detection:**
- Identified and reviewed extreme values for all continuous variables
- Winsorized vehicle values at 1st and 99th percentiles
- Reviewed policies with >5 drivers (0.2% of policies)
- Validated claims with unusual patterns with claims adjusters

**Data Transformations:**
- Exposure basis: Standardized to annual policy-year equivalents
- Date calculations: Policy tenure, driver age at policy effective date
- Aggregations: Prior claim counts over 3-year and 5-year lookback periods
- Categorical grouping: Vehicle make/model grouped into 15 categories

### 3.3 Variable Definitions

The following variables were available for model development:

**Driver Characteristics:**
- `driver_age`: Age of primary driver at policy effective date (continuous, 16-90)
- `driver_gender`: Gender of primary driver (Male, Female)
- `years_licensed`: Years since first licensed (continuous, 0-70)
- `marital_status`: Marital status (Single, Married, Divorced, Widowed)

**Vehicle Characteristics:**
- `vehicle_age`: Age of insured vehicle in years (continuous, 0-25)
- `vehicle_type`: Body style (Sedan, SUV, Truck, Van, Sports Car, Luxury)
- `vehicle_value`: Current market value in thousands (continuous, $2K-$95K)
- `annual_mileage`: Self-reported annual mileage (continuous, 1K-50K)

**Policy Characteristics:**
- `coverage_limit`: BI limit selection ($100K/$300K, $250K/$500K, $500K/$1M, $1M/$2M)
- `policy_tenure`: Years with ABC Insurance (continuous, 0-25)
- `prior_claims_3yr`: Count of at-fault claims in prior 3 years (0, 1, 2, 3+)
- `prior_claims_5yr`: Count of at-fault claims in prior 5 years (0, 1, 2, 3, 4, 5+)

**Geographic Variables:**
- `territory`: Geographic zone (Zone 1-10)
- `state`: State of residence (15 states, used for segmentation only)

**Credit-Based Variables (8 states only):**
- `insurance_score`: Credit-based insurance score (continuous, 300-900)
- Note: In 7 states where credit is prohibited, alternative risk segmentation applied

### 3.4 Data Exclusions

The following data were excluded from model development:

**Policy Exclusions:**
- Commercial auto policies (different rating structure)
- Policies with coverage gaps >30 days (data quality concerns)
- Policies with missing or invalid effective dates (0.3%)
- Policies written through non-standard channels (assigned risk pools)

**Claims Exclusions:**
- Claims still open or pending litigation at extraction date (13% of claims)
- Claims reopened after initial closure (data quality issues)
- Claims with coding errors or inconsistencies (0.8% of claims)

**Geographic Exclusions:**
- Two counties with <100 policies (insufficient credibility)
- One ZIP code with data quality issues (territory reassignment pending)

**Final Analysis Dataset:**
- Policies: 512,340 policy-years (98.4% of extracted data)
- Claims: 41,763 closed BI claims (87.1% of extracted claims)
- Overall claim frequency: 8.15 claims per 100 policy-years

---

## 4. Methodology

### 4.1 Model Type Selection

A Generalized Linear Model (GLM) was selected as the modeling technique for the following reasons:

**Actuarial Standards:**
- GLMs are widely accepted in insurance ratemaking and comply with actuarial standards
- Transparent and interpretable coefficients aid regulatory approval
- Multiplicative structure aligns with traditional rating factors

**Statistical Properties:**
- Poisson distribution appropriate for modeling count data (claim frequency)
- Log link function ensures positive predictions
- Handles exposure basis (policy-years) naturally through offset term
- Addresses overdispersion through quasi-Poisson or negative binomial extensions

**Business Requirements:**
- Coefficients can be directly translated to rating relativities
- Model output easily integrated into existing rating systems
- Supports state-specific adjustments and territorial differences
- Interpretability for underwriters and regulators

**Alternative Techniques Considered:**
- Decision Trees: Less stable, harder to implement in rating systems
- Neural Networks: Lack interpretability, regulatory challenges
- XGBoost: Considered for severity model but not frequency due to explainability needs

### 4.2 Mathematical Formulation

The frequency model follows a GLM framework with Poisson distribution:

**Distribution Assumption:**
```
Y_i ~ Poisson(λ_i × exposure_i)
```

Where:
- Y_i = claim count for policy i
- λ_i = expected claim frequency (per policy-year)
- exposure_i = exposure in policy-years

**Link Function:**
```
log(λ_i) = β_0 + β_1×X_1i + β_2×X_2i + ... + β_k×X_ki
```

**Equivalently:**
```
λ_i = exp(β_0 + Σ β_j×X_ji)
```

**Rating Relativity Interpretation:**
For a categorical variable with baseline level b and level j:
```
Relativity_j = exp(β_j - β_b)
```

**Continuous Variable Interpretation:**
For a continuous variable X with coefficient β:
```
Relativity for change Δ = exp(β × Δ)
```

**Example:**
If β_age = -0.015, then a 10-year increase in driver age corresponds to:
```
Relativity = exp(-0.015 × 10) = exp(-0.15) = 0.86 (14% decrease in frequency)
```

### 4.3 Assumptions

**Key Model Assumptions:**

1. **Independence**: Claims for different policies are independent
   - Justification: Large, geographically diverse portfolio
   - Limitation: May not hold for catastrophic events

2. **Poisson Distribution**: Claim counts follow Poisson distribution
   - Validation: Variance-to-mean ratio checked (ratio = 1.32, acceptable overdispersion)
   - Adjustment: Quasi-Poisson model used to account for overdispersion

3. **Log-Linear Relationship**: Log of expected frequency is linear in predictors
   - Validation: Partial residual plots reviewed for linearity
   - Adjustment: Continuous variables capped/floored where necessary

4. **No Interaction Terms (Base Model)**: Variables act multiplicatively
   - Justification: Parsimony and regulatory acceptance
   - Note: Interaction between vehicle_age and driver_age tested but not significant

5. **Proportional Exposure**: Claim frequency proportional to exposure time
   - Validation: Policies with <30 days exposure excluded
   - Justification: Standard insurance industry practice

6. **Stationarity**: Relationships are stable over the modeling period
   - Validation: Coefficients checked for stability across years 2019-2021
   - Monitoring: Quarterly validation tests for drift

### 4.4 Limitations

**Known Limitations:**

1. **Omitted Variables**: Some predictive factors not included:
   - Distracted driving behavior (data not available)
   - Real-time road conditions (telematics not yet deployed)
   - Driver health conditions (privacy concerns, data limitations)

2. **Credit Score Restrictions**: 7 states prohibit credit-based insurance scoring
   - Impact: Reduced predictive power in those states (AUC 0.68 vs 0.72)
   - Mitigation: Alternative risk variables given higher weight

3. **Self-Reported Data**: Annual mileage is self-reported
   - Risk: Potential underreporting bias
   - Mitigation: Winsorization and reasonability checks applied

4. **Temporal Effects**: Model does not explicitly account for:
   - Seasonality of claims (assumed to average out over exposure period)
   - Economic cycles affecting driving patterns
   - COVID-19 impact on 2020 data (addressed through data weights)

5. **Model Uncertainty**: Standard errors of coefficients indicate uncertainty
   - Confidence intervals calculated for all coefficients
   - Sensitivity testing performed on key variables

6. **Geographic Granularity**: 10-zone system may not capture all location risk
   - Trade-off: Balance between precision and credibility
   - Future: Plan to refine to 15-20 zones pending data accumulation

---

## 5. Model Development Process

### 5.1 Development Data

**Data Splitting Strategy:**

The dataset was split into training, validation, and holdout sets using temporal segmentation:

- **Training Set**: Policies effective 2019-2020 (68% of data)
  - 348,391 policy-years
  - 28,439 claims
  - Used for model fitting and variable selection

- **Validation Set**: Policies effective H1 2021 (16% of data)
  - 81,974 policy-years
  - 6,742 claims
  - Used for hyperparameter tuning and model selection

- **Holdout Set**: Policies effective H2 2021 (16% of data)
  - 81,975 policy-years
  - 6,582 claims
  - Used for final model evaluation (untouched until final testing)

**Rationale for Temporal Split:**
- Avoids data leakage from future to past
- Tests model's ability to predict forward in time
- Mimics real-world deployment scenario

**Exposure Adjustment:**
- All policy exposures standardized to annual equivalents
- Policies with <30 days exposure excluded (insufficient credibility)
- Leap year adjustments applied for 2020 data

### 5.2 Variable Selection

**Initial Variable Pool:**
- Started with 24 potential predictor variables
- Excluded protected class variables (race, religion, national origin)
- Tested univariate relationships with frequency

**Selection Process:**

**Step 1: Univariate Analysis**
- Calculated frequency relativities for each variable independently
- Ranked variables by predictive power (AUC, chi-square test)
- Eliminated 8 variables with weak relationships (p-value > 0.10)

**Step 2: Correlation Analysis**
- Checked for multicollinearity among remaining 16 variables
- `prior_claims_5yr` and `prior_claims_3yr` highly correlated (r=0.85)
- Selected `prior_claims_3yr` due to better data quality

**Step 3: Forward Selection**
- Started with null model (intercept only)
- Added variables one at a time based on AIC improvement
- Stopped when additional variables provided <2 AIC improvement

**Step 4: Refinement**
- Tested interaction terms between key variables
- `driver_age × vehicle_age` tested but not significant (p=0.23)
- `territory × vehicle_type` tested but not significant (p=0.17)

**Final Variable Set:**

12 variables selected for final model:

1. `driver_age` (continuous)
2. `vehicle_age` (continuous)
3. `vehicle_type` (6 categories)
4. `territory` (10 categories)
5. `coverage_limit` (4 categories)
6. `prior_claims_3yr` (4 categories: 0, 1, 2, 3+)
7. `policy_tenure` (continuous)
8. `vehicle_value` (continuous, log-transformed)
9. `annual_mileage` (continuous, log-transformed)
10. `marital_status` (4 categories)
11. `years_licensed` (continuous)
12. `insurance_score` (continuous, for 8 states only)

**Variable Selection Validation:**
- All selected variables statistically significant (p < 0.01)
- Direction of effects consistent with actuarial judgment
- Coefficients stable across train/validation splits

### 5.3 Model Calibration

**Estimation Method:**
- Maximum likelihood estimation (MLE)
- Iteratively reweighted least squares (IRLS) algorithm
- Convergence achieved in 12 iterations (tolerance = 1e-6)

**Offset Term:**
- Log(exposure) used as offset to account for varying policy durations
- Ensures frequency predictions are on per-policy-year basis

**Continuous Variable Transformations:**

- `driver_age`: Capped at 16 (minimum) and 90 (maximum)
- `vehicle_age`: Capped at 25 years (insufficient data beyond)
- `vehicle_value`: Log-transformed to reduce skewness
- `annual_mileage`: Log-transformed to reduce influence of outliers
- `policy_tenure`: Capped at 25 years

**Categorical Variable Baseline:**
- Territory: Zone 5 (median risk)
- Vehicle Type: Sedan (most common)
- Coverage Limit: $100K/$300K (most common)
- Marital Status: Married (lowest risk)
- Prior Claims: Zero claims (lowest risk)

**Handling of Missing Data:**
- Insurance score: Mean imputation for 2% missing values (with indicator variable)
- Annual mileage: Median imputation for 3% missing values
- Other variables: <1% missing, cases excluded from training

**Regularization:**
- Ridge penalty (L2 regularization) applied with λ = 0.01
- Prevents overfitting on rare categories
- Shrinks coefficients toward zero for stability

**Model Convergence Diagnostics:**
- Deviance: 381,245 (training set)
- Degrees of freedom: 348,352 (n - p)
- Dispersion parameter: 1.09 (mild overdispersion, acceptable)
- Pearson chi-square / df = 1.12

---

## 6. Model Performance & Validation

### 6.1 In-Sample Results

**Training Set Performance (2019-2020 data):**

**Discrimination Metrics:**
- AUC (Area Under ROC Curve): 0.74
- Gini Coefficient: 0.48
- Kendall's Tau: 0.32

**Lift Analysis:**
- Top Decile Lift: 2.5x vs. random
- Top Quintile Lift: 2.1x vs. random
- Bottom Decile: 0.42x (58% below average)

**Calibration:**
- Hosmer-Lemeshow test: χ² = 12.4, p-value = 0.14 (good fit)
- Mean predicted frequency: 8.17 per 100 policy-years
- Mean actual frequency: 8.16 per 100 policy-years
- Bias: 0.1% (excellent calibration)

**Predictive Accuracy by Decile:**

| Decile | Actual Freq | Predicted Freq | Ratio | Policy Count |
|--------|-------------|----------------|-------|--------------|
| 1      | 3.42        | 3.38           | 1.01  | 34,839       |
| 2      | 4.87        | 4.83           | 1.01  | 34,839       |
| 3      | 5.94        | 5.91           | 1.01  | 34,839       |
| 4      | 6.78        | 6.81           | 1.00  | 34,839       |
| 5      | 7.64        | 7.68           | 0.99  | 34,839       |
| 6      | 8.52        | 8.55           | 1.00  | 34,839       |
| 7      | 9.61        | 9.58           | 1.00  | 34,839       |
| 8      | 11.04       | 11.12          | 0.99  | 34,839       |
| 9      | 13.28       | 13.35          | 0.99  | 34,839       |
| 10     | 20.56       | 20.49          | 1.00  | 34,839       |

**Overall:** Excellent agreement between actual and predicted across all risk segments.

### 6.2 Out-of-Sample Validation

**Validation Set Performance (H1 2021 data):**

**Discrimination Metrics:**
- AUC: 0.72
- Gini Coefficient: 0.44
- Kendall's Tau: 0.29

**Lift Analysis:**
- Top Decile Lift: 2.3x vs. random
- Top Quintile Lift: 1.9x vs. random
- Bottom Decile: 0.45x (55% below average)

**Calibration:**
- Hosmer-Lemeshow test: χ² = 18.7, p-value = 0.02 (acceptable)
- Mean predicted frequency: 8.22 per 100 policy-years
- Mean actual frequency: 8.22 per 100 policy-years
- Bias: 0.0% (perfect calibration on average)

**Holdout Set Performance (H2 2021 data):**

**Discrimination Metrics:**
- AUC: 0.71
- Gini Coefficient: 0.42
- Kendall's Tau: 0.28

**Performance Consistency:**
- Difference in AUC between training and holdout: 0.03 (acceptable degradation)
- Model demonstrates good generalization without significant overfitting

### 6.3 Sensitivity Analysis

**Coefficient Stability Testing:**

Tested model stability by re-fitting on bootstrap samples (1,000 iterations):

**Key Variable Confidence Intervals (95%):**
- Driver Age: β ∈ [-0.017, -0.013], coefficient = -0.015
- Vehicle Age: β ∈ [0.008, 0.014], coefficient = 0.011
- Prior Claims (1 vs 0): β ∈ [0.42, 0.51], coefficient = 0.465
- Territory Zone 2 vs Zone 5: β ∈ [-0.22, -0.14], coefficient = -0.18

**Parameter Sensitivity:**

Tested model predictions under various scenarios:

**Scenario 1: Medical Cost Inflation**
- Assumption: BI severity increases 10% annually
- Impact: Frequency model unchanged (severity model addresses costs)
- Action: Monitor for potential behavioral changes in claim reporting

**Scenario 2: Autonomous Vehicle Adoption**
- Assumption: 5% of fleet equipped with advanced driver assistance by 2025
- Impact: May reduce frequency for equipped vehicles by 20-30%
- Action: Collect telematics data; plan model update for 2024

**Scenario 3: Economic Recession**
- Assumption: Reduced driving due to unemployment
- Impact: May reduce frequency by 5-10% system-wide
- Action: Monitor exposure trends; adjust base rates if necessary

**Variable Importance (Permutation Method):**

Measured decrease in AUC when each variable is randomly shuffled:

| Variable          | AUC Drop | Importance Rank |
|-------------------|----------|-----------------|
| prior_claims_3yr  | 0.09     | 1               |
| driver_age        | 0.06     | 2               |
| territory         | 0.05     | 3               |
| insurance_score   | 0.04     | 4               |
| vehicle_type      | 0.03     | 5               |
| vehicle_age       | 0.02     | 6               |
| annual_mileage    | 0.02     | 7               |
| policy_tenure     | 0.01     | 8               |
| (remaining vars)  | <0.01    | 9-12            |

**Insight:** Prior claims history is the strongest predictor, followed by driver age and geographic location.

---

## 7. Model Comparison & Selection

### 7.1 Champion Model (Existing Model)

**Current Production Model (Deployed 2016):**

- Technique: GLM with Poisson distribution
- Variables: 7 rating factors (fewer than proposed model)
- Performance:
  - AUC: 0.65 (based on 2021 validation)
  - Gini: 0.30
  - Top Decile Lift: 1.8x
  - Calibration: Underpredicts high-risk segment by 12%

**Known Issues:**
- Deteriorating performance over time (AUC declined from 0.68 in 2017)
- Missing key predictive variables (prior claims not included)
- Outdated territory definitions (based on 2014 analysis)
- Poor discrimination in high-risk segment

### 7.2 Challenger Model (Proposed Model)

**New GLM Model (Documented in this report):**

- Technique: GLM with quasi-Poisson (accounts for overdispersion)
- Variables: 12 rating factors including updated territory system
- Performance:
  - AUC: 0.72 (validation set)
  - Gini: 0.44
  - Top Decile Lift: 2.3x
  - Calibration: Bias <0.5% across all segments

**Improvements:**
- Substantially better discrimination (+0.07 AUC)
- Improved calibration across risk spectrum
- Incorporates prior claims history (strongest predictor)
- Updated territory system with better granularity

### 7.3 Comparison Results

**Side-by-Side Metrics:**

| Metric               | Champion | Challenger | Improvement |
|----------------------|----------|------------|-------------|
| AUC (validation)     | 0.65     | 0.72       | +10.8%      |
| Gini                 | 0.30     | 0.44       | +46.7%      |
| Top Decile Lift      | 1.8x     | 2.3x       | +27.8%      |
| Calibration Bias     | -5.2%    | +0.3%      | Better      |
| Variables            | 7        | 12         | +5          |
| Regulatory Approval  | At risk  | Compliant  | Better      |

**Business Impact Simulation:**

Using 2021 validation data, estimated impact of switching to challenger model:

- **Rate Adequacy**: Improved match between rates and expected losses
  - High-risk segment: Rates increase 8-15% (currently underpriced)
  - Low-risk segment: Rates decrease 3-8% (currently overpriced)

- **Competitive Position**: Better retention of preferred risks
  - Expected 10% reduction in quote-to-bind leakage
  - Estimated 5% improvement in retention of low-risk customers

- **Combined Ratio Impact**: $12M annual improvement
  - Reduced adverse selection: $7M
  - Improved rate adequacy: $5M

### 7.4 Selection Rationale

**Decision: Proceed with Challenger Model**

The Model Risk Governance Committee approved the challenger model for production deployment based on the following rationale:

1. **Superior Predictive Performance**: +10.8% AUC improvement is statistically and practically significant

2. **Better Calibration**: Reduced bias across all risk segments improves rate adequacy

3. **Regulatory Compliance**: Enhanced documentation and validation meet NAIC standards

4. **Business Value**: Projected $12M annual benefit exceeds implementation costs ($2M one-time, $500K annual)

5. **Risk Management**: Improved risk segmentation reduces exposure to adverse selection

6. **Stakeholder Acceptance**: Transparent GLM approach acceptable to regulators and internal users

**Implementation Decision:** Deploy to production in Q3 2022 with 6-month monitoring period before full rate filing.

---

## 8. Implementation Plan

### 8.1 Timeline

**Phase 1: Pre-Production Testing (June 1-30, 2022)**
- Parallel testing in rating engine (shadow mode)
- User acceptance testing with underwriters
- Final regulatory filing preparations
- Documentation review and approval

**Phase 2: Production Deployment (July 1-15, 2022)**
- Deploy model to production rating engine
- Activate model for new business quotes
- Begin transition for renewal policies
- Monitor daily for anomalies

**Phase 3: Renewal Rollout (July 16 - October 15, 2022)**
- Gradual transition of renewal book (10% per week)
- Monitor loss ratio impacts
- Address any customer inquiries
- Complete transition by October 15, 2022

**Phase 4: Monitoring & Validation (July 2022 - June 2023)**
- Monthly performance reviews
- Quarterly validation testing
- Annual model review by Chief Actuary
- Continuous monitoring dashboard

### 8.2 Integration

**Rating System Integration:**
- Model coefficients exported to rating tables
- Rating engine updated to accommodate 12 variables
- API endpoints modified for external quote systems
- Backward compatibility maintained for in-flight quotes

**Database Updates:**
- New fields added to policy database for tracking
- Historical model version stored for audit trail
- Data warehouse updated for reporting
- Performance metrics logged for monitoring

**User Interface Changes:**
- Underwriter workbench updated with new risk scores
- Quote comparison tool enhanced
- Rate indication reports updated
- Training materials prepared

### 8.3 Training

**Actuarial Staff Training:**
- Technical deep-dive on model methodology (4 hours)
- Model monitoring procedures (2 hours)
- Model documentation and governance (2 hours)

**Underwriter Training:**
- Overview of new rating factors (2 hours)
- How to interpret risk scores (1 hour)
- Exception handling procedures (1 hour)

**IT Staff Training:**
- Technical implementation details (4 hours)
- Troubleshooting procedures (2 hours)
- Monitoring dashboard usage (1 hour)

**Compliance & Audit Training:**
- Regulatory compliance documentation (2 hours)
- Model audit procedures (2 hours)

**Training Schedule:** All training completed by June 25, 2022

---

## 9. Ongoing Monitoring & Governance

### 9.1 Monitoring Metrics

**Key Performance Indicators (KPIs):**

**Monthly Monitoring:**
- Actual vs. Expected Frequency (overall and by territory)
- Prediction Bias (actual / predicted - 1)
- Distribution of Risk Scores
- New Business Quote Volume and Conversion Rate
- Loss Ratio Trends

**Quarterly Monitoring:**
- AUC on recent data (rolling 12-month window)
- Lift analysis by decile
- Variable coefficient stability
- Calibration testing (Hosmer-Lemeshow)
- Segment performance (by state, territory, vehicle type)

**Annual Monitoring:**
- Comprehensive model validation
- Regulatory compliance review
- Model assumption testing
- Competitive benchmark analysis
- Model documentation update

**Alert Thresholds:**

Automatic alerts triggered if:
- Actual/Expected frequency >1.10 or <0.90 for 2 consecutive months
- AUC declines below 0.68
- Any coefficient changes >20% when re-estimated on recent data
- Unexplained loss ratio deterioration >3 points
- Data quality issues affect >5% of policies

### 9.2 Review Frequency

**Validation Schedule:**

**Monthly Review (Pricing Team):**
- Review KPI dashboard
- Investigate any triggered alerts
- Document findings in monitoring log
- Escalate material issues to Model Risk Committee

**Quarterly Review (Chief Actuary):**
- Formal validation testing
- Statistical performance assessment
- Review of external changes (regulatory, competitive, economic)
- Sign-off on model continuation or modification

**Annual Review (Model Risk Governance Committee):**
- Comprehensive validation report
- Assessment of continued appropriateness
- Review of model limitations and assumptions
- Decision on model continuation, recalibration, or replacement
- Update to model documentation

**Ad-Hoc Reviews:**
- Triggered by alert thresholds
- Regulatory inquiries or audits
- Material changes to business or data environment
- Merger, acquisition, or strategic changes

### 9.3 Escalation Procedures

**Level 1: Performance Degradation (AUC decline 0.68-0.70)**
- Action: Enhanced monthly monitoring
- Responsibility: Pricing Team
- Timeline: Investigate within 30 days
- Outcome: Document findings; may continue with increased monitoring

**Level 2: Material Performance Issue (AUC decline <0.68)**
- Action: Detailed root cause analysis
- Responsibility: Chief Actuary
- Timeline: Investigation within 15 days, action plan within 30 days
- Outcome: Recalibration or model replacement plan

**Level 3: Regulatory or Audit Concerns**
- Action: Immediate investigation and remediation
- Responsibility: Model Risk Governance Committee + Chief Actuary
- Timeline: Response within 5 business days
- Outcome: Remediation plan with timeline

**Model Replacement Triggers:**

The model will be replaced or substantially revised if:
- AUC declines below 0.65 and cannot be restored through recalibration
- Regulatory requirements change materially
- Major shifts in business strategy (e.g., entering new states, products)
- Data environment changes (e.g., new data sources become available)
- Competitive landscape requires different approach

**Typical Model Lifecycle:** 3-5 years before major revision expected.

---

## Appendices

### Appendix A: Detailed Coefficient Tables

**Continuous Variables:**

| Variable       | Coefficient | Std Error | P-value | 95% CI           |
|----------------|-------------|-----------|---------|------------------|
| driver_age     | -0.0150     | 0.0010    | <0.001  | [-0.017, -0.013] |
| vehicle_age    | 0.0110      | 0.0015    | <0.001  | [0.008, 0.014]   |
| log(veh_value) | -0.0820     | 0.0180    | <0.001  | [-0.117, -0.047] |
| log(annual_mi) | 0.1450      | 0.0220    | <0.001  | [0.102, 0.188]   |
| policy_tenure  | -0.0280     | 0.0035    | <0.001  | [-0.035, -0.021] |
| years_licensed | -0.0090     | 0.0012    | <0.001  | [-0.011, -0.007] |
| insurance_score| -0.0015     | 0.0002    | <0.001  | [-0.002, -0.001] |

**Categorical Variables - Territory:**

| Territory | Coefficient | Std Error | Relativity | Loss Freq |
|-----------|-------------|-----------|------------|-----------|
| Zone 1    | -0.240      | 0.035     | 0.787      | 6.42      |
| Zone 2    | -0.180      | 0.032     | 0.835      | 6.81      |
| Zone 3    | -0.095      | 0.029     | 0.909      | 7.41      |
| Zone 4    | -0.042      | 0.027     | 0.959      | 7.82      |
| Zone 5    | 0.000       | -         | 1.000      | 8.15      |
| Zone 6    | 0.058       | 0.028     | 1.060      | 8.64      |
| Zone 7    | 0.112       | 0.030     | 1.118      | 9.11      |
| Zone 8    | 0.178       | 0.031     | 1.195      | 9.74      |
| Zone 9    | 0.245       | 0.033     | 1.278      | 10.42     |
| Zone 10   | 0.325       | 0.036     | 1.384      | 11.28     |

**Categorical Variables - Vehicle Type:**

| Vehicle Type | Coefficient | Std Error | Relativity | Comments        |
|--------------|-------------|-----------|------------|-----------------|
| Sedan        | 0.000       | -         | 1.000      | Baseline        |
| SUV          | -0.045      | 0.018     | 0.956      | Slightly lower  |
| Truck        | 0.032       | 0.022     | 1.033      | Slightly higher |
| Van          | 0.015       | 0.028     | 1.015      | Similar to base |
| Sports Car   | 0.185       | 0.035     | 1.203      | Highest risk    |
| Luxury       | 0.068       | 0.026     | 1.070      | Moderately high |

**Categorical Variables - Prior Claims (3-year):**

| Prior Claims | Coefficient | Std Error | Relativity | Comments        |
|--------------|-------------|-----------|------------|-----------------|
| 0            | 0.000       | -         | 1.000      | Baseline        |
| 1            | 0.465       | 0.025     | 1.592      | 59% increase    |
| 2            | 0.782       | 0.038     | 2.186      | 119% increase   |
| 3+           | 1.105       | 0.052     | 3.019      | 202% increase   |

### Appendix B: Validation Charts

**Figure B1: ROC Curve (Validation Set)**
```
   1.0 |                    ****
       |                ****
       |             ****
   0.8 |          ****
       |       ****
   TPR |     ****        AUC = 0.72
       |   ****
   0.4 |  ****
       | ****
   0.2 |****
       |
   0.0 |________________
       0.0  0.2  0.4  0.6  0.8  1.0
              FPR (False Positive Rate)
```

**Figure B2: Lift Chart by Decile**
```
Decile  1: ████████████████████████ 2.3x
Decile  2: ███████████████████ 1.9x
Decile  3: ████████████████ 1.6x
Decile  4: ██████████████ 1.4x
Decile  5: ████████████ 1.2x
Decile  6: ██████████ 1.0x (baseline)
Decile  7: ████████ 0.8x
Decile  8: ██████ 0.6x
Decile  9: ████ 0.5x
Decile 10: ██ 0.45x
```

**Figure B3: Actual vs Predicted by Territory**
```
Territory | Actual | Predicted | Ratio
----------|--------|-----------|-------
Zone 1    | ▓▓▓▓▓▓ 6.42 | ▓▓▓▓▓▓ 6.38 | 1.01
Zone 2    | ▓▓▓▓▓▓▓ 6.81 | ▓▓▓▓▓▓▓ 6.83 | 1.00
Zone 3    | ▓▓▓▓▓▓▓ 7.41 | ▓▓▓▓▓▓▓ 7.43 | 1.00
Zone 4    | ▓▓▓▓▓▓▓▓ 7.82 | ▓▓▓▓▓▓▓▓ 7.85 | 1.00
Zone 5    | ▓▓▓▓▓▓▓▓ 8.15 | ▓▓▓▓▓▓▓▓ 8.15 | 1.00
Zone 6    | ▓▓▓▓▓▓▓▓▓ 8.64 | ▓▓▓▓▓▓▓▓▓ 8.66 | 1.00
Zone 7    | ▓▓▓▓▓▓▓▓▓ 9.11 | ▓▓▓▓▓▓▓▓▓ 9.09 | 1.00
Zone 8    | ▓▓▓▓▓▓▓▓▓▓ 9.74 | ▓▓▓▓▓▓▓▓▓▓ 9.76 | 1.00
Zone 9    | ▓▓▓▓▓▓▓▓▓▓ 10.42 | ▓▓▓▓▓▓▓▓▓▓ 10.45 | 1.00
Zone 10   | ▓▓▓▓▓▓▓▓▓▓▓ 11.28 | ▓▓▓▓▓▓▓▓▓▓▓ 11.25 | 1.00
```

### Appendix C: Code Documentation

**Model Training Code (Simplified):**

```python
"""
GLM Frequency Model Training Script
ABC Insurance Company - Personal Auto BI Frequency
Model Version: 2022.1
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from statsmodels.genmod.generalized_linear_model import GLM
from statsmodels.genmod import families

# Load and prepare data
def prepare_data(df):
    """
    Prepare policy data for GLM frequency model.

    Parameters:
    -----------
    df : DataFrame with policy-level data including exposure and claims

    Returns:
    --------
    X : Feature matrix
    y : Target variable (claim counts)
    exposure : Exposure vector (policy-years)
    """

    # Transform continuous variables
    df['log_vehicle_value'] = np.log(df['vehicle_value'])
    df['log_annual_mileage'] = np.log(df['annual_mileage'])

    # Cap continuous variables
    df['driver_age'] = df['driver_age'].clip(16, 90)
    df['vehicle_age'] = df['vehicle_age'].clip(0, 25)

    # Create feature matrix
    feature_cols = [
        'driver_age', 'vehicle_age', 'log_vehicle_value',
        'log_annual_mileage', 'policy_tenure', 'years_licensed',
        'territory', 'vehicle_type', 'prior_claims_3yr',
        'coverage_limit', 'marital_status', 'insurance_score'
    ]

    X = pd.get_dummies(df[feature_cols], drop_first=False)
    y = df['claim_count']
    exposure = df['exposure_years']

    return X, y, exposure

# Train GLM model
def train_frequency_model(X, y, exposure):
    """
    Train Poisson GLM for claim frequency prediction.

    Parameters:
    -----------
    X : Feature matrix
    y : Claim counts
    exposure : Exposure in policy-years

    Returns:
    --------
    model : Fitted GLM model
    """

    # Fit quasi-Poisson GLM with log link
    model = GLM(
        y, X,
        exposure=exposure,
        family=families.Poisson(link=families.links.log())
    )

    results = model.fit(scale='X2')  # Quasi-Poisson for overdispersion

    return results

# Main execution
if __name__ == "__main__":
    # Load data
    df = pd.read_csv("policy_data_2019_2021.csv")

    # Prepare features
    X, y, exposure = prepare_data(df)

    # Train model
    model = train_frequency_model(X, y, exposure)

    # Print summary
    print(model.summary())

    # Export coefficients
    coefficients = model.params
    coefficients.to_csv("frequency_model_coefficients.csv")
```

---

## Document Control

**Version:** 1.0
**Date:** June 1, 2022
**Last Updated:** June 1, 2022

**Prepared by:**
Jane Smith, FSA, MAAA
Senior Actuary, Pricing & Analytics
ABC Insurance Company

**Reviewed by:**
Robert Johnson, FCAS, MAAA
Chief Actuary
ABC Insurance Company

**Approved by:**
Sarah Williams
Model Risk Officer
ABC Insurance Company

**Distribution:**
- Model Risk Governance Committee
- Pricing Committee
- State Insurance Department Filings
- Internal Audit Department
- Corporate Actuarial Library

**Next Review Date:** June 1, 2023

**Model ID:** PAUTO-FREQ-GLM-2022.1
**Documentation Reference:** DOC-2022-FREQ-001

---

**End of Document**
