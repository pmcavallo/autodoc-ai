"""
Writer Agent for AutoDoc AI

This agent is responsible for generating documentation sections based on
research findings and established templates/standards.

Key Responsibilities:
- Generate documentation sections with proper structure
- Follow established templates and style guides
- Incorporate research findings with citations
- Maintain professional actuarial tone
- Ensure consistency with existing documentation

Usage:
    from agents.writer_agent import WriterAgent

    agent = WriterAgent()
    section = agent.write_section(
        section_title="Model Validation",
        context=research_context,
        template="validation_section"
    )
"""

from pathlib import Path
from typing import List, Dict, Optional, Any
import logging
from dataclasses import dataclass
from datetime import datetime
from agents.prompts import (
    build_executive_summary_prompt,
    build_methodology_prompt,
    build_data_sources_prompt,
    build_variable_selection_prompt,
    build_model_results_prompt,  # Add this line
    build_model_development_prompt,  # Add this line
    build_validation_prompt,  # Add this line
    build_business_context_prompt,  # Add this line
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================
# FIXED VERSION: All methods now accept source_content parameter
# and require using actual data from source documents
# ============================================================


@dataclass
class SectionContent:
    """
    Represents generated documentation section content.
    """
    title: str
    content: str
    template_used: Optional[str] = None
    sources_cited: List[str] = None
    word_count: int = 0
    metadata: Dict = None

    def __post_init__(self):
        """Calculate word count and initialize metadata."""
        self.word_count = len(self.content.split())
        if self.sources_cited is None:
            self.sources_cited = []
        if self.metadata is None:
            self.metadata = {}

    def format_markdown(self) -> str:
        """Format section as markdown."""
        lines = [
            f"## {self.title}",
            "",
            self.content,
            ""
        ]
        return "\n".join(lines)


class DocumentTemplate:
    """
    Templates for common documentation sections.

    In production, these would be loaded from configuration files
    or a template database. For now, they're defined as class attributes.
    """

    EXECUTIVE_SUMMARY = """
This section should provide a high-level overview including:
- Purpose and scope of the model
- Key methodology and techniques used
- Main findings and results
- Business impact and recommendations
"""

    METHODOLOGY = """
This section should describe:
- Modeling approach and rationale
- Data sources and preparation
- Feature engineering and selection
- Model training and hyperparameter tuning
- Technical implementation details
"""

    VALIDATION = """
This section should cover:
- Validation framework and procedures
- Performance metrics and results
- Holdout testing and cross-validation
- Model stability and robustness checks
- Comparison to benchmarks or previous models
"""

    RESULTS = """
This section should present:
- Key performance metrics
- Model coefficients and variable importance
- Lift charts and diagnostic plots
- Comparison to business expectations
- Limitations and considerations
"""

    IMPLEMENTATION = """
This section should detail:
- Production deployment approach
- Integration with existing systems
- Monitoring and alerting procedures
- Maintenance and refresh schedule
- Documentation and handoff procedures
"""

    REGULATORY_COMPLIANCE = """
This section should address:
- Applicable regulatory requirements
- Compliance with actuarial standards (ASOPs)
- Model governance and oversight
- Audit trail and documentation
- Risk management considerations
"""

    @classmethod
    def get_template(cls, template_name: str) -> str:
        """Get template by name."""
        template_map = {
            "executive_summary": cls.EXECUTIVE_SUMMARY,
            "methodology": cls.METHODOLOGY,
            "validation": cls.VALIDATION,
            "results": cls.RESULTS,
            "implementation": cls.IMPLEMENTATION,
            "regulatory_compliance": cls.REGULATORY_COMPLIANCE,
        }
        return template_map.get(template_name.lower(), "")


class WriterAgent:
    """
    Agent for generating documentation content.

    This agent:
    1. Accepts writing requests with context and templates
    2. Generates structured documentation sections
    3. Incorporates research findings and citations
    4. Maintains consistent style and terminology
    5. Follows professional actuarial standards
    """

    def __init__(
            self,
            default_style: str = "professional_actuarial",
            include_citations: bool = True
        ):
            """
            Initialize the writer agent.

            Args:
                default_style: Writing style to use
                include_citations: Whether to include source citations
            """
            self.default_style = default_style
            self.include_citations = include_citations

            logger.info(f"WriterAgent initialized with style: {default_style}")


    def write_executive_summary(
        self,
        model_type: str,
        key_findings: str,
        context: str,
        source_content: str = ""
    ) -> SectionContent:
        """
        Generate an executive summary section.

        Args:
            model_type: Type of model (e.g., "frequency", "XGBoost")
            key_findings: Key findings to highlight
            context: Research context

        Returns:
            SectionContent object
        """
        logger.info(f"Writing Executive Summary for {model_type} model")

        try:
            from anthropic import Anthropic
            import os
            from .prompts import build_executive_summary_prompt

            # Combine model_type and key_findings into slide_content format
            slide_content = f"Model Type: {model_type}\n\nKey Findings:\n{key_findings}"

            # Build prompt WITH source content requirements
            prompt = f"""Write a comprehensive executive summary for a {model_type} model.

            CRITICAL REQUIREMENTS - YOU MUST FOLLOW THESE:
            1. Use ONLY specific facts, numbers, and metrics from the SOURCE DOCUMENT below
            2. Include ALL sample sizes, performance metrics, system names, dates, and geographic details
            3. Do NOT invent or estimate any quantitative data
            4. Every specific number in your response MUST come from the source document
            5. Preserve exact statistical measures (R², AUC, Gini, MAPE, sample sizes, etc.)
            6. Include specific system names and data sources mentioned in the source

            SOURCE DOCUMENT (use these specific facts):
            {source_content}

            Additional Context for Structure (optional reference only):
            {context}

            Generate an executive summary that includes:
            - Model purpose (with specific business systems and data sources from SOURCE)
            - Methodology overview (with exact sample sizes and time periods from SOURCE)
            - Key findings (with precise performance metrics from SOURCE)
            - Business impact (with quantitative improvements from SOURCE)

            Remember: ALL numbers and specific facts must come from the SOURCE DOCUMENT above.
            If a metric like "R² 0.52" appears in the source, it MUST appear in your output.
            """

            # Initialize client
            client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

            # Call Claude with appropriate parameters for executive summary
            logger.info("Calling Claude API for Executive Summary section")
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,  # Shorter section: 400-600 words
                temperature=0.3,  # Precision for executive communication
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            content = response.content[0].text

            logger.info(f"Executive Summary section generated: {len(content.split())} words, "
                    f"{response.usage.input_tokens} input tokens, "
                    f"{response.usage.output_tokens} output tokens")

            return SectionContent(
                title="Executive Summary",
                content=content,
                template_used="executive_summary",
                sources_cited=[],
                word_count=len(content.split()),
                metadata={
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens,
                    'model': 'claude-sonnet-4-20250514'
                }
            )

        except Exception as e:
            logger.error(f"Error generating Executive Summary section: {e}")

            # Fallback to placeholder
            placeholder = f"""# Executive Summary

This section provides an overview of the {model_type} model.

{key_findings}

[This is placeholder content. The actual implementation would call an LLM to generate detailed executive summary.]
"""

            return SectionContent(
                title="Executive Summary",
                content=placeholder,
                template_used="executive_summary",
                sources_cited=[],
                word_count=len(placeholder.split())
            )

    def write_methodology_section(
        self,
        model_type: str,
        methodology_details: str,
        context: str,
        source_content: str = ""
    ) -> SectionContent:
        """
        Generate methodology section with technical depth.
        
        This section requires more tokens and technical detail than executive summary.
        
        Args:
            model_type: Type of model (e.g., "frequency", "severity")
            methodology_details: Technical details about the model
            context: RAG-retrieved examples from past methodology sections
        
        Returns:
            SectionContent with generated methodology
        """
        logger.info("Writing Methodology section")
        
        try:
            from anthropic import Anthropic
            import os
            from .prompts import build_methodology_prompt
            
            # Build specialized methodology prompt
            prompt = build_methodology_prompt(model_type, methodology_details, context)
            
            # Build prompt WITH source content requirements
            prompt = f"""Write a comprehensive methodology section for a {model_type} model.

            CRITICAL REQUIREMENTS - YOU MUST FOLLOW THESE:
            1. Use ONLY specific facts, numbers, and metrics from the SOURCE DOCUMENT below
            2. Include ALL sample sizes, methodological details, and statistical specifications
            3. Do NOT invent or estimate any quantitative data
            4. Every specific number in your response MUST come from the source document
            5. Preserve exact model specifications, algorithms, and parameters mentioned
            6. Include specific techniques and approaches mentioned in the source

            SOURCE DOCUMENT (use these specific facts):
            {source_content}

            Additional Context for Structure (optional reference only):
            {context}

            Generate a methodology section that includes:
            - Model framework (with exact algorithms and specifications from SOURCE)
            - Predictor variables (with specific variable names and counts from SOURCE)
            - Estimation method (with exact techniques mentioned in SOURCE)
            - Model assumptions (with specific assumptions stated in SOURCE)

            Remember: ALL technical specifications must come from the SOURCE DOCUMENT above.
            """
            
            # Initialize client
            client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

            # Call Claude with higher max_tokens for longer content
            logger.info("Calling Claude API for Methodology section")
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=3000,  # Increased for longer technical content
                temperature=0.3,  # Still precise for technical accuracy
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            content = response.content[0].text
            
            logger.info(f"Methodology section generated: {len(content.split())} words, "
                    f"{response.usage.input_tokens} input tokens, "
                    f"{response.usage.output_tokens} output tokens")
            
            return SectionContent(
                title="Methodology",
                content=content,
                template_used="methodology",
                sources_cited=[],
                word_count=len(content.split()),
                metadata={
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens,
                    'model': 'claude-sonnet-4-20250514'
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating Methodology section: {e}")
            
            # Fallback to placeholder
            placeholder = f"""# Methodology

    This section describes the technical approach used for the {model_type} model.

    Model Framework:
    The model employs standard statistical techniques appropriate for {model_type} modeling.

    {methodology_details}

    [This is placeholder content. The actual implementation would call an LLM to generate detailed methodology.]
    """
            
            return SectionContent(
                title="Methodology",
                content=placeholder,
                template_used="methodology",
                sources_cited=[],
                word_count=len(placeholder.split())
            )
        
    def write_data_sources_section(
        self,
        model_type: str,
        data_details: str,
        context: str,
        source_content: str = ""
    ) -> SectionContent:
        """
        Generate data sources section with structured content.
        
        This section uses structured formatting (lists, categories) rather than
        pure narrative prose.
        
        Args:
            model_type: Type of model (e.g., "frequency", "severity")
            data_details: Details about data sources
            context: RAG-retrieved examples
        
        Returns:
            SectionContent with data sources documentation
        """
        logger.info("Writing Data Sources and Quality section")
        
        try:
            from anthropic import Anthropic
            import os
            from .prompts import build_data_sources_prompt
            
            # Build specialized data sources prompt
            # Build prompt WITH source content requirements
            prompt = f"""Write a comprehensive data sources section for a {model_type} model.

            CRITICAL REQUIREMENTS - YOU MUST FOLLOW THESE:
            1. Use ONLY specific facts, numbers, and metrics from the SOURCE DOCUMENT below
            2. Include ALL system names, data periods, sample sizes, and data sources
            3. Do NOT invent or estimate any quantitative data
            4. Every specific number in your response MUST come from the source document
            5. Preserve exact system names, database names, and data collection details
            6. Include specific geographic regions and time periods from the source

            SOURCE DOCUMENT (use these specific facts):
            {source_content}

            Additional Context for Structure (optional reference only):
            {context}

            Generate a data sources section that includes:
            - Data overview (with exact time periods and sample sizes from SOURCE)
            - Internal data sources (with specific system names from SOURCE)
            - External data sources (with specific sources mentioned in SOURCE)
            - Data quality (with specific quality metrics from SOURCE)

            Remember: ALL data specifications must come from the SOURCE DOCUMENT above.
            """
            
            # Initialize client
            client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            
            # Call Claude (medium length section)
            logger.info("Calling Claude API for Data Sources section")
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2500,  # Medium length: between exec summary and methodology
                temperature=0.3,  # Precision for factual data
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            content = response.content[0].text
            
            logger.info(f"Data Sources section generated: {len(content.split())} words, "
                    f"{response.usage.input_tokens} input tokens, "
                    f"{response.usage.output_tokens} output tokens")
            
            return SectionContent(
                title="Data Sources and Quality",
                content=content,
                template_used="data_sources",
                sources_cited=[],
                word_count=len(content.split()),
                metadata={
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens,
                    'model': 'claude-sonnet-4-20250514'
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating Data Sources section: {e}")
            
            # Fallback
            placeholder = f"""# Data Sources and Quality

    This section documents the data sources used for the {model_type} model.

    Data Overview:
    The model uses internal policy and claims data.

    {data_details}

    [This is placeholder content. The actual implementation would call an LLM to generate detailed data documentation.]
    """
            
            return SectionContent(
                title="Data Sources and Quality",
                content=placeholder,
                template_used="data_sources",
                sources_cited=[],
                word_count=len(placeholder.split())
            )   

    def write_variable_selection_section(
        self,
        model_type: str,
        variable_details: str,
        context: str,
        source_content: str = ""
    ) -> SectionContent:
        """
        Generate variable selection section with statistical justification.
        
        This section emphasizes reasoning and justification for variable choices,
        requiring persuasive technical writing.
        
        Args:
            model_type: Type of model (e.g., "frequency", "severity")
            variable_details: Details about variable selection process
            context: RAG-retrieved examples
        
        Returns:
            SectionContent with variable selection documentation
        """
        logger.info("Writing Variable Selection and Justification section")
        
        try:
            from anthropic import Anthropic
            import os
            from .prompts import build_variable_selection_prompt
            
            # Build specialized variable selection prompt
            # Build prompt WITH source content requirements
            prompt = f"""Write a comprehensive variable selection section for a {model_type} model.

            CRITICAL REQUIREMENTS - YOU MUST FOLLOW THESE:
            1. Use ONLY specific facts, numbers, and metrics from the SOURCE DOCUMENT below
            2. Include ALL predictor counts, variable names, and selection criteria
            3. Do NOT invent or estimate any quantitative data
            4. Every specific number in your response MUST come from the source document
            5. Preserve exact variable names, counts, and statistical significance levels
            6. Include specific selection methodologies mentioned in the source

            SOURCE DOCUMENT (use these specific facts):
            {source_content}

            Additional Context for Structure (optional reference only):
            {context}

            Generate a variable selection section that includes:
            - Variable selection process (with exact methods from SOURCE)
            - Candidate variables (with specific variable counts from SOURCE)
            - Final model variables (with exact variable names and counts from SOURCE)
            - Statistical significance (with specific p-values or criteria from SOURCE)

            Remember: ALL variable specifications must come from the SOURCE DOCUMENT above.
            """
            
            # Initialize client
            client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            
            # Call Claude (medium-long length)
            logger.info("Calling Claude API for Variable Selection section")
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2800,  # Medium-long: between data sources and methodology
                temperature=0.3,  # Precision for statistical arguments
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            content = response.content[0].text
            
            logger.info(f"Variable Selection section generated: {len(content.split())} words, "
                    f"{response.usage.input_tokens} input tokens, "
                    f"{response.usage.output_tokens} output tokens")
            
            return SectionContent(
                title="Variable Selection and Justification",
                content=content,
                template_used="variable_selection",
                sources_cited=[],
                word_count=len(content.split()),
                metadata={
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens,
                    'model': 'claude-sonnet-4-20250514'
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating Variable Selection section: {e}")
            
            # Fallback
            placeholder = f"""# Variable Selection and Justification

    This section explains the rationale for variable selection in the {model_type} model.

    Selection Process:
    Variables were selected based on statistical significance and business relevance.

    {variable_details}

    [This is placeholder content. The actual implementation would call an LLM to generate detailed justification.]
    """
            
            return SectionContent(
                title="Variable Selection and Justification",
                content=placeholder,
                template_used="variable_selection",
                sources_cited=[],
                word_count=len(placeholder.split())
            )
        
    def write_model_results_section(
            self,
            slide_content: str,
            context: str
        ) -> SectionContent:
            """
            Generate Model Results section with quantitative performance metrics.
            
            This section presents statistical evidence in structured format.
            
            Args:
                slide_content: Extracted text from PowerPoint slides
                context: RAG-retrieved examples from past model results sections
                
            Returns:
                SectionContent with model results documentation
            """
            logger.info("Writing Model Results section")
            
            try:
                from anthropic import Anthropic
                import os
                from .prompts import build_model_results_prompt
                
                # Build specialized model results prompt
                # Build prompt WITH source content requirements
                prompt = f"""Write a comprehensive model results section.

                CRITICAL REQUIREMENTS - YOU MUST FOLLOW THESE:
                1. Use ONLY specific facts, numbers, and metrics from the SOURCE DOCUMENT below
                2. Include ALL performance metrics, statistical measures, and result values
                3. Do NOT invent or estimate any quantitative data
                4. Every specific number in your response MUST come from the source document
                5. Preserve exact R², AUC, Gini, MAPE, lift, and all other metrics
                6. Include specific improvement percentages and comparison values

                SOURCE DOCUMENT (use these specific facts):
                {source_content}

                Additional Context for Structure (optional reference only):
                {context}

                Generate a model results section that includes:
                - Performance metrics (with exact values from SOURCE)
                - Model coefficients (with specific values from SOURCE)
                - Lift analysis (with exact lift percentages from SOURCE)
                - Comparison to benchmarks (with specific improvement percentages from SOURCE)

                Remember: ALL performance numbers must come from the SOURCE DOCUMENT above.
                If "AUC: 0.72" appears in source, it MUST appear as "AUC: 0.72" in output.
                """
                
                # Initialize client
                client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                
                # Call Claude (medium-long section with metrics)
                logger.info("Calling Claude API for Model Results section")
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=3000,  # Allow room for structured content
                    temperature=0.3,  # Precision for metrics
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                
                content = response.content[0].text
                
                logger.info(f"Model Results section generated: {len(content.split())} words, "
                        f"{response.usage.input_tokens} input tokens, "
                        f"{response.usage.output_tokens} output tokens")
                
                return SectionContent(
                    title="Model Results",
                    content=content,
                    template_used="model_results",
                    sources_cited=[],
                    word_count=len(content.split()),
                    metadata={
                        'input_tokens': response.usage.input_tokens,
                        'output_tokens': response.usage.output_tokens,
                        'model': 'claude-sonnet-4-20250514'
                    }
                )
            
            except Exception as e:
                logger.error(f"Error generating Model Results section: {e}")
                
                # Fallback
                return SectionContent(
                    title="Model Results",
                    content=f"Error generating section: {str(e)}",
                    template_used="model_results",
                    sources_cited=[],
                    word_count=0,
                    metadata={}
                )
            
    def write_model_development_section(
            self,
            slide_content: str,
            context: str
        ) -> SectionContent:
            """
            Generate Model Development section with iterative process narrative.
            
            This section documents the development journey and iterations.
            
            Args:
                slide_content: Details about model development process
                context: RAG-retrieved examples from past development sections
                
            Returns:
                SectionContent with model development documentation
            """
            logger.info("Writing Model Development section")
            
            try:
                from anthropic import Anthropic
                import os
                from .prompts import build_model_development_prompt
                
                # Build specialized model development prompt
                # Build prompt WITH source content requirements
                prompt = f"""Write a comprehensive model development section.

                CRITICAL REQUIREMENTS - YOU MUST FOLLOW THESE:
                1. Use ONLY specific facts, numbers, and metrics from the SOURCE DOCUMENT below
                2. Include ALL development timeline details, iterations, and decisions
                3. Do NOT invent or estimate any quantitative data
                4. Every specific number in your response MUST come from the source document
                5. Preserve exact dates, version numbers, and development milestones
                6. Include specific development challenges and solutions from the source

                SOURCE DOCUMENT (use these specific facts):
                {source_content}

                Additional Context for Structure (optional reference only):
                {context}

                Generate a model development section that includes:
                - Development timeline (with exact dates and milestones from SOURCE)
                - Model iterations (with specific version numbers from SOURCE)
                - Key decisions (with rationale mentioned in SOURCE)
                - Challenges and solutions (with specific issues from SOURCE)

                Remember: ALL development details must come from the SOURCE DOCUMENT above.
                """
                
                # Initialize client
                client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                
                # Call Claude (medium-long section)
                logger.info("Calling Claude API for Model Development section")
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=3000,  # Allow for detailed process narrative
                    temperature=0.3,  # Precision for process documentation
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                
                content = response.content[0].text
                
                logger.info(f"Model Development section generated: {len(content.split())} words, "
                        f"{response.usage.input_tokens} input tokens, "
                        f"{response.usage.output_tokens} output tokens")
                
                return SectionContent(
                    title="Model Development",
                    content=content,
                    template_used="model_development",
                    sources_cited=[],
                    word_count=len(content.split()),
                    metadata={
                        'input_tokens': response.usage.input_tokens,
                        'output_tokens': response.usage.output_tokens,
                        'model': 'claude-sonnet-4-20250514'
                    }
                )
                
            except Exception as e:
                logger.error(f"Error generating Model Development section: {e}")
                
                # Fallback
                return SectionContent(
                    title="Model Development",
                    content=f"Error generating section: {str(e)}",
                    template_used="model_development",
                    sources_cited=[],
                    word_count=0,
                    metadata={}
                )
            
    def write_validation_section(
            self,
            slide_content: str,
            context: str
        ) -> SectionContent:
            """
            Generate Validation section with testing procedures and evidence.
            
            This section documents systematic validation testing with audit trail.
            
            Args:
                slide_content: Details about validation testing performed
                context: RAG-retrieved examples from past validation sections
                
            Returns:
                SectionContent with validation documentation
            """
            logger.info("Writing Validation section")
            
            try:
                from anthropic import Anthropic
                import os
                from .prompts import build_validation_prompt
                
                # Build specialized validation prompt
                # Build prompt WITH source content requirements
                prompt = f"""Write a comprehensive validation section.

                CRITICAL REQUIREMENTS - YOU MUST FOLLOW THESE:
                1. Use ONLY specific facts, numbers, and metrics from the SOURCE DOCUMENT below
                2. Include ALL validation metrics, test results, and performance measures
                3. Do NOT invent or estimate any quantitative data
                4. Every specific number in your response MUST come from the source document
                5. Preserve exact holdout test results, cross-validation scores, and stability metrics
                6. Include specific validation methodologies and sample sizes from the source

                SOURCE DOCUMENT (use these specific facts):
                {source_content}

                Additional Context for Structure (optional reference only):
                {context}

                Generate a validation section that includes:
                - Validation framework (with exact methodology from SOURCE)
                - Performance metrics (with specific test set results from SOURCE)
                - Holdout testing (with exact sample sizes and results from SOURCE)
                - Stability analysis (with specific stability metrics from SOURCE)

                Remember: ALL validation numbers must come from the SOURCE DOCUMENT above.
                If "holdout AUC: 0.71" appears in source, it MUST appear in output.
                """
                
                # Initialize client
                client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                
                # Call Claude (longer section with detailed procedures)
                logger.info("Calling Claude API for Validation section")
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=3000,  # Allow for comprehensive validation documentation
                    temperature=0.3,  # Precision for test procedures and evidence
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                
                content = response.content[0].text
                
                logger.info(f"Validation section generated: {len(content.split())} words, "
                        f"{response.usage.input_tokens} input tokens, "
                        f"{response.usage.output_tokens} output tokens")
                
                return SectionContent(
                    title="Validation",
                    content=content,
                    template_used="validation",
                    sources_cited=[],
                    word_count=len(content.split()),
                    metadata={
                        'input_tokens': response.usage.input_tokens,
                        'output_tokens': response.usage.output_tokens,
                        'model': 'claude-sonnet-4-20250514'
                    }
                )
                
            except Exception as e:
                logger.error(f"Error generating Validation section: {e}")
                
                # Fallback
                return SectionContent(
                    title="Validation",
                    content=f"Error generating section: {str(e)}",
                    template_used="validation",
                    sources_cited=[],
                    word_count=0,
                    metadata={}
                )
            
    def write_business_context_section(
            self,
            slide_content: str,
            context: str
        ) -> SectionContent:
            """
            Generate Business Context section with strategic overview and background.
            
            This section provides high-level business framing and rationale.
            
            Args:
                slide_content: Business context and strategic information
                context: RAG-retrieved examples from past business context sections
                
            Returns:
                SectionContent with business context documentation
            """
            logger.info("Writing Business Context section")
            
            try:
                from anthropic import Anthropic
                import os
                from .prompts import build_business_context_prompt
                
                # Build specialized business context prompt
                # Build prompt WITH source content requirements
                prompt = f"""Write a comprehensive business context section.

                CRITICAL REQUIREMENTS - YOU MUST FOLLOW THESE:
                1. Use ONLY specific facts, numbers, and metrics from the SOURCE DOCUMENT below
                2. Include ALL business impact metrics, implementation details, and ROI figures
                3. Do NOT invent or estimate any quantitative data
                4. Every specific number in your response MUST come from the source document
                5. Preserve exact cost savings, efficiency gains, and business metrics
                6. Include specific implementation timelines and business units from the source

                SOURCE DOCUMENT (use these specific facts):
                {source_content}

                Additional Context for Structure (optional reference only):
                {context}

                Generate a business context section that includes:
                - Business objectives (with specific goals from SOURCE)
                - Implementation approach (with exact timeline and phases from SOURCE)
                - Expected impact (with specific ROI and metrics from SOURCE)
                - Stakeholder considerations (with specific groups mentioned in SOURCE)

                Remember: ALL business metrics must come from the SOURCE DOCUMENT above.
                """
                
                # Initialize client
                client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                
                # Call Claude (shorter section, strategic overview)
                logger.info("Calling Claude API for Business Context section")
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=2500,  # Shorter section focused on business overview
                    temperature=0.3,  # Precision for strategic communication
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                
                content = response.content[0].text
                
                logger.info(f"Business Context section generated: {len(content.split())} words, "
                        f"{response.usage.input_tokens} input tokens, "
                        f"{response.usage.output_tokens} output tokens")
                
                return SectionContent(
                    title="Business Context",
                    content=content,
                    template_used="business_context",
                    sources_cited=[],
                    word_count=len(content.split()),
                    metadata={
                        'input_tokens': response.usage.input_tokens,
                        'output_tokens': response.usage.output_tokens,
                        'model': 'claude-sonnet-4-20250514'
                    }
                )
                
            except Exception as e:
                logger.error(f"Error generating Business Context section: {e}")
                
                # Fallback
                return SectionContent(
                    title="Business Context",
                    content=f"Error generating section: {str(e)}",
                    template_used="business_context",
                    sources_cited=[],
                    word_count=0,
                    metadata={}
                )
        
    def write_regulatory_compliance_section(
        self,
        compliance_context: str,
        applicable_standards: Optional[List[str]] = None
    ) -> SectionContent:
        """
        Generate a regulatory compliance section.

        Args:
            compliance_context: Research context on compliance
            applicable_standards: List of applicable standards (ASOPs, regulations)

        Returns:
            SectionContent object
        """
        full_context = compliance_context

        if applicable_standards:
            standards_text = "\n".join([f"- {std}" for std in applicable_standards])
            full_context += f"\n\nApplicable Standards:\n{standards_text}"

        return self.write_section(
            section_title="Regulatory Compliance",
            context=full_context,
            template="regulatory_compliance",
            length_target="medium"
        )

    def write_custom_section(
        self,
        title: str,
        context: str,
        custom_instructions: str
    ) -> SectionContent:
        """
        Generate a custom section with specific instructions.

        Args:
            title: Section title
            context: Research context
            custom_instructions: Specific writing instructions

        Returns:
            SectionContent object
        """
        return self.write_section(
            section_title=title,
            context=context,
            template=None,
            custom_instructions=custom_instructions
        )

    def revise_section(
        self,
        original_content: SectionContent,
        revision_instructions: str,
        additional_context: Optional[str] = None
    ) -> SectionContent:
        """
        Revise an existing section based on feedback.

        Args:
            original_content: Original SectionContent object
            revision_instructions: Instructions for revision
            additional_context: Additional context for revision

        Returns:
            Revised SectionContent object
        """
        logger.info(f"Revising section: '{original_content.title}'")

        # In production, this would use an LLM with:
        # - Original content
        # - Revision instructions
        # - Additional context

        # Placeholder: Add revision marker
        revised_content = f"{original_content.content}\n\n[REVISED: {revision_instructions}]"

        if additional_context:
            revised_content += f"\n\n[Additional Context: {additional_context[:100]}...]"

        return SectionContent(
            title=original_content.title,
            content=revised_content,
            template_used=original_content.template_used,
            sources_cited=original_content.sources_cited,
            metadata={"revision": revision_instructions}
        )

    def combine_sections(
        self,
        sections: List[SectionContent],
        document_title: str,
        frontmatter: Optional[Dict] = None
    ) -> str:
        """
        Combine multiple sections into a complete document.

        Args:
            sections: List of SectionContent objects
            document_title: Overall document title
            frontmatter: Optional YAML frontmatter metadata

        Returns:
            Complete document as markdown string
        """
        logger.info(f"Combining {len(sections)} sections into document: '{document_title}'")

        parts = []

        # Add frontmatter if provided
        if frontmatter:
            parts.append("---")
            for key, value in frontmatter.items():
                parts.append(f"{key}: {value}")
            parts.append("---")
            parts.append("")

        # Add title
        parts.append(f"# {document_title}")
        parts.append("")

        # Add synthetic data disclaimer
        parts.append("**SYNTHETIC DATA DISCLAIMER**")
        parts.append("*This document contains synthetic data generated for demonstration purposes only. "
                    "All company names, personnel, data, and results are fictional.*")
        parts.append("")

        # Add sections
        for section in sections:
            parts.append(section.format_markdown())

        # Add sources cited
        all_sources = set()
        for section in sections:
            all_sources.update(section.sources_cited)

        if all_sources:
            parts.append("## References")
            parts.append("")
            parts.append("This document references the following source materials:")
            parts.append("")
            for source in sorted(all_sources):
                parts.append(f"- {source}")
            parts.append("")

        document = "\n".join(parts)
        logger.info(f"Document created: {len(document)} characters, {len(sections)} sections")

        return document


    def _extract_sources(self, context: str) -> List[str]:
        """
        Extract source citations from context string.

        Args:
            context: Context string with citations

        Returns:
            List of unique source filenames
        """
        sources = []

        # Simple extraction of [filename:section] citations
        import re
        citations = re.findall(r'\[([^\]]+\.md):[^\]]+\]', context)
        sources = list(set(citations))

        return sources

    def write_section(
        self,
        section_title: str,
        context: str,
        source_content: str = "",
        template: str = None,
        length_target: str = "medium",
        custom_instructions: str = None
    ) -> SectionContent:
        """
        Generic section writer that routes to specific section methods.
        This is the interface the orchestrator expects.
        
        CRITICAL: Methods have DIFFERENT signatures!
        - First 4: (model_type, details, context) 
        - Last 4: (slide_content, context)
        
        Args:
            section_title: Name of the section to generate
            context: Context from RAG retrieval
            template: Template type (kept for compatibility)
            length_target: Target length (kept for compatibility)
            custom_instructions: Additional instructions
        
        Returns:
            SectionContent object with generated section
        """
        logger.info(f"Routing '{section_title}' to appropriate section method")
        
        # Extract model type and details from custom_instructions or use defaults
        model_type = "frequency"  # Default, can be extracted from custom_instructions
        details = custom_instructions or f"Documentation for {section_title}"
        
        # For last 4 methods, prepare slide_content dict
        slide_content = {
            'title': section_title,
            'content': details
        }
        
        # Route to the appropriate method with CORRECT signature
        
        if section_title == 'Executive Summary':
            # FIRST 4: Use (model_type, details, context)
            return self.write_executive_summary(model_type, details, context, source_content)
            
        elif section_title == 'Methodology':
            return self.write_methodology_section(model_type, details, context, source_content)
            
        elif section_title == 'Data Sources':
            return self.write_data_sources_section(model_type, details, context, source_content)
            
        elif section_title == 'Variable Selection':
            return self.write_variable_selection_section(model_type, details, context, source_content)
            
        elif section_title == 'Model Results':
            # LAST 4: Use (slide_content, context) 
            return self.write_model_results_section(slide_content, context, source_content)
            
        elif section_title == 'Model Development':
            return self.write_model_development_section(slide_content, context, source_content)
            
        elif section_title == 'Validation':
            return self.write_validation_section(slide_content, context, source_content)
            
        elif section_title == 'Business Context':
            return self.write_business_context_section(slide_content, context, source_content)
            
        else:
            # Try partial matching for alternate names
            section_lower = section_title.lower()
            
            if 'executive' in section_lower or 'summary' in section_lower:
                return self.write_executive_summary(model_type, details, context, source_content)
            elif 'methodology' in section_lower or 'method' in section_lower:
                return self.write_methodology_section(model_type, details, context, source_content)
            elif 'data' in section_lower and 'source' in section_lower:
                return self.write_data_sources_section(model_type, details, context, source_content)
            elif 'variable' in section_lower:
                return self.write_variable_selection_section(model_type, details, context, source_content)
            elif 'result' in section_lower:
                return self.write_model_results_section(slide_content, context, source_content)
            elif 'development' in section_lower:
                return self.write_model_development_section(slide_content, context, source_content)
            elif 'validation' in section_lower:
                return self.write_validation_section(slide_content, context, source_content)
            elif 'business' in section_lower or 'context' in section_lower:
                return self.write_business_context_section(slide_content, context, source_content)
            else:
                logger.error(f"Unknown section type: {section_title}")
                raise ValueError(f"Unknown section type: {section_title}")


def main():
    """
    Test function for writer agent.
    """
    print("=" * 60)
    print("AutoDoc AI - Writer Agent Test")
    print("=" * 60)
    print()

    # Initialize agent
    print("1. Initializing WriterAgent...")
    agent = WriterAgent()
    print("   [OK] Agent initialized")
    print()

    # Test writing a section with template
    print("2. Testing section generation (with template)...")
    sample_context = """
[2023_comprehensive_model_doc.md:Validation]
The model was validated using a three-tier framework including holdout testing,
cross-validation, and sensitivity analysis. Performance metrics on holdout data
showed R² of 0.58 for frequency and 0.44 for severity.

[data_methodology_guide.md:Validation Procedures]
All models must undergo three-tier validation: (1) Data quality checks,
(2) Model performance testing, (3) Business reasonability review.
"""

    section = agent.write_section(
        section_title="Model Validation Framework",
        context=sample_context,
        template="validation",
        length_target="medium"
    )

    print(f"   [OK] Section generated: '{section.title}'")
    print(f"   [OK] Word count: {section.word_count}")
    print(f"   [OK] Sources cited: {len(section.sources_cited)}")
    print(f"   [OK] Template used: {section.template_used}")
    print()

    # Display section content
    print("3. Generated Section Content:")
    print(section.format_markdown()[:500])
    print("   [... content truncated ...]")
    print()

    # Test specialized section generation
    print("4. Testing executive summary generation...")
    exec_summary = agent.write_executive_summary(
        model_type="XGBoost Frequency Model",
        key_findings="Model achieved 38% improvement over GLM baseline",
        context=sample_context
    )
    print(f"   [OK] Executive summary: {exec_summary.word_count} words")
    print()

    # Test section revision
    print("5. Testing section revision...")
    revised = agent.revise_section(
        original_content=section,
        revision_instructions="Add more detail on cross-validation approach",
        additional_context="K-fold cross-validation with k=5 was used"
    )
    print(f"   [OK] Revised section: {revised.word_count} words")
    print(f"   [OK] Metadata: {revised.metadata}")
    print()

    # Test document combination
    print("6. Testing document combination...")
    sections = [exec_summary, section]
    document = agent.combine_sections(
        sections=sections,
        document_title="Model Documentation Example",
        frontmatter={
            "title": "Model Documentation Example",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "author": "WriterAgent",
            "type": "model_doc"
        }
    )
    print(f"   [OK] Combined document: {len(document)} characters")
    print(f"   [OK] Sections: {len(sections)}")
    print()
    print("   Document preview:")
    print(document[:400])
    print("   [... content truncated ...]")
    print()

    print("=" * 60)
    print("[OK] Writer Agent Test Complete!")
    print("=" * 60)
    print()
    print("Note: This agent uses placeholder content generation.")
    print("In production, it would integrate with an LLM for actual content generation.")
    print()


if __name__ == "__main__":
    main()
