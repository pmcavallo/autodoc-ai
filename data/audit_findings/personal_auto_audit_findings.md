---
title: "Personal Auto Insurance - Common Audit Findings"
portfolio: "personal_auto"
type: "audit_findings"
company: "ABC Insurance Company"
version: "1.0"
effective_date: "2024-01-01"
---

# Personal Auto Insurance - Common Audit Findings

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes.

---

## Purpose

This document catalogs common audit findings and regulatory examination issues identified in personal auto insurance model documentation. Model developers should review these findings and ensure new documentation addresses each area proactively.

---

## Category 1: Data Quality and Documentation

### Finding PA-DQ-001: Incomplete Data Lineage Documentation
**Severity:** HIGH
**Frequency:** Common

**Issue:** Model documentation fails to trace data from source systems through transformations to final model inputs. Auditors cannot verify data integrity.

**Typical Citation:** "Documentation does not clearly identify the source system for driver violation data or explain how violation counts were aggregated."

**Remediation:**
- Document all source systems with extraction dates
- Include transformation logic (SQL, Python) or pseudocode
- Show record counts at each transformation step
- Include data quality metrics (completeness, accuracy)

---

### Finding PA-DQ-002: Missing Data Treatment Not Documented
**Severity:** MEDIUM
**Frequency:** Very Common

**Issue:** Documentation does not explain how missing values were handled for key variables like annual mileage, insurance score, or driver age.

**Typical Citation:** "The model uses insurance_score as a predictor, but documentation does not explain treatment of the 4.2% of policies with no credit hit."

**Remediation:**
- Document missing rates for all variables
- Explain imputation method used (mean, median, model-based)
- Include missing indicator variables where appropriate
- Assess impact of missingness on model performance

---

### Finding PA-DQ-003: Outlier Treatment Insufficiently Justified
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Documentation mentions winsorization or capping but does not justify the chosen thresholds or assess impact.

**Typical Citation:** "Vehicle value was capped at the 99th percentile, but no analysis shows why this threshold was chosen over 95th or 99.5th percentile."

**Remediation:**
- Document outlier detection methodology
- Justify threshold selection with analysis
- Show sensitivity of model results to different thresholds
- Assess actuarial reasonableness of treatment

---

## Category 2: Methodology and Model Development

### Finding PA-MD-001: Variable Selection Process Not Documented
**Severity:** HIGH
**Frequency:** Common

**Issue:** Final model includes variables without documenting the selection process, including variables considered but rejected.

**Typical Citation:** "Documentation shows 12 final variables but does not explain why vehicle color or occupation were excluded from consideration."

**Remediation:**
- Document initial variable pool (all candidates)
- Show univariate analysis results
- Explain selection criteria (statistical, actuarial, regulatory)
- Document variables rejected and reasons

---

### Finding PA-MD-002: Interaction Terms Not Tested or Documented
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Model assumes no interactions between variables without testing, or includes interactions without justification.

**Typical Citation:** "Young driver × sports car interaction is known actuarially but model documentation does not show whether this was tested."

**Remediation:**
- Test key actuarially-motivated interactions
- Document statistical significance of tested interactions
- Justify inclusion or exclusion decisions
- Show impact on model performance

---

### Finding PA-MD-003: Model Assumptions Not Validated
**Severity:** HIGH
**Frequency:** Common

**Issue:** GLM assumptions (distribution, link function, independence) stated but not validated with diagnostic tests.

**Typical Citation:** "Model assumes Poisson distribution but no overdispersion test results are provided. Variance-to-mean ratio not documented."

**Remediation:**
- Test distributional assumptions (Q-Q plots, goodness-of-fit)
- Check for overdispersion (Pearson chi-square / df)
- Validate linearity assumptions (partial residual plots)
- Document any assumption violations and remediation

---

## Category 3: Validation and Performance

### Finding PA-VP-001: Holdout Set Contamination
**Severity:** CRITICAL
**Frequency:** Occasional

**Issue:** Holdout set was used during model development for decisions other than final evaluation, compromising independence.

**Typical Citation:** "Documentation indicates variable selection was finalized after reviewing holdout set performance, invalidating the holdout test."

**Remediation:**
- Use three-way split: train, validation, holdout
- Document that holdout was truly held out until final evaluation
- If contaminated, acknowledge limitation and consider additional testing

---

### Finding PA-VP-002: Insufficient Segment-Level Validation
**Severity:** MEDIUM
**Frequency:** Very Common

**Issue:** Overall model performance is strong, but documentation does not show performance by key segments (territory, age band, vehicle type).

**Typical Citation:** "Model AUC is 0.72 overall, but no segment-level analysis shows whether performance is consistent across territories or age groups."

**Remediation:**
- Show actual vs. expected by key segments
- Calculate segment-level discrimination metrics
- Identify any segments with material underperformance
- Document remediation for underperforming segments

---

### Finding PA-VP-003: Calibration Testing Incomplete
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Model discrimination (AUC, Gini) documented but calibration (actual vs. predicted alignment) not shown.

**Typical Citation:** "Documentation shows strong AUC but does not include lift charts, actual vs. expected by decile, or Hosmer-Lemeshow test results."

**Remediation:**
- Include actual vs. expected by decile (table and chart)
- Calculate and report calibration metrics
- Show lift chart with confidence intervals
- Address any systematic over/under prediction

---

## Category 4: Regulatory Compliance

### Finding PA-RC-001: ASOP Compliance Not Explicitly Addressed
**Severity:** HIGH
**Frequency:** Common

**Issue:** Documentation does not explicitly map to ASOP requirements (12, 23, 41, 56) or state how each standard is satisfied.

**Typical Citation:** "Documentation references ASOPs in general terms but does not demonstrate specific compliance with ASOP 56 modeling requirements."

**Remediation:**
- Include explicit ASOP compliance section
- Map documentation sections to specific ASOP requirements
- Address limitations disclosure per ASOP 41
- Document reliance on others per ASOP 41

---

### Finding PA-RC-002: Rate Filing Support Insufficient
**Severity:** HIGH
**Frequency:** Occasional

**Issue:** Documentation does not provide sufficient detail for state insurance department rate filing review.

**Typical Citation:** "Rate filing was delayed because model documentation did not include coefficient tables in format required by [State] DOI."

**Remediation:**
- Include full coefficient tables with standard errors
- Provide rate relativities in regulatory format
- Show impact analysis by state/territory
- Include regulatory-specific exhibits as appendices

---

### Finding PA-RC-003: Protected Class Analysis Missing
**Severity:** CRITICAL
**Frequency:** Occasional

**Issue:** Documentation does not demonstrate that model does not unfairly discriminate based on protected characteristics.

**Typical Citation:** "No analysis shows whether territory variable serves as proxy for race or ethnicity in violation of fair lending principles."

**Remediation:**
- Conduct disparate impact analysis
- Test for proxy discrimination
- Document actuarial justification for all variables
- Include fair lending compliance attestation

---

## Category 5: Governance and Monitoring

### Finding PA-GM-001: Monitoring Plan Not Specific
**Severity:** MEDIUM
**Frequency:** Very Common

**Issue:** Documentation mentions ongoing monitoring but does not specify metrics, thresholds, frequency, or responsible parties.

**Typical Citation:** "Documentation states model will be monitored quarterly but does not define what metrics will be tracked or what triggers remediation."

**Remediation:**
- Define specific monitoring metrics with thresholds
- Establish alert levels (yellow, orange, red)
- Assign responsibility for monitoring activities
- Document escalation procedures

---

### Finding PA-GM-002: Model Change Log Not Maintained
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Documentation does not include version history or explain changes from prior model version.

**Typical Citation:** "This is version 2.0 of the frequency model, but documentation does not explain what changed from version 1.0 or why."

**Remediation:**
- Include comprehensive version history
- Document all changes from prior version
- Explain rationale for changes
- Show performance comparison to prior version

---

## Quick Reference Checklist

Before submitting model documentation, verify:

- [ ] Data lineage fully documented from source to model input
- [ ] Missing data treatment explained with rates and methods
- [ ] Variable selection process documented with rejected variables
- [ ] Model assumptions tested and validated
- [ ] Holdout set truly independent (not used for development decisions)
- [ ] Segment-level validation included
- [ ] ASOP compliance explicitly addressed
- [ ] Monitoring plan specific with metrics and thresholds
- [ ] Version history and changes documented
- [ ] Protected class / fair lending analysis included

---

**Document Control**
- Version: 1.0
- Last Updated: January 2024
- Owner: Model Risk Governance Committee
- Next Review: January 2025
