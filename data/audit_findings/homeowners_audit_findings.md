---
title: "Homeowners Insurance - Common Audit Findings"
portfolio: "homeowners"
type: "audit_findings"
company: "ABC Insurance Company"
version: "1.0"
effective_date: "2024-01-01"
---

# Homeowners Insurance - Common Audit Findings

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes.

---

## Purpose

This document catalogs common audit findings and regulatory examination issues specific to homeowners insurance model documentation. Homeowners models face unique challenges around catastrophe modeling, property valuation, and geographic risk that require specialized documentation approaches.

---

## Category 1: Catastrophe Modeling

### Finding HO-CAT-001: Third-Party CAT Model Not Validated
**Severity:** CRITICAL
**Frequency:** Common

**Issue:** Documentation relies on third-party catastrophe model (AIR, RMS, CoreLogic) outputs without independent validation or sensitivity testing.

**Typical Citation:** "Model uses AIR hurricane loss estimates but documentation does not show any validation of AIR outputs against company historical experience."

**Remediation:**
- Compare CAT model outputs to historical company losses
- Document variance between modeled and actual for past events
- Show sensitivity to key CAT model assumptions
- Include CAT model version and vintage used
- Document any adjustments made to CAT model outputs

---

### Finding HO-CAT-002: CAT Model Blending Not Documented
**Severity:** HIGH
**Frequency:** Common

**Issue:** Multiple CAT models used but blending methodology not explained or justified.

**Typical Citation:** "Documentation states 'blended CAT model output' is used but does not explain whether AIR, RMS, and CoreLogic were weighted equally or based on historical performance."

**Remediation:**
- Document which CAT models are used
- Explain blending methodology (equal weight, performance-based, etc.)
- Justify blending approach with analysis
- Show sensitivity of results to different blending weights

---

### Finding HO-CAT-003: Non-Modeled CAT Perils Insufficiently Addressed
**Severity:** HIGH
**Frequency:** Very Common

**Issue:** Documentation focuses on hurricane/earthquake but does not adequately address convective storm (tornado, hail), wildfire, or flood risk.

**Typical Citation:** "Hurricane losses are modeled using AIR, but hail and tornado losses are estimated using simple trend factors without documentation of methodology."

**Remediation:**
- Document methodology for each peril separately
- Include non-modeled peril load calculations
- Show historical analysis supporting non-modeled peril estimates
- Address emerging perils (wildfire, convective storm trends)

---

### Finding HO-CAT-004: Demand Surge Not Incorporated
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** CAT loss estimates do not account for post-event demand surge (increased labor/material costs after major events).

**Typical Citation:** "Loss estimates assume normal construction costs but do not include demand surge factor for major hurricane scenarios."

**Remediation:**
- Document demand surge assumptions
- Include demand surge factors by event size
- Reference industry studies or company experience
- Show impact on modeled losses

---

## Category 2: Property Valuation and Exposure

### Finding HO-EXP-001: Replacement Cost Methodology Not Documented
**Severity:** HIGH
**Frequency:** Common

**Issue:** Model uses Coverage A (dwelling) limits but does not document how replacement cost estimates were validated.

**Typical Citation:** "Exposure basis uses Coverage A limits, but documentation does not explain whether limits reflect actual replacement costs or show validation against recent claims."

**Remediation:**
- Document replacement cost estimation methodology
- Compare Coverage A limits to actual claim settlement ratios
- Address insurance-to-value (ITV) concerns
- Include ITV distribution analysis

---

### Finding HO-EXP-002: Construction Type Classification Inaccurate
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Construction type (frame, masonry, etc.) data quality issues not addressed, affecting vulnerability assumptions.

**Typical Citation:** "Model uses construction type from policy system, but no validation shows whether policyholder-reported construction type matches actual property characteristics."

**Remediation:**
- Document construction type data source and quality
- Include validation studies (inspections, aerial imagery)
- Show sensitivity of results to construction type misclassification
- Address remediation for data quality issues

---

### Finding HO-EXP-003: Roof Age and Condition Not Considered
**Severity:** MEDIUM
**Frequency:** Very Common

**Issue:** Wind/hail vulnerability does not adequately incorporate roof age, material, or condition.

**Typical Citation:** "Wind model applies same vulnerability to 5-year-old and 25-year-old roofs despite materially different damage susceptibility."

**Remediation:**
- Document roof age data availability and quality
- Include roof age/condition in vulnerability functions
- Show analysis supporting roof age adjustments
- Address data limitations and future improvements

---

## Category 3: Geographic Risk and Territory

### Finding HO-GEO-001: Territory Definition Not Justified
**Severity:** HIGH
**Frequency:** Common

**Issue:** Territory boundaries defined without documentation of analytical basis or credibility considerations.

**Typical Citation:** "Documentation shows 25 territories but does not explain how boundaries were determined or whether territories have sufficient credibility."

**Remediation:**
- Document territory development methodology
- Show credibility analysis by territory
- Include geographic risk factor analysis (distance to coast, elevation, etc.)
- Justify territory granularity decisions

---

### Finding HO-GEO-002: Protection Class Not Validated
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Fire protection class (ISO PPC) used without validation against company fire loss experience.

**Typical Citation:** "Model applies protection class relativities from ISO without analysis showing these align with company's actual fire loss experience by protection class."

**Remediation:**
- Validate protection class relativities against company data
- Document any adjustments to standard ISO factors
- Show credibility of company experience by protection class
- Address rural/suburban protection class data issues

---

### Finding HO-GEO-003: Coastal Exposure Definition Inconsistent
**Severity:** HIGH
**Frequency:** Occasional

**Issue:** "Coastal" zone definition varies across analyses within same documentation.

**Typical Citation:** "Hurricane deductible applies within 'coastal zone' but this is defined differently in the rating section vs. the reinsurance section."

**Remediation:**
- Define coastal zones consistently throughout documentation
- Document distance-to-coast methodology
- Include coastal zone maps as appendices
- Reconcile any necessary differences with explanation

---

## Category 4: Non-CAT Perils

### Finding HO-NC-001: Water Damage Trend Not Addressed
**Severity:** MEDIUM
**Frequency:** Very Common

**Issue:** Water damage (non-weather) losses trending adversely but model does not incorporate trend or address root causes.

**Typical Citation:** "Water damage frequency increased 8% annually 2019-2023, but model documentation does not address this trend or its drivers."

**Remediation:**
- Document water damage loss trends
- Analyze drivers (aging infrastructure, appliance failures, etc.)
- Include trend assumptions in loss projections
- Address underwriting or mitigation implications

---

### Finding HO-NC-002: Liability Coverage Modeling Insufficient
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Homeowners liability (Coverage E) modeled superficially compared to property coverages.

**Typical Citation:** "Property coverages have detailed frequency/severity models, but liability coverage uses flat per-policy load without actuarial analysis."

**Remediation:**
- Document liability loss experience separately
- Include liability frequency and severity analysis
- Address liability trend and social inflation
- Show liability modeling methodology

---

## Category 5: Regulatory and Compliance

### Finding HO-RC-001: State-Specific CAT Requirements Not Addressed
**Severity:** CRITICAL
**Frequency:** Occasional

**Issue:** Documentation does not address state-specific catastrophe modeling requirements (e.g., Florida Commission on Hurricane Loss Projection Methodology).

**Typical Citation:** "Florida filing rejected because hurricane model not approved by Florida Commission; documentation did not address Commission requirements."

**Remediation:**
- Document state-specific CAT modeling requirements
- Ensure CAT models used are state-approved where required
- Include state approval status for each CAT model
- Address any state-specific methodology constraints

---

### Finding HO-RC-002: Inflation Guard Not Documented
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Automatic inflation increases to Coverage A limits not incorporated in exposure projections.

**Typical Citation:** "Exposure projections assume static Coverage A limits but policies include 4% annual inflation guard, overstating rate need."

**Remediation:**
- Document inflation guard provisions
- Include inflation guard in exposure projections
- Show impact of inflation guard on rate adequacy
- Address policyholder notification requirements

---

## Quick Reference Checklist

Before submitting homeowners model documentation, verify:

- [ ] Third-party CAT model outputs validated against company experience
- [ ] CAT model blending methodology documented and justified
- [ ] Non-modeled perils (hail, tornado, wildfire) adequately addressed
- [ ] Demand surge assumptions documented
- [ ] Replacement cost / ITV validated
- [ ] Roof age and condition incorporated or limitation documented
- [ ] Territory definitions justified with credibility analysis
- [ ] State-specific CAT requirements addressed (Florida, etc.)
- [ ] Water damage trends analyzed and incorporated
- [ ] Coastal zone definitions consistent throughout

---

**Document Control**
- Version: 1.0
- Last Updated: January 2024
- Owner: Model Risk Governance Committee
- Next Review: January 2025
