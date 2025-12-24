---
title: "Regulatory and Professional Standards Compilation"
type: "regulatory_reference"
company: "ABC Insurance Company"
version: "1.0"
effective_date: "2023-01-01"
status: "active"
---

# Regulatory and Professional Standards Compilation
## Personal Auto Insurance Model Development

⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration purposes. No real insurance data, customer information, proprietary methodologies, or confidential information from any insurance company or financial institution is used or simulated.

All company information is fictional. This compilation summarizes publicly available regulatory and professional standards for educational and demonstration purposes only.

---

## Document Purpose

This compilation provides a centralized reference for regulatory requirements and professional standards applicable to predictive modeling for personal auto insurance at ABC Insurance Company. It serves as a quick reference for model developers, validators, and governance committees.

**Primary Audience:**
- Actuaries developing pricing models
- Model validators
- Compliance officers
- Model Risk Governance Committee
- Regulatory affairs staff

**Scope:**
- NAIC Model Audit Rule requirements
- Actuarial Standards of Practice (ASOPs)
- State insurance department guidelines
- Model risk management principles

---

## Section 1: NAIC Model Audit Rule (MAR)

### 1.1 Overview

The NAIC Model Audit Rule establishes minimum standards for insurance company model governance and documentation. While requirements vary by state, most states have adopted substantially similar provisions.

**Effective Date:** Varies by state (2017-2020 in most jurisdictions)

**Scope:** Applies to models that:
- Support financial statement reserves
- Determine policy values
- Support pricing and risk classification
- Assess capital adequacy

**ABC Insurance Applicability:** All personal auto pricing models (frequency, severity, territory, etc.) fall under MAR requirements.

### 1.2 Key Requirements

**1. Model Governance Framework**

Insurance companies must establish:
- Written model governance policy
- Clear roles and responsibilities
- Model risk committee or equivalent oversight
- Model inventory and risk classification

**ABC Insurance Implementation:**
- Model Risk Governance Committee (quarterly meetings)
- Chief Actuary as Model Owner
- Model Risk Officer maintains inventory
- Annual model risk assessment

**2. Model Documentation**

Models must have comprehensive documentation including:
- Purpose and design
- Data sources and quality
- Methodology and assumptions
- Limitations and known weaknesses
- Validation and testing results
- Implementation and use

**ABC Insurance Standard:**
- Model documentation template (25-30 page minimum)
- Technical specification document
- Validation report (independent)
- User guide and training materials

**3. Model Validation**

Requirements include:
- Evaluation of conceptual soundness
- Assessment of data quality and relevance
- Analysis of model performance
- Sensitivity testing
- Comparison to alternatives or benchmarks

**ABC Insurance Practice:**
- Three-tier validation (development, pre-production, ongoing)
- Independent validator (separate from developer)
- Annual comprehensive validation
- Documented validation findings and remediation

**4. Model Use and Monitoring**

Ongoing requirements:
- Policies governing model use
- Limitations on extrapolation beyond data range
- Performance monitoring
- Periodic review and recalibration

**ABC Insurance Monitoring:**
- Monthly automated dashboards
- Quarterly review by Pricing Committee
- Annual Chief Actuary sign-off
- 3-5 year model refresh cycle

### 1.3 High-Risk Model Designation

Models classified as "high risk" require enhanced governance:

**High-Risk Criteria:**
- Material financial impact (>$5M annual premium)
- Complexity (machine learning, limited interpretability)
- New or novel methodology
- Material regulatory sensitivity

**ABC Insurance High-Risk Models:**
- 2023 Comprehensive Coverage XGBoost Model (ML complexity)
- All liability models (materiality threshold)

**Enhanced Requirements:**
- Model Risk Committee approval required
- Third-party validation (every 3-5 years)
- Quarterly performance reporting to executive leadership
- Enhanced documentation standards

### 1.4 Regulatory Examination

State regulators may examine:
- Model governance policies
- Model documentation
- Validation reports
- Monitoring procedures
- Committee meeting minutes

**ABC Insurance Preparedness:**
- Annual mock audit by Internal Audit
- Documentation library maintained (7-year retention)
- Designated regulatory liaison (VP Regulatory Affairs)
- Response protocol (<5 business days for information requests)

---

## Section 2: Actuarial Standards of Practice (ASOPs)

### 2.1 ASOP No. 12 - Risk Classification

**Effective Date:** May 1, 2005

**Scope:** Guidance on risk classification for all insurance products

**Key Principles:**

**1. Risk Classification Criteria**

Risk classification systems should be:
- **Related to Expected Outcomes:** Variables predictive of loss frequency/severity
- **Objective:** Based on observable, verifiable data
- **Practical:** Administratively feasible to implement
- **Applicable:** Statistically significant and credible
- **Causally Related:** Logical actuarial relationship to risk

**2. Permitted Considerations**

Factors actuaries may consider:
- Homogeneity within classes
- Credibility of data
- Predictive value and stability
- Causality vs. correlation
- Legal and regulatory constraints
- Social acceptability

**3. Prohibited Factors**

Variables that must NOT be used:
- Race, color, national origin
- Religion
- Sexual orientation (most states)
- Genetic information
- Other protected classes per state law

**ABC Insurance Application:**

All rating variables reviewed against ASOP 12:
- Statistical testing for predictive value (p < 0.05)
- Actuarial justification documented
- Prohibited factors excluded
- Annual compliance review

**Examples:**

✓ **Allowed:** Driver age, prior claims, vehicle type, territory
✓ **Allowed (with restrictions):** Credit-based insurance score (8 states permit)
✗ **Prohibited:** ZIP codes as proxy for race/ethnicity
✗ **Prohibited:** Occupation if correlated with protected class

### 2.2 ASOP No. 23 - Data Quality

**Effective Date:** December 1, 2016 (revised)

**Scope:** Guidance on reviewing data quality for actuarial analysis

**Key Requirements:**

**1. Data Quality Assessment**

Actuaries should review:
- **Appropriateness:** Data suitable for intended purpose
- **Completeness:** Sufficient data for credible analysis
- **Reasonableness:** Data values plausible and consistent
- **Currency:** Data sufficiently recent

**2. Data Characteristics to Evaluate**

- Data definitions and documentation
- Source systems and lineage
- Collection methods
- Known limitations or biases
- Historical accuracy
- Consistency across time periods

**3. Data Deficiencies**

When data quality issues exist:
- Document nature and extent of issues
- Assess materiality/impact
- Consider alternative approaches
- Disclose limitations in communications

**ABC Insurance Implementation:**

Monthly data quality dashboard tracking:
- Completeness (target >99% for critical fields)
- Accuracy (reconciliation to finance system)
- Consistency (cross-system validation)
- Timeliness (ETL latency <1 day)

Escalation for quality issues:
- Yellow alert: 5-business-day investigation
- Red alert: Immediate notification to Data Owner

### 2.3 ASOP No. 41 - Actuarial Communications

**Effective Date:** December 1, 2010 (revised)

**Scope:** Standards for actuarial communications (reports, presentations, filings)

**Key Requirements:**

**1. Form and Content**

Actuarial communications should:
- Be clear and appropriate for intended audience
- State the purpose and intended use
- Identify the actuary and principals
- Identify the effective date
- Disclose material conflicts of interest

**2. Required Disclosures**

Must disclose:
- Scope and intended purpose
- Significant assumptions and methods
- Data sources and quality issues
- Material limitations
- Reliance on data/work of others
- Subsequent events (if applicable)

**3. Deviation from ASOP Guidance**

If deviating from guidance:
- Disclose the nature of deviation
- Explain rationale for deviation

**ABC Insurance Model Documentation:**

Standard documentation includes:
- Executive summary (purpose, scope, results)
- Data section (sources, quality, limitations)
- Methodology (assumptions, techniques, justification)
- Results (performance, validation, comparison)
- Limitations (known weaknesses, uncertainty)
- Appendices (technical details, coefficients)

### 2.4 ASOP No. 56 - Modeling

**Effective Date:** December 1, 2019

**Scope:** Guidance for designing, developing, and using models

**Key Guidance:**

**1. Model Governance**

Organizations should establish:
- Model governance framework
- Policies for model development and use
- Oversight and accountability
- Documentation standards

**2. Model Design**

Considerations include:
- Appropriateness for intended purpose
- Model complexity vs. interpretability trade-offs
- Data availability and quality
- Regulatory and business constraints

**3. Model Development**

Process should include:
- Clear specification of inputs/outputs
- Testing and validation
- Sensitivity analysis
- Documentation of assumptions and limitations

**4. Model Use**

Appropriate use requires:
- Understanding of limitations
- Restrictions on extrapolation
- Ongoing monitoring
- Periodic review and updating

**5. Disclosure**

Model users should be informed of:
- Model purpose and scope
- Key assumptions and limitations
- Material uncertainty
- Appropriateness for specific application

**ABC Insurance Compliance:**

All models follow ASOP 56 framework:
- Documented in model governance policy
- Standard development process (Section 6 of Methodology Guide)
- Validation requirements (Section 8)
- Monitoring standards (Section 9)
- Annual comprehensive review

---

## Section 3: State Insurance Department Guidelines

### 3.1 Overview

ABC Insurance operates in 15 states, each with specific requirements for insurance rate filings and model governance. This section summarizes key state-level requirements.

### 3.2 Common State Requirements

**Rate Filing Submissions:**

Most states require:
- Actuarial memorandum supporting rate change
- Data exhibits (loss experience, exposures)
- Rate indication calculations
- Impact analysis (premium change by segment)
- Compliance certification

**Territory Definition Requirements:**

States vary in approach:
- **ZIP Code-Based:** 10 states allow ZIP code rating territories
- **County-Based:** 3 states require county-based territories
- **Hybrid:** 2 states allow ZIP-within-county

**Variable Approval:**

- **Pre-Approval Required:** 5 states (must file rating plan changes)
- **File-and-Use:** 7 states (implement after filing, pending review)
- **Use-and-File:** 3 states (implement immediately, file within 30 days)

**Credit Score Restrictions:**

- **Prohibited:** 7 of 15 ABC Insurance states
- **Allowed with restrictions:** 6 states (caps on impact, disclosure requirements)
- **Allowed:** 2 states (no material restrictions)

### 3.3 State-Specific Considerations

**State Group 1: Restrictive (5 states)**

Characteristics:
- Pre-approval required for rate changes
- Conservative view of machine learning models
- Enhanced documentation requirements
- Public hearings for material rate increases (>7%)

ABC Insurance Approach:
- GLM models only (no XGBoost)
- Enhanced actuarial memoranda
- Consumer impact analysis required
- 6-month advance filing timeline

**State Group 2: Moderate (7 states)**

Characteristics:
- File-and-use approval process
- Openness to advanced analytics with explainability
- Standard documentation requirements
- Expedited review for minor changes

ABC Insurance Approach:
- XGBoost allowed with SHAP explainability
- Standard model documentation
- 90-day filing timeline
- Regular communication with state actuaries

**State Group 3: Progressive (3 states)**

Characteristics:
- Use-and-file process
- Supportive of innovation and advanced analytics
- Flexibility in rating variable selection
- Focus on outcomes rather than process

ABC Insurance Approach:
- Full range of modeling techniques
- Streamlined documentation
- 30-day post-implementation filing
- Annual comprehensive filing

### 3.4 Multi-State Considerations

**Challenges:**
- Varying approval timelines (30 days to 6 months)
- Conflicting requirements (territory definitions)
- Different prohibited variables (credit scores)

**ABC Insurance Strategy:**
- National model with state-specific adjustments
- Staggered filing schedule (restrictive states first)
- State-specific rate relativities where required
- Dedicated regulatory affairs team per region

---

## Section 4: Model Risk Management Principles

### 4.1 Overview

Model risk management integrates regulatory requirements (NAIC MAR) with industry best practices. This section outlines principles guiding ABC Insurance's approach.

**Definition of Model Risk:**

Model risk is the potential for adverse consequences from:
- Decisions based on incorrect model outputs
- Misuse or misinterpretation of model results

**Sources of Model Risk:**
- Fundamental design flaws
- Incorrect assumptions
- Data quality issues
- Implementation errors
- Inappropriate use or extrapolation
- Failure to adapt to changing conditions

### 4.2 Three Lines of Defense

**First Line: Model Developers and Users**

Responsibilities:
- Develop models per standards
- Document methodology and limitations
- Perform initial validation and testing
- Use models appropriately
- Monitor performance

ABC Insurance Implementation:
- Actuarial and data science teams
- Adherence to Methodology Guide (Sections 1-10)
- Quarterly performance monitoring
- Escalation of issues

**Second Line: Model Risk Management Function**

Responsibilities:
- Independent model validation
- Model governance oversight
- Policy development and maintenance
- Model inventory management
- Risk assessment and reporting

ABC Insurance Implementation:
- Model Risk Officer (independent reporting to CRO)
- Model Risk Governance Committee
- Annual model inventory review
- Risk-based validation schedule

**Third Line: Internal Audit**

Responsibilities:
- Independent assurance
- Governance effectiveness review
- Compliance testing
- Audit findings and recommendations

ABC Insurance Implementation:
- Annual model governance audit
- Sample model documentation reviews
- Testing of validation procedures
- Reporting to Audit Committee of Board

### 4.3 Model Inventory and Risk Classification

**Model Inventory:**

All models tracked with:
- Model ID and version
- Model type and purpose
- Business owner and developer
- Last validation date
- Risk classification

**Risk Classification Criteria:**

Models classified as High/Medium/Low risk based on:
- Financial materiality (premium impact)
- Complexity (GLM = Low, XGBoost = High)
- Regulatory sensitivity
- Novelty (new methodology = higher risk)
- Performance track record

**ABC Insurance Model Inventory (Personal Auto):**

| Model | Type | Risk Level | Validation Frequency |
|-------|------|------------|----------------------|
| BI Frequency | GLM | High (materiality) | Annual |
| BI Severity | GLM | High (materiality) | Annual |
| PD Frequency | GLM | Medium | Annual |
| Collision Frequency | GLM | High (materiality) | Annual |
| Collision Severity | GLM | Medium | Annual |
| Comprehensive | XGBoost | High (complexity) | Semi-annual |
| Territory | Clustering+GLM | Medium | Annual |

### 4.4 Model Validation Standards

**Effective Challenge:**

Validators must provide:
- Independent assessment (not model developer)
- Appropriate expertise (actuarial or data science)
- Sufficient resources and authority
- Direct reporting to Model Risk Committee

**Validation Scope:**

- **Conceptual Soundness:** Is methodology appropriate?
- **Data Quality:** Are data suitable and reliable?
- **Performance:** Does model achieve objectives?
- **Stability:** Is model robust to perturbations?
- **Limitations:** Are weaknesses identified and managed?

**Validation Outcomes:**

- **Approved:** Model meets all standards, recommended for production
- **Approved with Conditions:** Minor issues, acceptable with monitoring or restrictions
- **Rejected:** Material issues, requires remediation before production use

**ABC Insurance Validation Process:**

1. Developer submits model documentation
2. Independent validator assigned (separate team)
3. Validation testing per standards (30-60 days)
4. Validation report with recommendation
5. Model Risk Committee review and decision
6. Chief Actuary approval (if Committee approves)

### 4.5 Emerging Model Risk Considerations

**Machine Learning Models:**

Special considerations:
- Explainability and interpretability
- Training data bias and fairness
- Overfitting and generalization
- Versioning and reproducibility
- Regulatory acceptance

ABC Insurance Approach:
- SHAP values for explainability
- Fairness testing (demographic parity where applicable)
- Comprehensive validation including stability testing
- Enhanced documentation requirements
- Regulatory pre-consultation for novel approaches

**External Data and Third-Party Models:**

Risks include:
- Data quality and reliability
- Vendor model opacity ("black box")
- Dependency on external provider
- Intellectual property constraints

ABC Insurance Mitigation:
- Vendor due diligence (annual reviews)
- Data quality agreements and monitoring
- Validation of vendor models where feasible
- Contingency plans for vendor termination

---

## Section 5: Ethical Considerations and Fairness

### 5.1 Fairness in Insurance Pricing

**Regulatory Framework:**

Insurance pricing must balance:
- Actuarial fairness (prices reflect risk)
- Social fairness (avoid discrimination)
- Affordability (prices accessible)

**Protected Classes:**

Federal and state laws prohibit discrimination based on:
- Race, color, national origin
- Religion
- Sex/gender (with actuarial justification exceptions)
- Age (ADEA for employment, varies for insurance)
- Disability
- Genetic information

**Permitted Risk Classification:**

Actuarially justified variables allowed even if correlated with protected class, provided:
- Causally related to risk (not merely proxy)
- Demonstrably predictive
- No less discriminatory alternative available
- Consistent with regulatory guidance

### 5.2 Disparate Impact Analysis

**Definition:**

Disparate impact occurs when a facially neutral practice disproportionately affects a protected class, even without discriminatory intent.

**ABC Insurance Monitoring:**

Annual disparate impact testing:
- Demographic analysis by protected class
- Rate differential analysis
- Statistical significance testing
- Causality assessment

**Remediation if Disparate Impact Found:**

1. Assess business necessity and actuarial justification
2. Evaluate less discriminatory alternatives
3. Adjust model or variables if appropriate
4. Document analysis and decision
5. Report findings to Model Risk Committee

### 5.3 Transparency and Explainability

**Consumer Right to Explanation:**

Some states require insurers to explain:
- Factors affecting individual premium
- Reason for rate increase
- How to improve rating (where controllable)

**ABC Insurance Practice:**

- Rate change notices include explanation of key factors
- Customer service training on model-driven pricing
- Website FAQs on rating variables
- Ability to provide individualized factor analysis on request

### 5.4 Algorithmic Bias and Fairness Testing

**Sources of Bias:**

Models can embed bias through:
- Historical data reflecting past discrimination
- Proxy variables correlated with protected class
- Sampling bias (unrepresentative training data)
- Label bias (biased ground truth)

**ABC Insurance Bias Testing:**

Pre-deployment:
- Demographic parity testing (where data available)
- Equalized odds testing (error rates by subgroup)
- Calibration testing (accuracy across subgroups)

Ongoing:
- Annual fairness audit by independent third party
- Monitoring of outcomes by demographic proxies (geography)
- Investigation of consumer complaints

**Ethical Guidelines:**

ABC Insurance Model Ethics Principles:
1. Fairness: Models must not discriminate against protected classes
2. Transparency: Consumers have right to understand pricing
3. Accountability: Clear ownership and governance
4. Privacy: Personal data protected and used appropriately
5. Safety: Models monitored for unintended harmful consequences

---

## Section 6: Compliance Checklist

### 6.1 New Model Deployment Checklist

Before deploying any new or materially updated model:

**Documentation:**
- ☐ Comprehensive model documentation prepared (25-30 pages minimum)
- ☐ Technical specification completed
- ☐ User guide and training materials created
- ☐ Data lineage documented
- ☐ Assumptions and limitations clearly stated

**Validation:**
- ☐ Independent validation performed
- ☐ Validation report completed with recommendation
- ☐ All validation findings addressed or accepted as limitations
- ☐ Performance metrics meet standards (R², AUC, calibration)
- ☐ Sensitivity analysis performed

**Governance:**
- ☐ Model Risk Governance Committee approval obtained
- ☐ Chief Actuary sign-off obtained
- ☐ Model added to inventory with risk classification
- ☐ Monitoring plan established (metrics, frequency, thresholds)

**Regulatory:**
- ☐ State filing requirements reviewed
- ☐ Actuarial memorandum prepared for rate filings
- ☐ Rate impact analysis completed
- ☐ Filings submitted per state timelines
- ☐ Regulatory approvals obtained (where required before implementation)

**Compliance:**
- ☐ ASOP 12 compliance verified (risk classification principles)
- ☐ ASOP 23 compliance verified (data quality)
- ☐ ASOP 41 compliance verified (actuarial communication)
- ☐ ASOP 56 compliance verified (modeling standards)
- ☐ Prohibited variables excluded (protected classes)
- ☐ Disparate impact analysis completed
- ☐ Fairness testing performed (if ML model)

**Implementation:**
- ☐ Parallel testing completed (shadow mode)
- ☐ User acceptance testing passed
- ☐ Production deployment plan approved
- ☐ Rollback procedure documented
- ☐ Training completed for all users
- ☐ Go-live approval from business stakeholders

### 6.2 Annual Model Review Checklist

For each production model, annually:

**Performance:**
- ☐ Actual vs. expected analysis (12-month rolling)
- ☐ Calibration testing (by decile)
- ☐ R² or AUC on recent data
- ☐ Loss ratio vs. budget
- ☐ Alert threshold violations reviewed

**Data Quality:**
- ☐ Data completeness and accuracy metrics reviewed
- ☐ Feature distribution shifts assessed (PSI)
- ☐ New data quality issues identified and resolved

**Validation:**
- ☐ Annual validation performed (in-house or third-party)
- ☐ Model assumptions re-assessed
- ☐ Limitations and risks re-evaluated
- ☐ Benchmark comparison (if champion-challenger in place)

**Governance:**
- ☐ Model Risk Committee annual review completed
- ☐ Chief Actuary annual sign-off obtained
- ☐ Model risk classification updated if needed
- ☐ Decision on model continuation, recalibration, or replacement

**Regulatory:**
- ☐ State regulatory changes reviewed for impact
- ☐ Rate filings updated if material model changes
- ☐ Regulatory examination preparedness verified

**Documentation:**
- ☐ Model documentation updated (version control)
- ☐ Change log updated
- ☐ Validation reports archived
- ☐ Meeting minutes documented

---

## Section 7: Resources and References

### 7.1 NAIC Resources

**Model Audit Rule:**
- NAIC Model Audit Rule (#205)
- Available: NAIC website (public)
- State-specific implementations: Consult state insurance department

**Model Governance Resources:**
- NAIC Own Risk Solvency Assessment (ORSA) Guidance
- NAIC Principles-Based Reserving Guidelines

### 7.2 Actuarial Standards Board

**Actuarial Standards of Practice:**
- ASOP No. 12: Risk Classification
- ASOP No. 23: Data Quality
- ASOP No. 41: Actuarial Communications
- ASOP No. 56: Modeling

**Access:** Academy of Actuaries website (www.actuary.org)
**Status:** All ASOPs are publicly available at no cost

### 7.3 Industry Best Practices

**Organizations:**
- Casualty Actuarial Society (CAS): Research papers, predictive modeling resources
- Society of Actuaries (SOA): Model risk management resources
- American Academy of Actuaries: Practice notes and public policy statements

**Conferences and Education:**
- CAS Ratemaking and Product Management Seminar (annual)
- Predictive Analytics and Futurism (PAF) Conference
- CAS Online courses on GLM and machine learning

### 7.4 ABC Insurance Internal Resources

**Policies and Procedures:**
- Model Governance Policy (Document MGP-2023-01)
- Data and Methodology Guide (this document's companion)
- Model Documentation Template (MDT-2023-Standard)
- Validation Procedures Manual (VPM-2023-01)

**Contacts:**
- Model Risk Officer: Sarah Williams, sarah.williams@abcinsurance.example.com
- Chief Actuary: Robert Johnson, FCAS, MAAA, robert.johnson@abcinsurance.example.com
- Regulatory Affairs: VP Thomas Martinez, thomas.martinez@abcinsurance.example.com

**Internal Training:**
- Model Risk Management 101 (required for all model developers, annual)
- Regulatory Compliance for Actuaries (annual update)
- ASOP Updates (as released)

---

## Conclusion

This Regulatory and Professional Standards Compilation provides a comprehensive reference for model development at ABC Insurance Company. Adherence to these standards ensures:

- **Regulatory Compliance:** Meeting NAIC, state, and federal requirements
- **Professional Standards:** Following actuarial best practices (ASOPs)
- **Risk Management:** Identifying and mitigating model risk
- **Ethical Conduct:** Fair and transparent treatment of consumers

**Continuous Improvement:**

This document is reviewed annually and updated for:
- New regulations or guidance
- ASOP revisions
- Lessons learned from model performance
- Industry best practice evolution

**Questions:**

For questions on regulatory compliance or professional standards:
- Model Risk Officer (governance and validation)
- Chief Actuary (technical actuarial questions)
- Regulatory Affairs (state-specific filing questions)

---

## Document Control

**Version:** 1.0
**Effective Date:** January 1, 2023
**Last Updated:** January 1, 2023
**Next Review:** January 1, 2024

**Prepared by:**
Regulatory Compliance Committee
ABC Insurance Company

**Reviewed by:**
- Robert Johnson, FCAS, MAAA (Chief Actuary)
- Sarah Williams (Model Risk Officer)
- Thomas Martinez (VP Regulatory Affairs)

**Approved by:**
Sarah Williams
Model Risk Officer

**Distribution:**
- All actuarial staff
- Model developers (data science team)
- Model Risk Governance Committee
- Regulatory Affairs team
- Internal Audit
- Legal/Compliance

**Change Log:**

| Version | Date       | Changes                                    | Author                |
|---------|------------|--------------------------------------------|-----------------------|
| 1.0     | 2023-01-01 | Initial release                            | Regulatory Compliance |

---

**End of Document**
