---
title: "Personal Auto Collision Coverage Model Update"
model_type: "collision"
technique: "GLM"
product: "personal_auto"
coverage: "collision"
year: 2024
status: "production"
---

# Personal Auto Collision Coverage Model - 2024 Update Documentation

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes. No real insurance data, customer information, proprietary methodologies, or confidential information from any insurance company or financial institution is used or simulated.

All names, addresses, policy numbers, claim amounts, and company information are fictional. Any resemblance to actual persons, organizations, or data is purely coincidental.

This project showcases AI agent capabilities for automated documentation generation and is not intended for production use with real data or models.

---

## Executive Summary

ABC Insurance Company completed a comprehensive update to its collision coverage rating model in 2024, representing the first major refresh since 2019. The collision model predicts frequency and severity of at-fault collision claims, which represent the largest coverage by premium volume (32% of total personal auto premium, $272M annually).

This update incorporates 5 years of recent loss experience (2019-2023), refreshes territory definitions to align with the 2023 territory rerating project, and adds new risk variables including advanced driver assistance system (ADAS) features and vehicle safety ratings. The model maintains the GLM framework for collision coverage due to its strong regulatory acceptance, interpretability, and proven performance for this coverage type.

**Key Drivers for Model Update:**
- Previous model based on 2014-2018 experience (outdated)
- Territory system updated (2023 rerating project)
- Vehicle safety technology evolution (ADAS becoming standard)
- Supply chain disruptions impacting severity (2021-2023)
- Changing driving patterns post-COVID-19

**Model Performance:**
- Frequency R²: 0.52 (vs. 0.48 for 2019 model, +8% improvement)
- Severity R²: 0.38 (vs. 0.33 for 2019 model, +15% improvement)
- AUC: 0.76 (vs. 0.73, +4% improvement)
- Implementation: January 1, 2024
- Expected annual benefit: $5.2M through improved rate adequacy and risk segmentation

**Model Changes vs. 2019:**
- Variables: 18 (vs. 14 in 2019 model), added ADAS features, safety ratings
- Territory system: 15 zones (vs. 10), aligns with 2023 territory definitions
- Experience period: 2019-2023 (vs. 2014-2018)
- Severity trend: Adjusted for supply chain inflation (+18% cumulative 2021-2023)

---

## 1. Business Context & Objectives

### 1.1 Background

**Collision Coverage Overview:**

Collision coverage pays for damage to the insured's vehicle from at-fault accidents with other vehicles, objects, or single-vehicle accidents (rollovers, run-off-road). It is the highest premium coverage in the personal auto portfolio.

**2019-2023 Loss Experience:**

ABC Insurance's collision coverage experienced mixed results over the model refresh period:

- **2019:** Loss ratio 67% (target 65%)
- **2020:** Loss ratio 58% (COVID-19 reduced driving)
- **2021:** Loss ratio 69% (return to driving + supply chain issues)
- **2022:** Loss ratio 72% (supply chain peak impact)
- **2023:** Loss ratio 68% (supply chain stabilizing)
- **5-Year Average:** 67% (2 points above target)

**Key Trends Impacting Collision:**

**1. Supply Chain Disruptions (2021-2023):**
- Parts shortages increased repair times and costs
- Average collision severity increased 18% (2021-2023)
- Increased use of aftermarket parts (quality concerns)
- Rental car reimbursement duration extended (avg 14 days vs. 8 days pre-COVID)

**2. ADAS Technology Proliferation:**
- Advanced Driver Assistance Systems (lane departure, automatic emergency braking, blind spot monitoring) becoming standard
- Evidence of frequency reduction (10-15%) for ADAS-equipped vehicles
- Severity impact mixed (expensive sensors but fewer/less severe claims)
- 2019 model did not capture ADAS impact (data not available)

**3. Vehicle Mix Changes:**
- Shift toward SUVs and trucks (52% of fleet in 2023 vs. 44% in 2018)
- These vehicles have different collision characteristics (higher severity, lower frequency than sedans)

**4. Driving Pattern Changes:**
- COVID-19 permanently altered commuting patterns (more remote work)
- Annual mileage down 8% on average vs. pre-COVID
- However, urban congestion returned by 2023

**5. Distracted Driving:**
- Continued increase in smartphone-related distraction claims
- Severity impact (higher-speed collisions when distracted)

### 1.2 Business Problem

**Issues with 2019 Model:**

1. **Outdated Experience:** Based on 2014-2018 data, missing 2019-2023 trends
2. **Territory Misalignment:** Used old 10-territory system (updated to 15 in 2023)
3. **Missing ADAS Variable:** No adjustment for safety technology
4. **Supply Chain Severity:** Under-predicted 2022-2023 severity by 12%
5. **Performance Degradation:** R² declined from 0.48 (in-sample 2018) to 0.42 (on 2023 data)

**Rate Inadequacy:**
- 2-point loss ratio miss driven primarily by severity underestimation
- High-mileage commuters under-priced (annual mileage variable stale)
- ADAS-equipped vehicles over-priced (frequency benefit not captured)

### 1.3 Objectives

**Primary Objectives:**
1. Update model with 2019-2023 experience (5 years, credible)
2. Align with 2023 territory definitions (15 zones)
3. Incorporate ADAS safety features
4. Recalibrate severity for supply chain inflation
5. Improve R² by ≥5% over 2019 model

**Secondary Objectives:**
- Maintain GLM framework (proven, interpretable, regulatory acceptance)
- Improve competitive position for low-risk drivers (ADAS, low mileage)
- Reduce rate inadequacy to achieve target 65% loss ratio
- Enhance model documentation and validation procedures

**Business Impact Goals:**
- $5.2M annual improvement (2% loss ratio improvement on $272M premium)
- Retention improvement of 3% for ADAS-equipped vehicles
- Rate adequacy for high-severity vehicles (+8-12% rate increase)

---

## 2. Regulatory Compliance & Methodology

### 2.1 Regulatory Compliance

This collision model update complies with NAIC Model Audit Rule, ASOPs 12, 23, 41, and 56. Rate filings submitted to all 15 states in Q4 2023, approved by December 2023 for January 1, 2024 implementation.

**Key Filing Points:**
- Update characterized as "model refresh" not "new model" (methodology unchanged, GLM)
- Territory system change extensively documented (approved separately in 2023)
- ADAS variable justified with third-party research (IIHS studies)
- Comparison to 2019 model demonstrates improved accuracy

### 2.2 Methodology: GLM Framework

**Frequency Model:**
- Distribution: Poisson (count of at-fault collision claims)
- Link: Log
- Offset: Log(exposure in policy-years)

**Severity Model:**
- Distribution: Gamma (collision claim amounts)
- Link: Log
- Sample: Closed collision claims only (12+ months development)

**Combined Loss Cost:**
```
Loss Cost = Frequency × Severity
```

---

## 3. Data & Features

### 3.1 Data Sources

**Internal:**
- PolicyMaster 3.0: Policies 2019-2023, 2,375,000 policy-years
- ClaimsVision 2.5: Collision claims 2019-2023, 285,000 claims (12% frequency)
- Average collision severity: $4,850

**External:**
- IIHS Vehicle Safety Ratings: ADAS feature data by make/model/year
- J.D. Power Vehicle Values: Updated vehicle valuation
- 2023 Territory Definitions: 15-territory system

### 3.2 Variables (18 Total)

**Driver Variables (6):**
1. driver_age (16-90, continuous)
2. years_licensed (0-70, continuous)
3. prior_collision_claims_3yr (0, 1, 2, 3+)
4. violations_3yr (0, 1, 2, 3+)
5. gender (Male, Female)
6. marital_status (Single, Married, Divorced, Widowed)

**Vehicle Variables (7):**
7. vehicle_age (0-25, continuous)
8. vehicle_value_log (log-transformed)
9. vehicle_type (Sedan, SUV, Truck, Van, Sports Car, Luxury)
10. vehicle_size (Small, Mid, Large)
11. adas_level (None, Basic, Advanced) **[NEW 2024]**
12. safety_rating (Poor, Average, Good, Excellent) **[NEW 2024]**
13. anti_lock_brakes (binary)

**Policy/Geographic Variables (5):**
14. territory (T1-T15, updated to 2023 system)
15. annual_mileage_log (log-transformed)
16. comprehensive_deductible ($250, $500, $1000, $2500, $5000)
17. policy_tenure (0-25 years)
18. multi_vehicle_policy (binary)

**Key Variable Changes from 2019:**
- **Added:** adas_level, safety_rating (capture safety technology)
- **Updated:** territory (10 zones → 15 zones)
- **Modified:** annual_mileage (updated self-reported + validation)

---

## 4. Model Development & Performance

### 4.1 Development Process

**Data Split:**
- Training: 2019-2022 (75%, 1,781,250 policy-years)
- Validation: 2023 H1 (12.5%, 148,438 policy-years)
- Holdout: 2023 H2 (12.5%, 148,437 policy-years)

**Variable Selection:**
- Forward selection based on AIC improvement
- All 18 variables significant (p < 0.05)
- Interaction terms tested: driver_age × vehicle_type (p = 0.08, not included)

**Model Training:**
- Maximum likelihood estimation via IRLS (Iteratively Reweighted Least Squares)
- Convergence: 14 iterations
- Dispersion parameter: 1.08 (mild overdispersion, acceptable)

### 4.2 Model Performance

**Frequency Model Results:**

| Metric              | 2019 Model | 2024 Model | Improvement |
|---------------------|------------|------------|-------------|
| R² (holdout)        | 0.48       | 0.52       | +8.3%       |
| AUC                 | 0.73       | 0.76       | +4.1%       |
| Top Decile Lift     | 2.8x       | 3.1x       | +10.7%      |
| Calibration Bias    | +2.3%      | +0.5%      | Better      |

**Severity Model Results:**

| Metric              | 2019 Model | 2024 Model | Improvement |
|---------------------|------------|------------|-------------|
| R² (holdout)        | 0.33       | 0.38       | +15.2%      |
| RMSE                | $1,950     | $1,820     | -6.7%       |
| MAPE                | 28.5%      | 25.8%      | -9.5%       |

**Combined Loss Cost Accuracy:**
- 2024 model predicts 2023 H2 loss costs with 2.1% error (vs. 8.7% for 2019 model)

### 4.3 Key Findings

**ADAS Impact:**
- Vehicles with Advanced ADAS: -12% frequency (relative to None)
- Vehicles with Basic ADAS: -6% frequency
- Severity impact: +3% (expensive sensors, but fewer total claims so net benefit)

**Territory Impact:**
- 15-territory system captures urban sub-market variation better
- High-density urban (T13): 1.68x frequency vs. base
- Rural low-risk (T1): 0.71x frequency

**Vehicle Safety Ratings:**
- Excellent safety rating: -8% frequency vs. Poor
- Good safety rating: -5% frequency
- Severity correlation: Better safety = lower severity (-6% for Excellent)

**Supply Chain Severity Adjustment:**
- 2021-2023 severity trend: +5.8% annually (vs. historical 3.2%)
- Adjusted base severity by +12% to reflect new cost environment
- Monitoring for normalization as supply chains stabilize

---

## 5. Implementation & Monitoring

### 5.1 Implementation Plan

**Timeline:**
- Model finalized: October 2023
- Rate filings submitted: November 2023
- State approvals: December 2023
- Production deployment: January 1, 2024

**Integration:**
- Updated rating tables in PolicyMaster
- API endpoint refresh for quoting system
- Territory mapping updated (10 → 15 zones)
- ADAS data integration from IIHS database

**Rollout:**
- New business: January 1, 2024
- Renewals: Immediate (all renewals effective Jan 1+)
- Rate change communication: Automated letters with explanations

### 5.2 Rate Impact

**Overall Rate Level:** +1.8% (rate adequacy adjustment)

**Rate Changes by Segment:**

| Segment                    | Avg Rate Change | Rationale                        |
|----------------------------|-----------------|----------------------------------|
| ADAS Advanced + Low Mileage| -8% to -12%     | Double benefit (safety + exposure)|
| Young drivers (16-25)      | +5% to +8%      | Updated age curves               |
| High mileage (>20K/year)   | +6% to +10%     | Exposure-based risk              |
| Old territories (T3, T7)   | -3% to +3%      | Territory remapping              |
| New high-risk territories  | +10% to +15%    | Better risk segmentation         |

### 5.3 Monitoring Plan

**Monthly Metrics:**
- Loss ratio by territory and vehicle type
- Actual vs. expected frequency/severity
- ADAS adoption rate and impact validation

**Quarterly Validation:**
- R² on rolling 12-month data
- Coefficient stability check
- Calibration testing (actual/expected by decile)

**Annual Review:**
- Comprehensive model re-validation
- Assessment of supply chain normalization
- ADAS penetration trends
- Decision on model refresh (typically every 3-5 years)

**Alert Thresholds:**
- Loss ratio >67% for 2 consecutive quarters → investigation
- R² drops below 0.48 → potential model degradation
- ADAS coefficient changes >20% → data quality check

---

## 6. Model Comparison & Business Impact

### 6.1 2019 vs. 2024 Model Comparison

**Summary of Changes:**

| Aspect                | 2019 Model      | 2024 Model      | Impact          |
|-----------------------|-----------------|-----------------|-----------------|
| Experience Period     | 2014-2018       | 2019-2023       | More recent     |
| Variables             | 14              | 18 (+4)         | ADAS, safety    |
| Territory System      | 10 zones        | 15 zones        | Better granularity |
| Frequency R²          | 0.48            | 0.52            | +8% improvement |
| Severity R²           | 0.33            | 0.38            | +15% improvement|
| Loss Cost MAPE        | 18.2%           | 13.5%           | -26% error reduction |

### 6.2 Business Impact

**Financial Impact:**
- Target loss ratio: 65%
- 2023 actual loss ratio (using 2019 model): 68%
- Projected 2024 loss ratio (using 2024 model): 66%
- **Improvement: 2 points = $5.4M annually**

**Competitive Impact:**
- ADAS-equipped vehicles: Rate reductions improve competitiveness
- Estimated retention improvement: +3% for ADAS segment
- Quote-to-bind conversion: +2% overall

**Customer Impact:**
- 42% of customers receive rate decrease or <2% increase
- 31% receive moderate increase (2-6%)
- 27% receive higher increase (>6%, high-risk segments)
- Overall: Premium-neutral to slight increase (+1.8% average)

---

## 7. Validation & Sensitivity Analysis

### 7.1 Validation Tests

**Holdout Performance:**
- 2024 model tested on 2023 H2 data (unseen during training)
- Frequency: Predicted 11.8%, actual 12.1% (bias +2.5%, acceptable)
- Severity: Predicted $4,820, actual $4,860 (bias +0.8%)

**Backtesting:**
- Applied 2024 model coefficients to 2022 data
- Loss ratio accuracy: Predicted 70.2%, actual 72% (within 2 points)

**Temporal Stability:**
- Coefficients stable across 2019-2022 training years
- Driver age coefficient: -0.018 to -0.016 (minimal variation)
- Territory coefficients: Consistent directional effects

### 7.2 Sensitivity Analysis

**ADAS Coefficient Uncertainty:**
- ADAS adoption still growing (32% of fleet in 2023)
- Frequency reduction: 95% CI [-15%, -9%] for Advanced ADAS
- Monitoring closely as adoption increases

**Supply Chain Normalization:**
- If severity returns to pre-COVID trend by 2025: -$0.8M impact (manageable)
- If severity stays elevated: Model accurate, no action needed
- Quarterly severity monitoring dashboard implemented

**Territory Sensitivity:**
- Tested alternative 12-territory and 18-territory systems
- 15 territories optimal (credibility vs. granularity trade-off)

---

## 8. Limitations & Future Work

### 8.1 Limitations

1. **ADAS Data Quality:** Relies on IIHS database, some vehicles missing ADAS flags (2.3%)
2. **Annual Mileage:** Self-reported, potential underreporting bias
3. **Supply Chain Uncertainty:** Unclear if elevated severity persists long-term
4. **Telematics:** Not integrated (future opportunity)
5. **EV Vehicles:** Small sample size (4% of fleet), limited differentiation

### 8.2 Future Enhancements

**Short-Term (2024-2025):**
- Integrate factory telematics data (for OEM-connected vehicles)
- Refine ADAS categories (AEB, lane keep, adaptive cruise separately)
- Add EV-specific variables as fleet grows

**Medium-Term (2025-2026):**
- Explore machine learning (XGBoost) for collision (following comprehensive model success)
- Incorporate real-time traffic data (congestion patterns)

**Long-Term (2026+):**
- Usage-based insurance (UBI) integration
- Autonomous vehicle adjustments as technology matures

---

## Appendices

### Appendix A: Coefficient Table

**Frequency Model (Selected Coefficients):**

| Variable                | Coefficient | Std Error | Relativity | 95% CI           |
|-------------------------|-------------|-----------|------------|------------------|
| Intercept               | -2.18       | 0.025     | -          | -                |
| driver_age              | -0.017      | 0.0008    | 0.983/yr   | [-0.019, -0.015] |
| prior_collision_1       | 0.52        | 0.018     | 1.68       | [0.485, 0.555]   |
| prior_collision_2       | 0.87        | 0.032     | 2.39       | [0.807, 0.933]   |
| prior_collision_3+      | 1.15        | 0.048     | 3.16       | [1.056, 1.244]   |
| violations_1            | 0.28        | 0.015     | 1.32       | [0.251, 0.309]   |
| adas_basic              | -0.062      | 0.012     | 0.94       | [-0.086, -0.038] |
| adas_advanced           | -0.127      | 0.015     | 0.88       | [-0.156, -0.098] |
| safety_rating_excellent | -0.083      | 0.014     | 0.92       | [-0.110, -0.056] |
| territory_T13           | 0.518       | 0.028     | 1.68       | [0.463, 0.573]   |
| vehicle_age             | 0.008       | 0.002     | 1.008/yr   | [0.004, 0.012]   |
| log_annual_mileage      | 0.235       | 0.018     | -          | [0.200, 0.270]   |

### Appendix B: Model Monitoring Dashboard Specification

**Dashboard Metrics (Monthly Update):**

**Section 1: Performance**
- Loss ratio: Actual vs. budget
- Frequency: Actual vs. expected (overall, by territory)
- Severity: Actual vs. expected (overall, by vehicle type)

**Section 2: Model Accuracy**
- R² (rolling 12-month)
- Calibration plot (10 deciles)
- Lift chart

**Section 3: Key Variables**
- ADAS adoption rate (% of new policies)
- Average annual mileage (trend monitoring)
- Territory mix shift

**Section 4: Alerts**
- Red flags for loss ratio >67%, R² <0.48, calibration error >10%

---

## Document Control

**Version:** 1.0
**Date:** October 30, 2023
**Last Updated:** October 30, 2023

**Prepared by:**
Thomas Lee, FCAS, MAAA
Senior Actuary, Personal Auto Pricing
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
- State Insurance Departments (15 states)
- Internal Audit
- Actuarial Library

**Next Review Date:** October 1, 2024

**Model ID:** PAUTO-COLL-GLM-2024.1
**Documentation Reference:** DOC-2024-COLL-001

---

**End of Document**
