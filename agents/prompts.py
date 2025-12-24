"""
Prompt templates for document generation
"""

def build_section_prompt(section_title: str, context: str, template: str, length_target: str) -> str:
    """
    Build a prompt for generating a documentation section.
    
    Args:
        section_title: The section being generated (e.g., "Executive Summary")
        context: Context from RAG and input data
        template: Template type (e.g., "executive_summary")
        length_target: "short" (400-600 words), "medium" (800-1200), "long" (1500-2000)
    
    Returns:
        Complete prompt for Claude API
    """
    
    # Define word count targets
    word_counts = {
        "short": "400-600 words",
        "medium": "800-1200 words",
        "long": "1500-2000 words"
    }
    target_length = word_counts.get(length_target, "800-1200 words")
    
    # Build the prompt
    prompt = f"""You are an expert insurance actuary with 15 years of experience writing regulatory model documentation. Your documentation is known for clarity, technical accuracy, and compliance with NAIC and ASOP standards.

TASK: Write the "{section_title}" section for an insurance model documentation package.

CONTEXT AND EXAMPLES:
{context}

REQUIREMENTS:
- Professional actuarial tone suitable for regulatory review
- Target length: {target_length}
- Include specific numbers and technical details from the context
- Reference industry standards (NAIC, ASOPs) where appropriate
- Use clear, precise language
- Structure content logically with smooth transitions
- Write in present tense for current state, past tense for development history

IMPORTANT: Write only the section content. Do not include the section heading, as it will be added separately. Do not add any meta-commentary or notes about the content.

Write the {section_title} section now:"""

    return prompt

def build_executive_summary_prompt(slide_content: str, rag_results: str) -> str:
    """
    Build specialized prompt for Executive Summary section.
    
    Focus: High-level business narrative, concise, executive-focused.
    Style: Clear, confident, suitable for leadership and regulators.
    """
    
    prompt = f"""You are an expert insurance actuary with 15 years of experience writing executive summaries for regulatory model documentation. Your summaries are known for clarity, conciseness, and strategic insight.

AUDIENCE: Senior actuaries, regulators, and executives who need to quickly understand the model's purpose, approach, and key findings.

SECTION PURPOSE:
Provide a high-level overview that allows readers to understand the model without reading the entire document. This section sets the tone for the full documentation.

YOUR TASK:
Write a compelling Executive Summary (400-600 words) that covers:

1. MODEL PURPOSE (1-2 paragraphs)
   - What business problem this model solves
   - Why the model was developed
   - Who will use it and how

2. MODELING APPROACH (1-2 paragraphs)
   - High-level methodology (e.g., "GLM with frequency-severity approach")
   - Key data sources
   - Major modeling decisions

3. KEY FINDINGS (1-2 paragraphs)
   - Model performance highlights
   - Important insights or patterns discovered
   - How results compare to expectations or prior models

4. BUSINESS IMPACT (1 paragraph)
   - How the model improves business processes
   - Expected benefits
   - Implementation considerations

TONE REQUIREMENTS:
- Professional but accessible
- Confident without overstating
- Focus on "what" and "why" not technical "how"
- Write for busy executives who may only read this section

DO NOT:
- Include excessive technical details
- Use jargon without explanation
- Make the summary longer than 600 words
- Include information not supported by the slide content

SLIDE CONTENT TO ANALYZE:
{slide_content}

REFERENCE EXAMPLES FROM PAST DOCUMENTATION:
{rag_results if rag_results else "No reference examples available - use your expertise in actuarial documentation standards."}

Write the Executive Summary now. Focus on clarity, conciseness, and strategic insight."""

    return prompt

def build_methodology_prompt(model_type: str, key_findings: str, context: str) -> str:
    """
    Build a specialized prompt for Methodology section.
    
    Methodology sections need more technical depth than executive summaries,
    including mathematical formulation, variable descriptions, and assumptions.
    
    Args:
        model_type: Type of model (e.g., "frequency", "severity")
        key_findings: Key model details from PowerPoint
        context: RAG-retrieved examples from past methodology sections
    
    Returns:
        Complete prompt for methodology generation
    """
    
    prompt = f"""You are a senior quantitative analyst with deep expertise in statistical modeling and actuarial science. You are documenting the technical methodology for an insurance model that will be reviewed by actuaries and regulatory bodies.

TASK: Write the "Methodology" section for a {model_type} model documentation package.

EXAMPLES FROM PAST MODEL DOCUMENTATION:
{context}

CURRENT MODEL DETAILS:
{key_findings}

REQUIRED STRUCTURE AND CONTENT:

1. Model Framework (3-4 paragraphs)
   - Mathematical formulation (e.g., GLM specification, loss function)
   - Distribution family and link function
   - Why this approach was selected over alternatives
   - Theoretical foundation and statistical properties

2. Predictor Variables (2-3 paragraphs)
   - Complete list of variables included in final model
   - Description of each variable (continuous, categorical, derived)
   - Any transformations applied (log, polynomial, binning)
   - Interaction terms if applicable

3. Estimation Method (2 paragraphs)
   - Parameter estimation approach (maximum likelihood, gradient boosting, etc.)
   - Software and tools used
   - Convergence criteria and optimization details
   - Training/validation split methodology

4. Model Assumptions (2 paragraphs)
   - Statistical assumptions of the chosen approach
   - How assumptions were validated
   - Known limitations and constraints
   - Sensitivity to assumption violations

REQUIREMENTS:
- Technical depth appropriate for actuarial peer review
- Use precise statistical terminology
- Include mathematical notation where relevant (e.g., "log link function", "Poisson distribution")
- Reference statistical theory and best practices
- Length: 800-1200 words
- Professional, academic tone
- Present tense for methodology description
- Cite relevant actuarial standards (ASOP) where appropriate

IMPORTANT: Write only the section content. Do not include the section heading "Methodology" as it will be added separately. Do not add meta-commentary about the content.

Write the Methodology section now:"""

    return prompt

def build_data_sources_prompt(model_type: str, data_details: str, context: str) -> str:
    """
    Build specialized prompt for Data Sources section.
    
    This section requires structured presentation with clear categorization
    of data by type, source, and quality attributes.
    
    Args:
        model_type: Type of model (e.g., "frequency", "severity")
        data_details: Details about data sources used
        context: RAG-retrieved examples from past data sources sections
    
    Returns:
        Complete prompt for data sources generation
    """
    
    prompt = f"""You are a data governance specialist and senior actuary documenting data sources for an insurance model. You excel at clearly organizing complex data lineage information for regulatory review.

TASK: Write the "Data Sources and Quality" section for a {model_type} model documentation package.

EXAMPLES FROM PAST DOCUMENTATION:
{context}

CURRENT MODEL DATA:
{data_details}

REQUIRED STRUCTURE AND CONTENT:

1. Data Overview (2 paragraphs)
   - Total volume of data (exposure, policy counts, time period)
   - Primary data sources used
   - Data extraction and preparation timeline

2. Internal Data Sources (organized by type)
   For each internal source, provide:
   - Source name and system
   - Data elements extracted
   - Time period covered
   - Volume/granularity
   - Known data quality issues or limitations

3. External Data Sources (if applicable)
   For each external source, provide:
   - Vendor/provider name
   - Data elements purchased
   - Coverage and geography
   - Update frequency
   - Integration methodology

4. Data Quality Assessment (2-3 paragraphs)
   - Data validation procedures performed
   - Completeness metrics (missing data rates)
   - Consistency checks conducted
   - Treatment of outliers and anomalies
   - Any data quality concerns and mitigation

5. Data Limitations (1-2 paragraphs)
   - Known gaps in data coverage
   - Potential biases in data sources
   - Constraints that affect model scope
   - Recommendations for future data enhancement

FORMATTING REQUIREMENTS:
- Use clear headings and subheadings
- Present data sources in structured lists or bullet points where appropriate
- Include specific metrics (percentages, counts, dates)
- Use tables or structured format for comparing multiple sources
- Maintain professional documentation tone

LENGTH: 600-800 words

IMPORTANT: Write only the section content. Do not include the section heading "Data Sources and Quality" as it will be added separately. Focus on clear organization and structured presentation.

Write the Data Sources and Quality section now:"""

    return prompt

def build_variable_selection_prompt(model_type: str, variable_details: str, context: str) -> str:
    """
    Build specialized prompt for Variable Selection section.
    
    This section requires justification and reasoning for why specific
    variables were included, emphasizing statistical significance and
    business rationale.
    
    Args:
        model_type: Type of model (e.g., "frequency", "severity")
        variable_details: Details about variables and selection process
        context: RAG-retrieved examples from past variable selection sections
    
    Returns:
        Complete prompt for variable selection generation
    """
    
    prompt = f"""You are a senior statistical modeler and actuary explaining variable selection methodology for regulatory review. You excel at presenting clear statistical reasoning combined with practical business justification.

TASK: Write the "Variable Selection and Justification" section for a {model_type} model documentation package.

EXAMPLES FROM PAST DOCUMENTATION:
{context}

CURRENT MODEL VARIABLES:
{variable_details}

REQUIRED STRUCTURE AND CONTENT:

1. Selection Methodology Overview (2 paragraphs)
   - Overall approach to variable selection (univariate testing, multivariate modeling, stepwise selection, etc.)
   - Criteria used to evaluate variables (statistical significance, business relevance, data quality)
   - Iteration process and refinement

2. Final Variables and Justification (3-4 paragraphs, organized by variable)
   For each key variable or variable group, explain:
   - Statistical significance and contribution to model performance
   - Business rationale (why this variable logically affects risk)
   - Coefficient sign and interpretation
   - Any transformations applied and why
   
3. Variables Considered but Excluded (1-2 paragraphs)
   - Variables tested but not included in final model
   - Reasons for exclusion (not significant, data quality issues, multicollinearity, business concerns)
   - Trade-offs and considerations

4. Variable Interactions (1 paragraph, if applicable)
   - Any interaction terms included
   - Justification for interactions
   - Contribution to model fit

5. Regulatory and Business Considerations (1-2 paragraphs)
   - Compliance with rate filing requirements
   - Variables reviewed for potential bias or unfair discrimination
   - Alignment with underwriting practices
   - Actuarial standards (ASOP) compliance

TONE AND STYLE:
- Persuasive and justification-focused
- "Variable X was selected BECAUSE..." not just "Variable X was selected"
- Support claims with statistical evidence (p-values, lift, AUC contribution)
- Balance statistical rigor with business logic
- Address potential concerns preemptively

LENGTH: 700-900 words

IMPORTANT: Write only the section content. Do not include the section heading as it will be added separately. Focus on clear reasoning and justification for each decision.

Write the Variable Selection and Justification section now:"""

    return prompt

def build_model_results_prompt(slide_content: str, rag_results: str) -> str:
    """
    Build prompt for Model Results section - metrics and performance data.
    
    Focus: Quantitative results, structured presentation, statistical evidence.
    Style: Data-driven, objective, precise with metrics and tables.
    """
    
    prompt = f"""You are a quantitative analyst and technical writer creating the Model Results section for actuarial model documentation.

AUDIENCE: Regulatory reviewers and actuarial leadership who need evidence of model performance.

SECTION PURPOSE:
Present quantitative evidence that demonstrates model accuracy, reliability, and performance across different segments and scenarios.

YOUR TASK:
Write a comprehensive Model Results section (600-800 words) that presents the model's performance metrics in a clear, structured, and evidence-based manner.

REQUIRED COMPONENTS:

1. OVERALL PERFORMANCE METRICS
   - Primary accuracy metrics (e.g., R², RMSE, MAE, lift, Gini)
   - Model fit statistics
   - Overall predictive power
   - Comparison to benchmarks or prior models

2. SEGMENT-LEVEL RESULTS
   - Performance across key segments (age groups, products, regions, etc.)
   - Identify strong and weak performing segments
   - Explain any segment variations
   - Show consistency or highlight differences

3. VALIDATION RESULTS
   - Out-of-sample performance
   - Hold-out set results
   - Cross-validation metrics if applicable
   - Stability across time periods

4. MODEL INTERPRETATION
   - What the metrics mean in business context
   - Whether performance meets requirements
   - Confidence in model predictions
   - Any limitations or caveats

FORMATTING REQUIREMENTS:
- Use structured formats: tables, bullet lists, metric summaries
- Present metrics with proper precision (e.g., R² = 0.847, not "about 0.85")
- Group related metrics together
- Use clear metric labels and definitions
- Make results easy to scan and compare

TONE REQUIREMENTS:
- Objective and evidence-based
- Confident but not overstating
- Precise with numbers
- Clear about what metrics measure
- Acknowledge limitations when relevant

DO NOT:
- Present metrics without context or interpretation
- Use vague language ("pretty good", "acceptable")
- Overwhelm with too many decimal places
- Hide or downplay poor results
- Make claims not supported by the metrics shown

SLIDE CONTENT TO ANALYZE:
{slide_content}

REFERENCE EXAMPLES FROM PAST DOCUMENTATION:
{rag_results if rag_results else "No reference examples available - use your expertise in statistical reporting and actuarial documentation standards."}

Write the Model Results section now. Focus on presenting clear, quantitative evidence of model performance with proper structure and interpretation."""

    return prompt

def build_model_development_prompt(slide_content: str, rag_results: str) -> str:
    """
    Build prompt for Model Development section - iterative process narrative.
    
    Focus: Process documentation, iterations, decision-making journey.
    Style: Chronological narrative showing how model evolved from initial to final.
    """
    
    prompt = f"""You are a senior actuary and model developer documenting the model development process for regulatory review and knowledge transfer.

AUDIENCE: Actuaries, auditors, and future model developers who need to understand the development journey, not just the final model.

SECTION PURPOSE:
Document the iterative process of developing the model, including initial approaches, refinements, challenges encountered, and rationale for key decisions. This creates a clear audit trail and knowledge base.

YOUR TASK:
Write a comprehensive Model Development section (700-900 words) that tells the story of how the model evolved from concept to final implementation.

REQUIRED COMPONENTS:

1. INITIAL MODEL DEVELOPMENT (2-3 paragraphs)
   - Starting point: baseline model or initial approach
   - Initial variable set and methodology choices
   - Preliminary results from first iteration
   - What worked and what needed improvement

2. ITERATIVE REFINEMENTS (3-4 paragraphs)
   - Document 2-3 major iterations or refinement cycles
   - For each iteration, explain:
     * What changes were made (variables added/removed, methodology adjustments)
     * Why these changes were made (data analysis, performance issues, business feedback)
     * Impact of changes on model performance
     * Key learnings from each iteration
   
3. CHALLENGES AND SOLUTIONS (2 paragraphs)
   - Technical challenges encountered (convergence issues, data quality, multicollinearity)
   - How challenges were addressed
   - Trade-offs considered
   - Alternative approaches tested but not selected

4. FINAL MODEL CONFIGURATION (1-2 paragraphs)
   - How final model differs from initial version
   - Key decisions that shaped the final specification
   - Rationale for final variable set and methodology
   - Validation of final choices

NARRATIVE STYLE REQUIREMENTS:
- Use chronological/iterative flow: "Initially... then... subsequently... finally..."
- Show progression: "Version 1.0 → Version 1.1 → Version 2.0 → Final"
- Explain causation: "Because X showed Y, we decided to Z"
- Balance detail with readability
- Make the development process transparent and logical

TONE REQUIREMENTS:
- Reflective and analytical
- Honest about challenges (not everything worked perfectly)
- Emphasize learning and continuous improvement
- Show thoughtful decision-making
- Professional but narrative (telling a story)

DO NOT:
- Just list changes without explaining why
- Hide failed attempts or challenges
- Make it read like a timeline (use narrative prose)
- Focus only on final model without the journey
- Include excessive technical jargon without context

SLIDE CONTENT TO ANALYZE:
{slide_content}

REFERENCE EXAMPLES FROM PAST DOCUMENTATION:
{rag_results if rag_results else "No reference examples available - use your expertise in model development documentation and actuarial standards."}

Write the Model Development section now. Focus on telling the clear, logical story of how the model evolved through iterations to reach its final form."""

    return prompt

def build_validation_prompt(slide_content: str, rag_results: str) -> str:
    """
    Build prompt for Validation section - testing procedures and evidence.
    
    Focus: Systematic testing, evidence presentation, audit trail.
    Style: Structured procedures with quantitative results and pass/fail evidence.
    """
    
    prompt = f"""You are a senior model validator and quality assurance specialist documenting validation testing for regulatory review and audit purposes.

AUDIENCE: Regulatory auditors, compliance teams, and validation specialists who need to verify the model was properly tested and meets quality standards.

SECTION PURPOSE:
Document the comprehensive validation testing performed on the model, providing clear evidence that the model is fit for purpose, performs as expected, and meets all technical and business requirements.

YOUR TASK:
Write a comprehensive Validation section (800-900 words) that documents the testing procedures, presents evidence systematically, and demonstrates model reliability.

REQUIRED COMPONENTS:

1. VALIDATION FRAMEWORK (2 paragraphs)
   - Overview of validation approach and methodology
   - Types of testing performed (statistical, business logic, implementation)
   - Validation standards and criteria used
   - Independent review process if applicable

2. STATISTICAL VALIDATION (3-4 paragraphs)
   For each major test, document:
   - Test name and purpose
   - Testing methodology and data used
   - Quantitative results and metrics
   - Pass/fail criteria and whether met
   - Key findings
   
   Include tests such as:
   - Out-of-sample testing
   - Backtesting across time periods
   - Stability testing
   - Sensitivity analysis
   - Goodness-of-fit tests

3. BUSINESS LOGIC VALIDATION (2 paragraphs)
   - Reasonability of predictions across segments
   - Alignment with underwriting expectations
   - Comparison to actual experience
   - Edge case testing
   - Monotonicity and directionality checks

4. IMPLEMENTATION VALIDATION (1-2 paragraphs)
   - Code review and testing procedures
   - Calculation verification
   - System integration testing
   - Reproducibility checks
   - Documentation completeness

5. VALIDATION RESULTS SUMMARY (1-2 paragraphs)
   - Overall validation conclusion
   - Any issues identified and resolutions
   - Model limitations and appropriate use cases
   - Recommendation for deployment/approval

FORMATTING REQUIREMENTS:
- Use structured format for test procedures (bullet lists work well)
- Present results with metrics and pass/fail indicators
- Group related tests together logically
- Make the audit trail clear and easy to follow
- Use specific numbers and evidence, not vague statements

TONE REQUIREMENTS:
- Systematic and thorough
- Evidence-based (show, don't just tell)
- Objective about results (report failures honestly)
- Confident in conclusions when evidence supports them
- Professional validation terminology

DO NOT:
- Skip documenting any major validation test
- Present opinions without supporting evidence
- Hide or minimize validation failures
- Use vague language like "the model seems fine"
- Make validation claims without showing the test results

SLIDE CONTENT TO ANALYZE:
{slide_content}

REFERENCE EXAMPLES FROM PAST DOCUMENTATION:
{rag_results if rag_results else "No reference examples available - use your expertise in model validation standards and actuarial documentation requirements."}

Write the Validation section now. Focus on creating a clear audit trail with systematic testing procedures and quantitative evidence of model reliability."""

    return prompt

def build_business_context_prompt(slide_content: str, rag_results: str) -> str:
    """
    Build prompt for Business Context section - strategic overview and background.
    
    Focus: Strategic rationale, organizational context, business drivers.
    Style: High-level business narrative for leadership and stakeholders.
    """
    
    prompt = f"""You are a senior business strategist and actuarial leader documenting the business context and strategic rationale for a model development initiative.

AUDIENCE: Executive leadership, business stakeholders, and future readers who need to understand the strategic business context and organizational drivers behind the model.

SECTION PURPOSE:
Provide the strategic context and business rationale that explains why this model was developed, how it supports organizational objectives, and what business value it delivers. This section frames the entire documentation in business terms.

YOUR TASK:
Write a comprehensive Business Context section (600-700 words) that provides strategic framing and organizational background for the model initiative.

REQUIRED COMPONENTS:

1. BUSINESS DRIVERS AND NEEDS (2-3 paragraphs)
   - What business challenges or opportunities prompted model development
   - Market conditions or competitive pressures
   - Regulatory or compliance requirements driving the need
   - Pain points with previous approaches or legacy systems
   - Strategic imperatives from leadership

2. ORGANIZATIONAL CONTEXT (1-2 paragraphs)
   - Relevant background about the organization and business unit
   - Portfolio characteristics and market position
   - Historical approach to the business problem
   - Why this initiative was prioritized and resourced
   - Stakeholder support and sponsorship

3. STRATEGIC OBJECTIVES (2 paragraphs)
   - Primary business goals the model aims to achieve
   - Expected benefits and value creation
   - How model supports broader organizational strategy
   - Success criteria from a business perspective
   - Alignment with company priorities and initiatives

4. IMPLEMENTATION AND BUSINESS INTEGRATION (1-2 paragraphs)
   - How the model will be operationalized
   - Business processes that will use the model
   - Integration with existing systems and workflows
   - Change management considerations
   - Timeline and rollout approach

5. FUTURE OUTLOOK (1 paragraph)
   - Next steps and future enhancements
   - Planned refinements or expansions
   - How model will evolve with business needs
   - Long-term vision and sustainability

TONE REQUIREMENTS:
- Strategic and business-focused (not overly technical)
- Forward-looking and positive
- Clear about business value and benefits
- Appropriate for executive consumption
- Professional yet accessible

STYLE REQUIREMENTS:
- High-level overview, not technical details
- Focus on "why" and "what business value" not "how technically"
- Connect to business strategy and objectives
- Show alignment with organizational priorities
- Emphasize practical business impact

DO NOT:
- Include technical modeling details (save for other sections)
- Use excessive actuarial jargon
- Focus on statistical methods
- Make it read like methodology documentation
- Lose sight of the business perspective

SLIDE CONTENT TO ANALYZE:
{slide_content}

REFERENCE EXAMPLES FROM PAST DOCUMENTATION:
{rag_results if rag_results else "No reference examples available - use your expertise in business documentation and strategic communication."}

Write the Business Context section now. Focus on providing clear strategic framing that helps readers understand the business rationale and organizational context for the model."""

    return prompt