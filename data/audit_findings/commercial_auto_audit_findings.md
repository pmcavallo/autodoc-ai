---
title: "Commercial Auto Insurance - Common Audit Findings"
portfolio: "commercial_auto"
type: "audit_findings"
company: "ABC Insurance Company"
version: "1.0"
effective_date: "2024-01-01"
---

# Commercial Auto Insurance - Common Audit Findings

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes.

---

## Purpose

This document catalogs common audit findings and regulatory examination issues specific to commercial auto insurance model documentation. Commercial auto models face unique challenges around fleet composition, driver turnover, vehicle classification, and large loss exposure.

---

## Category 1: Fleet and Exposure

### Finding CA-FL-001: Fleet Size Classification Not Validated
**Severity:** HIGH
**Frequency:** Very Common

**Issue:** Fleet size tiers (1-5 vehicles, 6-25 vehicles, etc.) used without validation of actual vehicle counts against policy data.

**Typical Citation:** "Model uses fleet size tier from application, but comparison to symbol schedule shows 15% of fleets have more vehicles than reported tier implies."

**Remediation:**
- Validate fleet size against vehicle schedule
- Document fleet size data quality issues
- Show impact of fleet size misclassification
- Include audit procedures for fleet counts

---

### Finding CA-FL-002: Vehicle Classification Codes Not Validated
**Severity:** HIGH
**Frequency:** Common

**Issue:** ISO vehicle classification codes (size, use, radius) used without validation against actual vehicle characteristics.

**Typical Citation:** "Model uses ISO class codes from policy, but audit reveals 20% of trucks underclassified by weight (light vs. medium duty)."

**Remediation:**
- Document vehicle classification methodology
- Validate class codes against VIN decoding
- Show impact of misclassification on loss experience
- Address GVW/GVWR determination

---

### Finding CA-FL-003: Radius of Operation Not Verified
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Radius of operation (local, intermediate, long-haul) based on insured representation without verification.

**Typical Citation:** "Radius factor assumes 'local' operation for 60% of fleets, but telematics data suggests many operate beyond 50-mile radius."

**Remediation:**
- Document radius determination methodology
- Validate against available telematics or ELD data
- Show loss experience by actual vs. rated radius
- Address misrepresentation detection

---

## Category 2: Driver Risk

### Finding CA-DR-001: Driver Turnover Impact Not Modeled
**Severity:** HIGH
**Frequency:** Common

**Issue:** Model does not account for driver turnover within policy period, affecting driver quality assumptions.

**Typical Citation:** "Driver list from policy inception used for driver factor, but fleets with 80% annual turnover have materially different driver quality by end of term."

**Remediation:**
- Document driver turnover assumptions
- Analyze loss experience by turnover rate
- Include driver turnover as rating variable
- Address mid-term driver changes

---

### Finding CA-DR-002: MVR Data Quality Not Documented
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Motor vehicle record (MVR) data used for driver scoring without documentation of data quality or refresh frequency.

**Typical Citation:** "Driver surcharges based on MVR violations, but no analysis shows whether MVRs are refreshed during policy period or at renewal only."

**Remediation:**
- Document MVR data source and refresh frequency
- Show MVR match rates and data quality metrics
- Address out-of-state license issues
- Include MVR validation procedures

---

### Finding CA-DR-003: Driver Experience Definition Inconsistent
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** "Driver experience" defined inconsistently across analyses (years licensed vs. years commercial driving).

**Typical Citation:** "Driver experience factor uses years since license issuance, but for commercial drivers, years of CDL experience is more relevant."

**Remediation:**
- Define driver experience consistently
- Document data source for experience (license date vs. CDL date)
- Validate experience factor against loss experience
- Address non-CDL vs. CDL driver differences

---

## Category 3: Coverage and Liability

### Finding CA-CV-001: Hired and Non-Owned Auto Not Separately Modeled
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Hired and non-owned auto (HNOA) exposure bundled with owned auto without separate analysis.

**Typical Citation:** "HNOA premium included in total, but model does not separately analyze HNOA exposure or loss experience."

**Remediation:**
- Analyze HNOA exposure and losses separately
- Document HNOA rating methodology
- Show HNOA loss frequency and severity
- Address HNOA exposure measurement challenges

---

### Finding CA-CV-002: Split Limits vs. CSL Not Adequately Addressed
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Model does not properly address difference between split limit and combined single limit (CSL) policies.

**Typical Citation:** "Loss experience includes both split limit and CSL policies, but ILFs applied assume split limit structure."

**Remediation:**
- Document limit structure distribution
- Develop separate ILFs for split vs. CSL
- Show methodology for combining experience
- Address limit selection anti-selection

---

### Finding CA-CV-003: Motor Carrier Filing Requirements Not Addressed
**Severity:** HIGH
**Frequency:** Occasional

**Issue:** For-hire carriers subject to MCS-90 and BMC-91 filing requirements, affecting minimum limits and cancellation.

**Typical Citation:** "Model includes for-hire trucking but does not address MCS-90 endorsement requirements or impact on claims handling."

**Remediation:**
- Identify for-hire vs. private carrier exposure
- Document filing requirement impacts
- Address minimum limit requirements by carrier type
- Include MCS-90 cancellation restrictions

---

## Category 4: Loss Experience and Development

### Finding CA-LE-001: Large Loss Treatment Not Consistent
**Severity:** HIGH
**Frequency:** Common

**Issue:** Large loss treatment varies across analyses without consistent methodology.

**Typical Citation:** "Frequency analysis caps losses at $250K, but severity analysis uses $500K cap; inconsistent treatment affects loss cost estimates."

**Remediation:**
- Document large loss threshold selection
- Apply consistent treatment across analyses
- Show sensitivity to large loss threshold
- Validate excess/large loss loading

---

### Finding CA-LE-002: Cargo/Physical Damage vs. Liability Not Distinguished
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Model combines liability and physical damage experience without distinguishing coverage characteristics.

**Typical Citation:** "Combined loss ratio used, but physical damage (shorter tail) and liability (longer tail) have materially different development patterns."

**Remediation:**
- Analyze liability and physical damage separately
- Document development patterns by coverage
- Show loss cost breakdown by coverage
- Address coverage-specific trends

---

### Finding CA-LE-003: Subrogation Not Properly Credited
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Subrogation recoveries not consistently credited in loss experience.

**Typical Citation:** "Physical damage losses shown gross of subrogation, but subrogation recovery rates vary significantly by vehicle type and are not documented."

**Remediation:**
- Document subrogation treatment
- Show subrogation recovery rates by coverage/segment
- Develop net loss costs where appropriate
- Address timing of subrogation recoveries

---

## Category 5: Industry and Class

### Finding CA-IN-001: Industry Classification Not Validated
**Severity:** HIGH
**Frequency:** Common

**Issue:** Industry classification (SIC/NAICS) used without validation against actual business operations.

**Typical Citation:** "Model uses NAICS code from application, but 18% of accounts have primary operations different from coded industry."

**Remediation:**
- Document industry classification methodology
- Validate against business descriptions and audits
- Show loss experience by industry classification
- Address multi-industry operations

---

### Finding CA-IN-002: Business Use Classification Subjective
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Business use categories (service, retail, contractor, etc.) assigned subjectively without consistent definitions.

**Typical Citation:** "Business use factor varies significantly, but documentation does not provide clear definitions distinguishing 'service' from 'contractor' use."

**Remediation:**
- Provide clear business use definitions
- Document classification decision rules
- Validate classification against loss experience
- Train underwriters on consistent classification

---

## Category 6: Experience Rating

### Finding CA-ER-001: Experience Modification Methodology Not Documented
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Experience rating plan mechanics not documented, making it difficult to assess impact on rate adequacy.

**Typical Citation:** "Experience modifications range from 0.70 to 1.50, but documentation does not explain how mods are calculated or their expected off-balance."

**Remediation:**
- Document experience rating plan formula
- Show experience mod distribution
- Calculate expected off-balance
- Analyze mod predictive power

---

### Finding CA-ER-002: Schedule Rating Credits Not Analyzed
**Severity:** MEDIUM
**Frequency:** Common

**Issue:** Schedule rating credits/debits applied without analysis of whether they correlate with actual loss experience.

**Typical Citation:** "Average schedule credit is 15%, but no analysis shows whether accounts receiving credits have better-than-average loss experience."

**Remediation:**
- Analyze schedule credit correlation with loss experience
- Document schedule rating criteria
- Show distribution of schedule modifications
- Validate underwriter consistency

---

## Quick Reference Checklist

Before submitting commercial auto model documentation, verify:

- [ ] Fleet size validated against vehicle schedules
- [ ] Vehicle classification codes validated against VIN data
- [ ] Driver turnover impact analyzed and documented
- [ ] MVR data quality and refresh frequency documented
- [ ] HNOA exposure analyzed separately
- [ ] Large loss treatment consistent across analyses
- [ ] Liability vs. physical damage analyzed separately
- [ ] Industry classification validated
- [ ] Experience modification methodology documented
- [ ] For-hire carrier filing requirements addressed (if applicable)

---

**Document Control**
- Version: 1.0
- Last Updated: January 2024
- Owner: Model Risk Governance Committee
- Next Review: January 2025
