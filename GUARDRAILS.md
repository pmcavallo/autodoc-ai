# Sensitive Data Prevention Guardrails
## Critical Rules for AutoDoc AI Development

---

## 🚨 PRIORITY INSTRUCTION

**These guardrails MUST be followed at all times. Violation of these rules could expose real individuals or organizations to harm, even in a demonstration project.**

---

## Rule 1: Personal Identifiable Information (PII)

### ❌ NEVER Generate:

**Names:**
- Real people's names (customers, employees, executives, anyone)
- Names that could be confused with real individuals
- Celebrity names or public figures

**Contact Information:**
- Real email addresses
- Real phone numbers (even formatted differently)
- Real physical addresses
- Real social media handles

**Identification Numbers:**
- Social Security Numbers (even fake-formatted ones like XXX-XX-XXXX)
- Driver's License Numbers
- Passport Numbers
- Employee IDs that could be real
- Tax ID Numbers (TIN, EIN)

### ✅ ALWAYS Use:

**Generic Fictional Names:**
```
✅ John Smith, Jane Doe, Alex Johnson, Maria Garcia
✅ Bob Anderson, FSA, MAAA (with professional designations)
✅ Sarah Chen, Chief Actuary
```

**Placeholder Contact Info:**
```
✅ Email: john.smith@example.com, info@example-insurance.com
✅ Phone: (555) 123-4567 (555 is reserved for fiction)
✅ Address: 123 Main Street, Anytown, ST 12345
```

**Obvious Placeholder IDs:**
```
✅ POL-2023-001234 (policy number)
✅ CLM-2024-567890 (claim number)
✅ EMP-2023-00042 (employee ID)
✅ VIN: 1HGCM82633A123456 (clearly synthetic pattern)
```

---

## Rule 2: Financial and Insurance Data

### ❌ NEVER Generate:

**Real Financial Data:**
- Actual premium amounts for real customers
- Actual claim amounts tied to individuals
- Real credit scores or credit histories
- Real bank account numbers
- Real policy details from actual customers

**Proprietary Information:**
- Actual pricing models from real insurers
- Real competitive intelligence
- Confidential rate structures
- Actual underwriting guidelines from real companies

### ✅ ALWAYS Use:

**Aggregated Statistics:**
```
✅ "Average annual premium: $1,250"
✅ "Median claim severity: $3,500"
✅ "Loss ratio: 68%"
✅ "Top decile lift: 2.3x"
```

**Generic Model Outputs:**
```
✅ "Model AUC: 0.72"
✅ "Gini coefficient: 0.44"
✅ "RMSE: $450"
✅ "R-squared: 0.61"
```

**Fictional Company Data:**
```
✅ "ABC Insurance Company"
✅ "XYZ Mutual"
✅ "Northern States Insurance"
✅ "Midwest Auto Group"
```

---

## Rule 3: Medical and Health Information

### ❌ NEVER Generate:

- Real medical records or health information
- Specific diagnoses tied to individuals
- Prescription information
- Medical ID numbers
- Health insurance details that could identify someone

### ✅ ALWAYS Use:

**Aggregate Health Statistics (if needed):**
```
✅ "Injury type distribution: 60% minor, 30% moderate, 10% severe"
✅ "Average medical cost: $5,000"
✅ "Treatment duration categories: <7 days, 7-30 days, 30+ days"
```

---

## Rule 4: Sensitive Demographics

### ❌ NEVER Generate:

- Individual-level demographic data that could identify someone
- Protected class information tied to specific people
- Discriminatory rating factors

### ✅ ALWAYS Use:

**Aggregated Demographics:**
```
✅ "Age distribution: 18-24 (15%), 25-34 (25%), 35-44 (20%)..."
✅ "Territory A: Urban, high traffic density"
✅ "Vehicle type: Sedan (50%), SUV (30%), Truck (20%)"
```

**Standard Insurance Variables:**
```
✅ Driver age, vehicle age, years of driving experience
✅ Territory/geographic zone (not specific addresses)
✅ Prior claims frequency (0, 1, 2, 3+)
✅ Coverage types (liability, collision, comprehensive)
```

---

## Rule 5: Real Companies and Organizations

### ❌ NEVER Generate:

- Actual insurance companies' internal documents
- Real audit findings from named companies
- Confidential regulatory actions
- Real competitive data
- Actual company methodologies or processes

### ✅ ALWAYS Use:

**Generic Company Names:**
```
✅ "ABC Insurance Company"
✅ "XYZ Mutual Insurance"
✅ "Northern Auto Insurance Group"
✅ "Midwest Regional Insurer"
```

**Publicly Available Information:**
```
✅ NAIC Model Audit Rule (publicly available)
✅ Actuarial Standards of Practice (public documents)
✅ State insurance department guidelines (public)
✅ General industry statistics (public sources)
```

---

## Rule 6: Dates and Temporal Data

### ❌ NEVER Use:

- Very recent dates that could tie to actual events
- Specific dates that could identify individuals
- Real-time data that could reveal actual incidents

### ✅ ALWAYS Use:

**Safe Date Ranges:**
```
✅ Development data: "2019-2021 policy years"
✅ Model deployment: "Q3 2022"
✅ Validation period: "2022-2023"
✅ Review date: "March 2024"
```

**Generic Timeframes:**
```
✅ "Previous year", "Current quarter", "Next review cycle"
✅ "Historical 3-year period"
✅ "Rolling 12-month window"
```

---

## Rule 7: Vehicle and Property Data

### ❌ NEVER Generate:

- Real Vehicle Identification Numbers (VINs)
- Actual license plate numbers
- Specific property addresses that could identify someone
- Real accident locations with identifying details

### ✅ ALWAYS Use:

**Generic Vehicle Data:**
```
✅ Vehicle type: "2020 Honda Civic"
✅ Vehicle class: "Sedan, 4-door"
✅ Vehicle age: "3 years"
✅ VIN pattern: "1HGCM82633A123456" (clearly synthetic)
```

**Generic Location Data:**
```
✅ Territory: "Zone 1", "Region A", "Urban Territory"
✅ State: "Midwest Region"
✅ Area: "Metropolitan area with population >1M"
```

---

## Rule 8: Code and Technical Examples

### ❌ NEVER Include:

- Real API keys or credentials
- Actual database connection strings
- Real file paths that could identify systems
- Production URLs or endpoints

### ✅ ALWAYS Use:

**Placeholder Credentials:**
```python
✅ API_KEY = "sk-ant-api03-xxx-PLACEHOLDER"
✅ DATABASE_URL = "postgresql://user:pass@localhost:5432/synthetic_db"
✅ BASE_URL = "https://api.example.com/v1"
```

**Generic File Paths:**
```python
✅ data_path = "C:\\Projects\\autodoc-ai\\data\\synthetic_docs\\"
✅ output_path = "./outputs/model_documentation.pdf"
```

---

## Validation Checklist

Before committing ANY synthetic data, verify:

### Personal Data Check:
- [ ] No real names (search Google if unsure)
- [ ] No real addresses
- [ ] No real phone numbers or emails
- [ ] No real identification numbers
- [ ] No real VINs or license plates

### Financial Data Check:
- [ ] No individual-level financial data
- [ ] Only aggregated statistics
- [ ] No real company proprietary information
- [ ] No actual pricing or claims data

### Company Data Check:
- [ ] No real company names in sensitive contexts
- [ ] Only publicly available regulatory info
- [ ] No confidential audit findings
- [ ] Generic company names used throughout

### Disclaimer Check:
- [ ] Synthetic data disclaimer at top of document
- [ ] Clear indication this is demonstration only
- [ ] No claims of real data or real accuracy

---

## Disclaimer Template

**Add this to the top of EVERY synthetic document:**

```markdown
⚠️ **SYNTHETIC DATA - FOR DEMONSTRATION ONLY**

This document contains entirely synthetic data created for portfolio demonstration 
purposes. No real insurance data, customer information, proprietary methodologies, 
or confidential information from any insurance company or financial institution is 
used or simulated.

All names, addresses, policy numbers, claim amounts, and company information are 
fictional. Any resemblance to actual persons, organizations, or data is purely 
coincidental.

This project showcases AI agent capabilities for automated documentation generation 
and is not intended for production use with real data or models.
```

---

## Red Flags - Stop Immediately If:

🚨 You're about to use a name you recognize as real  
🚨 You're using an address that could be real  
🚨 You're using data that seems too specific  
🚨 You're copying content from a real company's website  
🚨 You're uncertain if something violates these rules  

**When in doubt → ASK. Don't guess.**

---

## Examples of Good vs. Bad

### ❌ BAD:
```
John Smith at 1234 Oak Street, Chicago IL 60601
Phone: (312) 555-0123, SSN: 123-45-6789
Policy #: ABC123456, Premium: $1,456.32
VIN: 1HGBH41JXMN109186 (real VIN format)
Claim for accident on 10/15/2024 at intersection of Michigan Ave and Wacker Dr
```

### ✅ GOOD:
```
John Smith at 123 Main Street, Anytown, IL 60000
Phone: (555) 123-4567, Customer ID: CUST-2023-00142
Policy #: POL-2023-001234, Average premium: $1,450
VIN: 1HGCM82633A123456 (synthetic pattern)
Claim for accident in Urban Territory Zone 3
```

---

## Testing for Compliance

Before committing, run these checks:

### Name Check:
```bash
# Search for common real names
grep -i "elon musk\|jeff bezos\|[known CEO names]" *.md
```

### SSN Pattern Check:
```bash
# Look for SSN-like patterns
grep -E "[0-9]{3}-[0-9]{2}-[0-9]{4}" *.md
```

### Real Company Check:
```bash
# Check for actual insurance company names
grep -i "state farm\|geico\|progressive\|allstate" *.md
```

### Real Address Check:
```bash
# Flag specific addresses
grep -E "[0-9]+ [A-Z][a-z]+ (Street|Avenue|Boulevard|Road)" *.md
```

---

## Summary: The Three Principles

1. **If it could identify a real person → Don't use it**
2. **If it could be proprietary to a real company → Don't use it**
3. **If you're uncertain → Stop and ask**

---

## Enforcement

**Violations of these guardrails will result in:**
1. Immediate halt of development
2. Removal of violating content
3. Review of all previously generated content
4. Additional safeguards before resuming

**This is not optional. These rules protect real people and organizations.**

---

## Questions?

If you need clarification on whether something violates these rules:
1. Stop what you're doing
2. Ask explicitly
3. Wait for confirmation before proceeding
4. Err on the side of caution

**When in doubt, use more generic placeholders rather than risk using real data.**

---

**Last Updated:** October 2025  
**Must be reviewed before:** Starting any data generation  
**Next review:** After Phase 1 completion
