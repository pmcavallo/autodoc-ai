---
title: "2023 Commercial Auto Fleet Frequency Model Documentation"
model_id: "CA-FREQ-2023-001"
portfolio: "commercial_auto"
type: "model_documentation"
company: "ABC Insurance Company"
version: "1.0"
model_owner: "Jennifer Martinez, FCAS"
effective_date: "2023-07-01"
status: "active"
---

# 2023 Commercial Auto Fleet Frequency Model

**SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes. No real insurance data, customer information, proprietary methodologies, or confidential information from any insurance company or financial institution is used or simulated.

All names, addresses, policy numbers, claim amounts, and company information are fictional. Any resemblance to actual persons, organizations, or data is purely coincidental.

This project showcases AI agent capabilities for automated documentation generation and is not intended for production use with real data or models.

---

## Executive Summary

### Model Purpose

The 2023 Commercial Auto Fleet Frequency Model predicts the expected number of liability claims per vehicle-year for commercial auto fleets. This model supports loss cost development, fleet underwriting, experience rating validation, and risk segmentation across ABC Insurance Company's commercial auto portfolio.

### Key Findings

- Fleet size tier is a significant predictor with large fleets showing 30% lower frequency than micro fleets
- Vehicle class (GVW-based) creates substantial frequency differentiation
- Industry NAICS code and radius of operation are strong predictors
- Driver turnover rate emerges as a key fleet-level risk indicator
- Model achieves AUC of 0.68 on holdout validation data

### Business Impact

- Supports ISO class code loss cost validation
- Enables fleet-level risk differentiation beyond class rating
- Improves small fleet underwriting accuracy
- Informs fleet safety program recommendations
- Expected annual premium impact: $8.5M improvement in rate adequacy

---

## 1. Business Context & Objectives

### 1.1 Background

ABC Insurance Company writes approximately $420M in annual commercial auto premium across 12,500 fleet accounts. The commercial auto portfolio has experienced frequency volatility driven by:

**Recent Frequency Trends:**
- 2019: 12.8 claims per 100 vehicle-years
- 2020: 9.2 claims per 100 vehicle-years (COVID impact)
- 2021: 11.5 claims per 100 vehicle-years (recovery)
- 2022: 13.4 claims per 100 vehicle-years (elevated post-COVID)
- 2023 YTD: 12.9 claims per 100 vehicle-years (stabilizing)

**Business Challenges:**
- Fleet heterogeneity creates significant within-class variation
- Driver turnover in trucking and delivery segments affects loss experience
- ISO class codes alone insufficient for modern fleet risk segmentation
- Growing last-mile delivery segment with unique risk characteristics

### 1.2 Business Problem

The primary challenges addressed by this model include:

1. **Inadequate Fleet Segmentation**: ISO class codes capture vehicle type and use but not fleet-level characteristics (size, driver quality, management practices)

2. **Industry Mix Variation**: Same vehicle types used across vastly different industries with different risk profiles

3. **Driver Quality Assessment**: Fleet-level driver metrics not systematically incorporated into rating

4. **Overdispersion in Claim Counts**: Fleet claim counts exhibit overdispersion relative to Poisson, requiring Negative Binomial modeling

### 1.3 Objectives

**Primary Objectives:**
- Achieve AUC >= 0.65 on holdout validation data
- Capture fleet size effect with appropriate credibility weighting
- Incorporate driver quality metrics at fleet level
- Address overdispersion in claim count distribution

**Secondary Objectives:**
- Validate ISO class code relativities
- Support experience rating plan calibration
- Enable targeted safety program recommendations
- Provide transparency for underwriting decisions

---

## 2. Regulatory Compliance Statement

### 2.1 NAIC Model Audit Rule (MAR)

This model documentation complies with NAIC Model Audit Rule requirements including:
- Comprehensive documentation of data, methodology, assumptions, and limitations
- Independent validation by qualified professionals
- Ongoing monitoring procedures
- Model risk management framework integration

### 2.2 Actuarial Standards of Practice (ASOPs)

**ASOP No. 12 - Risk Classification:**
- Fleet size, vehicle class, radius, and industry selected based on actuarial relevance
- All variables demonstrate statistically significant relationships with claim frequency
- Variables comply with state insurance regulations

**ASOP No. 23 - Data Quality:**
- Fleet data quality assessment performed including vehicle count validation
- Driver roster accuracy documented with known limitations
- Data quality issues disclosed and assessed for materiality

**ASOP No. 56 - Modeling:**
- Model purpose and design clearly stated
- Negative Binomial distribution selection justified
- Validation testing documented
- Monitoring plan established

### 2.3 State Requirements

The model complies with commercial auto rating requirements in all 35 states where ABC Insurance operates commercial auto lines. ISO class code relativities remain the foundation with model factors as supplemental rating variables.

### 2.4 Internal Governance

**Model Approvals:**
- Model Risk Governance Committee: June 12, 2023
- Chief Actuary: June 15, 2023
- Commercial Lines Underwriting: June 18, 2023
- Pricing Committee: June 22, 2023

---

## 3. Data Sources

### 3.1 Internal Data Sources

**FleetMaster - Fleet Management System**

| Field Category | Description | Records | Date Range |
|----------------|-------------|---------|------------|
| Fleet Profile | Account-level fleet characteristics | 12,500 accounts | 2018-2022 |
| Vehicle Schedule | Individual vehicle records | 185,000 vehicles | 2018-2022 |
| Driver Roster | Listed drivers with hire dates | 142,000 drivers | 2018-2022 |

**Key Data Elements:**
- Fleet identifiers: Account number, policy number, fleet size tier
- Vehicle details: VIN, year, make, model, GVW, ISO class code
- Fleet characteristics: Industry NAICS, years in business, radius of operation
- Driver metrics: Count, turnover rate, average experience

**Data Quality:**
- Vehicle count accuracy: 95% (validated against symbol schedule)
- Driver roster completeness: 85% (turnover creates lag)
- VIN decode rate: 98%

---

**DriverQualify - MVR Integration System**

| Data Type | Description | Refresh | Coverage |
|-----------|-------------|---------|----------|
| MVR Data | Motor vehicle records | Annual/Continuous | 92% of drivers |
| Violations | Moving violations, points | 3-year lookback | 88% |
| Accidents | At-fault accident history | 3-year lookback | 90% |

**Key Data Elements:**
- License status: Valid, suspended, revoked
- Violation count: Major and minor violations
- Accident history: At-fault accidents
- CDL status: Class A, B, C, or non-CDL

**Fleet Driver Quality Score:**
```python
fleet_driver_score = weighted_average(
    individual_driver_scores,
    weights=vehicle_assignments
)
# Score range: 0-100 (higher = better quality)
# Fleet average: 72
```

---

**ClaimsVision CA - Commercial Auto Claims**

| Claim Type | Description | Records | Date Range |
|------------|-------------|---------|------------|
| Liability BI | Bodily injury claims | 18,400 | 2018-2022 |
| Liability PD | Property damage claims | 32,600 | 2018-2022 |
| Total Liability | Combined liability | 51,000 | 2018-2022 |

**Key Data Elements:**
- Claim identifiers: Claim number, policy number, vehicle
- Accident details: Date, location, fault determination
- Driver assignment: Driver ID (92% assignment rate)
- Financials: Incurred loss, paid, reserve

---

### 3.2 External Data Sources

**ISO Commercial Auto Data**

| Data Type | Description | Usage |
|-----------|-------------|-------|
| Class Codes | ISO vehicle classification | Rating basis |
| Loss Costs | Published loss costs by state/class | Benchmark |
| Territory | Geographic risk factors | Validation |

**D&B Business Data**

| Data Type | Description | Usage |
|-----------|-------------|-------|
| NAICS Code | Industry classification | Risk segmentation |
| Years in Business | Business tenure | Stability indicator |
| Employee Count | Company size proxy | Validation |

---

### 3.3 Data Quality Assessment

**Fleet Size Validation:**
```
Comparison: Reported fleet size vs. vehicle schedule count
- Match rate: 95%
- Understated (>10% difference): 3%
- Overstated (>10% difference): 2%
Action: Use vehicle schedule count as primary measure
```

**Driver Turnover Calculation:**
```python
driver_turnover_rate = (
    drivers_terminated_in_year / average_driver_count
) * 100

# Fleet distribution:
# < 20% turnover: 35% of fleets
# 20-50% turnover: 40% of fleets
# 50-100% turnover: 18% of fleets
# > 100% turnover: 7% of fleets (high-turnover trucking)
```

---

## 4. Feature Engineering

### 4.1 Fleet Size Tiers

**Tier Definitions:**

| Tier | Vehicles | % of Accounts | % of Exposure | Characteristics |
|------|----------|---------------|---------------|-----------------|
| Micro | 1-5 | 52% | 12% | Owner-operators, small contractors |
| Small | 6-15 | 28% | 22% | Local service, small delivery |
| Medium | 16-50 | 12% | 28% | Regional fleets, mid-size trucking |
| Large | 51-200 | 6% | 24% | Large regional carriers |
| Jumbo | 200+ | 2% | 14% | National carriers, major fleets |

**Rationale for Tiers:**
- Actuarial credibility considerations
- Natural breakpoints in fleet management practices
- Alignment with experience rating thresholds
- ISO commercial auto segmentation

---

### 4.2 Vehicle Classification

**ISO-Based Vehicle Classes:**

| Class | GVW (lbs) | Description | % of Vehicles |
|-------|-----------|-------------|---------------|
| Light Truck | <10,000 | Pickup, van, SUV | 45% |
| Medium Truck | 10,001-26,000 | Box truck, delivery van | 28% |
| Heavy Truck | >26,000 | Straight truck, tractor | 18% |
| Service Vehicle | Varies | Specialized service equipment | 9% |

**VIN Decoding Integration:**
```python
def classify_vehicle(vin):
    decoded = vin_decoder.decode(vin)
    gvw = decoded.get('gvw_rating', 0)

    if gvw <= 10000:
        return 'light_truck'
    elif gvw <= 26000:
        return 'medium_truck'
    elif gvw > 26000:
        return 'heavy_truck'
    else:
        return 'service_vehicle'
```

---

### 4.3 Radius of Operation

**Radius Categories:**

| Radius | Definition | % of Fleets | Characteristics |
|--------|------------|-------------|-----------------|
| Local | <50 miles from base | 55% | Service, local delivery |
| Intermediate | 50-200 miles | 28% | Regional delivery, contractors |
| Long-Haul | >200 miles | 17% | Interstate trucking, national delivery |

**Validation:**
- Self-reported radius validated against telematics where available (15% of fleets)
- Telematics validation shows 12% of "local" fleets operate in intermediate radius

---

### 4.4 Industry Classification

**NAICS-Based Industry Groups:**

| Industry Group | NAICS Codes | % of Fleets | Risk Profile |
|----------------|-------------|-------------|--------------|
| Construction | 23xxxx | 22% | Medium-high frequency |
| Retail Delivery | 44-45xxxx | 18% | High frequency, urban |
| Service/Repair | 811xxx | 25% | Medium frequency |
| For-Hire Trucking | 484xxx | 15% | Variable by operation |
| Wholesale | 42xxxx | 12% | Medium frequency |
| Other | Various | 8% | Mixed |

---

### 4.5 Driver Quality Score

**Fleet-Level Driver Quality Score:**

```python
def calculate_fleet_driver_score(fleet):
    """
    Calculate fleet-level driver quality score (0-100).
    Higher score = better quality drivers.
    """
    driver_scores = []

    for driver in fleet.drivers:
        score = 100

        # Violation deductions
        score -= driver.major_violations * 15
        score -= driver.minor_violations * 5

        # Accident deductions
        score -= driver.at_fault_accidents * 20

        # Experience bonus
        if driver.years_licensed > 10:
            score += 5

        # CDL bonus
        if driver.has_cdl:
            score += 5

        driver_scores.append(max(0, min(100, score)))

    # Fleet average
    return np.mean(driver_scores)
```

**Driver Quality Score Distribution:**

| Score Range | % of Fleets | Description |
|-------------|-------------|-------------|
| 85-100 | 15% | Excellent driver quality |
| 70-84 | 45% | Good driver quality |
| 55-69 | 30% | Average driver quality |
| <55 | 10% | Below average driver quality |

---

## 5. Methodology

### 5.1 Model Selection

**Approach:** Generalized Linear Model (GLM)
**Distribution:** Negative Binomial
**Link Function:** Log
**Offset:** Log(vehicle-years)

**Rationale for Negative Binomial:**

Commercial auto claim counts exhibit overdispersion (variance > mean) due to:
- Fleet-level heterogeneity not captured by covariates
- Correlation of claims within fleets
- Heavy-tailed claim frequency for some fleets

**Overdispersion Analysis:**
```
Poisson assumption: Variance = Mean
Actual data: Variance = 1.4 × Mean
Overdispersion parameter (α): 1.42
Result: Negative Binomial provides superior fit
```

### 5.2 Model Specification

```
log(E[claims]) = β₀ + β₁(fleet_size_tier) + β₂(vehicle_class)
                 + β₃(radius) + β₄(industry) + β₅(driver_quality_score)
                 + β₆(driver_turnover) + β₇(years_in_business)
                 + log(vehicle_years)
```

**Variable Definitions:**

| Variable | Type | Levels/Range | Selection Rationale |
|----------|------|--------------|---------------------|
| Fleet Size Tier | Categorical | 5 levels | Safety resources, selection |
| Vehicle Class | Categorical | 4 levels | ISO classification, exposure |
| Radius | Categorical | 3 levels | Miles driven, exposure |
| Industry | Categorical | 6 levels | Industry risk differences |
| Driver Quality Score | Continuous | 0-100 | Driver risk indicator |
| Driver Turnover | Continuous | 0-200% | Fleet stability |
| Years in Business | Continuous | 0-50+ | Experience, stability |

### 5.3 Assumptions

**Key Model Assumptions:**

1. **Negative Binomial Distribution**: Claim counts follow NB distribution with constant overdispersion
   - Validation: Pearson dispersion test confirms overdispersion ~1.4
   - Alternative: Poisson tested but rejected (likelihood ratio test p<0.001)

2. **Conditional Independence**: Claims independent given covariates
   - Limitation: Some within-fleet correlation remains
   - Mitigation: Fleet-level random effects tested (marginal improvement)

3. **Log-Linear Relationship**: Log expected claims linear in predictors
   - Validation: Partial residual plots reviewed
   - Adjustment: Continuous variables capped/transformed as needed

4. **Proportional Exposure**: Claim frequency proportional to vehicle-years
   - Validation: Exposure coefficient close to 1 when not constrained
   - Implementation: Use as offset (coefficient = 1)

### 5.4 Limitations

**Known Limitations:**

1. **Driver Roster Lag**: 15% of drivers may not be reflected in current roster due to turnover

2. **Radius Self-Reporting**: Radius based on insured representation; telematics validation limited

3. **Small Fleet Credibility**: Micro fleets (1-5 vehicles) have limited individual experience

4. **COVID Impact**: 2020 data affected by pandemic; model includes accident year adjustment

5. **Telematics Gap**: Only 15% of fleets have telematics data; cannot incorporate driving behavior

6. **Vehicle Age**: Vehicle age not included (weak univariate signal in commercial auto)

---

## 6. Model Results

### 6.1 Coefficient Summary

**Fleet Size Tier:**

| Level | Coefficient | Std Error | P-value | Relativity | Expected Freq |
|-------|-------------|-----------|---------|------------|---------------|
| Micro (1-5) | 0.000 | - | - | 1.00 | 14.2 |
| Small (6-15) | -0.095 | 0.032 | 0.003 | 0.91 | 12.9 |
| Medium (16-50) | -0.182 | 0.038 | <0.001 | 0.83 | 11.8 |
| Large (51-200) | -0.274 | 0.045 | <0.001 | 0.76 | 10.8 |
| Jumbo (200+) | -0.357 | 0.058 | <0.001 | 0.70 | 9.9 |

**Vehicle Class:**

| Level | Coefficient | Std Error | P-value | Relativity | Expected Freq |
|-------|-------------|-----------|---------|------------|---------------|
| Light Truck (<10K) | 0.000 | - | - | 1.00 | 11.2 |
| Medium Truck (10-26K) | 0.182 | 0.028 | <0.001 | 1.20 | 13.4 |
| Heavy Truck (>26K) | 0.336 | 0.035 | <0.001 | 1.40 | 15.7 |
| Service Vehicle | 0.077 | 0.042 | 0.067 | 1.08 | 12.1 |

**Radius of Operation:**

| Level | Coefficient | Std Error | P-value | Relativity | Expected Freq |
|-------|-------------|-----------|---------|------------|---------------|
| Local (<50 mi) | 0.000 | - | - | 1.00 | 11.5 |
| Intermediate (50-200 mi) | 0.154 | 0.025 | <0.001 | 1.17 | 13.5 |
| Long-Haul (>200 mi) | 0.262 | 0.032 | <0.001 | 1.30 | 14.9 |

**Industry:**

| Level | Coefficient | Std Error | P-value | Relativity | Expected Freq |
|-------|-------------|-----------|---------|------------|---------------|
| Service/Repair | 0.000 | - | - | 1.00 | 11.8 |
| Construction | 0.095 | 0.028 | <0.001 | 1.10 | 13.0 |
| Retail Delivery | 0.182 | 0.032 | <0.001 | 1.20 | 14.2 |
| For-Hire Trucking | 0.140 | 0.035 | <0.001 | 1.15 | 13.6 |
| Wholesale | -0.051 | 0.038 | 0.180 | 0.95 | 11.2 |
| Other | 0.030 | 0.045 | 0.505 | 1.03 | 12.2 |

**Continuous Variables:**

| Variable | Coefficient | Std Error | P-value | Effect |
|----------|-------------|-----------|---------|--------|
| Driver Quality Score | -0.008 | 0.001 | <0.001 | -0.8% per point |
| Driver Turnover Rate | 0.003 | 0.001 | <0.001 | +0.3% per 1% turnover |
| Years in Business | -0.012 | 0.003 | <0.001 | -1.2% per year |

### 6.2 Model Fit Statistics

| Metric | Value |
|--------|-------|
| Log-Likelihood | -42,850 |
| AIC | 85,780 |
| BIC | 86,120 |
| Deviance | 38,420 |
| Pearson Chi-Square | 39,100 |
| Degrees of Freedom | 38,200 |
| Overdispersion (α) | 1.42 |

### 6.3 Variable Importance

**Permutation Importance (AUC Drop):**

| Variable | AUC Drop | Importance Rank |
|----------|----------|-----------------|
| Vehicle Class | 0.045 | 1 |
| Radius | 0.038 | 2 |
| Industry | 0.032 | 3 |
| Fleet Size Tier | 0.028 | 4 |
| Driver Quality Score | 0.025 | 5 |
| Driver Turnover | 0.018 | 6 |
| Years in Business | 0.012 | 7 |

---

## 7. Model Validation

### 7.1 Data Split

**Temporal Split:**
- Training: 2018-2021 (75% of exposure)
- Holdout: 2022 (25% of exposure)

**Training Set:**
- Fleet-years: 42,500
- Vehicle-years: 148,000
- Claims: 38,400
- Frequency: 12.6 per 100 vehicle-years

**Holdout Set:**
- Fleet-years: 12,500
- Vehicle-years: 52,000
- Claims: 12,600
- Frequency: 12.1 per 100 vehicle-years (post-COVID normalization)

### 7.2 Discrimination Performance

| Metric | Training | Holdout | Degradation |
|--------|----------|---------|-------------|
| AUC | 0.71 | 0.68 | -0.03 |
| Gini | 0.42 | 0.36 | -0.06 |
| KS Statistic | 0.35 | 0.31 | -0.04 |

**Assessment:** Acceptable discrimination with minimal overfitting.

### 7.3 Calibration - Actual vs Expected

**By Fleet Size Tier:**

| Tier | Expected | Actual | A/E Ratio | Vehicle-Years |
|------|----------|--------|-----------|---------------|
| Micro (1-5) | 1,820 | 1,890 | 1.04 | 12,800 |
| Small (6-15) | 2,680 | 2,620 | 0.98 | 22,400 |
| Medium (16-50) | 3,420 | 3,380 | 0.99 | 28,600 |
| Large (51-200) | 3,150 | 3,080 | 0.98 | 24,200 |
| Jumbo (200+) | 1,530 | 1,630 | 1.07 | 14,000 |

**By Vehicle Class:**

| Class | Expected | Actual | A/E Ratio | Vehicle-Years |
|-------|----------|--------|-----------|---------------|
| Light Truck | 5,280 | 5,180 | 0.98 | 46,800 |
| Medium Truck | 3,920 | 4,020 | 1.03 | 29,100 |
| Heavy Truck | 2,680 | 2,620 | 0.98 | 18,700 |
| Service Vehicle | 720 | 780 | 1.08 | 7,400 |

**By Radius:**

| Radius | Expected | Actual | A/E Ratio | Vehicle-Years |
|--------|----------|--------|-----------|---------------|
| Local | 6,420 | 6,280 | 0.98 | 57,200 |
| Intermediate | 3,880 | 3,980 | 1.03 | 29,100 |
| Long-Haul | 2,300 | 2,340 | 1.02 | 15,700 |

**By Industry:**

| Industry | Expected | Actual | A/E Ratio | Vehicle-Years |
|----------|----------|--------|-----------|---------------|
| Construction | 2,820 | 2,920 | 1.04 | 22,900 |
| Retail Delivery | 2,680 | 2,580 | 0.96 | 18,700 |
| Service/Repair | 3,080 | 3,020 | 0.98 | 26,000 |
| For-Hire Trucking | 2,180 | 2,280 | 1.05 | 15,600 |
| Wholesale | 1,320 | 1,280 | 0.97 | 12,500 |
| Other | 520 | 520 | 1.00 | 6,300 |

### 7.4 Lift Analysis

| Decile | Expected Freq | Actual Freq | Lift vs Random |
|--------|---------------|-------------|----------------|
| 1 (lowest risk) | 7.2 | 7.4 | 0.58x |
| 2 | 8.8 | 8.5 | 0.67x |
| 3 | 9.8 | 10.1 | 0.79x |
| 4 | 10.8 | 10.6 | 0.83x |
| 5 | 11.6 | 11.8 | 0.93x |
| 6 | 12.4 | 12.2 | 0.96x |
| 7 | 13.4 | 13.6 | 1.07x |
| 8 | 14.6 | 14.4 | 1.13x |
| 9 | 16.2 | 16.8 | 1.32x |
| 10 (highest risk) | 19.8 | 20.2 | 1.59x |

**Top Decile Lift: 1.59x** vs. random assignment demonstrates meaningful discrimination.

---

## 8. Implementation

### 8.1 Production Scoring

**Fleet Frequency Factor Calculation:**

```python
def calculate_fleet_frequency_factor(fleet):
    """
    Calculate expected frequency factor for a commercial auto fleet.
    Returns claims per vehicle-year.
    """
    base_frequency = 0.126  # 12.6 claims per 100 vehicle-years
    factor = 1.0

    # Fleet size factor
    size_factors = {
        'micro': 1.00,
        'small': 0.91,
        'medium': 0.83,
        'large': 0.76,
        'jumbo': 0.70
    }
    factor *= size_factors.get(fleet.size_tier, 1.0)

    # Vehicle class factor (fleet average)
    vehicle_factors = {
        'light_truck': 1.00,
        'medium_truck': 1.20,
        'heavy_truck': 1.40,
        'service_vehicle': 1.08
    }
    fleet_vehicle_factor = weighted_average(
        [vehicle_factors[v.class_code] for v in fleet.vehicles],
        weights=[1 for v in fleet.vehicles]
    )
    factor *= fleet_vehicle_factor

    # Radius factor
    radius_factors = {
        'local': 1.00,
        'intermediate': 1.17,
        'long_haul': 1.30
    }
    factor *= radius_factors.get(fleet.radius, 1.0)

    # Industry factor
    industry_factors = {
        'construction': 1.10,
        'retail_delivery': 1.20,
        'service_repair': 1.00,
        'for_hire_trucking': 1.15,
        'wholesale': 0.95,
        'other': 1.03
    }
    factor *= industry_factors.get(fleet.industry, 1.0)

    # Driver quality factor (continuous)
    driver_quality_factor = math.exp(-0.008 * (fleet.driver_quality_score - 72))
    factor *= driver_quality_factor

    # Driver turnover factor (continuous)
    turnover_factor = math.exp(0.003 * (fleet.driver_turnover_rate - 40))
    factor *= turnover_factor

    # Years in business factor (continuous)
    years_factor = math.exp(-0.012 * min(fleet.years_in_business, 25))
    factor *= years_factor

    return base_frequency * factor
```

### 8.2 Rating Integration

**Loss Cost Calculation:**
```python
def calculate_fleet_loss_cost(fleet):
    """
    Calculate expected loss cost per vehicle-year.
    Combines frequency and severity models.
    """
    # Get frequency factor
    frequency = calculate_fleet_frequency_factor(fleet)

    # Get severity factor (from separate severity model)
    severity = calculate_fleet_severity_factor(fleet)

    # Loss cost = frequency × severity
    loss_cost = frequency * severity

    # Apply trend factor
    loss_cost *= get_loss_cost_trend_factor(fleet.effective_date)

    return loss_cost
```

### 8.3 System Integration

**Data Flow:**
1. Fleet data extracted from FleetMaster nightly
2. Driver quality scores calculated from DriverQualify MVR data
3. Frequency factors calculated for all active fleets
4. Factors stored in rating engine database
5. New business/renewal quotes retrieve current factors
6. Monthly batch recalculation for fleet changes

**API Endpoint:**
```
POST /api/v1/commercial-auto/frequency-factor
Input: fleet_id, vehicles[], drivers[], industry, radius
Output: frequency_factor, confidence_interval, risk_tier
```

---

## 9. Monitoring Plan

### 9.1 Key Performance Indicators

**Monthly Monitoring:**

| Metric | Target | Yellow Alert | Red Alert |
|--------|--------|--------------|-----------|
| A/E Ratio (Overall) | 0.95-1.05 | 0.90-0.95 or 1.05-1.10 | <0.90 or >1.10 |
| Large Fleet A/E | 0.95-1.05 | 0.90-1.10 | <0.90 or >1.10 |
| New Business A/E | 0.90-1.10 | 0.85-1.15 | <0.85 or >1.15 |
| Claim Count | +/-10% of expected | +/-15% | +/-20% |

**Quarterly Monitoring:**

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| AUC (rolling 12mo) | >0.65 | <0.62 |
| Gini (rolling 12mo) | >0.30 | <0.25 |
| Top Decile Lift | >1.4x | <1.2x |
| Coefficient Stability | Within 20% | >25% change |

### 9.2 Monitoring Dashboard

**Weekly Alerts:**
- Fleets with >3 claims in 30 days
- New large losses (>$100K)
- Fleet size changes >20%
- Driver quality score drops >10 points

**Monthly Reports:**
- A/E by fleet size, vehicle class, radius, industry
- Frequency trend emergence
- New vs. renewal business comparison
- Segment-level performance

### 9.3 Model Refresh Schedule

| Activity | Frequency | Responsibility |
|----------|-----------|----------------|
| KPI Review | Monthly | Actuarial Analyst |
| Full Validation | Quarterly | Senior Actuary |
| Coefficient Update | Annual | Model Owner |
| Major Revision | 3-5 years | Model Risk Committee |

### 9.4 Escalation Procedures

**Level 1 - Elevated Monitoring:**
- Trigger: A/E 1.05-1.10 for 2 consecutive months
- Action: Enhanced monitoring, segment deep-dive
- Owner: Actuarial Analyst

**Level 2 - Model Review:**
- Trigger: A/E >1.10 or AUC <0.65
- Action: Full model review, recalibration assessment
- Owner: Model Owner / Senior Actuary

**Level 3 - Model Override:**
- Trigger: A/E >1.15 or systematic bias identified
- Action: Temporary adjustments, expedited revision
- Owner: Chief Actuary / Model Risk Committee

---

## Appendices

### Appendix A: Full Coefficient Table

**Model Specification:**
```
log(E[claims]) = β₀ + Σ βᵢ × Xᵢ + log(vehicle_years)

Distribution: Negative Binomial
Link: Log
Overdispersion (α): 1.42
```

**Complete Coefficient Estimates:**

| Variable | Level | Coefficient | Std Error | P-value | Relativity |
|----------|-------|-------------|-----------|---------|------------|
| Intercept | - | -4.15 | 0.12 | <0.001 | - |
| Fleet Size | Micro (base) | 0.000 | - | - | 1.00 |
| Fleet Size | Small | -0.095 | 0.032 | 0.003 | 0.91 |
| Fleet Size | Medium | -0.182 | 0.038 | <0.001 | 0.83 |
| Fleet Size | Large | -0.274 | 0.045 | <0.001 | 0.76 |
| Fleet Size | Jumbo | -0.357 | 0.058 | <0.001 | 0.70 |
| Vehicle Class | Light (base) | 0.000 | - | - | 1.00 |
| Vehicle Class | Medium | 0.182 | 0.028 | <0.001 | 1.20 |
| Vehicle Class | Heavy | 0.336 | 0.035 | <0.001 | 1.40 |
| Vehicle Class | Service | 0.077 | 0.042 | 0.067 | 1.08 |
| Radius | Local (base) | 0.000 | - | - | 1.00 |
| Radius | Intermediate | 0.154 | 0.025 | <0.001 | 1.17 |
| Radius | Long-Haul | 0.262 | 0.032 | <0.001 | 1.30 |
| Industry | Service/Repair (base) | 0.000 | - | - | 1.00 |
| Industry | Construction | 0.095 | 0.028 | <0.001 | 1.10 |
| Industry | Retail Delivery | 0.182 | 0.032 | <0.001 | 1.20 |
| Industry | For-Hire Trucking | 0.140 | 0.035 | <0.001 | 1.15 |
| Industry | Wholesale | -0.051 | 0.038 | 0.180 | 0.95 |
| Industry | Other | 0.030 | 0.045 | 0.505 | 1.03 |
| Driver Quality | Per point | -0.008 | 0.001 | <0.001 | 0.992 |
| Driver Turnover | Per 1% | 0.003 | 0.001 | <0.001 | 1.003 |
| Years in Business | Per year | -0.012 | 0.003 | <0.001 | 0.988 |

### Appendix B: Data Dictionary

| Field | Description | Source | Format |
|-------|-------------|--------|--------|
| fleet_id | Unique fleet identifier | FleetMaster | VARCHAR(20) |
| policy_number | Policy identifier | FleetMaster | VARCHAR(15) |
| vehicle_count | Count of scheduled vehicles | FleetMaster | INTEGER |
| fleet_size_tier | Size tier (Micro/Small/Medium/Large/Jumbo) | Calculated | VARCHAR(10) |
| industry_naics | 6-digit NAICS code | FleetMaster | VARCHAR(6) |
| industry_group | Grouped industry | Calculated | VARCHAR(20) |
| radius_code | Radius of operation | FleetMaster | VARCHAR(15) |
| driver_count | Count of listed drivers | DriverQualify | INTEGER |
| driver_quality_score | Fleet average driver score | Calculated | DECIMAL(5,2) |
| driver_turnover_rate | Annual driver turnover % | Calculated | DECIMAL(5,2) |
| years_in_business | Years since founding | D&B | INTEGER |
| vehicle_years | Exposure in vehicle-years | Calculated | DECIMAL(10,4) |
| claim_count | Liability claim count | ClaimsVision | INTEGER |

### Appendix C: SQL Data Extraction

```sql
-- Commercial Auto Fleet Frequency Model Training Data
SELECT
    f.fleet_id,
    f.policy_number,
    f.vehicle_count,
    CASE
        WHEN f.vehicle_count BETWEEN 1 AND 5 THEN 'Micro'
        WHEN f.vehicle_count BETWEEN 6 AND 15 THEN 'Small'
        WHEN f.vehicle_count BETWEEN 16 AND 50 THEN 'Medium'
        WHEN f.vehicle_count BETWEEN 51 AND 200 THEN 'Large'
        ELSE 'Jumbo'
    END as fleet_size_tier,
    f.naics_code,
    ig.industry_group,
    f.radius_code,
    d.driver_count,
    d.avg_driver_score as driver_quality_score,
    d.turnover_rate as driver_turnover_rate,
    f.years_in_business,
    SUM(v.exposure_days) / 365.25 as vehicle_years,
    COUNT(DISTINCT c.claim_id) as claim_count
FROM fleets f
INNER JOIN industry_groups ig ON LEFT(f.naics_code, 2) = ig.naics_prefix
LEFT JOIN (
    SELECT fleet_id,
           COUNT(*) as driver_count,
           AVG(driver_score) as avg_driver_score,
           AVG(turnover_rate) as turnover_rate
    FROM fleet_drivers
    GROUP BY fleet_id
) d ON f.fleet_id = d.fleet_id
INNER JOIN vehicles v ON f.fleet_id = v.fleet_id
LEFT JOIN claims c ON v.vehicle_id = c.vehicle_id
    AND c.coverage_type IN ('LIABILITY_BI', 'LIABILITY_PD')
    AND c.accident_date BETWEEN '2018-01-01' AND '2022-12-31'
WHERE f.policy_status = 'ACTIVE'
GROUP BY f.fleet_id, f.policy_number, f.vehicle_count,
         f.naics_code, ig.industry_group, f.radius_code,
         d.driver_count, d.avg_driver_score, d.turnover_rate,
         f.years_in_business;
```

### Appendix D: Model Training Code

```python
"""
Commercial Auto Fleet Frequency Model
Training Script
Model ID: CA-FREQ-2023-001
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.genmod.generalized_linear_model import GLM
from statsmodels.genmod import families
from sklearn.metrics import roc_auc_score

def prepare_features(df):
    """Prepare features for fleet frequency model."""

    # Create dummy variables for categorical features
    size_dummies = pd.get_dummies(df['fleet_size_tier'], prefix='size')
    vehicle_dummies = pd.get_dummies(df['vehicle_class'], prefix='vehicle')
    radius_dummies = pd.get_dummies(df['radius_code'], prefix='radius')
    industry_dummies = pd.get_dummies(df['industry_group'], prefix='industry')

    # Drop baseline categories
    size_dummies = size_dummies.drop('size_Micro', axis=1, errors='ignore')
    vehicle_dummies = vehicle_dummies.drop('vehicle_light_truck', axis=1, errors='ignore')
    radius_dummies = radius_dummies.drop('radius_local', axis=1, errors='ignore')
    industry_dummies = industry_dummies.drop('industry_service_repair', axis=1, errors='ignore')

    # Continuous variable transformations
    df['driver_quality_centered'] = df['driver_quality_score'] - 72
    df['turnover_centered'] = df['driver_turnover_rate'] - 40
    df['years_capped'] = df['years_in_business'].clip(0, 25)

    # Combine features
    X = pd.concat([
        size_dummies,
        vehicle_dummies,
        radius_dummies,
        industry_dummies,
        df[['driver_quality_centered', 'turnover_centered', 'years_capped']]
    ], axis=1)

    return X

def train_frequency_model(df):
    """Train Negative Binomial GLM for claim frequency."""

    # Prepare features and target
    X = prepare_features(df)
    X = sm.add_constant(X)
    y = df['claim_count']
    exposure = df['vehicle_years']

    # Fit Negative Binomial GLM with log link
    model = GLM(
        y, X,
        exposure=exposure,
        family=families.NegativeBinomial(alpha=1.42)
    )

    results = model.fit()

    return results

def calculate_auc(model, X, y, exposure):
    """Calculate AUC for claim occurrence."""

    predictions = model.predict(X) * exposure
    binary_outcome = (y > 0).astype(int)

    return roc_auc_score(binary_outcome, predictions)

if __name__ == "__main__":
    # Load data
    df = pd.read_csv("fleet_frequency_data.csv")

    # Train-test split (temporal)
    train_df = df[df['accident_year'] <= 2021]
    test_df = df[df['accident_year'] == 2022]

    # Train model
    model = train_frequency_model(train_df)

    # Validate
    X_test = sm.add_constant(prepare_features(test_df))
    auc = calculate_auc(model, X_test, test_df['claim_count'], test_df['vehicle_years'])

    print("Model Summary:")
    print(model.summary())
    print(f"\nHoldout AUC: {auc:.3f}")
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
- Model Risk Committee: Approved June 22, 2023

---

**End of Document**
