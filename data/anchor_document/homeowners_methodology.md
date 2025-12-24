---
title: "Data and Methodology Guide - Homeowners Insurance"
portfolio: "homeowners"
type: "anchor_document"
company: "ABC Insurance Company"
version: "1.0"
effective_date: "2024-01-01"
status: "active"
---

# Data and Methodology Guide
## Model Development Standards for Homeowners Insurance

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes. No real insurance data, customer information, proprietary methodologies, or confidential information from any insurance company is used or simulated.

---

## Document Purpose and Scope

### Overview

This Data and Methodology Guide serves as the authoritative reference for homeowners insurance model development practices at ABC Insurance Company. It establishes standards specific to property insurance modeling, including catastrophe risk, property valuation, and geographic risk factors.

**Target Audience:**
- Actuaries developing pricing, reserving, or risk selection models
- Data scientists building predictive models
- Catastrophe modeling specialists
- Model validators and auditors
- Model Risk Governance Committee members

**Document Scope:**
- Data sourcing and property data standards (Sections 1-2)
- Catastrophe modeling integration (Section 3)
- Non-catastrophe peril modeling (Section 4)
- Geographic and territory development (Section 5)
- Feature engineering and variable standards (Section 6)
- Model validation and monitoring (Section 7)

---

## Section 1: Data Sources and Property Information

### 1.1 Primary Internal Data Sources

**PolicyAdmin HO - Homeowners Policy Administration System**

**Description:** Core system for all homeowners, renters, and condo policies.

**Key Data Elements:**
- Policy identifiers: Policy number, term dates, form type (HO-3, HO-5, etc.)
- Property information: Address, construction type, year built, square footage
- Coverage: Coverage A-F limits, deductibles, endorsements
- Premium and rating: Written premium, territory, protection class
- Property characteristics: Roof type, number of stories, heating type

**Data Quality:**
- Completeness: >98% for required fields
- Address match rate: 96% to rooftop geocode
- Known Issues: Year built missing for 2% of older policies

---

**PropertyData 360 - Property Characteristics Database**

**Description:** Consolidated property data from inspections, public records, and third-party sources.

**Key Data Elements:**
- Construction details: Frame, masonry, superior construction
- Roof information: Material, age, condition (from inspections)
- Property features: Pool, trampoline, wood stove
- Replacement cost estimate: Updated annually

**Data Refresh:** Quarterly from public records, inspection data within 30 days

---

**ClaimsManager HO - Homeowners Claims System**

**Description:** All homeowners claims from FNOL through closure.

**Key Data Elements:**
- Claim identifiers: Claim number, policy number, CAT code
- Loss information: Date of loss, cause of loss, location
- Coverage: Coverage applied (A, B, C, D, etc.)
- Financials: Paid, reserved, subrogation, salvage
- Catastrophe: CAT event code, PCS number if applicable

**Data Quality:**
- Cause of loss coding: 95% accuracy (validated by claims review)
- CAT coding: 99% accuracy for declared events

---

### 1.2 Third-Party Data Sources

**AIR Worldwide - Catastrophe Model**

**Description:** Hurricane, earthquake, severe storm modeling.

**Key Outputs:**
- Expected Annual Loss (AAL) by peril and geography
- Exceedance probability curves
- Event loss tables

**Integration:** Annual model run on full portfolio, quarterly for new business

---

**CoreLogic RCT - Replacement Cost Estimator**

**Description:** Property-level replacement cost estimates.

**Key Data Elements:**
- Replacement cost estimate
- Confidence score
- Valuation date

**Refresh:** At new business, renewal, and claim

---

**ISO Location Data - Protection Class**

**Description:** Fire protection class based on fire department capability and water supply.

**Key Data:**
- Protection class (1-10, 10 being worst)
- Distance to fire station
- Distance to hydrant

**Refresh:** Annual ISO updates

---

### 1.3 Geocoding Standards

**Accuracy Requirements:**
- New business: Rooftop-level geocoding required
- Renewal: Rooftop preferred, ZIP+4 minimum
- CAT modeling: Rooftop required for coastal/wildfire zones

**Geocoding Vendors:**
- Primary: Google Maps API
- Secondary: USPS address validation

**Match Rate Tracking:**
- Target: >95% rooftop match
- Current: 96.2%
- Fallback: ZIP centroid with flag for CAT review

---

## Section 2: Exposure and Property Valuation

### 2.1 Exposure Basis

**Primary Exposure: House-Years**
```
Exposure = (Policy_End_Date - Policy_Start_Date) / 365.25

Rules:
- Minimum exposure: 30 days
- Maximum exposure: 1.0 per annual term
- Mid-term cancellations: Prorated
```

**Secondary Exposure: Amount of Insurance (AOI)**
```
AOI_Exposure = Coverage_A_Limit * Exposure_Years

Used for:
- Severity analysis
- Catastrophe loading
- Large loss analysis
```

### 2.2 Replacement Cost Validation

**Insurance-to-Value (ITV) Analysis:**
```
ITV_Ratio = Coverage_A_Limit / Replacement_Cost_Estimate

Target: ITV between 80% and 120%
Action Triggers:
- ITV < 80%: Underinsured flag, underwriting review
- ITV > 120%: Overinsured flag, potential moral hazard
```

**Replacement Cost Sources:**
1. CoreLogic RCT (primary)
2. Marshall & Swift (validation)
3. Inspection-based estimate (gold standard)

**Annual ITV Audit:**
- Sample 1% of policies
- Compare estimate to claim settlement ratios
- Adjust estimator calibration as needed

### 2.3 Property Characteristic Validation

**Construction Type:**
- Frame (wood): Most common, highest fire risk
- Masonry (brick/stone): Lower fire, moderate wind
- Superior (fire resistive): Lowest fire risk

**Validation Methods:**
- Public records (tax assessor)
- Inspection photos
- Aerial imagery review

**Roof Information:**
- Roof age: Critical for wind/hail vulnerability
- Roof material: Shingle, tile, metal, flat
- Roof condition: Inspections for policies >15 years

---

## Section 3: Catastrophe Modeling Standards

### 3.1 CAT Model Framework

**Approved Catastrophe Models:**
- AIR Worldwide: Hurricane, earthquake, severe storm
- RMS: Hurricane (secondary validation)
- CoreLogic: Wildfire

**Model Components:**
1. **Hazard Module:** Event frequency, intensity, geographic footprint
2. **Vulnerability Module:** Damage ratio given hazard intensity
3. **Financial Module:** Apply policy terms to damage

### 3.2 Exposure Data Requirements

**Minimum Data for CAT Modeling:**

| Field | Requirement | CAT Model Impact |
|-------|-------------|------------------|
| Address | Rooftop geocode | Hazard accuracy |
| Construction | Frame/Masonry/Superior | Vulnerability |
| Year Built | Actual year | Building code proxy |
| Stories | Number | Wind vulnerability |
| Roof Type | Material and age | Wind/hail vulnerability |
| Coverage A | Dwelling limit | Financial calculation |
| Deductible | All-peril and CAT-specific | Financial calculation |

**Data Quality Thresholds:**
- Geocoding: >95% rooftop
- Construction: >98% populated
- Year built: >95% populated
- Unknown defaults documented

### 3.3 CAT vs. Non-CAT Loss Separation

**Catastrophe Definition:**
- PCS-declared events (Industry threshold: $25M+)
- Company threshold: $2M+ in losses from single event
- Event duration: Typically 72-hour window

**CAT Coding Process:**
1. Claims flagged at FNOL for event date/location
2. Daily review during active events
3. Post-event audit of all claims in affected area
4. Final CAT designation within 90 days

**Non-Modeled CAT Perils:**
- Convective storm (tornado, hail): Historical trend + load
- Wildfire: CoreLogic model + historical adjustment
- Winter storm: Historical trend + load

### 3.4 CAT Model Validation

**Validation Requirements:**
1. Compare AAL to 10-year historical average (adjusted for exposure)
2. Backtest against major historical events
3. Sensitivity analysis on key assumptions
4. Model-to-model comparison (AIR vs. RMS)

**Documentation:**
- Model version and run date
- Exposure data quality metrics
- Validation results and commentary
- Adjustments to model output (if any)

---

## Section 4: Non-Catastrophe Peril Modeling

### 4.1 Fire (Non-Weather)

**Key Risk Factors:**
- Protection class (fire department, hydrant)
- Construction type
- Heating type (wood stove, space heater)
- Occupancy (owner vs. tenant)
- Age of electrical system

**Modeling Approach:**
- GLM frequency model: Poisson, log link
- GLM severity model: Gamma, log link
- Territory factor captures residual geographic variation

### 4.2 Water Damage (Non-Weather)

**Key Risk Factors:**
- Age of home (plumbing age proxy)
- Construction type
- Basement presence
- Prior water claims

**Trend Considerations:**
- Water damage frequency trending +5-8% annually
- Drivers: Aging infrastructure, appliance failures
- Model must incorporate appropriate trend

### 4.3 Theft and Vandalism

**Key Risk Factors:**
- Territory (crime rate correlation)
- Protective devices (alarm, deadbolt)
- Occupancy
- Policy tenure (adverse selection for new)

**External Data:**
- FBI Uniform Crime Reports
- Local crime statistics by ZIP

### 4.4 Liability (Coverage E/F)

**Key Risk Factors:**
- Coverage limit selected
- Property features (pool, trampoline, dog)
- Number of residents
- Territory (litigation environment)

**Modeling Approach:**
- Lower frequency than property coverages
- Longer tail (monitor development)
- Social inflation trend consideration

---

## Section 5: Geographic Risk and Territory

### 5.1 Territory Development Methodology

**Objective:** Group geographic areas with similar loss characteristics.

**Process:**
1. Start with ZIP code level data
2. Analyze loss experience by ZIP (credibility-weighted)
3. Cluster ZIPs with similar experience
4. Apply geographic contiguity constraints
5. Test stability over time
6. Regulatory and business constraints

**Credibility Standard:**
- Full credibility: 1,082 claims (within 5% of true mean, 95% confidence)
- Partial credibility: Buhlmann credibility formula
- Complement: State or regional average

### 5.2 Territory Risk Components

**Fire Risk:**
- Protection class (ISO)
- Fire department proximity
- Hydrant proximity

**Weather Risk:**
- Hurricane exposure (distance to coast, historical)
- Hail/tornado exposure (historical frequency)
- Wildfire exposure (WUI proximity)

**Theft Risk:**
- Crime rates
- Population density

### 5.3 Coastal Zone Definition

**Hurricane Deductible Zones:**
- Tier 1: Within 1 mile of coast
- Tier 2: 1-5 miles from coast
- Tier 3: 5-25 miles from coast (selected counties)

**Definition Methodology:**
- Distance to coast calculated from property geocode
- FEMA flood zone overlay
- Historical storm surge maps

---

## Section 6: Feature Engineering Standards

### 6.1 Property Age Variables

**Age of Home:**
```python
home_age = current_year - year_built
home_age_capped = min(home_age, 100)  # Cap at 100 years

# Age bands for modeling
home_age_band = pd.cut(home_age, bins=[0, 10, 25, 50, 75, 100],
                        labels=['0-10', '11-25', '26-50', '51-75', '76+'])
```

**Roof Age:**
```python
roof_age = current_year - roof_year
# If roof_year missing, estimate from home age
roof_age_estimated = min(home_age, 25)  # Assume replacement every 25 years
```

### 6.2 Protection and Risk Mitigation

**Protection Class:**
```python
# ISO protection class 1-10
protection_class_grouped = np.where(protection_class <= 3, 'Protected',
                            np.where(protection_class <= 6, 'Semi-Protected',
                                     'Unprotected'))
```

**Protective Devices:**
```python
has_alarm = (alarm_type != 'None').astype(int)
has_sprinkler = (sprinkler_system == 'Yes').astype(int)
protection_score = has_alarm + has_sprinkler + has_deadbolt
```

### 6.3 Geographic Features

**Distance Calculations:**
```python
distance_to_coast_miles = haversine(property_lat, property_lon, 
                                     nearest_coast_lat, nearest_coast_lon)
distance_to_fire_station = property_to_station_distance  # From ISO
```

**Derived Geographic:**
```python
coastal_zone = np.where(distance_to_coast_miles <= 1, 'Tier1',
               np.where(distance_to_coast_miles <= 5, 'Tier2',
               np.where(distance_to_coast_miles <= 25, 'Tier3', 'Inland')))
```

---

## Section 7: Model Validation and Monitoring

### 7.1 Validation Framework

**Development Validation:**
- 70/15/15 train/validation/holdout split
- Stratified by territory and year
- CAT years handled separately

**Performance Metrics:**
- Frequency: AUC, actual vs. expected by decile
- Severity: R², mean absolute error
- Loss cost: Combined ratio, lift analysis

**CAT Model Validation:**
- AAL comparison to historical
- Event backtesting
- Sensitivity analysis

### 7.2 Monitoring Standards

**Monthly Monitoring:**
- Actual vs. expected loss ratio (non-CAT)
- Claim frequency by territory
- Severity trends

**Quarterly Monitoring:**
- CAT loss attribution
- Territory performance
- New business vs. renewal performance

**Annual Review:**
- Full model re-validation
- CAT model update assessment
- Territory re-evaluation
- Regulatory compliance review

### 7.3 Alert Thresholds

| Metric | Yellow | Orange | Red |
|--------|--------|--------|-----|
| Non-CAT A/E | 1.05-1.10 | 1.10-1.15 | >1.15 |
| Territory variance | 10-15% | 15-25% | >25% |
| Severity trend | +5-10% | +10-15% | >+15% |

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
