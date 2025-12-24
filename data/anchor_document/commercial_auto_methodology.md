---
title: "Data and Methodology Guide - Commercial Auto Insurance"
portfolio: "commercial_auto"
type: "anchor_document"
company: "ABC Insurance Company"
version: "1.0"
effective_date: "2024-01-01"
status: "active"
---

# Data and Methodology Guide
## Model Development Standards for Commercial Auto Insurance

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes. No real insurance data, customer information, proprietary methodologies, or confidential information from any insurance company is used or simulated.

---

## Document Purpose and Scope

### Overview

This Data and Methodology Guide serves as the authoritative reference for commercial auto insurance model development practices at ABC Insurance Company. It establishes standards specific to fleet and commercial vehicle modeling, including driver risk assessment, vehicle classification, and large loss considerations.

**Target Audience:**
- Actuaries developing pricing, reserving, or risk selection models
- Data scientists building predictive models
- Underwriters evaluating fleet risks
- Model validators and auditors
- Model Risk Governance Committee members

**Document Scope:**
- Data sourcing and fleet data standards (Sections 1-2)
- Vehicle and driver classification (Section 3)
- Coverage-specific modeling (Section 4)
- Large loss and excess modeling (Section 5)
- Experience rating integration (Section 6)
- Model validation and monitoring (Section 7)

---

## Section 1: Data Sources and Fleet Information

### 1.1 Primary Internal Data Sources

**PolicyAdmin CA - Commercial Auto Policy System**

**Description:** Core system for all commercial auto policies.

**Key Data Elements:**
- Policy identifiers: Policy number, term dates, account number
- Named insured: Business name, FEIN, NAICS, SIC
- Vehicles: VIN, year, make, model, GVW, use, radius
- Drivers: Name, DOB, license, hire date, violations
- Coverages: Liability, physical damage, hired/non-owned
- Rating: Territory, fleet size tier, experience mod

**Data Quality:**
- Vehicle count accuracy: 95% (validated at audit)
- Driver list accuracy: 85% (turnover creates lag)
- VIN decode rate: 98%

---

**FleetManager - Vehicle and Driver Database**

**Description:** Centralized fleet and driver information with MVR integration.

**Key Data Elements:**
- Vehicle schedule: All covered vehicles with characteristics
- Driver roster: All listed drivers with MVR data
- Telematics: Miles driven, hard braking, speeding (where available)
- MVR refresh: Annual or continuous monitoring

**Data Refresh:**
- Vehicle schedule: Updated at policy change
- Driver MVR: Annual refresh or continuous monitoring
- Telematics: Daily where integrated

---

**ClaimsVision CA - Commercial Auto Claims System**

**Description:** All commercial auto claims from FNOL through closure.

**Key Data Elements:**
- Claim identifiers: Claim number, policy number, vehicle
- Accident information: Date, location, description
- Coverage: Liability BI, liability PD, collision, comprehensive
- Claimant: Type (insured driver, third party, passenger)
- Financials: Paid, reserved, subrogation

**Data Quality:**
- Coverage coding: 98% accurate
- Driver assignment: 92% (some claims lack driver ID)
- Subrogation tracking: 95%

---

### 1.2 Third-Party Data Sources

**Motor Vehicle Records (MVR)**

**Sources:** State DMVs via third-party aggregators (LexisNexis, etc.)

**Key Data Elements:**
- License status (valid, suspended, revoked)
- Violations (type, date, points)
- Accidents (at-fault, not-at-fault)
- License class (CDL, non-CDL)

**Refresh Frequency:**
- Annual at policy renewal
- Continuous monitoring (selected accounts)

---

**VIN Decoding Services**

**Source:** NHTSA database, commercial decoders

**Key Data Elements:**
- Year, make, model
- Body style, GVW/GVWR
- Engine, fuel type
- Safety features

**Use:** Validate reported vehicle characteristics

---

**Telematics Data (Where Available)**

**Sources:** OEM partnerships, aftermarket devices

**Key Data Elements:**
- Miles driven
- Hard braking events
- Speeding incidents
- Time of day patterns
- Geographic patterns

**Current Penetration:** 15% of fleet policies

---

### 1.3 ISO Commercial Auto Data

**ISO Loss Costs:**
- Published by state and class
- Updated annually
- Includes development and trend

**ISO Classification:**
- Vehicle type and size
- Business use
- Radius of operation
- Industry class

---

## Section 2: Exposure Basis

### 2.1 Vehicle-Year Exposure

**Primary Exposure: Vehicle-Years**
```
Vehicle_Exposure = Sum of (Vehicle_End_Date - Vehicle_Start_Date) / 365.25

For each vehicle on schedule:
- Minimum exposure: 30 days
- Mid-term additions: Prorated from add date
- Mid-term deletions: Prorated to delete date
```

**Power Unit vs. Trailer:**
- Power units: Full exposure
- Trailers: Typically lower rate, separate exposure

### 2.2 Alternative Exposure Bases

**Miles Driven:**
- Used for some large fleets
- Requires telematics or odometer readings
- More accurate for loss prediction
- Limited availability

**Revenue or Payroll:**
- Used for some commercial classes
- For-hire trucking: Revenue-based
- Service contractors: Payroll-based

### 2.3 Fleet Size Considerations

**Fleet Size Tiers:**

| Tier | Vehicles | Characteristics |
|------|----------|-----------------|
| Small | 1-5 | Limited credibility, class-rated |
| Medium | 6-25 | Some experience credibility |
| Large | 26-100 | Experience-rated |
| Major | 100+ | Significant experience credibility |

**Modeling Implications:**
- Small fleets: Rely more on class factors
- Large fleets: More weight on experience
- Major fleets: Individual account analysis

---

## Section 3: Vehicle and Driver Classification

### 3.1 Vehicle Classification

**ISO Size Classes:**

| Class | GVW (lbs) | Examples |
|-------|-----------|----------|
| Light | ≤10,000 | Pickup, van, SUV |
| Medium | 10,001-20,000 | Box truck, delivery van |
| Heavy | 20,001-45,000 | Straight truck |
| Extra-Heavy | >45,000 | Tractor-trailer |

**Use Classification:**
- Service: Visiting customers, service calls
- Commercial: Carrying goods for business
- Retail: Pickup/delivery to retail customers
- For-Hire: Transporting goods for others (trucking)

**Radius Classification:**
- Local: ≤50 miles from base
- Intermediate: 51-200 miles
- Long Distance: >200 miles

### 3.2 Driver Classification

**Driver Factors:**

| Factor | Categories | Impact |
|--------|------------|--------|
| Age | <25, 25-65, 65+ | Young higher risk |
| Experience | Years licensed, CDL years | More experience = lower risk |
| Violations | 0, 1, 2, 3+ in 3 years | Strong predictor |
| At-fault accidents | 0, 1, 2+ in 3 years | Strong predictor |
| License type | Non-CDL, CDL Class A/B/C | CDL = professional |

**Driver Score Development:**
```python
driver_score = (
    age_factor * 0.15 +
    experience_factor * 0.15 +
    violation_factor * 0.35 +
    accident_factor * 0.35
)
# Higher score = higher risk
```

### 3.3 Fleet Driver Summary

**For Fleet Rating:**
```python
fleet_driver_factor = weighted_average(driver_scores, weights=vehicle_assignments)

# Alternative: Worst driver approach for small fleets
fleet_driver_factor = max(driver_scores)  # For fleets < 5 vehicles
```

---

## Section 4: Coverage-Specific Modeling

### 4.1 Liability Coverage

**Bodily Injury (BI):**
- Third-party injuries
- Longer tail than PD
- Subject to social inflation trend

**Key Predictors:**
- Vehicle type (heavy vehicles = more damage potential)
- Radius (more miles = more exposure)
- Territory (litigation environment)
- Driver quality

**Modeling Approach:**
```
BI_Frequency: Poisson GLM, log link
BI_Severity: Gamma GLM, log link
```

**Property Damage (PD):**
- Third-party property damage
- Shorter tail than BI
- Vehicle repair cost trends

### 4.2 Physical Damage Coverage

**Collision:**
- Damage from collision with vehicle/object
- Own vehicle coverage
- Deductible applies

**Key Predictors:**
- Driver quality (accidents, violations)
- Vehicle age and value
- Vehicle use (more miles = more exposure)

**Comprehensive:**
- Non-collision damage (theft, weather, vandalism)
- Generally lower frequency than collision
- Theft risk varies by geography and vehicle type

### 4.3 Hired and Non-Owned Auto

**Coverage Description:**
- Employees using personal vehicles for business
- Rented or borrowed vehicles

**Exposure Basis:**
- Number of employees
- Miles driven (estimated)
- Payroll as proxy

**Modeling Considerations:**
- Lower frequency per exposure unit
- Severity similar to owned auto
- Limited loss data for some accounts

---

## Section 5: Large Loss and Excess Modeling

### 5.1 Large Loss Definition

**Thresholds:**
- Large loss: >$100,000
- Excess loss: >$250,000
- Shock loss: >$1,000,000

**Commercial Auto Large Loss Characteristics:**
- Higher severity than personal auto
- Nuclear verdicts increasingly common
- Trucking BI losses can exceed $10M

### 5.2 Large Loss Treatment in Ratemaking

**Capping Approach:**
```python
capped_loss = min(actual_loss, cap_threshold)
excess_loss = max(0, actual_loss - cap_threshold)

# Separate large loss loading
large_loss_load = excess_losses / total_exposure
```

**ILF (Increased Limits Factors):**
- Develop ILFs for limits above basic
- Commercial often written at $1M CSL
- Excess liability for higher limits

### 5.3 Social Inflation Trend

**Definition:** Trend in claims costs above economic inflation, driven by changing legal environment.

**Indicators:**
- Nuclear verdict frequency
- Attorney involvement rate
- Jury awards trending
- Settlement demands

**Current Assumption:**
```
BI_Severity_Trend = Economic_Inflation + Social_Inflation_Load
                  = 3% + 5% = 8% annually (illustrative)
```

---

## Section 6: Experience Rating

### 6.1 Commercial Auto Experience Rating

**ISO Experience Rating Plan:**
- Applies to accounts meeting premium threshold
- Three-year experience period
- Primary/excess split similar to WC

**Formula:**
```
Mod = (Actual_Primary + W*Actual_Excess + (1-W)*Expected_Excess) / Expected_Total

Where:
W = Credibility weight based on expected losses
Primary = Capped per-occurrence losses
Excess = Losses above cap
```

### 6.2 Schedule Rating

**Commercial Auto Schedule Factors:**

| Factor | Credit Range | Debit Range |
|--------|--------------|-------------|
| Management | -15% to +10% | Supervision, oversight |
| Safety programs | -15% to +10% | Training, equipment |
| Fleet age/condition | -10% to +10% | Newer, maintained |
| Driver selection | -15% to +15% | Hiring, monitoring |
| Financial stability | -5% to +5% | Ability to pay |

**Total Range:** Typically ±25% maximum

### 6.3 Experience Rating in Modeling

**Incorporating Experience:**
```python
# For large fleets with credibility
expected_loss = fleet_experience_loss * credibility + class_expected * (1 - credibility)

# For small fleets
expected_loss = class_expected * experience_mod
```

---

## Section 7: Model Validation and Monitoring

### 7.1 Validation Framework

**Frequency Model:**
- AUC for claim occurrence
- Actual vs. expected by class and territory
- Fleet size segmentation

**Severity Model:**
- Mean absolute error, R²
- Actual vs. expected by coverage
- Large loss backtesting

**Loss Cost Model:**
- Combined ratio analysis
- Lift by predicted risk decile
- Champion-challenger testing

### 7.2 Monitoring Standards

**Monthly:**
- Claim counts by coverage
- Reported losses vs. expected
- Large loss alerts (>$100K)

**Quarterly:**
- Loss development emergence
- Experience mod distribution
- New business vs. renewal loss ratios

**Annually:**
- Full model re-validation
- Social inflation trend review
- Class and territory re-evaluation

### 7.3 Alert Thresholds

| Metric | Yellow | Orange | Red |
|--------|--------|--------|-----|
| Liability frequency A/E | 1.05-1.10 | 1.10-1.15 | >1.15 |
| BI severity trend | +8-12% | +12-18% | >+18% |
| Large loss frequency | +15-25% | +25-40% | >+40% |
| Combined ratio | 102-107% | 107-115% | >115% |

---

## Section 8: Industry-Specific Considerations

### 8.1 For-Hire Trucking

**Unique Characteristics:**
- FMCSA regulation (MCS-90, BMC-91)
- Higher liability limits required
- Cargo coverage separate
- Hours of service compliance

**Modeling Considerations:**
- Operating authority verified
- Safety scores (SMS, CSA)
- Commodity type impacts cargo risk
- Interstate vs. intrastate

### 8.2 Contractor/Service

**Unique Characteristics:**
- Varied vehicle types
- Job site exposure
- Tools and equipment
- Workers comp interface

**Modeling Considerations:**
- Industry hazard grade
- Vehicle utilization
- Geographic concentration

### 8.3 Delivery/Last Mile

**Unique Characteristics:**
- High mileage
- Frequent stops
- Urban exposure
- Driver turnover

**Modeling Considerations:**
- Delivery density (stops per mile)
- Time pressure impacts
- Vehicle wear and tear

---

## Document Version Control

**Version:** 1.0
**Effective Date:** January 1, 2024
**Last Updated:** January 1, 2024
**Next Review:** January 1, 2025

**Prepared by:** Actuarial Standards Committee
**Approved by:** Chief Actuary

---

**End of Document**
