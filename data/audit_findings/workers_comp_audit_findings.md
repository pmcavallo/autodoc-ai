---
title: "Workers Compensation Insurance - Common Audit Findings"
portfolio: "workers_comp"
type: "audit_findings"
company: "ABC Insurance Company"
version: "1.0"
effective_date: "2024-01-01"
---

# Workers Compensation Insurance - Common Audit Findings

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes.

---

## Purpose

This document catalogs common audit findings and regulatory examination issues specific to workers compensation insurance model documentation. Workers comp models face unique challenges around injury classification, medical cost inflation, experience rating, and state-specific bureau requirements.

---

## Category 1: Classification and Exposure

### Finding WC-CL-001: NCCI Classification Code Accuracy Not Validated
**Severity:** HIGH
**Frequency:** Very Common

**Issue:** Model uses NCCI or state bureau classification codes without validation of accuracy or analysis of misclassification impact.

**Typical Citation:** "Model uses governing class code from policy system, but audit data shows 12% of policies had class code corrections at audit, indicating systematic misclassification."

**Remediation:**
- Document classification code data source and quality
- Analyze audit adjustment patterns by class code
- Show impact of misclassification on model accuracy
- Include class code validation procedures
- Address premium audit adjustment factors

---

### Finding WC-CL-002: Payroll Exposure Not Validated Against Audits
**Severity:** HIGH
**Frequency:** Common

**Issue:** Estimated payroll used as exposure basis without reconciliation to audited payroll.

**Typical Citation:** "Model uses estimated payroll from policy inception, but no analysis shows relationship between estimated and audited payroll by class code."

**Remediation:**
- Compare estimated to audited payroll by class
- Document audit development patterns
- Include payroll audit adjustment factors
- Show exposure basis validation methodology

---

### Finding WC-CL-003: Multi-State Employer Exposure Allocation Not Documented
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** For multi-state employers, methodology for allocating exposure to states not documented.

**Typical Citation:** "National accounts have employees in multiple states, but documentation does not explain how exposure was allocated for modeling purposes."

**Remediation:**
- Document multi-state allocation methodology
- Show validation of allocation approach
- Address interstate compact considerations
- Include state-specific exposure calculations

---

## Category 2: Medical Cost Modeling

### Finding WC-MC-001: Medical Inflation Assumptions Not Justified
**Severity:** HIGH
**Frequency:** Very Common

**Issue:** Medical cost trend assumptions stated without supporting analysis or comparison to industry benchmarks.

**Typical Citation:** "Model assumes 6% annual medical inflation, but documentation does not show analysis supporting this assumption or comparison to NCCI medical benchmarks."

**Remediation:**
- Document medical trend analysis methodology
- Compare assumptions to NCCI and industry data
- Show historical medical trend by injury type
- Address medical fee schedule impacts by state
- Include sensitivity analysis for trend assumptions

---

### Finding WC-MC-002: Medical Fee Schedule Impacts Not Addressed
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** State-specific medical fee schedules not incorporated in severity projections.

**Typical Citation:** "Severity model uses average costs but does not reflect that State X recently reduced fee schedules by 15%, affecting future claim costs."

**Remediation:**
- Document fee schedule assumptions by state
- Include recent and pending fee schedule changes
- Show impact of fee schedule changes on projections
- Address states without fee schedules separately

---

### Finding WC-MC-003: Pharmacy Cost Trend Not Separately Modeled
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Pharmacy costs bundled with other medical without separate trend analysis.

**Typical Citation:** "Medical costs include pharmacy, but pharmacy costs are trending at 12% annually vs. 5% for other medical; combined analysis masks this divergence."

**Remediation:**
- Analyze pharmacy costs separately
- Document pharmacy trend methodology
- Address formulary and PBM impacts
- Include pharmacy as separate cost component

---

## Category 3: Indemnity and Duration

### Finding WC-ID-001: Duration Analysis Insufficient
**Severity:** HIGH
**Frequency:** Common

**Issue:** Model predicts total indemnity cost but does not separately analyze claim duration (weeks of disability).

**Typical Citation:** "Indemnity severity modeled as total cost, but no analysis of duration vs. weekly benefit enables validation against return-to-work data."

**Remediation:**
- Model duration (weeks) separately from weekly benefit
- Document duration analysis by injury type
- Include return-to-work assumptions
- Validate against actual duration data

---

### Finding WC-ID-002: Benefit Level Changes Not Incorporated
**Severity:** HIGH
**Frequency:** Occasional

**Issue:** State benefit level changes (maximum weekly benefit, COLA) not reflected in projections.

**Typical Citation:** "State X increased maximum weekly benefit by 8% effective January 1, but indemnity projections do not reflect this change."

**Remediation:**
- Document benefit levels by state
- Include scheduled benefit changes
- Show impact of benefit changes on projections
- Address COLA adjustments where applicable

---

### Finding WC-ID-003: Permanent Partial Disability Not Adequately Modeled
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** PPD claims modeled with inadequate granularity, missing impairment rating distributions.

**Typical Citation:** "PPD claims modeled as average severity without impairment rating distribution, despite significant variation from 5% to 50% impairment ratings."

**Remediation:**
- Analyze PPD by impairment rating band
- Document impairment rating distribution by injury type
- Include state-specific PPD schedules
- Show PPD severity by body part

---

## Category 4: Loss Development and Reserving

### Finding WC-LD-001: Tail Development Not Adequately Addressed
**Severity:** CRITICAL
**Frequency:** Common

**Issue:** Loss development patterns truncated without adequate tail factor analysis.

**Typical Citation:** "Development factors shown through 10 years, but workers comp claims can develop beyond 20 years; no tail factor methodology documented."

**Remediation:**
- Document tail factor methodology
- Show analysis supporting tail assumptions
- Compare to industry tail factors
- Address specific tail issues (medical inflation, reopened claims)

---

### Finding WC-LD-002: Case Reserve Adequacy Not Validated
**Severity:** HIGH
**Frequency:** Common

**Issue:** Model relies on case reserves without validation of reserve adequacy.

**Typical Citation:** "Loss development uses incurred (paid + case reserve) but no analysis validates whether case reserves are adequate; systematic under-reserving would bias results."

**Remediation:**
- Analyze paid-to-incurred ratios by maturity
- Document case reserving practices
- Show case reserve development patterns
- Validate reserve adequacy by claim type

---

### Finding WC-LD-003: Reopened Claims Not Separately Analyzed
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Reopened claims bundled with original claims without separate analysis.

**Typical Citation:** "Claims can reopen years after closure, but model does not separately analyze reopened claim frequency or timing."

**Remediation:**
- Analyze reopened claim frequency by closure age
- Document reopened claim severity patterns
- Include reopened claim provisions in projections
- Show reopened claim trends over time

---

## Category 5: Experience Rating and Large Loss

### Finding WC-ER-001: Experience Modification Impact Not Documented
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Model does not document how experience rating affects loss projections and rate adequacy.

**Typical Citation:** "Loss projections do not adjust for experience modification credits/debits, potentially overstating loss expectations for accounts with favorable experience mods."

**Remediation:**
- Document experience modification distribution
- Show impact of experience rating on expected losses
- Address off-balance in experience rating plan
- Include mod distribution by class/industry

---

### Finding WC-ER-002: Large Loss Loading Not Adequately Documented
**Severity:** HIGH
**Frequency:** Common

**Issue:** Large loss / excess loading methodology not documented or validated.

**Typical Citation:** "Rate includes 15% large loss load but documentation does not show analysis supporting this load or threshold selection."

**Remediation:**
- Document large loss threshold selection
- Show large loss experience by threshold
- Validate large loss frequency and severity
- Address shock loss potential

---

## Category 6: State-Specific Requirements

### Finding WC-ST-001: Monopolistic State Requirements Not Addressed
**Severity:** HIGH (if applicable)
**Frequency:** Occasional

**Issue:** Documentation does not address monopolistic state fund requirements (OH, WA, WY, ND).

**Typical Citation:** "Company writes employers with Ohio operations, but model does not address that Ohio is a monopolistic state with separate requirements."

**Remediation:**
- Identify monopolistic states in operating territory
- Document monopolistic state treatment
- Address employers with multi-state operations
- Include state fund assessment obligations

---

### Finding WC-ST-002: NCCI vs. Independent Bureau States Not Distinguished
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Model treats all states identically without addressing NCCI vs. independent bureau (CA, DE, IN, MA, MI, MN, NJ, NY, NC, PA, WI) differences.

**Typical Citation:** "Loss costs from NCCI states applied to California, but California is an independent bureau state with different classification and rating structures."

**Remediation:**
- Distinguish NCCI from independent bureau states
- Document state-specific rating structures
- Address class code mapping between bureaus
- Show state-specific loss cost adjustments

---

## Quick Reference Checklist

Before submitting workers compensation model documentation, verify:

- [ ] NCCI/bureau classification codes validated against audit data
- [ ] Payroll exposure reconciled to audited payroll
- [ ] Medical inflation assumptions justified with benchmark comparison
- [ ] Fee schedule impacts by state incorporated
- [ ] Indemnity duration modeled separately from weekly benefit
- [ ] Benefit level changes incorporated
- [ ] Tail development factors documented and justified
- [ ] Case reserve adequacy validated
- [ ] Large loss loading methodology documented
- [ ] Monopolistic and independent bureau states addressed
- [ ] Experience modification impact documented

---

**Document Control**
- Version: 1.0
- Last Updated: January 2024
- Owner: Model Risk Governance Committee
- Next Review: January 2025
