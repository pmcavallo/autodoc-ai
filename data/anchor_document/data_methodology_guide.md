---
title: "Data and Methodology Guide - Model Development Standards"
type: "anchor_document"
company: "ABC Insurance Company"
version: "2.0"
effective_date: "2023-01-01"
status: "active"
---

# Data and Methodology Guide
## Model Development Standards for Personal Auto Insurance

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes. No real insurance data, customer information, proprietary methodologies, or confidential information from any insurance company or financial institution is used or simulated.

All names, addresses, policy numbers, claim amounts, and company information are fictional. Any resemblance to actual persons, organizations, or data is purely coincidental.

This project showcases AI agent capabilities for automated documentation generation and is not intended for production use with real data or models.

---

## Document Purpose and Scope

### Overview

This Data and Methodology Guide serves as the authoritative reference for model development practices at ABC Insurance Company. It establishes standards, procedures, and best practices that must be followed by all actuaries, data scientists, and analysts involved in predictive modeling for personal auto insurance products.

**Target Audience:**
- Actuaries developing pricing, reserving, or risk selection models
- Data scientists building machine learning models
- Analytics team members supporting model development
- Model validators and auditors
- Model Risk Governance Committee members

**Document Scope:**

This guide covers:
- Data sourcing, quality, and governance (Sections 1-3)
- Feature engineering and variable standards (Section 4-5)
- Modeling methodology guidelines (Section 6-7)
- Model validation procedures (Section 8)
- Performance monitoring standards (Section 9)
- Governance and documentation requirements (Section 10)

**Out of Scope:**
- Commercial auto insurance (separate guide exists)
- Homeowners and property products (separate standards)
- Claims reserving-specific methodologies (see Reserving Manual)

**Document Maintenance:**
- Owner: Chief Actuary
- Review Frequency: Annual
- Last Updated: January 1, 2023
- Next Review: January 1, 2024

---

## Section 1: Data Sources and Lineage

### 1.1 Primary Internal Data Sources

**PolicyMaster 3.0 - Policy Administration System**

**Description:** Core system of record for all personal auto policies, containing policy-level, coverage-level, vehicle-level, and driver-level information.

**Key Data Elements:**
- Policy identifiers: Policy number, version number, term effective dates
- Coverage information: Coverage types, limits, deductibles, endorsements
- Vehicle details: VIN, make, model, year, value, usage, garaging location
- Driver information: Name, date of birth, license date, gender, marital status, violations
- Premium and rating: Written premium, earned premium, rating factors, territory
- Policy history: Tenure, lapse history, prior carrier

**Data Refresh Frequency:** Real-time (transactional system)

**Extraction Process:**
- Nightly batch extract to Enterprise Data Warehouse (EDW)
- Incremental updates captured
- Full snapshot extracted monthly for modeling purposes

**Data Quality:**
- Completeness: >99% for required fields
- Accuracy: Validated against underwriting guidelines
- Known Issues:
  - VIN decoding errors (~0.3% of policies)
  - ZIP code assignment issues for PO Box addresses (~0.5%)

**Data Retention:** 10 years of policy history maintained

**Ownership:** VP, Personal Auto Insurance

---

**ClaimsVision 2.5 - Claims Management System**

**Description:** System of record for all claims, from First Notice of Loss (FNOL) through claim closure, including payment details, reserves, recoveries, and claim characteristics.

**Key Data Elements:**
- Claim identifiers: Claim number, policy number, coverage type
- Accident details: Accident date, report date, location, description
- Injury information: Injury type, severity, body part, medical treatment
- Claimant information: Claimant name, age, relationship to insured
- Financial data: Payments (indemnity, expense), reserves, recoveries, subrogation
- Claim handling: Adjuster assigned, attorney involvement, litigation status, closure reason

**Data Refresh Frequency:** Real-time

**Extraction Process:**
- Nightly batch extract to EDW
- Claims extracted with 90-day maturity lag for modeling (to allow development)
- IBNR (Incurred But Not Reported) estimated separately

**Data Quality:**
- Completeness: 98% for core fields
- Accuracy: Payments validated against finance system (99.8% match)
- Known Issues:
  - Injury coding inconsistency (5-8% of claims missing severity coding)
  - Attorney involvement flag sometimes updated late

**Data Retention:** 15 years of claim history

**Ownership:** Chief Claims Officer

---

**Customer360 - Customer Data Platform**

**Description:** Consolidated view of customer interactions, preferences, demographics, and lifetime value metrics.

**Key Data Elements:**
- Customer identifiers: Customer ID (links to policy)
- Demographics: Age, household composition, homeownership status
- Behavioral data: Quote history, shopping patterns, channel preferences
- Tenure and loyalty: Years with company, product holdings, lifetime value
- Marketing preferences: Communication preferences, opt-ins/outs

**Data Refresh Frequency:** Daily

**Extraction Process:** API integration to EDW

**Data Quality:**
- Completeness: 85% (not all customers fully profiled)
- Accuracy: Self-reported data, limited validation

**Data Retention:** 7 years

**Ownership:** Chief Marketing Officer

---

### 1.2 Third-Party Data Sources

**LexisNexis Attract - Credit-Based Insurance Scoring**

**Description:** Credit-based insurance score and supporting credit attributes for use in pricing and risk selection (where permitted by state law).

**Coverage:** Available in 8 of 15 operating states (7 states prohibit)

**Key Data Elements:**
- Insurance score: Continuous score (300-900 range)
- Credit attributes: Account types, payment history, utilization
- Refresh date: Score timestamp

**Refresh Frequency:** Policy inception and renewal

**Integration:** API call during quote and policy issuance

**Data Quality:**
- Match rate: 96% of eligible policies
- No-hit rate: 4% (thin file or no credit history)

**Cost:** $1.50 per score retrieval

**Vendor Contract:** Annual, expires December 31, 2024

**Regulatory:** State-specific model filings required; compliance matrix maintained

---

**J.D. Power Vehicle Valuation Service**

**Description:** Current market values for insured vehicles based on make, model, year, mileage, and condition.

**Key Data Elements:**
- Vehicle value: Estimated market value
- Valuation confidence: High/Medium/Low based on data availability

**Refresh Frequency:** Monthly update file

**Integration:** Batch file loaded to EDW

**Data Quality:**
- Coverage: 99.5% of vehicles valued
- Accuracy: +/- 5% of actual transaction prices (per vendor SLA)

**Cost:** $0.15 per vehicle valuation

**Vendor Contract:** 3-year, expires June 30, 2025

---

**National Weather Service - Weather Data**

**Description:** Historical weather data by location for analyzing weather-related risk, particularly for comprehensive coverage.

**Key Data Elements:**
- Daily precipitation, temperature, wind speed
- Severe weather events (hail, tornado, flood)
- Geographic granularity: County level

**Source:** Public data, no cost

**Refresh Frequency:** Monthly historical updates

**Integration:** Manual download and load to EDW

**Data Quality:**
- Completeness: 100% for counties in operating territory
- Latency: 30-60 day lag for finalized data

---

**U.S. Census Bureau - Demographic Data**

**Description:** Population demographics, economic indicators, and geographic characteristics by ZIP code and county.

**Key Data Elements:**
- Population density, household size, age distribution
- Median income, unemployment rate
- Education levels, homeownership rates

**Source:** Public data (American Community Survey 5-year estimates)

**Refresh Frequency:** Annual

**Integration:** Manual download and load

**Data Quality:**
- Granularity: ZIP Code Tabulation Area (ZCTA) level
- Recency: 1-2 year lag in published data

---

### 1.3 Data Lineage and Governance

**Data Lineage Tracking:**

All model development datasets must document:
- Source systems and extraction dates
- Transformation logic applied
- Join keys and match rates
- Data quality issues and resolutions
- Version control (dataset version number)

**Example Lineage Documentation:**
```
Dataset: Policy_Claims_Model_Dev_2023Q1
Version: v1.0
Created: 2023-01-15

Sources:
- PolicyMaster 3.0: Policies 2019-2022 (extracted 2023-01-10)
- ClaimsVision 2.5: Claims 2019-2022 (extracted 2023-01-10, 90-day lag)
- LexisNexis: Insurance scores (extracted at policy inception)

Transformations:
1. Policy-level aggregation (one record per policy-year)
2. Claim counts and costs rolled up to policy-year
3. Exposure calculated as earned policy-years
4. ZIP code mapped to territory (2023 territory definition)
5. Missing insurance scores imputed with mean (2.3% of records)

Join Logic:
- Policy ← Claims: LEFT JOIN on policy_number (99.6% match)
- Policy ← LexisNexis: LEFT JOIN on policy_number (96.2% match)

Quality Checks:
- Exposure sum matches financial reports: 99.8%
- Claim payments match finance: 99.7%
- No duplicate policy-years: PASS

Final Record Count: 1,524,800 policy-years
Final Claim Count: 124,300 claims
```

**Data Governance Roles:**

- **Data Owner**: Business executive accountable for data quality (e.g., Chief Claims Officer owns claims data)
- **Data Steward**: Operational manager responsible for data maintenance
- **Data Consumer**: Model developer using data (must document usage)

**Data Access Controls:**

- Production data access requires approval from Data Owner
- Personal Identifiable Information (PII) restricted to need-to-know basis
- Synthetic/anonymized data used for model development when feasible
- All data extractions logged and auditable

---

## Section 2: ETL Processes

### 2.1 Extract, Transform, Load (ETL) Standards

**ETL Architecture:**

```
Source Systems → Staging Layer → EDW → Analytics Layer → Model Dev Environment
```

**Staging Layer:**
- Raw data extracted from source systems
- Minimal transformation (datatype conversions only)
- Audit columns added (extract_date, source_system, record_count)
- Retention: 90 days

**Enterprise Data Warehouse (EDW):**
- Cleaned and conformed data
- Historical archive (policy: 10 years, claims: 15 years)
- Slowly Changing Dimension (SCD Type 2) for policy changes
- Star schema design (fact tables + dimension tables)

**Analytics Layer:**
- Pre-aggregated tables for common analyses
- Model-ready datasets with features engineered
- Refreshed monthly

**Model Development Environment:**
- Snapshots extracted for specific model projects
- Version-controlled datasets
- Isolated from production (no write-back)

---

### 2.2 Transformation Rules

**Policy-Level Transformations:**

**1. Exposure Calculation:**
```
Exposure (policy-years) = (Policy_End_Date - Policy_Start_Date) / 365.25

Rules:
- Minimum exposure: 30 days (policies < 30 days excluded)
- Maximum exposure: 1.0 policy-year per annual term
- Mid-term cancellations: Prorated based on cancellation date
- Reinstatements: Separate policy records created
```

**2. Territory Assignment:**
```
Territory = F(ZIP_Code, Effective_Date)

Rules:
- Use ZIP code from garaging address (not mailing address)
- If ZIP code invalid/missing: Use county-level default
- If ZIP code changed mid-term: Use territory at policy effective date
- New ZIP codes: Assigned to nearest similar territory pending recalibration
```

**3. Driver Age Calculation:**
```
Driver_Age = (Policy_Effective_Date - Driver_Birth_Date) / 365.25

Rules:
- Use primary driver age (highest listed driver responsibility)
- Floor at 16 (minimum licensing age)
- Cap at 90 (data sparsity beyond)
- Missing birth date: Exclude policy from modeling
```

**Claim-Level Transformations:**

**1. Claim Development:**
```
Ultimate_Incurred = Paid_to_Date + Case_Reserve + IBNR_Reserve

Rules:
- Claims evaluated with 90-day maturity lag
- Development factors applied based on coverage and accident year
- Large claims (>$250K) individually reviewed
- Reopened claims: Aggregate all payments
```

**2. Claim Frequency:**
```
Claim_Frequency = Claim_Count / Exposure

Rules:
- Count at-fault claims only (for rating)
- Exclude subrogation recoveries (double-count risk)
- Multiple claimants on single policy = 1 claim for frequency
```

**3. Claim Severity:**
```
Claim_Severity = Total_Incurred / Claim_Count

Rules:
- Exclude $0 claims (closed with no payment)
- Include allocated loss adjustment expenses (ALAE)
- Exclude unallocated LAE (ULAE)
- Cap at policy limit + excess (for outlier management)
```

---

### 2.3 Data Aggregation Levels

**Policy-Year Level (Most Common for Modeling):**
```
One record per policy per year

Includes:
- Policy characteristics (as of effective date)
- Aggregated claim counts by coverage
- Aggregated claim costs by coverage
- Exposure in policy-years
```

**Use Cases:** Frequency modeling, loss cost modeling

---

**Claim-Level:**
```
One record per claim

Includes:
- Claim characteristics (injury, treatment, attorney)
- Claim payments and reserves
- Link to policy characteristics
```

**Use Cases:** Severity modeling, claim cost prediction

---

**Driver-Level:**
```
One record per driver per policy-year

Includes:
- Driver characteristics (age, gender, violations)
- Driver's share of exposure
- Claims attributed to driver
```

**Use Cases:** Driver-specific risk modeling (less common)

---

**Coverage-Level:**
```
One record per coverage per policy-year

Includes:
- Coverage-specific limits and deductibles
- Coverage-specific claims
- Coverage-specific premium
```

**Use Cases:** Coverage-specific model development

---

### 2.4 Data Refresh and Version Control

**Model Development Dataset Refresh Cycle:**

- **Frequency:** Quarterly for ongoing model monitoring
- **Timing:** 15th of month following quarter end (to allow for data maturity)
- **Naming Convention:** `PolicyClaims_YYYYQQ_vX.X`
  - Example: `PolicyClaims_2023Q1_v1.0`

**Version Control Standards:**

- **Major Version (X.0):** Change in data structure, new variables added, definition changes
- **Minor Version (0.X):** Data refresh only, no structural changes

**Dataset Documentation:**

Each dataset version must include README file with:
- Source system versions and extraction dates
- Transformation logic changes from prior version
- Data quality metrics (completeness, accuracy)
- Known issues and workarounds
- Record counts and aggregation levels

**Archival:**

- Model development datasets archived for 7 years
- Reproduction scripts (SQL, Python, R) version-controlled in Git
- Allows model reproduction for audit or regulatory review

---

## Section 3: Data Quality Procedures

### 3.1 Data Quality Framework

**Data Quality Dimensions:**

ABC Insurance evaluates data quality across six dimensions:

1. **Completeness:** Percentage of required fields populated
2. **Accuracy:** Data matches source of truth
3. **Consistency:** Data consistent across systems and over time
4. **Validity:** Data conforms to defined formats and ranges
5. **Timeliness:** Data available when needed
6. **Uniqueness:** No unintended duplicate records

**Quality Thresholds:**

| Dimension    | Critical Fields | Important Fields | Optional Fields |
|--------------|-----------------|------------------|-----------------|
| Completeness | ≥99%            | ≥95%             | ≥80%            |
| Accuracy     | ≥99.5%          | ≥98%             | ≥95%            |
| Consistency  | ≥99%            | ≥97%             | ≥90%            |
| Validity     | 100%            | ≥99%             | ≥95%            |
| Timeliness   | Within SLA      | Within SLA+1 day | Within SLA+3 days|
| Uniqueness   | 100%            | ≥99.9%           | ≥99%            |

**Critical Fields (must meet highest standards):**
- Policy number, effective dates, coverage limits
- Claim number, accident date, total incurred
- Premium amounts, exposure calculations

**Important Fields:**
- Driver age, vehicle type, territory
- Injury type, treatment code
- Attorney involvement, claim status

**Optional Fields:**
- Vehicle color, annual mileage (self-reported)
- Secondary driver characteristics
- Claimant demographics (non-rating factors)

---

### 3.2 Data Quality Checks

**Automated Data Quality Checks (Run on Every ETL):**

**Completeness Checks:**
```sql
-- Example: Check policy effective date completeness
SELECT
  COUNT(*) AS total_records,
  SUM(CASE WHEN policy_effective_date IS NULL THEN 1 ELSE 0 END) AS missing_count,
  ROUND(100.0 * SUM(CASE WHEN policy_effective_date IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS completeness_pct
FROM policy_table;

-- Threshold: completeness_pct >= 99%
```

**Accuracy Checks:**
```sql
-- Example: Reconcile claim payments to finance system
SELECT
  SUM(claims_system.paid_loss) AS claims_total,
  SUM(finance_system.paid_loss) AS finance_total,
  ABS(SUM(claims_system.paid_loss) - SUM(finance_system.paid_loss)) / SUM(finance_system.paid_loss) AS variance_pct
FROM claims_table claims_system
JOIN finance_table finance_system ON claims_system.claim_id = finance_system.claim_id;

-- Threshold: variance_pct < 0.5%
```

**Consistency Checks:**
```sql
-- Example: Ensure accident date ≤ report date
SELECT
  COUNT(*) AS total_claims,
  SUM(CASE WHEN accident_date > report_date THEN 1 ELSE 0 END) AS inconsistent_count
FROM claims_table;

-- Threshold: inconsistent_count = 0
```

**Validity Checks:**
```sql
-- Example: Validate driver age in reasonable range
SELECT
  COUNT(*) AS total_policies,
  SUM(CASE WHEN driver_age < 16 OR driver_age > 100 THEN 1 ELSE 0 END) AS invalid_count
FROM policy_table;

-- Threshold: invalid_count < 0.1% of total
```

**Timeliness Checks:**
```sql
-- Example: Check data freshness
SELECT
  MAX(extract_date) AS latest_extract,
  DATEDIFF(CURRENT_DATE, MAX(extract_date)) AS days_since_extract
FROM policy_table;

-- Threshold: days_since_extract <= 1 day (for daily ETL)
```

**Uniqueness Checks:**
```sql
-- Example: Detect duplicate policy records
SELECT
  policy_number,
  policy_term_start_date,
  COUNT(*) AS record_count
FROM policy_table
GROUP BY policy_number, policy_term_start_date
HAVING COUNT(*) > 1;

-- Threshold: No duplicates found
```

---

### 3.3 Outlier Detection and Treatment

**Univariate Outlier Detection:**

**Method 1: Z-Score (for normally distributed variables)**
```
Z-Score = (X - mean) / std_dev

Flag as outlier if |Z-Score| > 3
```

**Method 2: Interquartile Range (IQR) - for skewed distributions**
```
IQR = Q3 - Q1
Lower Fence = Q1 - 1.5 * IQR
Upper Fence = Q3 + 1.5 * IQR

Flag as outlier if X < Lower Fence OR X > Upper Fence
```

**Treatment Options:**

1. **Winsorization:** Cap/floor at percentile threshold
   - Example: Cap vehicle value at 99th percentile
   - Use when: Outliers represent data errors or extreme rare cases

2. **Transformation:** Log or Box-Cox transformation
   - Example: Log(claim_severity) to reduce skewness
   - Use when: Distribution is highly right-skewed

3. **Exclusion:** Remove outliers from training data
   - Example: Exclude claims >$2M (catastrophic injuries)
   - Use when: Outliers require special treatment outside standard model

4. **Separate Modeling:** Model outliers separately
   - Example: Large loss model for claims >$100K
   - Use when: Outliers have different risk drivers

**Documentation Requirement:**

All outlier treatment must be documented:
- Method used (winsorization, transformation, exclusion)
- Threshold applied (percentiles, standard deviations)
- Number of records affected
- Rationale for treatment choice

---

### 3.4 Missing Data Handling

**Missing Data Patterns:**

**1. Missing Completely at Random (MCAR):**
- Missingness unrelated to observed or unobserved data
- Example: Random data entry errors
- Treatment: Simple imputation acceptable

**2. Missing at Random (MAR):**
- Missingness related to observed variables but not the missing value itself
- Example: Income missing more often for younger customers
- Treatment: Conditional imputation or modeling

**3. Missing Not at Random (MNAR):**
- Missingness related to the unobserved value
- Example: High-risk drivers not disclosing violations
- Treatment: Careful analysis; may need selection model

---

**Imputation Methods:**

**Mean/Median Imputation:**
```python
# For continuous variables with <5% missing
df['annual_mileage'].fillna(df['annual_mileage'].median(), inplace=True)

# Also create indicator variable
df['annual_mileage_missing'] = df['annual_mileage'].isna().astype(int)
```

**Use when:** MCAR, <5% missing, low correlation with outcome

---

**Mode Imputation:**
```python
# For categorical variables with <10% missing
df['vehicle_type'].fillna(df['vehicle_type'].mode()[0], inplace=True)
```

**Use when:** MCAR, categorical variable, <10% missing

---

**Regression Imputation:**
```python
# For variables with MAR pattern
from sklearn.linear_model import LinearRegression

# Train imputation model on non-missing cases
train = df[df['vehicle_value'].notna()]
model = LinearRegression()
model.fit(train[['vehicle_age', 'vehicle_type_encoded']], train['vehicle_value'])

# Impute missing values
missing = df[df['vehicle_value'].isna()]
df.loc[df['vehicle_value'].isna(), 'vehicle_value'] = model.predict(
    missing[['vehicle_age', 'vehicle_type_encoded']]
)
```

**Use when:** MAR, predictable from other variables, <20% missing

---

**Multiple Imputation:**
```python
# For complex missing patterns, create multiple imputed datasets
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

imputer = IterativeImputer(n_iter=10, random_state=42)
df_imputed = imputer.fit_transform(df[numeric_cols])

# Fit model on each imputed dataset, combine results
# (Requires specialized packages like statsmodels or R:mice)
```

**Use when:** MAR, complex patterns, important variables with >10% missing

---

**Exclusion:**
```python
# Remove records with missing critical fields
df_clean = df[df['coverage_limit'].notna() & df['territory'].notna()]
```

**Use when:** Critical fields, low completeness (<80%), or MNAR pattern

---

**Standard Practice at ABC Insurance:**

1. **<1% Missing:** Exclude records (minimal impact)
2. **1-5% Missing (continuous):** Median imputation + missing indicator
3. **1-10% Missing (categorical):** Mode imputation + missing indicator
4. **5-20% Missing (predictable):** Regression imputation + missing indicator
5. **>20% Missing:** Investigate root cause; typically exclude or separate analysis

**Always include missing indicator variable** to capture information in missingness pattern.

---

### 3.5 Data Quality Reporting

**Monthly Data Quality Dashboard:**

Metrics tracked and reported to Model Risk Governance Committee:

| Metric                  | Target  | Current | Status |
|-------------------------|---------|---------|--------|
| Policy Data Completeness| ≥99%    | 99.2%   | ✓      |
| Claims Data Completeness| ≥99%    | 98.9%   | ✓      |
| Payment Reconciliation  | ≥99.5%  | 99.7%   | ✓      |
| ZIP Code Match Rate     | ≥99%    | 99.1%   | ✓      |
| Duplicate Records       | 0       | 0       | ✓      |
| ETL Timeliness (days)   | ≤1      | 0.8     | ✓      |

**Status Indicators:**
- ✓ Green: Meets target
- ⚠ Yellow: Within 5% of target (requires monitoring)
- ✗ Red: Fails to meet target (requires remediation plan)

**Escalation:**
- Yellow status: Data Steward investigates within 5 business days
- Red status: Data Owner notified immediately; remediation plan within 3 business days

---

## Section 4: Feature Engineering Standards

### 4.1 Feature Engineering Principles

**Definition:**

Feature engineering is the process of transforming raw data into predictive variables (features) that improve model performance while maintaining interpretability and regulatory compliance.

**Key Principles:**

1. **Actuarial Relevance:** Features should have logical relationship to insurance risk
2. **Stability:** Features should be stable over time (not subject to rapid drift)
3. **Availability:** Features must be available at quote/rating time (no leakage)
4. **Simplicity:** Prefer simpler transformations unless complexity justified by performance
5. **Interpretability:** Features should be explainable to regulators and business users
6. **Compliance:** Features must not violate anti-discrimination laws or regulations

---

### 4.2 Common Feature Transformations

**Age and Tenure Variables:**

**Driver Age:**
```python
# Continuous age (preferred for GLM)
driver_age = (policy_effective_date - driver_birth_date).days / 365.25

# Capped for stability
driver_age_capped = np.clip(driver_age, 16, 90)

# Binned age (if needed for segmentation)
driver_age_band = pd.cut(driver_age, bins=[16, 21, 25, 30, 40, 50, 60, 70, 90],
                          labels=['16-20', '21-24', '25-29', '30-39', '40-49', '50-59', '60-69', '70+'])
```

**Policy Tenure:**
```python
# Years with company
policy_tenure = (current_date - first_policy_date).days / 365.25

# Capped at 25 years (diminishing returns beyond)
policy_tenure_capped = np.clip(policy_tenure, 0, 25)
```

**Actuarial Rationale:**
- Young drivers (16-25) have higher frequency due to inexperience
- Senior drivers (70+) may have higher severity due to fragility
- Longer tenure correlates with loyalty and lower lapse propensity

---

**Prior Claims History:**

**Claims Count (3-year lookback):**
```python
# Count at-fault claims in prior 3 years
prior_claims_3yr = claims_history[
    (claims_history['accident_date'] >= current_date - timedelta(days=1095)) &
    (claims_history['at_fault'] == True)
].shape[0]

# Cap at 3+ (sparse data beyond)
prior_claims_3yr_binned = min(prior_claims_3yr, 3)  # 0, 1, 2, 3+
```

**Claims Frequency (per year exposed):**
```python
# Frequency rate
prior_frequency = prior_claims_count / years_exposed

# Use only if sufficient exposure (≥2 years)
```

**Actuarial Rationale:**
- Prior claims are strongest predictor of future claims
- 3-year window balances recency and credibility
- At-fault claims only (no-fault claims not indicative of risk)

---

**Vehicle Characteristics:**

**Vehicle Age:**
```python
# Age in years
vehicle_age = current_year - vehicle_model_year

# Cap at 25 years
vehicle_age_capped = min(vehicle_age, 25)
```

**Vehicle Value (Log-Transformed):**
```python
# Log transformation reduces skewness
vehicle_value_log = np.log(vehicle_value + 1)  # +1 to handle $0 values

# Alternative: Binning
vehicle_value_band = pd.cut(vehicle_value, bins=[0, 10000, 20000, 35000, 50000, 100000],
                             labels=['<$10K', '$10-20K', '$20-35K', '$35-50K', '>$50K'])
```

**Actuarial Rationale:**
- Older vehicles may have higher frequency (less safety features) but lower severity (lower repair costs)
- Vehicle value impacts severity (comprehensive, collision)
- Log transformation handles wide value range

---

**Geographic Features:**

**Territory (Categorical):**
```python
# ZIP code mapped to territory
territory = zip_to_territory_map[zip_code]

# One-hot encoding for modeling
territory_dummies = pd.get_dummies(territory, prefix='territory', drop_first=True)
```

**Population Density:**
```python
# Derived from Census data
population_density = census_data.loc[zip_code, 'population'] / census_data.loc[zip_code, 'land_area_sq_mi']

# Log transformation
population_density_log = np.log(population_density + 1)
```

**Actuarial Rationale:**
- Urban areas have higher frequency (more traffic) but similar/lower severity
- Territory captures multiple risk factors (traffic, weather, medical costs, legal environment)

---

### 4.3 Interaction Terms

**Definition:** Interaction terms capture non-additive relationships between variables.

**When to Use:**
- Strong actuarial hypothesis for interaction
- Statistical testing shows significance (p < 0.05)
- Improves model performance materially (ΔR² > 0.01)
- Interaction is interpretable and explainable

**Common Interactions:**

**Driver Age × Vehicle Type:**
```python
# Young drivers in sports cars have disproportionately high risk
df['young_driver_sports_car'] = ((df['driver_age'] < 25) & (df['vehicle_type'] == 'Sports Car')).astype(int)
```

**Prior Claims × Territory:**
```python
# Drivers with prior claims in high-risk territories have compounding effect
df['prior_claims_x_high_risk_terr'] = df['prior_claims_3yr'] * (df['territory_risk_score'] > 1.2).astype(int)
```

**Attorney × Injury Severity:**
```python
# Attorney involvement amplifies severity effect for serious injuries
df['attorney_x_severe_injury'] = ((df['attorney_involved'] == True) &
                                   (df['injury_severity'] == 'Severe')).astype(int)
```

**Testing Procedure:**
1. Fit model without interaction
2. Add interaction term
3. Likelihood ratio test (GLM) or ANOVA F-test
4. If p < 0.05 and ΔR² > 0.01, include interaction
5. Document rationale in model documentation

---

### 4.4 Feature Selection Methods

**Objective:** Select subset of features that maximize predictive power while maintaining parsimony (avoid overfitting).

**Method 1: Univariate Analysis**

Test each feature individually:
```python
from sklearn.feature_selection import f_regression

# For continuous outcome
f_stats, p_values = f_regression(X, y)

# Rank features by F-statistic
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'f_stat': f_stats,
    'p_value': p_values
}).sort_values('f_stat', ascending=False)

# Select features with p < 0.10 for further consideration
```

---

**Method 2: Forward Selection (GLM)**

Start with null model, add variables iteratively:
```python
import statsmodels.api as sm

selected_features = []
remaining_features = list(X.columns)

for i in range(len(X.columns)):
    best_aic = float('inf')
    best_feature = None

    for feature in remaining_features:
        test_features = selected_features + [feature]
        model = sm.GLM(y, X[test_features], family=sm.families.Poisson()).fit()

        if model.aic < best_aic:
            best_aic = model.aic
            best_feature = feature

    if best_aic < current_aic - 5:  # AIC improvement threshold
        selected_features.append(best_feature)
        remaining_features.remove(best_feature)
        current_aic = best_aic
    else:
        break  # No more meaningful improvements
```

---

**Method 3: LASSO (L1 Regularization)**

Penalized regression that performs feature selection:
```python
from sklearn.linear_model import LassoCV

# Cross-validated LASSO
lasso = LassoCV(cv=5, random_state=42)
lasso.fit(X_scaled, y)

# Features with non-zero coefficients selected
selected_features = X.columns[lasso.coef_ != 0]
```

---

**Method 4: Tree-Based Importance (XGBoost/Random Forest)**

For exploratory analysis (not final GLM model):
```python
import xgboost as xgb

# Fit XGBoost
model = xgb.XGBRegressor()
model.fit(X, y)

# Feature importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

# Use top features as candidates for GLM
```

---

**ABC Insurance Standard Practice:**

1. **Univariate Screening:** Remove features with p > 0.10
2. **Correlation Check:** Remove highly correlated features (r > 0.8), keep more interpretable
3. **Forward Selection:** Build GLM iteratively (AIC-based)
4. **Expert Review:** Actuarial review of selected features for reasonableness
5. **Validation:** Test on holdout data to ensure generalization

**Feature Selection Criteria:**
- Statistical significance: p < 0.05 in final model
- Actuarial relevance: Logical relationship to risk
- Stability: Coefficients stable across train/validation
- Regulatory acceptability: No prohibited factors
- Interpretability: Explainable to business and regulators

---

## Section 5: Variable Definitions

### 5.1 Standard Variable Catalog

This section provides a comprehensive catalog of standard variables used in personal auto modeling at ABC Insurance Company. All model development should use these standardized definitions to ensure consistency across projects.

---

### 5.2 Policy-Level Variables

**Policy Identifiers:**

| Variable Name       | Type   | Description                          | Source         |
|---------------------|--------|--------------------------------------|----------------|
| policy_number       | String | Unique policy identifier             | PolicyMaster   |
| policy_version      | Int    | Policy version number (for renewals) | PolicyMaster   |
| policy_eff_date     | Date   | Policy effective date                | PolicyMaster   |
| policy_exp_date     | Date   | Policy expiration date               | PolicyMaster   |
| customer_id         | String | Unique customer identifier           | Customer360    |

---

**Policy Characteristics:**

| Variable Name       | Type        | Description                                   | Values/Range         |
|---------------------|-------------|-----------------------------------------------|----------------------|
| policy_tenure       | Float       | Years with ABC Insurance                      | 0-25                 |
| coverage_bi_limit   | Categorical | Bodily injury liability limit                 | $100K/$300K, $250K/$500K, $500K/$1M, $1M/$2M |
| coverage_pd_limit   | Categorical | Property damage liability limit               | $50K, $100K, $250K   |
| collision_deductible| Categorical | Collision deductible                          | $250, $500, $1000, $2500 |
| comp_deductible     | Categorical | Comprehensive deductible                      | $100, $250, $500, $1000 |
| has_collision       | Binary      | Collision coverage elected (1=Yes, 0=No)      | 0, 1                 |
| has_comprehensive   | Binary      | Comprehensive coverage elected                | 0, 1                 |
| has_rental          | Binary      | Rental reimbursement coverage                 | 0, 1                 |
| has_roadside        | Binary      | Roadside assistance coverage                  | 0, 1                 |
| written_premium     | Float       | Annual written premium ($)                    | $400-$8,000          |

---

### 5.3 Driver Variables

**Primary Driver Characteristics:**

| Variable Name         | Type        | Description                               | Values/Range         |
|-----------------------|-------------|-------------------------------------------|----------------------|
| driver_age            | Float       | Age of primary driver (years)             | 16-90 (capped)       |
| driver_gender         | Categorical | Gender of primary driver                  | Male, Female         |
| driver_marital_status | Categorical | Marital status                            | Single, Married, Divorced, Widowed |
| years_licensed        | Float       | Years since first licensed                | 0-70 (capped)        |
| prior_claims_3yr      | Categorical | At-fault claims in prior 3 years          | 0, 1, 2, 3+          |
| prior_claims_5yr      | Categorical | At-fault claims in prior 5 years          | 0, 1, 2, 3, 4, 5+    |
| violations_3yr        | Categorical | Moving violations in prior 3 years        | 0, 1, 2, 3+          |
| dui_5yr               | Binary      | DUI/DWI in prior 5 years (1=Yes)          | 0, 1                 |
| license_status        | Categorical | Driver's license status                   | Valid, Suspended, Revoked |
| num_drivers           | Int         | Number of drivers on policy               | 1-5                  |

**Derived Driver Variables:**

| Variable Name         | Derivation                                    |
|-----------------------|-----------------------------------------------|
| young_driver          | 1 if driver_age < 25, else 0                 |
| senior_driver         | 1 if driver_age >= 65, else 0                |
| new_driver            | 1 if years_licensed < 3, else 0              |
| good_driver           | 1 if prior_claims_3yr==0 AND violations_3yr==0|

---

### 5.4 Vehicle Variables

**Vehicle Characteristics:**

| Variable Name       | Type        | Description                                   | Values/Range         |
|---------------------|-------------|-----------------------------------------------|----------------------|
| vin                 | String      | Vehicle Identification Number                 | 17 characters        |
| vehicle_year        | Int         | Model year of vehicle                         | 1990-2024            |
| vehicle_age         | Int         | Age of vehicle (current_year - vehicle_year)  | 0-25 (capped)        |
| vehicle_make        | Categorical | Vehicle manufacturer                          | 50+ values           |
| vehicle_model       | Categorical | Vehicle model                                 | 500+ values          |
| vehicle_type        | Categorical | Body style                                    | Sedan, SUV, Truck, Van, Sports Car, Luxury |
| vehicle_value       | Float       | Current market value ($)                      | $2,000-$95,000       |
| annual_mileage      | Float       | Self-reported annual miles driven             | 1,000-50,000 (capped)|
| vehicle_use         | Categorical | Primary vehicle use                           | Commute, Pleasure, Business |
| anti_theft          | Binary      | Anti-theft device installed (1=Yes)           | 0, 1                 |
| passive_restraint   | Binary      | Airbags/passive restraint (1=Yes)             | 0, 1                 |

**Derived Vehicle Variables:**

| Variable Name         | Derivation                                    |
|-----------------------|-----------------------------------------------|
| vehicle_value_log     | log(vehicle_value)                            |
| annual_mileage_log    | log(annual_mileage)                           |
| high_performance      | 1 if vehicle_type == 'Sports Car', else 0    |
| old_vehicle           | 1 if vehicle_age > 10, else 0                |

---

### 5.5 Geographic Variables

**Territory and Location:**

| Variable Name         | Type        | Description                               | Values/Range         |
|-----------------------|-------------|-------------------------------------------|----------------------|
| zip_code              | String      | 5-digit ZIP code of garaging address      | 00501-99950          |
| territory             | Categorical | Rating territory (2023 system)            | T1-T15               |
| state                 | Categorical | State of residence                        | 15 states            |
| county                | String      | County name                               | Varies by state      |
| population_density    | Float       | Population per square mile (ZIP level)    | 1-50,000+            |
| urban_rural           | Categorical | Urban/rural classification                | Urban, Suburban, Rural |

**Derived Geographic Variables:**

| Variable Name             | Derivation/Source                         |
|---------------------------|-------------------------------------------|
| population_density_log    | log(population_density + 1)               |
| medical_cost_index        | Medical CPI by region (base 1.0)          |
| territory_risk_score      | Loss cost relativity for territory        |

---

### 5.6 Claim Variables

**Claim Identifiers and Characteristics:**

| Variable Name       | Type        | Description                                   | Values/Range         |
|---------------------|-------------|-----------------------------------------------|----------------------|
| claim_number        | String      | Unique claim identifier                       | 10-digit number      |
| accident_date       | Date        | Date of accident/loss                         | Date                 |
| report_date         | Date        | Date claim reported                           | Date                 |
| close_date          | Date        | Date claim closed (if closed)                 | Date or NULL         |
| coverage_type       | Categorical | Coverage under which claim filed              | BI, PD, Coll, Comp   |
| at_fault            | Binary      | Insured at fault (1=Yes)                      | 0, 1                 |
| claim_status        | Categorical | Current status of claim                       | Open, Closed, Reopened|

**Claim Financial Variables:**

| Variable Name       | Type    | Description                                   | Range                |
|---------------------|---------|-----------------------------------------------|----------------------|
| paid_loss           | Float   | Total paid loss to date ($)                   | $0-$500,000+         |
| case_reserve        | Float   | Case reserve (for open claims) ($)            | $0-$500,000+         |
| total_incurred      | Float   | Paid + case reserve ($)                       | $0-$500,000+         |
| alae                | Float   | Allocated loss adjustment expense ($)         | $0-$50,000           |
| salvage_subrogation | Float   | Recoveries from salvage/subrogation ($)       | $0-$100,000          |
| claim_count         | Int     | Count of claims (typically 1 per record)      | 1                    |

**Claim Characteristics (BI/PD):**

| Variable Name       | Type        | Description                                   | Values               |
|---------------------|-------------|-----------------------------------------------|----------------------|
| injury_severity     | Categorical | Severity of bodily injury                     | Minor, Moderate, Serious, Severe |
| body_part           | Categorical | Primary body part injured                     | Head, Neck, Back, Extremity, Multiple, Other |
| treatment_type      | Categorical | Medical treatment category                    | Outpatient, Inpatient, Surgery, Physical Therapy |
| attorney_involved   | Binary      | Claimant represented by attorney (1=Yes)      | 0, 1                 |
| claimant_age        | Float       | Age of injured claimant                       | 0-95                 |
| multiple_claimants  | Binary      | Multiple claimants on this claim (1=Yes)      | 0, 1                 |

**Derived Claim Variables:**

| Variable Name         | Derivation                                    |
|-----------------------|-----------------------------------------------|
| claim_age_days        | (current_date - accident_date) in days        |
| report_lag_days       | (report_date - accident_date) in days         |
| claim_severity        | total_incurred / claim_count                  |
| large_claim           | 1 if total_incurred > $50,000, else 0        |

---

### 5.7 Time-Based Variables

**Temporal Features:**

| Variable Name       | Type        | Description                                   | Values/Range         |
|---------------------|-------------|-----------------------------------------------|----------------------|
| policy_year         | Int         | Year of policy effective date                 | 2017-2024            |
| accident_year       | Int         | Year of accident date                         | 2017-2024            |
| calendar_year       | Int         | Current calendar year (for trending)          | 2017-2024            |
| quarter             | Int         | Calendar quarter                              | 1, 2, 3, 4           |
| month               | Int         | Calendar month                                | 1-12                 |
| days_to_renewal     | Int         | Days until policy renewal                     | 0-365                |

**Derived Temporal Variables:**

| Variable Name         | Derivation                                    |
|-----------------------|-----------------------------------------------|
| trend_factor          | Annual trend adjustment (e.g., 1.07 for +7%) |
| development_months    | Months since accident (for claims)            |
| policy_age_days       | (current_date - policy_eff_date) in days      |

---

### 5.8 External Data Variables

**Credit-Based Insurance Score (8 states only):**

| Variable Name       | Type    | Description                                   | Range                |
|---------------------|---------|-----------------------------------------------|----------------------|
| insurance_score     | Float   | Credit-based insurance score                  | 300-900              |
| score_available     | Binary  | Score successfully retrieved (1=Yes)          | 0, 1                 |
| score_date          | Date    | Date of score retrieval                       | Date                 |

**Third-Party Enrichment:**

| Variable Name         | Type    | Source              | Description                        |
|-----------------------|---------|---------------------|------------------------------------|
| vehicle_value_jdp     | Float   | J.D. Power          | Vehicle market value ($)           |
| weather_severity_idx  | Float   | National Weather    | Weather severity index (0-100)     |
| traffic_density_idx   | Float   | Dept of Trans.      | Traffic density score (0-100)      |

---

### 5.9 Variable Naming Conventions

**Standard Naming Rules:**

1. **Lowercase with underscores:** `driver_age` not `DriverAge` or `driverAge`
2. **Descriptive names:** `prior_claims_3yr` not `pc3`
3. **Units in name if ambiguous:** `claim_age_days` not `claim_age`
4. **Binary flags:** Prefix with `is_` or `has_` (e.g., `is_urban`, `has_collision`)
5. **Derived variables:** Suffix with transformation type (e.g., `vehicle_value_log`, `driver_age_binned`)

**Prohibited Variable Names:**
- Single letters (e.g., `x`, `y`, `z`) - unclear meaning
- Abbreviations without context (e.g., `cov` could mean coverage or covariance)
- Reserved keywords in SQL/Python (e.g., `select`, `from`, `class`)

---

**End of Sections 1-5**

---

## Document Version Control

**Version:** 2.0
**Effective Date:** January 1, 2023
**Last Updated:** January 1, 2023
**Next Review:** January 1, 2024

**Prepared by:**
Actuarial Standards Committee
ABC Insurance Company

**Approved by:**
Robert Johnson, FCAS, MAAA
Chief Actuary

**Distribution:**
- All actuarial and analytics staff
- Model Risk Governance Committee
- Internal audit department
- Model validators

**Change Log:**

| Version | Date       | Changes                                          | Author              |
|---------|------------|--------------------------------------------------|---------------------|
| 1.0     | 2020-01-01 | Initial release                                  | Actuarial Standards |
| 1.1     | 2021-06-15 | Added third-party data sources section           | Actuarial Standards |
| 1.2     | 2022-03-01 | Updated feature engineering for credit scores    | Actuarial Standards |
| 2.0     | 2023-01-01 | Major update: added Sections 6-10 placeholders   | Actuarial Standards |

---

## Section 6: Modeling Methodology Guidelines

### 6.1 Approved Modeling Techniques

ABC Insurance approves the following modeling techniques for personal auto insurance applications:

**Generalized Linear Models (GLMs):**
- **Status:** Preferred method for most applications
- **Use Cases:** Frequency, severity, loss cost models for all coverages
- **Advantages:** Interpretable, regulatory acceptance, actuarial tradition
- **Distributions:** Poisson (frequency), Gamma/Tweedie (severity)
- **Requirements:** Document link function, distribution choice, dispersion
- **Regulatory:** Generally accepted, minimal explainability concerns

**Gradient Boosting Machines (GBM/XGBoost):**
- **Status:** Approved for specific use cases with justification
- **Use Cases:** Complex coverages (comprehensive), high-dimensional data
- **Advantages:** Superior predictive power, automatic interaction detection
- **Requirements:** SHAP explainability, GLM benchmark comparison
- **Regulatory:** Requires enhanced documentation, explainability analysis
- **Approval:** Model Risk Governance Committee approval required

**Generalized Additive Models (GAMs):**
- **Status:** Approved
- **Use Cases:** When non-linear relationships suspected
- **Advantages:** Flexible, interpretable smoothing functions
- **Requirements:** Document spline choices, degrees of freedom

**Other Techniques (Require Special Approval):**
- Neural Networks: Rarely approved (explainability challenges)
- Random Forests: Approved for exploratory analysis, not production rating
- Support Vector Machines: Not approved (lack of actuarial precedent)

### 6.2 Model Specification Standards

**Frequency Models:**

Objective: Predict probability/rate of claim occurrence

Standard Formulation (Poisson GLM):
```
log(λ_i) = β_0 + β_1×X_1i + ... + β_k×X_ki + log(exposure_i)

Where:
- λ_i = expected claim count for observation i
- log(exposure_i) = offset term
- β coefficients estimated via maximum likelihood
```

Requirements:
- Offset for exposure (policy-years)
- Over-dispersion check (Pearson χ² / df)
- Residual analysis (deviance residuals)

**Severity Models:**

Objective: Predict claim cost given claim occurred

Standard Formulation (Gamma GLM):
```
log(μ_i) = α_0 + α_1×X_1i + ... + α_k×X_ki

Where:
- μ_i = expected claim severity for observation i
- Gamma distribution with log link
```

Requirements:
- Train on closed claims only
- Development adjustments documented
- Outlier treatment specified

### 6.3 Statistical Testing Requirements

All models must include:

**Coefficient Significance:**
- p-value < 0.05 for inclusion (or strong actuarial justification)
- Confidence intervals reported (95%)
- Wald or likelihood ratio tests documented

**Model Goodness-of-Fit:**
- Deviance and Pearson χ² statistics
- AIC/BIC for model comparison
- R² or pseudo-R² reported
- Hosmer-Lemeshow test (if applicable)

**Assumption Testing:**
- Linearity (for GLM, partial residual plots)
- Independence (no systematic residual patterns)
- Distribution fit (Q-Q plots, K-S tests)

---

## Section 7: Model Selection Rationale

### 7.1 Technique Selection Criteria

When choosing between modeling techniques, consider:

**1. Business Objective:**
- Pricing/rating: Prefer interpretable (GLM)
- Claim triage/segmentation: Complex ML acceptable
- Regulatory filing: GLM strongly preferred

**2. Data Characteristics:**
- Linear relationships: GLM sufficient
- Complex interactions: Consider GBM/XGBoost
- High dimensionality: Tree-based or regularized regression

**3. Regulatory Environment:**
- Conservative states: GLM only
- Progressive states: May accept ML with explainability

**4. Performance Improvement:**
- Threshold: ML must show ≥10% improvement over GLM benchmark (R², AUC)
- Cost-benefit: Implementation cost justified by performance gain

**5. Interpretability Requirements:**
- Rate filing: High (GLM preferred)
- Internal use: Moderate (ML acceptable)

### 7.2 Champion-Challenger Framework

Standard practice for model updates:

**Champion Model:**
- Current production model
- Baseline for comparison
- Retained as backup if challenger fails

**Challenger Model:**
- New/updated model being evaluated
- Must outperform champion
- Subject to comprehensive validation

**Promotion Criteria:**

Challenger becomes champion if:
1. Superior performance (statistical significance testing)
2. Passes all validation tests
3. Model Risk Committee approval
4. Regulatory approval (if applicable)
5. Business stakeholder acceptance

**Parallel Running:**
- Run both models for 3-6 months
- Monitor comparative performance
- Document any divergence

### 7.3 Model Complexity Trade-offs

**Parsimony Principle:** Prefer simpler models unless complexity justified

Acceptable reasons for complexity:
- Material performance improvement (>10% R²)
- Capturing known actuarial relationships
- Business requirements demand granularity

---

## Section 8: Validation Procedures

### 8.1 Validation Framework

Three types of validation required:

**1. Development Validation (During Model Building):**
- Train/validation/holdout split
- Cross-validation for hyperparameter tuning
- Residual analysis
- Assumption testing

**2. Pre-Production Validation (Before Deployment):**
- Holdout set performance
- Backtesting on historical data
- Sensitivity analysis
- Stress testing

**3. Ongoing Validation (Post-Deployment):**
- Quarterly performance monitoring
- Annual comprehensive review
- Champion-challenger comparison

### 8.2 Validation Testing Requirements

**Statistical Performance:**
- R² or AUC on holdout data (untouched during development)
- Calibration testing (actual vs. predicted by decile)
- Lift analysis (top/bottom decile comparison)
- Confidence intervals for key metrics

**Business Logic:**
- Coefficient directionality review (actuarial judgment)
- Monotonicity checks (age, claims history should be monotonic)
- Segmentation analysis (high/low risk segments reasonable)

**Stability:**
- Temporal stability (train on Year 1-2, validate on Year 3)
- Geographic stability (performance similar across states/territories)
- Segment stability (no population subgroup with poor performance)

**Sensitivity Analysis:**
- Parameter perturbation (±10% change in key coefficients)
- Scenario testing (recession, catastrophe, trend changes)
- Feature importance stability (bootstrap sampling)

### 8.3 Validation Documentation

Required documentation:

**Validation Report Sections:**
1. Executive Summary
2. Model Description
3. Data Quality Assessment
4. Performance Metrics (train/validation/holdout)
5. Assumption Testing
6. Sensitivity Analysis
7. Comparison to Benchmark
8. Limitations and Risks
9. Recommendation (approve/reject)

**Validation Sign-Off:**
- Validator: Independent of model developer
- Chief Actuary: Final approval authority
- Model Risk Committee: Governance oversight

---

## Section 9: Performance Monitoring Standards

### 9.1 Monitoring Metrics

**Monthly Monitoring (Automated Dashboard):**

Performance Metrics:
- Actual vs. Expected (A/E) Frequency (overall, by segment)
- Actual vs. Expected Severity
- Loss Ratio (actual vs. budget)
- R² or AUC (rolling 12-month window)

Data Quality Metrics:
- Missing data rates
- Feature distribution shifts (PSI - Population Stability Index)
- New/unseen categorical values

**Quarterly Review (Actuarial Team):**

Model Performance:
- Comprehensive A/E analysis by multiple dimensions
- Calibration plots (10 deciles)
- Lift charts
- Segment deep-dives

Model Drift:
- Coefficient stability (refit on recent data, compare coefficients)
- Feature importance changes
- Distribution shifts (input and output)

**Annual Review (Comprehensive):**

- Full model re-validation
- Regulatory compliance review
- Benchmark against champion (if challenger)
- Decision: Continue, recalibrate, or replace

### 9.2 Alert Thresholds

Automatic alerts triggered if:

**Level 1 - Monitoring (Yellow Alert):**
- A/E ratio 1.05-1.10 or 0.90-0.95 for single month
- R² decline 0.02-0.05 from baseline
- PSI > 0.10 for any key feature

Action: Enhanced monitoring, investigation within 30 days

**Level 2 - Material Issue (Orange Alert):**
- A/E ratio >1.10 or <0.90 for 2 consecutive months
- R² decline >0.05 from baseline
- Loss ratio >2 points above budget for quarter
- PSI > 0.25 (severe distribution shift)

Action: Root cause analysis within 15 days, remediation plan within 30 days

**Level 3 - Critical Issue (Red Alert):**
- A/E ratio >1.15 or <0.85 for any month
- R² decline >0.10
- Regulatory inquiry or audit finding
- Systematic bias detected (discrimination concerns)

Action: Immediate escalation to Chief Actuary, Model Risk Committee notification within 5 days

### 9.3 Model Refresh Cadence

**Standard Refresh Cycles:**

- **Frequency/Severity Models:** 3-5 years (or trigger-based)
- **Territory Models:** 5-7 years (major geography changes)
- **Simple Recalibration:** Annually (coefficient re-estimation)

**Trigger-Based Refresh:**

Immediate model refresh if:
- Alert Level 3 (critical issue)
- Regulatory requirement change
- Major business change (M&A, new states)
- Data environment change (new data source, system migration)
- Catastrophe or major market disruption

---

## Section 10: Governance Framework

### 10.1 Model Risk Governance Committee

**Composition:**
- Chief Actuary (Chair)
- Model Risk Officer
- VP Personal Auto Pricing
- Chief Data Scientist
- Internal Audit Representative
- Regulatory Affairs Representative

**Responsibilities:**
- Approve new models and major model updates
- Review quarterly model performance reports
- Approve model policies and standards
- Escalation point for model issues
- Annual model inventory review

**Meeting Frequency:**
- Quarterly (scheduled)
- Ad-hoc (for new model approvals or issues)

### 10.2 Model Documentation Requirements

All production models must have:

**Core Documentation:**
1. **Model Documentation** (this type of document):
   - Business context, objectives
   - Data sources, quality, transformations
   - Methodology, assumptions, limitations
   - Performance metrics, validation results
   - Implementation plan, monitoring procedures

2. **Technical Specification:**
   - Code repository location
   - Model artifacts (serialized models, coefficients)
   - Deployment architecture
   - API documentation

3. **Change Log:**
   - Version history
   - Changes from prior version
   - Impact analysis

**Supporting Documentation:**
- Independent validation report
- Regulatory filing materials (if applicable)
- Business case / ROI analysis
- Training materials for users

### 10.3 Roles and Responsibilities

**Model Developer:**
- Develops model per standards
- Documents methodology
- Performs initial validation
- Implements model in production
- Maintains model documentation

**Model Validator:**
- Independent review (separate from developer)
- Validation testing per Section 8
- Validation report preparation
- Recommendation to approve/reject

**Model Owner (Chief Actuary):**
- Accountable for model performance
- Approves model for production
- Annual performance sign-off
- Escalation authority

**Model Risk Officer:**
- Maintains model inventory
- Coordinates Model Risk Committee
- Ensures policy compliance
- Audit liaison

**Business Stakeholder (Pricing Committee):**
- Defines business requirements
- Reviews model results
- Approves rate changes
- Monitors business impact

### 10.4 Model Lifecycle

**Phase 1: Development (3-6 months)**
- Business case approval
- Data acquisition and exploration
- Model development and testing
- Documentation preparation

**Phase 2: Validation (1-2 months)**
- Independent validation
- Model Risk Committee review
- Regulatory filing (if needed)
- User acceptance testing

**Phase 3: Implementation (1-2 months)**
- Production deployment
- Parallel testing
- User training
- Go-live

**Phase 4: Monitoring (Ongoing)**
- Performance tracking
- Quarterly reviews
- Annual comprehensive review
- Issue resolution

**Phase 5: Retirement (As needed)**
- Replacement model approved
- Transition plan
- Historical model archived
- Lessons learned documentation

### 10.5 Audit and Compliance

**Internal Audit:**
- Annual review of model governance
- Sample model documentation reviews
- Compliance with policies

**Regulatory Audit:**
- NAIC Model Audit Rule compliance
- State insurance department examinations
- Response within required timelines

**Third-Party Validation:**
- Independent actuarial firm review (every 3-5 years)
- Methodology peer review
- Regulatory submission support

---

## Conclusion

This Data and Methodology Guide provides comprehensive standards for personal auto insurance model development at ABC Insurance Company. Adherence to these standards ensures:

- Actuarially sound models
- Regulatory compliance
- Business value delivery
- Risk management
- Audit readiness

**Questions or Clarifications:**
Contact: Chief Actuary's Office
Email: actuarial.standards@abcinsurance.example.com
Phone: (555) 123-4567

---

## Document Version Control

**Version:** 2.0 (Complete)
**Effective Date:** January 1, 2023
**Last Updated:** April 1, 2023 (Sections 6-10 added)
**Next Review:** January 1, 2024

**Prepared by:**
Actuarial Standards Committee
ABC Insurance Company

**Approved by:**
Robert Johnson, FCAS, MAAA
Chief Actuary

**Distribution:**
- All actuarial and analytics staff
- Model Risk Governance Committee
- Internal audit department
- Model validators

**Change Log:**

| Version | Date       | Changes                                          | Author              |
|---------|------------|--------------------------------------------------|---------------------|
| 1.0     | 2020-01-01 | Initial release (Sections 1-5)                   | Actuarial Standards |
| 1.1     | 2021-06-15 | Added third-party data sources                   | Actuarial Standards |
| 1.2     | 2022-03-01 | Updated feature engineering                      | Actuarial Standards |
| 2.0     | 2023-04-01 | Complete: Added Sections 6-10                    | Actuarial Standards |

---

**End of Document (Complete)**
