---
title: "Personal Auto Comprehensive Coverage Model"
model_type: "comprehensive"
technique: "XGBoost"
product: "personal_auto"
coverage: "comprehensive"
year: 2023
status: "production"
---

# Personal Auto Comprehensive Coverage Model - Documentation

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes. No real insurance data, customer information, proprietary methodologies, or confidential information from any insurance company or financial institution is used or simulated.

All names, addresses, policy numbers, claim amounts, and company information are fictional. Any resemblance to actual persons, organizations, or data is purely coincidental.

This project showcases AI agent capabilities for automated documentation generation and is not intended for production use with real data or models.

---

## Executive Summary

ABC Insurance Company developed an advanced machine learning model using Extreme Gradient Boosting (XGBoost) to predict comprehensive coverage loss costs in its personal auto insurance portfolio. This model represents a strategic departure from traditional Generalized Linear Models (GLMs) for comprehensive coverage, leveraging advanced ensemble learning techniques to capture complex non-linear relationships between risk factors and claim frequency/severity.

Comprehensive coverage protects against non-collision losses including theft, vandalism, weather damage (hail, flood, wind), animal collisions, falling objects, and fire. The loss patterns for comprehensive coverage differ fundamentally from collision and liability coverages, exhibiting strong dependencies on geographic weather patterns, vehicle theft rates, and animal population densities that are difficult to capture with traditional linear models.

The XGBoost model incorporates 42 predictive features including vehicle characteristics, geographic risk factors, weather patterns, crime statistics, and temporal features. The model was developed on 4 years of claims experience (2019-2022) representing 1,850,000 policy-years and 185,000 comprehensive claims.

**Key Results:**
- R-squared (frequency): 0.58 (vs. 0.42 for GLM benchmark)
- R-squared (severity): 0.44 (vs. 0.31 for GLM benchmark)
- AUC (claim/no-claim prediction): 0.79 (vs. 0.71 for GLM)
- Mean Absolute Percentage Error (MAPE): 22.8% (vs. 31.5% for GLM)
- Implementation: Q2 2023 (deployed April 1, 2023)
- Expected annual benefit: $8.5M through improved risk segmentation and pricing accuracy

The model underwent rigorous validation including explainability analysis (SHAP values), regulatory review, and business acceptance testing. While XGBoost models are more complex than GLMs, the substantial performance improvement justified the additional complexity for this coverage, and extensive explainability measures ensure regulatory and business acceptance.

---

## 1. Business Context & Objectives

### 1.1 Background

**Comprehensive Coverage Characteristics:**

Comprehensive coverage is unique among personal auto coverages due to its exposure to diverse, often uncorrelated perils:

- **Weather-Related Claims:** Hail damage (28% of claims), wind damage (8%), flood (4%)
- **Theft:** Vehicle theft and theft of vehicle contents (15% of claims)
- **Animal Collisions:** Deer strikes and other wildlife (22% of claims)
- **Vandalism:** Intentional damage (7% of claims)
- **Other:** Fire, falling objects, glass breakage (16% of claims)

**Business Challenges (2019-2022):**

ABC Insurance's comprehensive coverage experienced significant volatility and adverse loss ratio trends:

- **2019 Loss Ratio:** 62%
- **2020 Loss Ratio:** 71% (severe hail season in Midwest)
- **2021 Loss Ratio:** 68%
- **2022 Loss Ratio:** 74% (supply chain issues drove repair costs +18%)
- **Target Loss Ratio:** 60%

**Primary Drivers of Underperformance:**

1. **Weather Volatility:**
   - Catastrophic hail events in 2020 and 2022 (8 CAT events total)
   - Lack of granular weather risk differentiation in pricing
   - Existing GLM model treated all "high hail risk" territories similarly

2. **Theft Trends:**
   - Vehicle theft rates increased 35% (2019-2022) due to organized crime rings
   - Certain vehicle makes/models targeted disproportionately (e.g., pickup trucks for parts)
   - Territory-level theft data not incorporated in GLM model

3. **Supply Chain Impact on Severity:**
   - Parts availability issues (especially for older vehicles)
   - Increased use of aftermarket/OEM parts driving costs up
   - Rental car reimbursement duration extended due to repair delays

4. **Wildlife Patterns:**
   - Deer population growth in suburban expansion areas
   - Existing model used state-level proxies, insufficient granularity
   - Seasonal variation not captured (fall/winter higher risk)

5. **Model Limitations:**
   - GLM model used only 12 variables, R² = 0.42
   - Linear assumptions unable to capture complex interactions
   - Weather × territory, theft × vehicle type interactions missed
   - Poor predictive performance for high-risk segments (top decile MAPE 48%)

### 1.2 Business Problem

**Specific Issues:**

1. **Inadequate Risk Segmentation:**
   - Within-territory loss ratio variation (C.V. = 1.8)
   - High-risk vehicles (theft-prone) insufficiently differentiated
   - Weather risk captured only at territory level, not microclimate

2. **Catastrophe Exposure:**
   - Lack of granular hail risk scoring
   - Concentration risk in severe weather corridors
   - Post-CAT rate inadequacy

3. **Competitive Disadvantage:**
   - Competitors using advanced analytics (some with telematics)
   - Losing low-risk rural business (overpriced)
   - Retaining high-risk urban theft exposure (underpriced)

4. **Operational Inefficiency:**
   - Manual underwriting exceptions for high-risk vehicles
   - Territory-only rating insufficient for granular pricing
   - Frequent out-of-cycle rate adjustments needed

### 1.3 Objectives

**Primary Objectives:**

1. **Improve Predictive Accuracy:**
   - Increase frequency model R² from 0.42 to ≥0.55
   - Increase severity model R² from 0.31 to ≥0.40
   - Reduce MAPE by 25% (from 31.5% to <24%)

2. **Capture Complex Interactions:**
   - Weather × geography interactions
   - Vehicle type × theft risk interactions
   - Temporal patterns (seasonality, trends)

3. **Business Impact:**
   - Improve loss ratio by 4-6 points ($7M-10M annually)
   - Reduce catastrophe loss volatility through better risk segmentation
   - Improve competitive position in low-risk segments

4. **Regulatory Compliance:**
   - Maintain explainability despite model complexity
   - Document validation and monitoring procedures
   - Ensure compliance with NAIC Model Audit Rule and relevant ASOPs

**Secondary Objectives:**

- Establish capability for advanced ML in insurance rating
- Build framework for XGBoost use in other coverages (collision, BI)
- Enhance data science team skills
- Improve integration of external data (weather, crime, wildlife)

**Success Criteria:**

- XGBoost model outperforms GLM benchmark by ≥20% (R²)
- Regulatory approval obtained in all 15 states
- Business stakeholder acceptance (underwriters, actuaries)
- Implementation completed within 6 months
- Positive ROI within 12 months

---

## 2. Regulatory Compliance Statement

### 2.1 NAIC Model Audit Rule Compliance

This XGBoost model has been developed in accordance with NAIC Model Audit Rule requirements for advanced analytics:

**Comprehensive Documentation:**
- Model purpose, data, methodology, assumptions, and limitations fully documented
- Explainability measures implemented (SHAP values, feature importance)
- Comparison to GLM benchmark provided

**Independent Validation:**
- Third-party validation performed by external actuarial firm (January 2023)
- Internal validation by separate team (Model Risk Management)
- Validation findings addressed and documented

**Ongoing Monitoring:**
- Quarterly performance reviews
- Drift detection for input features and predictions
- Champion-challenger framework with GLM as ongoing benchmark

**Governance Oversight:**
- Model Risk Governance Committee approval (February 2023)
- Annual comprehensive review scheduled

### 2.2 Actuarial Standards of Practice

**ASOP No. 12 - Risk Classification:**

This model adheres to risk classification principles:
- All features demonstrate actuarial relevance to comprehensive coverage risk
- No prohibited factors used (race, religion, national origin, credit in prohibited states)
- Feature importance rankings align with actuarial judgment
- Variables subject to statistical significance testing

**ASOP No. 23 - Data Quality:**

Comprehensive data quality procedures applied:
- 4-year experience period (2019-2022) with credibility analysis
- External data sources (weather, crime) validated and documented
- Missing data handling and outlier treatment documented
- Data limitations assessed for materiality

**ASOP No. 41 - Actuarial Communications:**

Documentation meets professional communication standards:
- Clear statement of purpose, scope, and intended use
- Methodology explained at appropriate technical level
- Assumptions, limitations, and uncertainty disclosed
- Reliance on external data and validation work disclosed

**ASOP No. 56 - Modeling:**

Model development follows modeling standards:
- Model design appropriate for purpose (capturing non-linear relationships)
- Validation comprehensive (backtesting, holdout testing, sensitivity analysis)
- Limitations disclosed (e.g., catastrophe modeling separate, limited interpretability)
- Monitoring plan established with performance thresholds

### 2.3 Explainability and Interpretability

**Addressing "Black Box" Concerns:**

While XGBoost is more complex than GLM, extensive explainability measures implemented:

1. **Global Explainability:**
   - Feature importance rankings (which variables matter most)
   - Partial dependence plots (marginal effect of each feature)
   - Comparison to GLM coefficients (directional consistency)

2. **Local Explainability:**
   - SHAP (SHapley Additive exPlanations) values for individual predictions
   - Example predictions with feature contribution breakdowns
   - Ability to explain any individual quote

3. **Regulatory Reporting:**
   - Rate filing includes feature importance tables
   - Example predictions with explanations provided
   - Comparison to GLM benchmark demonstrates superiority
   - All states accepted explainability measures

### 2.4 State Rate Filings

**Filing Strategy:**

- Filed as "Alternative Rating Plan" or "Advanced Analytics" depending on state requirements
- 15 states, all filings submitted November 2022
- All states approved by March 2023 (longest review: 4 months)
- Implementation April 1, 2023

**State-Specific Requirements:**

- **12 states:** Standard approval, explainability documentation accepted
- **2 states:** Required GLM comparison and demonstration of superiority
- **1 state:** Required independent actuarial certification (obtained)

**Regulatory Questions Addressed:**

Common questions and responses:
- **"How do you explain individual predictions?"** → SHAP value examples provided
- **"Is model more discriminatory than GLM?"** → Demonstrated comparable Gini lift, better risk segmentation
- **"How do you monitor for bias?"** → Quarterly monitoring reports, bias metrics tracked
- **"What if model performs poorly?"** → Champion-challenger framework allows reversion to GLM if needed

---

## 3. Data Environment

### 3.1 Data Sources

**Internal Data Sources:**

**Policy and Claims Data:**
- Source: PolicyMaster 3.0 + ClaimsVision 2.5
- Time Period: January 1, 2019 - December 31, 2022 (4 years)
- Policy-Years: 1,850,000
- Comprehensive Claims: 185,000 (10% frequency)
- Average Claim Severity: $3,200
- Total Incurred: $592M

**Comprehensive Claim Types (detailed coding):**
- Hail: 28% of claims, avg severity $3,800
- Animal collision: 22% of claims, avg severity $2,600
- Theft (vehicle): 8% of claims, avg severity $18,500
- Theft (contents): 7% of claims, avg severity $800
- Vandalism: 7% of claims, avg severity $1,400
- Wind: 8% of claims, avg severity $2,800
- Flood: 4% of claims, avg severity $12,400
- Fire: 3% of claims, avg severity $22,000
- Other: 13% of claims, avg severity $1,900

**External Data Sources:**

**NOAA Weather Data:**
- Source: National Oceanic and Atmospheric Administration (public data)
- Granularity: ZIP code level (interpolated from weather stations)
- Time Period: 2019-2022 daily observations
- Variables:
  - Annual hail events (count)
  - Hail severity index (0-10 scale based on hail size)
  - Annual precipitation (inches)
  - Snow days per year
  - Severe wind events (>50 mph)
  - Temperature extremes

**FBI Crime Statistics:**
- Source: FBI Uniform Crime Reporting (UCR) Program
- Granularity: County level
- Time Period: Annual 2019-2022
- Variables:
  - Motor vehicle theft rate (per 100K population)
  - Property crime rate
  - Violent crime rate (contextual)

**State Wildlife Management Data:**
- Source: State Departments of Natural Resources (15 states)
- Granularity: County level
- Time Period: Annual estimates 2019-2022
- Variables:
  - Deer population density (per square mile)
  - Vehicle-wildlife collision reports
  - Hunting season dates (temporal risk variation)

**NICB Vehicle Theft Data:**
- Source: National Insurance Crime Bureau (subscription service)
- Granularity: Make/model/year
- Time Period: Annual theft rates 2019-2022
- Variables:
  - Theft frequency by vehicle type
  - Recovery rate
  - Target vehicle list (organized crime)

**U.S. Census Bureau:**
- Demographics by ZIP code (population density, income, age)
- Used for contextual analysis and missing data imputation

### 3.2 Data Quality Procedures

**Comprehensive Claims Quality:**

**Peril Coding Validation:**
- 94.2% of claims have peril coded (hail, theft, animal, etc.)
- 5.8% coded as "other comprehensive" (manual review for large claims)
- Cross-validation: Hail claims matched to weather events (98.3% consistency)

**Loss Development:**
- Comprehensive claims typically settle quickly (85% closed within 90 days)
- Theft claims longer settlement (vehicle recovery period)
- Development factors applied: 1.05 at 12 months, 1.02 at 24 months

**Outlier Treatment:**
- Total loss vehicles (claim = vehicle value) validated against valuation data
- Fraud-suspected claims flagged and excluded from training (0.4% of claims)
- Catastrophe claims (8 CAT events) flagged but included with weight adjustment

**External Data Quality:**

**Weather Data:**
- Weather station coverage: 99.2% of ZIP codes within 25 miles of station
- Missing daily observations interpolated (spatial interpolation)
- Hail reports validated against Storm Prediction Center database

**Crime Data:**
- County-level data mapped to ZIP codes via population-weighted allocation
- 2022 data not yet available at time of model development (used 2021 as proxy)
- Consistency checks: Year-over-year change <50% flagged for review (all passed)

**Wildlife Data:**
- Deer population estimates vary by state methodology (documented)
- Correlation with reported vehicle-wildlife collisions: r=0.78 (acceptable)
- Missing county data: Imputed using adjacent county average

### 3.3 Feature Engineering

**42 Features Used in XGBoost Model:**

**Vehicle Features (12):**
1. vehicle_age (years)
2. vehicle_value (dollars, log-transformed)
3. vehicle_type (categorical: Sedan, SUV, Truck, Van, Luxury, Sports)
4. vehicle_make (grouped into 15 categories)
5. theft_risk_score (NICB-based, continuous 0-100)
6. vehicle_size (Small, Mid, Large, Very Large)
7. anti_theft_device (binary)
8. glass_type (standard, advanced driver assistance)
9. convertible_flag (binary)
10. vehicle_age_squared (capture non-linearity)
11. high_value_flag (>$50K)
12. classic_car_flag (>25 years old, collectible)

**Geographic Features (10):**
13. territory (categorical, 15 territories)
14. population_density (log-transformed)
15. urban_rural (Urban, Suburban, Rural)
16. latitude (for spatial patterns)
17. longitude (for spatial patterns)
18. coastal_proximity (miles to coast, flood risk)
19. elevation (feet above sea level)
20. hail_risk_zone (5 zones: Very Low to Very High)
21. deer_density (per square mile)
22. crime_index (composite of theft and property crime)

**Weather Features (8):**
23. annual_hail_events (count)
24. hail_severity_index (0-10)
25. annual_precipitation (inches)
26. snow_days_per_year (count)
27. severe_wind_events (count)
28. freeze_thaw_cycles (count, windshield damage risk)
29. tornado_risk_index (0-10)
30. flood_zone (binary, FEMA designated)

**Temporal Features (6):**
31. policy_year (2019-2022)
32. quarter (1-4, seasonality)
33. month (1-12, finer seasonality)
34. deer_season_flag (fall/winter months)
35. severe_weather_season (spring/summer)
36. year_trend (linear trend variable)

**Policy Features (6):**
37. comprehensive_deductible ($100, $250, $500, $1000, $2500)
38. policy_tenure (years with ABC Insurance)
39. multi_vehicle_policy (binary)
40. homeowner_flag (bundled policy)
41. prior_comp_claims_3yr (count)
42. coverage_limit (actual cash value vs. stated amount)

**Interaction Features (Built Automatically by XGBoost):**
XGBoost automatically discovers interactions; no manual interaction terms needed.

### 3.4 Data Exclusions

**Policy Exclusions:**
- Leased vehicles with gap insurance (different recovery patterns): 4.2%
- Commercial use vehicles: 2.8%
- Exotic/specialty vehicles (>$150K): 0.2%
- Policies with <30 days exposure: 1.1%

**Claim Exclusions:**
- Catastrophe claims from 8 CAT events: Flagged, downweighted but not excluded
- Suspected fraud (SIU referrals): Excluded (0.4%)
- Claims with coding errors: Excluded (0.3%)
- Large subrogation recoveries (>$10K): Adjusted

**Final Dataset:**
- Policy-Years: 1,697,500 (91.8% of original)
- Claims: 179,200 (96.9% of original)
- Data Splits: 70% train, 15% validation, 15% holdout

---

## 4. Methodology

### 4.1 Model Selection: Why XGBoost?

**XGBoost (Extreme Gradient Boosting) Overview:**

XGBoost is an ensemble learning method that builds multiple decision trees sequentially, where each tree corrects errors made by previous trees. It is particularly effective for insurance applications due to:

1. **Handles Non-Linearity:** Captures complex relationships without manual specification
2. **Automatic Interaction Detection:** Discovers feature interactions automatically
3. **Robust to Outliers:** Tree-based splits less sensitive to extreme values
4. **Handles Missing Data:** Built-in methods for missing value treatment
5. **Regularization:** Prevents overfitting through L1/L2 penalties and tree pruning
6. **Feature Importance:** Provides interpretability metrics

**Why XGBoost for Comprehensive Coverage:**

Comprehensive coverage has unique characteristics that benefit from XGBoost:

- **Multiple Perils:** Different perils (hail, theft, animal) have different risk profiles
- **Non-Linear Relationships:** Weather risk not linear with precipitation/hail events
- **Complex Interactions:** Theft risk depends on vehicle × location × time
- **Geographic Complexity:** Microclimate weather patterns within territories
- **Temporal Patterns:** Seasonality (deer in fall, hail in spring)

**Comparison to GLM:**

| Aspect                | GLM                          | XGBoost                      |
|-----------------------|------------------------------|------------------------------|
| Interpretability      | High (coefficients)          | Medium (SHAP, feature importance) |
| Non-linearity         | Manual (polynomials)         | Automatic                    |
| Interactions          | Manual specification         | Automatic discovery          |
| Categorical variables | Manual encoding              | Native support               |
| Missing data          | Imputation required          | Built-in handling            |
| Regularization        | Manual (ridge/lasso)         | Built-in                     |
| Computational cost    | Low                          | Moderate                     |
| Regulatory acceptance | High                         | Growing (explainability needed) |

**Decision Rationale:**

- XGBoost offers 38% R² improvement over GLM (0.58 vs. 0.42)
- Complex weather-geography relationships better captured
- Automatic interaction discovery found 15+ important interactions
- Explainability measures (SHAP) address regulatory concerns
- Benefit ($8.5M annually) justifies complexity investment

### 4.2 XGBoost Algorithm Details

**Mathematical Formulation:**

XGBoost builds an ensemble of K trees:
```
ŷ_i = Σ f_k(x_i)
      k=1 to K
```

Where:
- ŷ_i = predicted value for observation i
- f_k = k-th decision tree
- x_i = feature vector for observation i

**Training Objective:**

Minimize regularized objective function:
```
L = Σ l(y_i, ŷ_i) + Σ Ω(f_k)
    i                k

Where:
- l = loss function (MSE for regression, log-loss for classification)
- Ω(f_k) = regularization term = γT + (λ/2)||w||²
  - T = number of leaves in tree k
  - w = leaf weights
  - γ, λ = regularization parameters
```

**Gradient Boosting Process:**

1. Initialize with constant prediction (mean for regression)
2. For k = 1 to K:
   a. Compute gradients and Hessians of loss function
   b. Build tree f_k to predict residuals (with regularization)
   c. Add tree to ensemble: ŷ^(k) = ŷ^(k-1) + η × f_k(x)
      - η = learning rate (shrinkage parameter)
3. Final prediction: ŷ = Σ f_k(x)

**Key Hyperparameters:**

- **n_estimators:** Number of trees (100-1000)
- **max_depth:** Maximum tree depth (3-10), controls complexity
- **learning_rate (η):** Shrinkage factor (0.01-0.3), prevents overfitting
- **subsample:** Fraction of data for each tree (0.5-1.0), stochastic boosting
- **colsample_bytree:** Fraction of features for each tree (0.5-1.0)
- **gamma (γ):** Minimum loss reduction to split (0-10), pruning parameter
- **lambda (λ):** L2 regularization (0-10)
- **alpha:** L1 regularization (0-10)

### 4.3 Model Development Process

**Separate Models for Frequency and Severity:**

Following actuarial standards, frequency and severity modeled separately:

**Frequency Model:**
- Target: Binary (claim / no claim)
- XGBoost objective: `binary:logistic`
- Evaluation metric: AUC, log-loss, lift

**Severity Model:**
- Target: Claim amount (given claim occurred)
- XGBoost objective: `reg:squarederror` (can also use `reg:gamma` or `reg:tweedie`)
- Evaluation metric: RMSE, MAPE, R²

**Data Preparation:**

```python
# Frequency data: All policy-years
X_freq = policy_data[feature_columns]
y_freq = (policy_data['claim_count'] > 0).astype(int)  # Binary
weights_freq = policy_data['exposure']  # Exposure weighting

# Severity data: Only claim records
X_sev = claim_data[feature_columns]
y_sev = claim_data['claim_amount']  # Continuous
weights_sev = None  # Equal weighting of claims
```

**Hyperparameter Tuning:**

Used Randomized Search Cross-Validation:

```python
from sklearn.model_selection import RandomizedSearchCV
import xgboost as xgb

param_distributions = {
    'n_estimators': [100, 200, 500, 1000],
    'max_depth': [3, 4, 5, 6, 7, 8],
    'learning_rate': [0.01, 0.03, 0.05, 0.1, 0.2],
    'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0],
    'gamma': [0, 0.1, 0.5, 1, 2],
    'lambda': [0, 0.1, 1, 5, 10],
}

xgb_model = xgb.XGBClassifier(objective='binary:logistic', random_state=42)

random_search = RandomizedSearchCV(
    xgb_model,
    param_distributions,
    n_iter=100,  # Test 100 random combinations
    cv=5,        # 5-fold cross-validation
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)

random_search.fit(X_train, y_train, sample_weight=weights_train)
best_params = random_search.best_params_
```

**Optimal Hyperparameters (Frequency Model):**
- n_estimators: 500
- max_depth: 6
- learning_rate: 0.05
- subsample: 0.8
- colsample_bytree: 0.8
- gamma: 0.1
- lambda: 1.0
- alpha: 0

**Optimal Hyperparameters (Severity Model):**
- n_estimators: 300
- max_depth: 5
- learning_rate: 0.03
- subsample: 0.9
- colsample_bytree: 0.9
- gamma: 0.5
- lambda: 5.0
- alpha: 0

**Training Process:**

```python
# Train frequency model with optimal hyperparameters
freq_model = xgb.XGBClassifier(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=0.1,
    reg_lambda=1.0,
    objective='binary:logistic',
    random_state=42
)

freq_model.fit(
    X_train_freq,
    y_train_freq,
    sample_weight=weights_train_freq,
    eval_set=[(X_val_freq, y_val_freq)],
    early_stopping_rounds=50,  # Stop if no improvement for 50 rounds
    verbose=False
)

# Train severity model
sev_model = xgb.XGBRegressor(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.03,
    subsample=0.9,
    colsample_bytree=0.9,
    gamma=0.5,
    reg_lambda=5.0,
    objective='reg:squarederror',
    random_state=42
)

sev_model.fit(X_train_sev, y_train_sev)
```

**Early Stopping:**
- Monitors validation performance during training
- Stops training if validation metric doesn't improve for N rounds
- Prevents overfitting, reduces training time

---

## 5. Model Performance & Validation

### 5.1 Frequency Model Performance

**Training Set (2019-2021, 70% of data):**
- AUC: 0.81
- Log-Loss: 0.315
- Accuracy: 0.88 (claim/no-claim)
- Top Decile Lift: 3.8x vs. random

**Validation Set (2022 H1, 15% of data):**
- AUC: 0.79
- Log-Loss: 0.328
- Accuracy: 0.87
- Top Decile Lift: 3.5x vs. random

**Holdout Set (2022 H2, 15% of data):**
- AUC: 0.79
- Log-Loss: 0.331
- Accuracy: 0.87
- Top Decile Lift: 3.6x vs. random

**Comparison to GLM Benchmark:**

| Metric      | GLM  | XGBoost | Improvement |
|-------------|------|---------|-------------|
| AUC         | 0.71 | 0.79    | +11.3%      |
| Log-Loss    | 0.398| 0.331   | -16.8%      |
| R² (pseudo) | 0.42 | 0.58    | +38.1%      |
| Top Decile Lift | 2.6x | 3.6x | +38.5%   |

**Lift by Decile (Holdout Set):**

| Decile | Actual Freq | Predicted Freq (XGB) | Predicted Freq (GLM) | XGB Lift | GLM Lift |
|--------|-------------|----------------------|----------------------|----------|----------|
| 1      | 3.2%        | 3.1%                 | 4.8%                 | 1.03     | 0.67     |
| 2      | 5.1%        | 5.0%                 | 5.9%                 | 1.02     | 0.86     |
| 3      | 6.8%        | 6.9%                 | 7.2%                 | 0.99     | 0.94     |
| 4      | 8.2%        | 8.3%                 | 8.5%                 | 0.99     | 0.96     |
| 5      | 9.6%        | 9.7%                 | 9.8%                 | 0.99     | 0.98     |
| 6      | 11.2%       | 11.1%                | 11.0%                | 1.01     | 1.02     |
| 7      | 13.4%       | 13.5%                | 12.8%                | 0.99     | 1.05     |
| 8      | 16.1%       | 16.0%                | 14.9%                | 1.01     | 1.08     |
| 9      | 20.8%       | 20.5%                | 18.2%                | 1.01     | 1.14     |
| 10     | 35.6%       | 36.2%                | 27.9%                | 0.98     | 1.28     |

**Calibration:** XGBoost shows excellent calibration across all deciles (ratio near 1.0). GLM underpredicts low-risk, overpredicts high-risk.

### 5.2 Severity Model Performance

**Training Set:**
- R²: 0.46
- RMSE: $1,820
- MAPE: 21.5%

**Validation Set:**
- R²: 0.44
- RMSE: $1,890
- MAPE: 22.1%

**Holdout Set:**
- R²: 0.44
- RMSE: $1,910
- MAPE: 22.8%

**Comparison to GLM Benchmark:**

| Metric | GLM    | XGBoost | Improvement |
|--------|--------|---------|-------------|
| R²     | 0.31   | 0.44    | +41.9%      |
| RMSE   | $2,420 | $1,910  | -21.1%      |
| MAPE   | 31.5%  | 22.8%   | -27.6%      |

**Severity by Peril Type (Holdout Set):**

| Peril           | Actual Avg | XGB Predicted | GLM Predicted | XGB MAPE | GLM MAPE |
|-----------------|------------|---------------|---------------|----------|----------|
| Hail            | $3,800     | $3,750        | $3,200        | 18.4%    | 28.7%    |
| Animal          | $2,600     | $2,580        | $2,800        | 19.2%    | 24.3%    |
| Vehicle Theft   | $18,500    | $17,800       | $16,200       | 21.5%    | 35.8%    |
| Contents Theft  | $800       | $820          | $900          | 16.5%    | 22.1%    |
| Vandalism       | $1,400     | $1,380        | $1,500        | 17.8%    | 23.9%    |
| Wind            | $2,800     | $2,750        | $2,600        | 19.6%    | 26.4%    |
| Flood           | $12,400    | $11,900       | $10,800       | 24.2%    | 38.6%    |
| Fire            | $22,000    | $21,200       | $19,500       | 22.7%    | 40.5%    |
| Other           | $1,900     | $1,920        | $1,850        | 18.9%    | 25.2%    |

**XGBoost substantially outperforms GLM across all peril types**, especially for high-severity perils (theft, flood, fire).

### 5.3 Feature Importance

**Top 20 Features (Frequency Model):**

| Rank | Feature                  | Importance | Actuarial Interpretation                          |
|------|--------------------------|------------|---------------------------------------------------|
| 1    | hail_risk_zone           | 0.142      | Hail is #1 driver of comp claims                 |
| 2    | theft_risk_score         | 0.098      | Vehicle theft risk critical                       |
| 3    | deer_density             | 0.085      | Animal collisions major peril                     |
| 4    | territory                | 0.072      | Geography matters (aggregates multiple factors)   |
| 5    | vehicle_value_log        | 0.061      | Higher value = higher theft risk                  |
| 6    | annual_hail_events       | 0.055      | Frequency of hail storms                          |
| 7    | vehicle_age              | 0.048      | Newer vehicles higher comp risk                   |
| 8    | severe_weather_season    | 0.042      | Temporal pattern (spring/summer hail)             |
| 9    | crime_index              | 0.038      | General theft/vandalism environment               |
| 10   | deer_season_flag         | 0.035      | Fall/winter deer collisions spike                 |
| 11   | comprehensive_deductible | 0.032      | Higher deductible = moral hazard reduction        |
| 12   | urban_rural              | 0.029      | Urban = theft, Rural = animal                     |
| 13   | vehicle_type             | 0.028      | Trucks higher theft, SUVs higher animal           |
| 14   | population_density_log   | 0.026      | Density correlates with vandalism                 |
| 15   | prior_comp_claims_3yr    | 0.024      | Prior claims predictive                           |
| 16   | anti_theft_device        | 0.021      | Reduces theft risk                                |
| 17   | snow_days_per_year       | 0.019      | Winter weather driving risk                       |
| 18   | policy_tenure            | 0.018      | Longer tenure = loyalty, better risk              |
| 19   | flood_zone               | 0.017      | FEMA flood zones predictive                       |
| 20   | freeze_thaw_cycles       | 0.015      | Windshield damage risk                            |

**Key Interactions Discovered (via SHAP analysis):**

1. **Hail Risk × Vehicle Age:** Newer vehicles more susceptible (PDR/replacement)
2. **Theft Risk × Urban:** High theft risk amplified in urban areas
3. **Deer Density × Season:** Fall/winter deer risk highest
4. **Territory × Weather:** Microclimate effects within territories
5. **Vehicle Value × Crime:** High-value vehicles in high-crime areas

### 5.4 Explainability: SHAP Values

**SHAP (SHapley Additive exPlanations):**

SHAP values provide local interpretability—explaining why a specific prediction was made.

**Example Prediction 1: High-Risk Policy**

Policy Characteristics:
- 2021 Ford F-150 (high theft risk), vehicle value $45,000
- Territory 12 (urban, high crime)
- Hail risk zone: High
- No anti-theft device

Predicted Frequency: 24.5% (vs. average 10%)

SHAP Value Breakdown:
- Base rate: 10.0%
- Theft risk score (+8.2%): "Ford F-150 on NICB hot list"
- Territory 12 (+3.5%): "High crime urban area"
- Hail risk zone (+2.1%): "Frequent hail storms"
- No anti-theft (-0.5%): Absence of protective device
- Other features (+1.2%)
- **Total: 24.5%**

**Example Prediction 2: Low-Risk Policy**

Policy Characteristics:
- 2018 Honda Civic (low theft risk), vehicle value $12,000
- Territory 3 (suburban, low crime)
- Hail risk zone: Low
- Anti-theft device installed
- 5-year policy tenure

Predicted Frequency: 4.2% (vs. average 10%)

SHAP Value Breakdown:
- Base rate: 10.0%
- Theft risk score (-2.8%): "Honda Civic low theft target"
- Territory 3 (-1.9%): "Low crime suburban area"
- Hail risk zone (-0.8%): "Rare hail events"
- Anti-theft device (-0.2%): "Factory alarm system"
- Policy tenure (-0.1%): "Loyal customer"
- **Total: 4.2%**

**Regulatory Acceptance:**

SHAP explanations provided in rate filings, accepted by all regulators as sufficient interpretability.

---

## 6. Model Comparison & Selection

### 6.1 Champion Model (GLM)

**Existing GLM (2019-2022):**
- Technique: Poisson GLM (frequency), Gamma GLM (severity)
- Variables: 12 predictors
- Frequency R²: 0.42, AUC: 0.71
- Severity R²: 0.31, MAPE: 31.5%

**Strengths:**
- High interpretability
- Regulatory familiarity
- Simple implementation

**Weaknesses:**
- Linear assumptions inadequate for comprehensive coverage
- Manual interaction specification required
- Poor performance for high-risk segments
- Unable to capture weather microclimates

### 6.2 Challenger Model (XGBoost)

**XGBoost Model (2023):**
- Technique: Gradient boosting ensemble
- Variables: 42 features
- Frequency R²: 0.58 (+38%), AUC: 0.79 (+11%)
- Severity R²: 0.44 (+42%), MAPE: 22.8% (-28%)

**Strengths:**
- Captures non-linear relationships
- Automatic interaction detection
- Superior predictive accuracy
- Better high-risk segment performance

**Weaknesses:**
- Lower interpretability (mitigated with SHAP)
- Higher computational cost
- Requires more data science expertise

### 6.3 Business Impact Analysis

**Loss Ratio Improvement Simulation (2022 data):**

Applied both models to 2022 experience:

| Segment               | Actual LR | GLM LR | XGB LR | XGB Improvement |
|-----------------------|-----------|--------|--------|-----------------|
| Low Risk (Deciles 1-3)| 42%       | 48%    | 43%    | Better (less overpriced) |
| Medium Risk (4-7)     | 65%       | 64%    | 64%    | Comparable      |
| High Risk (8-10)      | 89%       | 78%    | 86%    | Better (less underpriced) |
| **Overall**           | **68%**   | **65%**| **64%**| **-4 pts**      |

**XGBoost reduces loss ratio by 4 points** = $8.5M annual benefit on $212M comp premium.

**Competitive Impact:**

- Low-risk segment: XGBoost prices 5-8% lower → improved retention
- High-risk segment: XGBoost prices 8-15% higher → reduced adverse selection
- Quote-to-bind conversion: +4% in competitive territories

### 6.4 Selection Rationale

**Decision: Deploy XGBoost as Primary Model**

Model Risk Governance Committee approved XGBoost (February 2023) based on:

1. **Superior Performance:** 38-42% R² improvement material and statistically significant
2. **Business Value:** $8.5M annual benefit far exceeds $1.5M implementation cost
3. **Explainability Addressed:** SHAP values provide sufficient interpretability
4. **Regulatory Approval:** All 15 states approved rate filings
5. **Risk Management:** Champion-challenger framework allows reversion to GLM if issues arise

**Implementation Strategy:**
- XGBoost primary model for rating (April 2023)
- GLM maintained as benchmark and backup
- Quarterly performance comparison
- Annual comprehensive review

---

## 7. Implementation & Monitoring

### 7.1 Implementation Plan

**Phase 1: Production Deployment (March 2023)**
- Model training on final dataset
- API endpoint development for real-time scoring
- Integration with rating engine
- User acceptance testing

**Phase 2: Rollout (April 1, 2023)**
- New business: Immediate application
- Renewals: 100% immediately (no phase-in due to competitive pressure)
- Agent training and communication

**Phase 3: Monitoring (April-September 2023)**
- Weekly monitoring (first month)
- Monthly performance reviews
- Quarterly comprehensive validation
- Ongoing champion-challenger comparison

### 7.2 Monitoring Metrics

**Model Performance Metrics (Monthly):**
- AUC (rolling 3-month window)
- Calibration (actual/expected by decile)
- Lift analysis
- R² on recent claims

**Business Metrics:**
- Loss ratio by segment
- Quote volume and conversion
- Retention rates
- Competitive win/loss rates

**Model Drift Metrics:**
- Feature distribution shift (PSI - Population Stability Index)
- Prediction distribution shift
- Comparison to GLM benchmark

**Alert Thresholds:**
- AUC drops below 0.75 (from 0.79)
- Calibration error >10% in any decile
- Loss ratio deteriorates >2 points vs. expected

### 7.3 Model Governance

**Quarterly Review:**
- Performance metrics dashboard
- Comparison to GLM benchmark
- Feature importance stability
- SHAP value spot checks

**Annual Comprehensive Review:**
- Full revalidation on recent data
- Regulatory compliance review
- Model refresh decision (retrain with new data)
- Technology/methodology assessment

**Model Refresh Cadence:**
- Annual retraining with most recent 4 years of data
- Hyperparameter tuning if performance degrades
- Feature engineering review (add new external data sources)

---

## 8. Limitations and Future Enhancements

### 8.1 Known Limitations

1. **Catastrophe Modeling:** Model does not explicitly model catastrophe frequency/severity (handled separately via CAT loading)
2. **Rare Perils:** Fire and flood have limited training data (infrequent)
3. **External Data Lag:** Crime data has 1-year lag, wildlife data varies by state
4. **Interpretability:** Despite SHAP, not as transparent as GLM
5. **Computational Cost:** Real-time scoring slower than GLM (50ms vs. 5ms)

### 8.2 Future Enhancements

**Short-Term (2023-2024):**
- Integrate real-time weather API for dynamic hail risk scoring
- Add vehicle trim-level theft data (more granular than make/model)
- Explore calibrated probability outputs (Platt scaling)

**Medium-Term (2024-2025):**
- Incorporate telematics data (driving behavior may affect comp risk via garaging location)
- Add social media-derived wildfire risk scores
- Develop separate model for total loss vs. partial loss

**Long-Term (2025+):**
- Neural network ensemble (combine XGBoost + deep learning)
- Real-time dynamic pricing based on weather forecasts
- Integration with IoT vehicle data (factory telematics)

---

## Appendices

### Appendix A: Hyperparameter Tuning Results

**Frequency Model Cross-Validation (Top 10 Configurations):**

| Rank | n_estimators | max_depth | learning_rate | subsample | colsample | gamma | lambda | CV AUC |
|------|--------------|-----------|---------------|-----------|-----------|-------|--------|--------|
| 1    | 500          | 6         | 0.05          | 0.8       | 0.8       | 0.1   | 1.0    | 0.795  |
| 2    | 700          | 6         | 0.03          | 0.8       | 0.9       | 0.1   | 1.0    | 0.794  |
| 3    | 500          | 7         | 0.05          | 0.7       | 0.8       | 0.0   | 1.0    | 0.793  |
| 4    | 1000         | 5         | 0.03          | 0.9       | 0.9       | 0.5   | 1.0    | 0.792  |
| 5    | 500          | 6         | 0.05          | 0.9       | 0.7       | 0.1   | 0.5    | 0.791  |

**Selected: Rank 1 (optimal trade-off of performance and speed)**

### Appendix B: SHAP Summary Plot Interpretation

**Global Feature Importance via SHAP:**

SHAP summary plots show:
- Feature importance (ranked by mean |SHAP value|)
- Feature effect direction (red = high feature value, blue = low)
- Density of observations at each SHAP value

**Key Insights from SHAP Analysis:**
1. Hail risk zone: High zones (red) have high positive SHAP → increases frequency
2. Theft risk score: High scores (red) strongly increase frequency
3. Deer density: High density (red) increases frequency, but saturates beyond threshold
4. Vehicle value: Non-monotonic effect (interaction with theft risk)

### Appendix C: Model Monitoring Dashboard

**Real-Time Dashboard Metrics (Grafana):**

**Panel 1: Model Performance**
- AUC (rolling 30-day)
- Calibration plot (actual vs. predicted by decile)
- Lift chart

**Panel 2: Business Metrics**
- Loss ratio by territory
- Premium volume
- Quote-to-bind conversion

**Panel 3: Data Drift**
- PSI (Population Stability Index) for top 10 features
- Prediction distribution shift
- Alert indicators

**Panel 4: Champion-Challenger**
- XGBoost vs. GLM performance comparison
- Relative lift
- Business impact differential

---

## Document Control

**Version:** 1.0
**Date:** March 15, 2023
**Last Updated:** March 15, 2023

**Prepared by:**
Dr. Lisa Zhang, PhD
Lead Data Scientist, Advanced Analytics
ABC Insurance Company

**Reviewed by:**
Robert Johnson, FCAS, MAAA
Chief Actuary
ABC Insurance Company

**Reviewed by:**
David Miller, FSA, MAAA
VP, Model Risk Management
ABC Insurance Company

**Approved by:**
Sarah Williams
Model Risk Officer
ABC Insurance Company

**Distribution:**
- Model Risk Governance Committee
- Pricing Committee
- State Insurance Departments (all 15 states)
- Internal Audit
- Data Science Team
- Actuarial Library

**Next Review Date:** March 1, 2024

**Model ID:** PAUTO-COMP-XGB-2023.1
**Documentation Reference:** DOC-2023-COMP-001

---

**End of Document**
