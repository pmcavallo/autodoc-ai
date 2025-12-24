---
title: "Data and Methodology Guide - Workers Compensation Insurance"
portfolio: "workers_comp"
type: "anchor_document"
company: "ABC Insurance Company"
version: "1.0"
effective_date: "2024-01-01"
status: "active"
---

# Data and Methodology Guide
## Model Development Standards for Workers Compensation Insurance

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes. No real insurance data, customer information, proprietary methodologies, or confidential information from any insurance company is used or simulated.

---

## Document Purpose and Scope

### Overview

This Data and Methodology Guide serves as the authoritative reference for workers compensation insurance model development practices at ABC Insurance Company. It establishes standards specific to occupational injury modeling, including medical cost inflation, indemnity duration, and experience rating considerations.

**Target Audience:**
- Actuaries developing pricing, reserving, or risk selection models
- Data scientists building predictive models
- Claims analysts and medical cost specialists
- Model validators and auditors
- Model Risk Governance Committee members

**Document Scope:**
- Data sourcing and classification standards (Sections 1-2)
- Medical cost modeling (Section 3)
- Indemnity and duration modeling (Section 4)
- Loss development and reserving (Section 5)
- Experience rating integration (Section 6)
- Model validation and monitoring (Section 7)

---

## Section 1: Data Sources and Classification

### 1.1 Primary Internal Data Sources

**PolicyAdmin WC - Workers Compensation Policy System**

**Description:** Core system for all workers compensation policies.

**Key Data Elements:**
- Policy identifiers: Policy number, term dates, state(s)
- Employer information: Name, FEIN, NAICS, governing class
- Payroll: Estimated payroll by class code and state
- Rating: Experience mod, schedule credits/debits
- Premium: Standard premium, modified premium

**Data Quality:**
- Completeness: >99% for required fields
- Class code accuracy: Validated at audit (88% match)
- Payroll accuracy: Estimated vs. audited variance tracked

---

**ClaimsVision WC - Workers Compensation Claims System**

**Description:** All WC claims from injury report through closure.

**Key Data Elements:**
- Claim identifiers: Claim number, policy number, state
- Injury information: Date of injury, nature of injury, body part, cause
- Claimant: Age, gender, occupation, wage
- Medical: Paid medical, medical reserves, treatment type
- Indemnity: Paid indemnity, indemnity reserves, benefit type
- Status: Open, closed, reopened

**Data Quality:**
- Injury coding: 94% accuracy (ICD-10 based)
- Body part coding: 96% accuracy
- Medical/indemnity split: 99% accurate

---

**AuditResults - Premium Audit System**

**Description:** Final audit results reconciling estimated to actual payroll.

**Key Data Elements:**
- Audit type: Physical, voluntary, phone, waived
- Payroll adjustments: By class code
- Classification changes: Reclassifications found
- Premium adjustments: Additional premium, return premium

**Use in Modeling:**
- Calibrate estimated payroll accuracy
- Identify systematic classification issues
- Adjust exposure basis for modeling

---

### 1.2 Bureau Data Sources

**NCCI Unit Statistical Data**

**Description:** Industry loss and premium data from NCCI.

**Key Data Elements:**
- Loss costs by class and state
- Development factors
- Trend factors
- Experience rating values

**Use:** Benchmark company experience, complement low-credibility segments

---

**State Bureau Data (Non-NCCI States)**

**Description:** Bureau data for independent bureau states.

**Key Bureaus:**
- California: WCIRB
- New York: NYCIRB
- Pennsylvania: PCRB
- Others: DE, IN, MA, MI, MN, NJ, NC, WI

**Data Elements:** Similar to NCCI but state-specific formats

---

### 1.3 Classification System

**NCCI Classification Codes:**
- Four-digit codes (e.g., 8810 = Clerical, 5183 = Plumbing)
- Governing class: Primary classification based on employer operations
- Standard exceptions: Clerical (8810), Outside Sales (8742)

**Classification Assignment:**
- Underwriter assigns at new business
- Premium auditor validates at audit
- Appeals process for disputes

**Classification Accuracy Tracking:**

| Metric | Target | Actual |
|--------|--------|--------|
| Audit class change rate | <15% | 12% |
| Class code match to governing | >90% | 88% |
| Exception class accuracy | >95% | 97% |

---

## Section 2: Exposure Basis

### 2.1 Payroll Exposure

**Primary Exposure: Payroll ($100s)**
```
Exposure = Audited_Payroll / 100

If audited payroll not available:
Exposure = Estimated_Payroll / 100 * Audit_Development_Factor
```

**Payroll by Class Code:**
- Each class code has separate payroll
- Standard exception payroll separated
- Overtime typically counted at straight-time rate

### 2.2 Estimated vs. Audited Payroll

**Audit Development Factor:**
```
Audit_Dev_Factor = Historical_Audited_Payroll / Historical_Estimated_Payroll

Typical values: 0.95 - 1.05 (varies by class and size)
```

**Application:**
- Apply to estimated payroll for exposure calculations
- Segment by class group and employer size
- Update annually based on audit experience

### 2.3 Multi-State Allocation

**For Multi-State Employers:**
- Allocate payroll to state of employment
- Use state-specific rates and loss costs
- Experience mod may differ by state

**Modeling Approach:**
- Model at state level where credible
- Pool small states for credibility
- Document allocation methodology

---

## Section 3: Medical Cost Modeling

### 3.1 Medical Cost Components

**Treatment Categories:**
- Hospital (inpatient, outpatient, emergency)
- Physician services
- Physical therapy
- Diagnostic (imaging, lab)
- Pharmacy
- Durable medical equipment

**Cost Drivers:**
- Fee schedules (state-specific)
- Utilization patterns
- Provider networks
- Treatment duration

### 3.2 Medical Severity Model

**Modeling Approach:**
```
Medical_Severity = f(Injury_Type, Body_Part, State, Claimant_Age, ...)

Distribution: Gamma (right-skewed, positive)
Link: Log
```

**Key Variables:**

| Variable | Description | Impact |
|----------|-------------|--------|
| Injury type | Nature of injury (fracture, strain, etc.) | High |
| Body part | Location of injury | High |
| State | Fee schedule, legal environment | Medium |
| Claimant age | Recovery time, complications | Medium |
| Treatment type | Surgery vs. conservative | High |

### 3.3 Medical Inflation

**Trend Components:**
- Fee schedule changes (state-specific)
- Utilization changes (procedure mix)
- Provider cost inflation

**Trend Analysis:**
```python
# Separate trend by component
hospital_trend = 0.04  # 4% annual
physician_trend = 0.03  # 3% annual
pharmacy_trend = 0.08  # 8% annual

# Weighted average based on cost mix
medical_trend = (0.40 * hospital_trend + 
                 0.35 * physician_trend + 
                 0.15 * pharmacy_trend +
                 0.10 * other_trend)
```

**Prospective Trend:**
- Apply trend from experience period midpoint to projection period
- Adjust for known fee schedule changes
- Document assumption basis

---

## Section 4: Indemnity and Duration Modeling

### 4.1 Indemnity Benefit Types

**Temporary Total Disability (TTD):**
- Weekly benefit = % of pre-injury wage (typically 66 2/3%)
- Subject to state maximum/minimum
- Duration: Until maximum medical improvement (MMI)

**Temporary Partial Disability (TPD):**
- Reduced benefit for partial return to work
- Based on wage loss
- Less common than TTD

**Permanent Partial Disability (PPD):**
- Scheduled: Specific body part (weeks x benefit)
- Unscheduled: Whole body impairment rating

**Permanent Total Disability (PTD):**
- Lifetime benefits (most states)
- COLA in some states
- Rare but high severity

### 4.2 Duration Modeling

**TTD Duration Model:**
```
Duration_Weeks = f(Injury_Type, Body_Part, Age, Occupation, ...)

Distribution: Negative binomial (count of weeks)
Link: Log
```

**Key Drivers:**
- Injury severity
- Job physical demands
- Age (longer recovery for older)
- Return-to-work programs
- Attorney involvement

### 4.3 Indemnity Severity Model

**Approach:**
```
Indemnity_Severity = Duration_Weeks * Weekly_Benefit

Or model directly:
Indemnity_Severity = f(Injury_Type, Body_Part, State, Wage, ...)
```

**State Benefit Level Adjustment:**
- Maximum weekly benefit varies by state
- COLA provisions in some states
- Update for benefit level changes

---

## Section 5: Loss Development and Reserving

### 5.1 Development Patterns

**Workers Compensation Tail:**
- Long-tail line (claims develop 10+ years)
- Medical tail longer than indemnity
- Reopened claims add development

**Development Factor Selection:**

| Maturity | Medical LDF | Indemnity LDF | Combined LDF |
|----------|-------------|---------------|--------------|
| 12-24 | 2.50 | 2.20 | 2.35 |
| 24-36 | 1.45 | 1.35 | 1.40 |
| 36-48 | 1.20 | 1.15 | 1.18 |
| 48-60 | 1.12 | 1.08 | 1.10 |
| 60-72 | 1.08 | 1.05 | 1.07 |
| 72-Ult | 1.15 | 1.08 | 1.12 |

**Tail Factor Methodology:**
- Exponential decay extrapolation
- Benchmark to NCCI industry factors
- Sensitivity test selected tail

### 5.2 Case Reserve Adequacy

**Reserve Review Process:**
- Initial reserve set at FNOL
- Revised as claim develops
- Large claims (>$100K) individually reviewed

**Adequacy Testing:**
```
Paid_to_Incurred_Ratio = Paid_Loss / Incurred_Loss

Expected pattern: Increases with maturity
Concern: Ratio flat or declining suggests case inadequacy
```

### 5.3 Reopened Claims

**Reopened Claim Definition:**
- Claim closed, then additional payments made
- Can occur years after original closure
- Common for medical-only reopen to indemnity

**Modeling Approach:**
- Track reopened claim frequency by closure age
- Include reopened provision in reserves
- Monitor reopened trend

---

## Section 6: Experience Rating

### 6.1 NCCI Experience Rating Plan

**Formula:**
```
Mod = (Ap + We * Ae + (1-We) * Ee + B) / (Ee + B)

Where:
Ap = Actual primary losses
Ae = Actual excess losses
Ee = Expected excess losses
We = Weighting factor (credibility)
B = Ballast factor
```

**Components:**
- Primary losses: Capped per-claim (emphasizes frequency)
- Excess losses: Above split point (large claim impact limited)
- Split point: State-specific ($15K-$20K typical)

### 6.2 Experience Rating in Modeling

**Off-Balance Adjustment:**
```
Expected_Mod_Distribution ≠ 1.00 (due to plan mechanics)

Off_Balance = (Sum of Premium-Weighted Mods) - 1.00

Typically: -2% to -5% (average mod < 1.00)
```

**Incorporating in Rate Analysis:**
- Adjust indicated rate for off-balance
- Segment analysis by mod tier
- Monitor mod distribution shifts

### 6.3 Schedule Rating

**Factors:**
- Management and supervision
- Safety programs and equipment
- Training
- Claims management
- Financial stability

**Documentation:**
- Maximum credit/debit: Typically ±25%
- Justify credits with specific criteria
- Track schedule credit correlation with loss experience

---

## Section 7: Model Validation and Monitoring

### 7.1 Validation Framework

**Medical Severity Model:**
- Holdout testing (most recent year)
- Actual vs. expected by injury type
- State-level validation

**Indemnity Duration Model:**
- Kaplan-Meier survival analysis
- Validation against closed claims
- Segment by injury type

**Frequency Model:**
- AUC on claim occurrence
- Actual vs. expected by class group
- Territory validation

### 7.2 Monitoring Standards

**Monthly:**
- Claim counts vs. expected
- Reported loss vs. expected
- Medical vs. indemnity split

**Quarterly:**
- Development factor emergence
- Experience mod distribution
- Large loss tracking

**Annually:**
- Full model re-validation
- Loss cost comparison to NCCI
- Trend assumption review

### 7.3 Alert Thresholds

| Metric | Yellow | Orange | Red |
|--------|--------|--------|-----|
| Frequency A/E | 1.05-1.10 | 1.10-1.15 | >1.15 |
| Medical severity trend | +8-10% | +10-15% | >+15% |
| Development emergence | 5-10% | 10-15% | >15% |

---

## Section 8: State-Specific Considerations

### 8.1 Benefit Level Summary

**Sample State Maximums (2024):**

| State | Max Weekly TTD | Waiting Period | Retro Period |
|-------|----------------|----------------|--------------|
| CA | $1,620 | 3 days | 14 days |
| TX | $1,111 | 7 days | 28 days |
| FL | $1,197 | 7 days | 21 days |
| NY | $1,145 | 7 days | 14 days |
| PA | $1,273 | 7 days | 14 days |

### 8.2 Fee Schedule Impact

**States with Fee Schedules:**
- Most states have medical fee schedules
- Based on Medicare or state-developed
- Updates vary (annual, biennial)

**States without Fee Schedules:**
- Small number of states
- Higher medical costs
- Usual and customary charges

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
