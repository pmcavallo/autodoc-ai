---
title: "Personal Auto Territory Rating Model"
model_type: "territory"
technique: "Clustering + GLM"
product: "personal_auto"
coverage: "all_coverages"
year: 2023
status: "production"
---

# Personal Auto Territory Rating Model - Documentation

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes. No real insurance data, customer information, proprietary methodologies, or confidential information from any insurance company or financial institution is used or simulated.

All names, addresses, policy numbers, claim amounts, and company information are fictional. Any resemblance to actual persons, organizations, or data is purely coincidental.

This project showcases AI agent capabilities for automated documentation generation and is not intended for production use with real data or models.

---

## Executive Summary

ABC Insurance Company completed a comprehensive territory rerating project to refine geographic risk segmentation across its 15-state operating footprint. The territory rating model defines geographic rating zones that capture loss cost variation driven by traffic density, weather patterns, medical costs, litigation trends, and demographic factors.

The previous territory system, established in 2016, consisted of 10 zones and showed declining predictive power due to population shifts, urbanization, changing traffic patterns, and regional economic changes. The updated territory model expands to 15 zones with enhanced granularity in urban areas and incorporates six years of recent loss experience (2017-2022).

The methodology combines unsupervised clustering techniques (K-means) to identify natural groupings of similar ZIP codes, followed by GLM analysis to quantify territory relativities for frequency and severity across all major coverages (bodily injury, property damage, collision, comprehensive).

**Key Results:**
- Territory zones expanded from 10 to 15 (50% increase in granularity)
- R-squared improvement: 0.28 to 0.35 for frequency, 0.19 to 0.24 for severity
- Lift in highest vs. lowest territory: 3.2x (vs. 2.4x in old system)
- Implementation: Q1 2023 (January 15, 2023)
- Rate impact: Premium neutral overall, but +/-15% redistributionby geography
- Expected annual benefit: $6.5M through improved risk segmentation

The territory model supports all major personal auto coverages and provides foundation for future enhancements including dynamic territory adjustments and integration with telematics-based risk scoring.

---

## 1. Business Context & Objectives

### 1.1 Background

**ABC Insurance Company Geographic Footprint:**

ABC Insurance operates in 15 states across the Midwest and Southern regions:
- Midwest Region: 8 states, 62% of premium
- Southern Region: 7 states, 38% of premium
- Total policies in force: 485,000 (as of December 2022)
- Geographic distribution: 45% urban, 35% suburban, 20% rural

**Territory System History:**

The company's territory rating structure has evolved over time:
- **2008-2015**: 7-zone system (county-based)
- **2016-2022**: 10-zone system (ZIP code-based, current champion)
- **2023 onward**: 15-zone system (ZIP code-based, new challenger)

**Drivers of Territory Rerating:**

1. **Population Migration and Urbanization:**
   - Significant population growth in suburban areas (15% increase 2017-2022)
   - Urban core population shifts affecting traffic and claim patterns
   - Emergence of new high-growth ZIP codes not well-represented in old zones

2. **Traffic Pattern Changes:**
   - Increased traffic congestion in previously suburban areas
   - Changes in commuting patterns (COVID-19 impact 2020-2021)
   - Infrastructure development creating new high-traffic corridors

3. **Regional Economic Divergence:**
   - Some territories experiencing rapid economic growth, others declining
   - Medical cost inflation varying significantly by region (6-14% annually)
   - Litigation costs and attorney representation rates diverging geographically

4. **Model Performance Degradation:**
   - Within-territory loss ratio variation increasing (C.V. >1.4 in some territories)
   - Territory model R² declining from 0.28 (2017) to 0.22 (2022)
   - Competitive pressure in mis-rated territories

### 1.2 Business Problem

**Key Issues with Existing Territory System:**

1. **Inadequate Urban Granularity:**
   - Single zone covering large metropolitan area (400+ ZIP codes)
   - Loss ratios ranging from 45% to 95% within same territory
   - Unable to compete in low-risk urban submarkets

2. **Rural Overaggregation:**
   - Large geographic territories combining dissimilar rural areas
   - Agricultural areas grouped with resort/recreational areas
   - Significant differences in claim frequency and severity

3. **Competitive Disadvantage:**
   - Competitors using 15-25 territory systems in key markets
   - Losing low-risk business in under-priced territories
   - Retaining high-risk business in over-priced territories
   - Quote-to-bind ratio deteriorated 12% in key competitive markets

4. **State-Level Heterogeneity:**
   - Multi-state zones obscuring state-specific loss drivers
   - Medical cost and litigation environments vary significantly by state
   - Regulatory requirements differing across jurisdictions

5. **Data Quality and Assignment:**
   - 2.3% of policies with ZIP code assignment errors
   - New ZIP codes not mapped to territories (require manual intervention)
   - Territory boundary definitions outdated

### 1.3 Objectives

**Primary Objectives:**

1. **Improve Predictive Accuracy:**
   - Increase territory model R² from 0.22 to ≥0.30 for frequency
   - Increase territory model R² from 0.19 to ≥0.22 for severity
   - Reduce within-territory loss ratio C.V. by 25%

2. **Enhance Granularity:**
   - Expand from 10 to 12-18 territories (optimal number data-driven)
   - Split large metropolitan zones into 3-4 sub-zones
   - Maintain credibility (minimum 2,000 policies per territory)

3. **Regulatory Compliance:**
   - Meet state-specific territory definition requirements
   - Ensure rate filings supported by credible data
   - Pass actuarial reasonableness and non-discrimination tests

4. **Business Impact:**
   - Improve competitive position in key markets
   - Reduce adverse selection by $4M annually
   - Increase quote-to-bind conversion by 8% in competitive territories
   - Overall premium-neutral implementation (redistributive, not rate increase)

**Secondary Objectives:**

- Establish foundation for future dynamic territory adjustments
- Enable ZIP code-level analytics for marketing and distribution
- Support telematics integration (territory × driving behavior interactions)
- Improve transparency and auditability of territory assignments

---

## 2. Regulatory Compliance Statement

### 2.1 NAIC Model Audit Rule

This territory rating model complies with the NAIC Model Audit Rule requirements for rating plan documentation, including comprehensive data analysis, methodology description, validation procedures, and governance oversight.

### 2.2 Actuarial Standards of Practice

**ASOP No. 12 - Risk Classification:**

The territory rating system adheres to actuarial principles of risk classification:

- **Causality**: Geographic location demonstrably related to loss frequency and severity through traffic density, weather, medical costs, and legal environment
- **Objectivity**: Territory assignments based on objective geographic data (ZIP codes)
- **Practicality**: ZIP code-based system integrates with existing policy administration
- **Mutually Exclusive**: Each ZIP code assigned to exactly one territory
- **Credibility**: All territories meet minimum credibility standards (2,000+ policies)

**ASOP No. 23 - Data Quality:**

Comprehensive data quality procedures applied:
- Loss experience analyzed over 6-year period (2017-2022)
- Data completeness verified (>99% ZIP code match rate)
- Outlier investigation and treatment documented
- Data source lineage tracked and validated

**ASOP No. 41 - Actuarial Communications:**

Documentation includes scope, methodology, data, assumptions, limitations, and intended use. Uncertainty quantified through confidence intervals and sensitivity testing.

**ASOP No. 56 - Modeling:**

Model design appropriate for purpose, validation comprehensive, limitations disclosed, monitoring plan established.

### 2.3 State Insurance Department Requirements

**State-Specific Compliance:**

Territory definitions comply with state regulations in all 15 operating states:

- **ZIP Code-Based Systems**: Approved in 12 states
- **County-Based Requirements**: 3 states require county-based territories (hybrid approach used)
- **Rate Filing Requirements**: Territory relativities filed and approved in all states (Q4 2022)
- **Anti-Discrimination**: Territory definitions do not use prohibited factors (race, religion, national origin)
- **Contiguity Requirements**: Some states require geographically contiguous territories (met via clustering constraints)

**Regulatory Approval Timeline:**
- Rate filings submitted: October 2022
- All states approved: December 2022
- Implementation date: January 15, 2023

### 2.4 Internal Governance

**Approvals:**
- Model Risk Governance Committee: November 18, 2022
- Chief Actuary: November 22, 2022
- Pricing Committee: December 1, 2022
- State Regulatory Affairs: December 5, 2022
- Executive Risk Committee: December 8, 2022

---

## 3. Data Environment

### 3.1 Data Sources

**Policy-Level Experience Data:**
- Source: PolicyMaster 3.0 + ClaimsVision 2.5
- Time Period: January 1, 2017 - December 31, 2022 (6 years)
- Policy-years: 2,847,500 (avg 474,583 per year)
- Coverages: Bodily Injury, Property Damage, Collision, Comprehensive
- Geographic Coverage: 15 states, 3,428 unique ZIP codes

**Claim Data:**
- Claim Counts: 245,800 total claims
- Claim Costs: $2.1B total incurred losses
- Coverage Distribution:
  - Collision: 42% of claim count, 38% of cost
  - Comprehensive: 28% of count, 18% of cost
  - Bodily Injury: 18% of count, 32% of cost
  - Property Damage: 12% of count, 12% of cost

**Geographic Variables (Third-Party Data):**

**U.S. Census Bureau:**
- Population density by ZIP code
- Median household income
- Age distribution
- Urban/rural classification

**Department of Transportation:**
- Annual vehicle miles traveled (VMT) by county
- Road density and highway miles
- Traffic accident statistics

**National Weather Service:**
- Annual precipitation by region
- Snow/ice days by location
- Severe weather event frequency

**Medical Cost Data:**
- Medical cost index by region (commercial source)
- Hospital density and proximity
- Average medical costs by market

**Legal Environment:**
- Attorney representation rates by county
- Average tort awards by jurisdiction
- Litigation frequency indices

### 3.2 Data Quality Procedures

**ZIP Code Assignment Validation:**
- 99.1% of policies successfully geocoded to ZIP code
- 0.9% with invalid or missing ZIP codes (excluded from analysis)
- New ZIP codes identified and mapped (78 new ZIP codes since 2016)
- ZIP code boundary changes tracked and reconciled

**Loss Experience Credibility:**
- Minimum credibility threshold: 50 claims per coverage per ZIP code over 6 years
- ZIP codes below threshold grouped with adjacent similar ZIP codes
- 3,428 ZIP codes aggregated into 15 credible territories

**Exposure Calculation:**
- Earned exposures calculated as policy-year equivalents
- Adjustment for partial-year policies (pro-rata)
- Exclusion of commercial policies and non-standard business
- Final earned exposures: 2,847,500 policy-years

**Loss Development:**
- Claims evaluated with 12-month lag (development to ultimate)
- IBNR (Incurred But Not Reported) added based on historical patterns
- Large losses (>$250K) reviewed individually
- Loss triangles developed by coverage and state

**Outlier Treatment:**
- ZIP codes with <500 policies excluded from clustering (insufficient data)
- Claim frequency outliers (>3 standard deviations) investigated
- Large loss events (catastrophes) excluded or adjusted
- 1.2% of ZIP codes treated as outliers and merged with neighbors

### 3.3 Variable Definitions

**Geographic Variables Used in Clustering:**

**Demographic:**
- `population_density`: Population per square mile
- `median_income`: Median household income
- `pct_urban`: Percentage urban classification
- `age_median`: Median age of population

**Traffic and Road:**
- `vmt_per_capita`: Vehicle miles traveled per capita
- `road_density`: Road miles per square mile
- `highway_access`: Distance to nearest major highway (miles)
- `traffic_congestion_index`: Relative congestion score (0-100)

**Weather:**
- `annual_precipitation`: Inches per year
- `snow_ice_days`: Days with snow/ice per year
- `severe_weather_events`: Count of severe weather events annually

**Economic:**
- `unemployment_rate`: Percentage unemployed
- `commute_time_avg`: Average commute time in minutes

**Medical and Legal:**
- `medical_cost_index`: Regional medical cost factor (base 1.0)
- `hospital_density`: Hospitals per 100,000 population
- `attorney_rate`: Percentage of claims with attorney representation
- `litigation_index`: Relative litigation frequency (base 1.0)

**Loss Experience Variables (Outcome Measures):**
- `frequency_bi`: BI claim frequency per 100 policy-years
- `severity_bi`: Average BI claim cost
- `frequency_pd`: PD claim frequency per 100 policy-years
- `severity_pd`: Average PD claim cost
- `frequency_coll`: Collision claim frequency per 100 policy-years
- `severity_coll`: Average collision claim cost
- `frequency_comp`: Comprehensive claim frequency per 100 policy-years
- `severity_comp`: Average comprehensive claim cost

### 3.4 Data Exclusions

**Policy Exclusions:**
- Commercial auto policies (different risk profile)
- Non-standard/assigned risk policies
- Policies with <30 days exposure
- Policies with missing/invalid ZIP codes (0.9%)

**Geographic Exclusions:**
- ZIP codes with <500 policies over 6-year period (insufficient credibility)
- Newly established ZIP codes with <2 years of experience
- Military base ZIP codes (transient population, special risk profile)
- PO Box-only ZIP codes (no residential risk)

**Claim Exclusions:**
- Catastrophic weather events (hurricanes, widespread flooding)
- Large subrogation claims (>$500K, special handling)
- Claims with coding errors or inconsistencies

**Final Dataset:**
- ZIP codes: 3,201 (out of 3,428 original)
- Policy-years: 2,821,400 (99.1% of original)
- Claims: 243,500 (99.1% of original)
- Geographic coverage: 15 states, 99.3% of operating territory

---

## 4. Methodology

### 4.1 Model Type Selection

The territory rating model uses a **two-stage approach**:

**Stage 1: Unsupervised Clustering (K-means)**
- Purpose: Group similar ZIP codes into natural geographic risk zones
- Inputs: Demographic, traffic, weather, medical cost, and legal environment variables
- Output: 12-18 candidate territory groupings
- Method: K-means clustering with geographic contiguity constraints

**Stage 2: GLM Relativities Estimation**
- Purpose: Quantify loss cost differences between territories
- Inputs: Loss experience (frequency and severity by coverage)
- Outputs: Territory relativities for rating
- Method: Poisson GLM (frequency) and Gamma GLM (severity)

**Rationale for Two-Stage Approach:**

**Why Clustering First:**
- Identifies natural groupings based on objective risk factors
- Avoids arbitrary geographic boundaries (e.g., county lines)
- Incorporates multiple dimensions of risk simultaneously
- Data-driven and reproducible

**Why GLM Second:**
- Quantifies actual loss experience differences
- Produces relativities directly usable in rating
- Statistical testing of territory differences
- Confidence intervals for uncertainty quantification

**Alternative Approaches Considered:**

**County-Based Territories:**
- Pros: Simple, regulatory familiarity
- Cons: Arbitrary boundaries, insufficient granularity in large counties
- Decision: Rejected in favor of ZIP code-based approach

**Pure GLM (No Clustering):**
- Pros: Directly models loss experience
- Cons: Requires pre-defined territory structure, lacks flexibility
- Decision: Clustering provides better starting point

**Geospatial Modeling:**
- Pros: Smooth continuous risk surface
- Cons: Implementation challenges, regulatory acceptance issues
- Decision: Considered for future Phase 2 enhancement

### 4.2 Mathematical Formulation

**Stage 1: K-means Clustering**

**Objective Function:**
```
Minimize: Σ Σ ||x_i - μ_k||²
         k i∈C_k
```

Where:
- x_i = feature vector for ZIP code i
- μ_k = centroid of cluster k
- C_k = set of ZIP codes assigned to cluster k
- ||·||² = squared Euclidean distance

**Geographic Contiguity Constraint:**
```
For clusters k and k':
If ZIP code i ∈ C_k and ZIP code j ∈ C_k',
and i and j are adjacent,
then clusters k and k' must be geographically contiguous
```

**Credibility Constraint:**
```
For each cluster k:
Σ exposure_i ≥ 2,000 policy-years per year
i∈C_k
```

**Stage 2: GLM Relativities**

**Frequency Model (Poisson GLM):**
```
log(λ_t) = β_0 + β_t
```

Where:
- λ_t = expected claim frequency for territory t
- β_t = territory coefficient (β_baseline = 0)

**Relativity:**
```
Rel_t = exp(β_t)
```

**Severity Model (Gamma GLM):**
```
log(μ_t) = α_0 + α_t
```

Where:
- μ_t = expected claim severity for territory t
- α_t = territory coefficient (α_baseline = 0)

**Relativity:**
```
Rel_t = exp(α_t)
```

**Combined Loss Cost Relativity:**
```
Loss Cost Rel_t = Frequency Rel_t × Severity Rel_t
```

**Example:**
If Territory 8 has:
- Frequency relativity = 1.25 (25% higher frequency)
- Severity relativity = 1.10 (10% higher severity)
- Loss cost relativity = 1.25 × 1.10 = 1.375 (37.5% higher loss cost)

### 4.3 Assumptions

**Key Assumptions:**

1. **Homogeneity Within Territories:**
   - Assumption: ZIP codes within a territory have similar risk profiles
   - Validation: Within-territory coefficient of variation <1.2
   - Limitation: Some heterogeneity inevitable, balanced against credibility

2. **Geographic Stability:**
   - Assumption: Risk characteristics of ZIP codes remain stable over model period
   - Validation: Year-over-year territory performance tracked
   - Limitation: Major demographic shifts may occur (monitored annually)

3. **Sufficiency of Variables:**
   - Assumption: Clustering variables capture primary drivers of loss cost variation
   - Validation: Clustered territories show strong loss cost differentiation
   - Limitation: Some omitted factors (e.g., driver quality not geography-specific)

4. **Independence of Territories:**
   - Assumption: Loss experience in one territory independent of others
   - Justification: Large, geographically dispersed portfolio
   - Limitation: Regional economic shocks may affect multiple territories

5. **Stationarity:**
   - Assumption: Territory relativities stable over time
   - Validation: 6-year experience window smooths short-term volatility
   - Monitoring: Annual recalibration of relativities

6. **Linear Combination:**
   - Assumption: Territory effects multiplicative with other rating variables
   - Justification: Consistent with GLM rating structure
   - Validation: No significant interactions detected with other rating factors

### 4.4 Limitations

**Known Limitations:**

1. **ZIP Code Assignment Errors:**
   - 0.9% of policies have missing/invalid ZIP codes
   - Impact: Minimal (<1% of premium)
   - Mitigation: Default territory assignment rules established

2. **Small Territory Credibility:**
   - Some territories near minimum credibility threshold (2,000 policies)
   - Impact: Wider confidence intervals, potential volatility
   - Mitigation: Complement statistic calculated; monitoring plan

3. **State Boundary Effects:**
   - Adjacent ZIP codes in different states assigned to different territories despite similarity
   - Reason: State-level regulatory and legal environment differences
   - Trade-off: Regulatory compliance vs. pure geographic similarity

4. **Temporal Lag:**
   - Model based on 2017-2022 experience
   - Impact: Recent changes (2022 onward) not fully reflected
   - Mitigation: Annual monitoring and recalibration

5. **Urban Complexity:**
   - Large metropolitan areas have high within-city variation
   - Limitation: 15 territories may not fully capture micro-geographic risk
   - Future: Consider increasing territories in Phase 2 (pending credibility)

6. **Weather Volatility:**
   - Comprehensive coverage sensitive to weather events
   - Limitation: 6-year average may not represent long-term expectation
   - Mitigation: Catastrophe loadings applied separately

7. **Omitted Variables:**
   - Driver quality, vehicle mix vary by geography but not explicitly modeled
   - Reason: Captured in other rating variables (age, prior claims, vehicle type)
   - Impact: Territory model captures residual geographic effect

---

## 5. Model Development Process

### 5.1 Development Data

**Loss Experience Period:**
- Calendar Years: 2017-2022 (6 years)
- Rationale: Balance between recency and credibility
- COVID-19 Impact: 2020-2021 experience downweighted by 20% due to atypical driving patterns

**Data Aggregation:**
- Level: ZIP code × Coverage × Year
- Exposures: Earned policy-years
- Claims: Claim counts and total incurred costs
- Development: All claims developed to ultimate with 12-month lag

**Weighting:**
To account for COVID-19 impact and recency:
```
Weight_2017 = 1.0
Weight_2018 = 1.0
Weight_2019 = 1.0
Weight_2020 = 0.8 (COVID impact)
Weight_2021 = 0.8 (COVID impact)
Weight_2022 = 1.2 (most recent)
```

**Effective Experience Period:**
- Standard years: 4.0 (2017-2019, 2022 with weight)
- COVID years: 1.6 (2020-2021 downweighted)
- Total effective years: 5.6

### 5.2 Clustering Process

**Step 1: Feature Engineering**

Standardized all clustering variables (mean=0, std=1):
```python
X_scaled = (X - X.mean()) / X.std()
```

Included 14 features:
- Demographics: 4 variables
- Traffic: 4 variables
- Weather: 3 variables
- Economic: 2 variables
- Medical/Legal: 2 variables (weighted 1.5x due to importance)

**Step 2: Optimal Cluster Number Selection**

Tested K = 8, 10, 12, 15, 18, 20, 25 clusters

**Evaluation Metrics:**
- Within-cluster sum of squares (WCSS)
- Silhouette score
- Territory credibility (exposure per territory)
- Loss cost R² when GLM applied

**Results:**

| K  | WCSS    | Silhouette | Min Exposure | R² (Freq) | R² (Sev) |
|----|---------|------------|--------------|-----------|----------|
| 8  | 3,850   | 0.42       | 3,850        | 0.26      | 0.20     |
| 10 | 3,420   | 0.44       | 2,950        | 0.28      | 0.21     |
| 12 | 3,120   | 0.46       | 2,420        | 0.31      | 0.22     |
| 15 | 2,880   | 0.48       | 2,010        | 0.35      | 0.24     |
| 18 | 2,710   | 0.46       | 1,680        | 0.36      | 0.24     |
| 20 | 2,590   | 0.43       | 1,520        | 0.36      | 0.25     |
| 25 | 2,420   | 0.39       | 1,150        | 0.37      | 0.25     |

**Decision: K = 15 territories**

Rationale:
- Balances predictive power (R²) and credibility (minimum 2,010 policies/year)
- Silhouette score highest at K=15 (good cluster separation)
- Diminishing returns beyond K=15 (<1% R² improvement)
- Meets regulatory credibility standards
- 50% increase over existing 10-territory system (material improvement)

**Step 3: Geographic Contiguity Enforcement**

Applied constrained clustering algorithm:
- Started with unconstrained K-means result
- Identified non-contiguous territories (3 cases)
- Reassigned isolated ZIP codes to nearest contiguous territory
- Re-computed centroids
- Iterated until all territories geographically contiguous

**Step 4: State Boundary Adjustments**

For regulatory compliance:
- Split territories crossing state boundaries where legal environments differ significantly
- Result: 2 territories split into state-specific sub-territories
- Final territory count: 15

**Step 5: Manual Refinement**

Subject matter expert review:
- Verified territory assignments make geographic sense
- Checked for competitive implications
- Ensured no territories split major metropolitan areas awkwardly
- Minor adjustments: 12 ZIP codes reassigned (0.4% of total)

### 5.3 Relativity Estimation

**GLM Estimation by Coverage:**

Separate models fit for frequency and severity for each coverage:
- Bodily Injury (BI)
- Property Damage (PD)
- Collision (Coll)
- Comprehensive (Comp)

**Frequency Models:**

Poisson GLM with territory as single predictor:
```
log(frequency_t) = β_0 + β_t
exposure as offset
```

Estimated for each coverage separately.

**Severity Models:**

Gamma GLM with territory as single predictor:
```
log(severity_t) = α_0 + α_t
```

Estimated on closed claims only.

**Baseline Territory Selection:**

Territory 7 selected as baseline (relativity = 1.00):
- Median loss cost across all coverages
- Largest exposure (18.2% of total)
- Geographic diversity (urban and suburban mix)

**Credibility Weighting:**

For territories with 2,000-4,000 policies:
```
Credibility = min(1, exposure / 4,000)
Relativity_adjusted = Credibility × Relativity_full + (1 - Credibility) × 1.00
```

Applied to 3 smaller territories.

**Statistical Significance:**

All territory coefficients tested:
- Null hypothesis: β_t = 0 (no difference from baseline)
- Significance level: α = 0.05
- Result: 13 of 15 territories significantly different from baseline (p < 0.05)
- 2 territories not significant but retained for geographic completeness

**Combined Loss Cost Relativities:**

For pricing, combined frequency and severity:
```
Loss Cost Rel_t = Frequency Rel_t × Severity Rel_t
```

Weighted by coverage premium mix:
- BI: 35% of premium
- PD: 18% of premium
- Coll: 32% of premium
- Comp: 15% of premium

---

## 6. Model Performance & Validation

### 6.1 Territory Definitions

**Final 15-Territory System:**

| Territory | Description           | ZIP Codes | Exposure | Avg Loss Cost |
|-----------|-----------------------|-----------|----------|---------------|
| T1        | Rural North           | 285       | 95,400   | $625          |
| T2        | Small Town Midwest    | 342       | 118,200  | $695          |
| T3        | Suburban Low-Density  | 298       | 156,800  | $745          |
| T4        | Suburban Mid-Density  | 245       | 208,300  | $825          |
| T5        | Exurban Growth        | 188       | 142,600  | $765          |
| T6        | Small City Centers    | 156       | 124,900  | $915          |
| T7        | Mid-Size Metro (Base) | 224       | 312,400  | $880          |
| T8        | Suburban High-Density | 198       | 245,700  | $945          |
| T9        | Urban Mid-Density     | 142       | 198,500  | $1,050        |
| T10       | High-Traffic Corridor | 118       | 186,200  | $1,125        |
| T11       | Large Metro Suburban  | 185       | 268,900  | $1,085        |
| T12       | Large Metro Urban     | 156       | 224,600  | $1,245        |
| T13       | Dense Urban Core      | 94        | 142,800  | $1,450        |
| T14       | High-Litigation South | 225       | 185,600  | $1,285        |
| T15       | Weather-Prone Region  | 345       | 210,500  | $795          |

**Baseline:** Territory 7 (Mid-Size Metro), Relativity = 1.00, Avg Loss Cost = $880

### 6.2 Territory Relativities

**Combined Loss Cost Relativities (All Coverages):**

| Territory | Frequency Rel | Severity Rel | Loss Cost Rel | vs. Baseline |
|-----------|---------------|--------------|---------------|--------------|
| T1        | 0.68          | 0.98         | 0.67          | -33%         |
| T2        | 0.75          | 1.05         | 0.79          | -21%         |
| T3        | 0.82          | 0.98         | 0.80          | -20%         |
| T4        | 0.91          | 1.02         | 0.93          | -7%          |
| T5        | 0.84          | 1.03         | 0.87          | -13%         |
| T6        | 1.00          | 1.08         | 1.08          | +8%          |
| T7 (Base) | 1.00          | 1.00         | 1.00          | 0%           |
| T8        | 1.04          | 1.03         | 1.07          | +7%          |
| T9        | 1.15          | 1.05         | 1.21          | +21%         |
| T10       | 1.22          | 1.06         | 1.29          | +29%         |
| T11       | 1.18          | 1.05         | 1.24          | +24%         |
| T12       | 1.32          | 1.10         | 1.45          | +45%         |
| T13       | 1.48          | 1.15         | 1.70          | +70%         |
| T14       | 1.28          | 1.18         | 1.51          | +51%         |
| T15       | 0.86          | 1.02         | 0.88          | -12%         |

**Range of Relativities:**
- Lowest: T1 at 0.67 (Rural North, -33%)
- Highest: T13 at 1.70 (Dense Urban Core, +70%)
- Spread: 2.54x (highest/lowest)
- Old system spread: 2.08x (improvement in differentiation)

**Statistical Significance:**
- 13 of 15 territories significant at p < 0.05
- T6 and T8 not statistically different from baseline but retained for geographic coverage

### 6.3 Model Performance Metrics

**Predictive Accuracy:**

**Frequency Model:**
- R-squared: 0.35 (vs. 0.28 for old 10-territory system)
- Improvement: +25%
- Interpretation: Territory explains 35% of variation in claim frequency

**Severity Model:**
- R-squared: 0.24 (vs. 0.19 for old system)
- Improvement: +26%
- Interpretation: Territory explains 24% of variation in claim severity

**Combined Loss Cost:**
- R-squared: 0.38 (frequency + severity combined)
- Old system: 0.30
- Improvement: +27%

**Within-Territory Homogeneity:**

Coefficient of variation (C.V.) of loss ratios within territories:

| Metric               | Old System | New System | Improvement |
|----------------------|------------|------------|-------------|
| Average C.V.         | 1.42       | 1.08       | -24%        |
| Max C.V. (worst territory) | 2.15 | 1.65       | -23%        |
| % Territories with C.V. >1.5 | 40% | 13%        | -67%        |

**Loss Ratio Analysis:**

Simulated impact of new territories on 2022 experience:

| Territory | Old LR | New LR | Improvement | Premium Impact |
|-----------|--------|--------|-------------|----------------|
| T1        | 58%    | 61%    | +3 pts      | +5% rate       |
| T3        | 72%    | 68%    | -4 pts      | -6% rate       |
| T7        | 65%    | 65%    | 0 pts       | No change      |
| T9        | 68%    | 66%    | -2 pts      | -3% rate       |
| T12       | 78%    | 71%    | -7 pts      | -10% rate      |
| T13       | 82%    | 73%    | -9 pts      | -12% rate      |

**Overall:** Rate adjustments +/- 15% across territories, premium-neutral overall.

**Validation Tests:**

**1. Temporal Stability:**
- Estimated relativities using 2017-2019 data only
- Compared to 2020-2022 relativities
- Correlation: 0.94 (high stability)
- Largest shift: T13 relativity changed from 1.65 to 1.70 (+3%)

**2. Coverage Consistency:**
- Calculated relativities separately for BI, PD, Coll, Comp
- Correlation between coverages: 0.82-0.91
- Indicates territories capture fundamental geographic risk (not coverage-specific artifacts)

**3. Holdout Validation:**
- Withheld 2022 H2 data
- Estimated territories using 2017-2022 H1
- Applied to holdout period
- Predicted vs. actual loss costs: correlation 0.88

**4. Competitive Benchmark:**
- Compared ABC's territory relativities to Industry (where available)
- Correlation: 0.79
- ABC territories align with industry view of geographic risk

---

## 7. Implementation & Rate Filing

### 7.1 Rate Filing Strategy

**Filing Approach:**

- **Filing Type**: Territory definition change + rate rebalancing
- **Overall Rate Level**: Premium-neutral (no aggregate rate change)
- **Rate Impact**: Redistributive (+/- 15% by territory)
- **Justification**: Improved actuarial accuracy and fairness

**State-by-State Filings:**

Filed in all 15 states, Q4 2022:

| State Region | States | Filing Date | Approval Date | Implementation |
|--------------|--------|-------------|---------------|----------------|
| Midwest-1    | 4      | Oct 1, 2022 | Nov 15, 2022  | Jan 15, 2023   |
| Midwest-2    | 4      | Oct 1, 2022 | Nov 22, 2022  | Jan 15, 2023   |
| South-1      | 4      | Oct 8, 2022 | Dec 1, 2022   | Jan 15, 2023   |
| South-2      | 3      | Oct 8, 2022 | Dec 8, 2022   | Jan 15, 2023   |

**All states approved by December 8, 2022.**

**Regulatory Questions Addressed:**

Common regulator questions and responses:

1. **"Why increase from 10 to 15 territories?"**
   - Response: Improved predictive accuracy (R² +27%), reduced within-territory variation (-24% C.V.), aligns with competitive market practice

2. **"Are minimum credibility standards met?"**
   - Response: Yes, all territories exceed 2,000 policies per year; complement statistics provided

3. **"Does this comply with anti-discrimination laws?"**
   - Response: Yes, territory assignments based solely on objective geographic and loss experience data; no prohibited factors used

4. **"Why premium-neutral overall?"**
   - Response: Purpose is risk redistribution, not rate increase; aggregate rate level addressed separately

### 7.2 Implementation Timeline

**Phase 1: Pre-Implementation (October-December 2022)**
- Rate filing submissions (October 2022)
- System configuration and testing (November 2022)
- User training and documentation (December 2022)

**Phase 2: Production Deployment (January 15, 2023)**
- New business: Immediate application of new territories
- Renewals: Phased transition over 12 months
  - Jan-Mar 2023: 25% of renewals
  - Apr-Jun 2023: 25%
  - Jul-Sep 2023: 25%
  - Oct-Dec 2023: 25%
- Reason for phased renewal: Smooth customer impact, monitor performance

**Phase 3: Monitoring (Jan 2023-Jan 2024)**
- Weekly: First month post-launch
- Monthly: Feb-Jun 2023
- Quarterly: Jul 2023 onward

### 7.3 System Integration

**Policy Administration System (PolicyMaster 3.0):**
- ZIP code to territory mapping table updated
- Rating engine configured with 15-territory relativities
- Historical policy records remapped (for analytics, not billing)

**Quoting System:**
- Territory lookup API updated
- Quote interface displays territory assignment
- Territory-driven rate changes clearly disclosed

**Analytics and Reporting:**
- Territory performance dashboards created
- Loss ratio monitoring by territory
- Geographic heat maps for visualization

**Customer Communication:**
- Rate change notices include territory reassignment explanation (if applicable)
- Website updated with territory FAQ
- Agent training materials provided

### 7.4 Customer Impact Management

**Rate Increase Management:**

For customers experiencing >10% rate increase due to territory change:
- Personalized explanatory letter sent
- Emphasizes fairness and actuarial accuracy
- Highlights long-term rate stability
- Retention offer (discount) provided for loyal customers (5+ years tenure)

**Rate Decrease Communication:**

For customers receiving >10% rate decrease:
- Automatic application to renewal premium
- Proactive notification of savings
- Marketing opportunity: "Your loyalty rewarded"

**Expected Retention Impact:**
- Customers with rate increase >10%: 3-5% retention decline expected
- Customers with rate decrease >10%: 2-3% retention improvement expected
- Net retention impact: -0.5% (acceptable)

---

## 8. Ongoing Monitoring & Governance

### 8.1 Monitoring Metrics

**Monthly KPIs:**
- Actual vs. Expected Frequency by Territory
- Actual vs. Expected Severity by Territory
- Loss Ratio by Territory
- New Business Quote Volume by Territory
- Retention Rate by Territory
- Competitive Win Rate by Territory

**Quarterly Metrics:**
- Territory R² on rolling 12-month data
- Within-territory loss ratio C.V.
- Relativity stability (compare to expected)
- Large loss frequency by territory
- Credibility metrics (exposure by territory)

**Annual Review:**
- Comprehensive re-validation of territory definitions
- Assess need for territory re-mapping
- Update clustering variables with latest data
- Recalculate relativities on most recent 6 years
- Evaluate expansion to more territories (if credibility permits)

**Alert Thresholds:**

Automatic alerts if:
- Any territory A/E ratio >1.15 or <0.85 for 2 consecutive months
- Loss ratio for any territory >80% or <50% for 3 consecutive months
- Credibility drops below 1,500 policies/year for any territory
- R² drops below 0.30

### 8.2 Annual Recalibration Process

**Performed every October for upcoming year:**

1. **Update Loss Experience:**
   - Add most recent year of data
   - Drop oldest year (maintain 6-year rolling window)
   - Adjust COVID-19 weights as patterns normalize

2. **Re-estimate Relativities:**
   - Re-run GLM models for frequency and severity
   - Compare new relativities to current
   - Identify territories with >10% relativity change

3. **Test Territory Definitions:**
   - Run clustering algorithm on updated data
   - Compare to existing 15-territory system
   - Assess if re-mapping needed (typically every 5-7 years)

4. **Rate Filing:**
   - If relativities change >5%, file updated rates
   - If relativities stable (<5%), no filing required (use existing)

5. **Governance Approval:**
   - Present findings to Model Risk Governance Committee
   - Chief Actuary sign-off
   - Document annual review

### 8.3 Model Enhancement Roadmap

**Short-Term (2023-2024):**
- Integrate territory model with telematics risk scoring
- Develop territory-specific marketing strategies
- Enhance within-territory segmentation using micro-geographic data

**Medium-Term (2024-2026):**
- Explore expansion to 18-20 territories (pending credibility accumulation)
- Develop dynamic territory adjustment methodology (annual recalibration)
- Incorporate emerging risk factors (e.g., autonomous vehicle penetration)

**Long-Term (2026+):**
- Geospatial modeling with continuous risk surfaces
- Real-time territory risk scoring using IoT data
- Integration with usage-based insurance (UBI) programs

---

## Appendices

### Appendix A: Territory Maps

**Figure A1: Territory Geographic Distribution**

```
[Map visualization - 15 territories color-coded]

Legend:
T1-T5: Low to Medium Risk (Green to Yellow)
T6-T11: Medium to High Risk (Yellow to Orange)
T12-T15: High to Very High Risk (Orange to Red)

Key Metropolitan Areas:
- Metro A: Territories T7, T9, T11, T12, T13
- Metro B: Territories T6, T8
- Rural Regions: Territories T1, T2, T5, T15
```

**Figure A2: Territory Exposure Distribution**

```
Territory | Exposure Distribution
T1        | ████ 3.4%
T2        | ██████ 4.2%
T3        | ████████ 5.6%
T4        | ████████████ 7.4%
T5        | ███████ 5.1%
T6        | ██████ 4.4%
T7        | ████████████████ 11.1% (Baseline)
T8        | ███████████ 8.7%
T9        | ████████ 7.0%
T10       | ███████ 6.6%
T11       | ████████████ 9.5%
T12       | █████████ 8.0%
T13       | ██████ 5.1%
T14       | ███████ 6.6%
T15       | ████████ 7.5%
```

### Appendix B: Clustering Variable Importance

**Feature Importance in K-means Clustering:**

Measured by contribution to cluster separation (variance explained):

| Feature                  | Importance | Rank |
|--------------------------|------------|------|
| Traffic Congestion Index | 18.2%      | 1    |
| Population Density       | 15.6%      | 2    |
| Medical Cost Index       | 14.8%      | 3    |
| Attorney Rate            | 12.4%      | 4    |
| Median Income            | 9.2%       | 5    |
| Road Density             | 7.8%       | 6    |
| VMT per Capita           | 6.5%       | 7    |
| Urban %                  | 5.4%       | 8    |
| Severe Weather Events    | 4.2%       | 9    |
| Snow/Ice Days            | 3.1%       | 10   |
| (remaining 4 features)   | 2.8%       | 11-14|

**Insight:** Traffic congestion, population density, and medical costs are dominant clustering drivers.

### Appendix C: Sensitivity Analysis

**Scenario 1: Different Cluster Counts**

Tested K = 10, 12, 15, 18 territories:

| K  | R² (Freq) | R² (Sev) | Min Exposure | Recommendation |
|----|-----------|----------|--------------|----------------|
| 10 | 0.28      | 0.21     | 2,950        | Acceptable     |
| 12 | 0.31      | 0.22     | 2,420        | Good           |
| 15 | 0.35      | 0.24     | 2,010        | Selected       |
| 18 | 0.36      | 0.24     | 1,680        | Marginal gain  |

**Decision:** K=15 optimal balance of accuracy and credibility.

**Scenario 2: Experience Period Length**

Tested 3-year, 5-year, 6-year, 8-year windows:

| Years | Recency | Credibility | Relativity Stability | Recommendation |
|-------|---------|-------------|----------------------|----------------|
| 3     | High    | Low         | Volatile             | Too short      |
| 5     | Good    | Good        | Stable               | Acceptable     |
| 6     | Good    | High        | Very stable          | Selected       |
| 8     | Low     | High        | Stable but outdated  | Too long       |

**Decision:** 6 years balances recency and stability.

**Scenario 3: COVID-19 Weighting**

Tested different weights for 2020-2021:

| Weight | 2020-2021 Impact | Territory Relativity Change | Selection |
|--------|------------------|-----------------------------|-----------|
| 1.0    | Full inclusion   | +8% avg shift               | Too high  |
| 0.8    | 20% discount     | +2% avg shift               | Selected  |
| 0.5    | 50% discount     | -3% avg shift               | Too low   |
| 0.0    | Exclude          | -5% avg shift               | Too low   |

**Decision:** 0.8 weight (20% discount) provides appropriate balance.

---

## Document Control

**Version:** 1.0
**Date:** December 15, 2022
**Last Updated:** December 15, 2022

**Prepared by:**
Emily Rodriguez, FCAS, MAAA
Director, Geographic Analytics
ABC Insurance Company

**Reviewed by:**
Robert Johnson, FCAS, MAAA
Chief Actuary
ABC Insurance Company

**Approved by:**
Sarah Williams
Model Risk Officer
ABC Insurance Company

**Approved by:**
Thomas Martinez
VP, State Regulatory Affairs
ABC Insurance Company

**Distribution:**
- Model Risk Governance Committee
- Pricing Committee
- State Insurance Departments (all 15 states)
- Internal Audit Department
- Corporate Actuarial Library

**Next Review Date:** October 1, 2023 (Annual Recalibration)

**Model ID:** PAUTO-TERR-CLUSTER-2023.1
**Documentation Reference:** DOC-2023-TERR-001

---

**End of Document**
