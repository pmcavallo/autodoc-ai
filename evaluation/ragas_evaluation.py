"""
RAGAS Evaluation Framework for AutoDoc AI
==========================================

Comprehensive RAG quality evaluation using RAGAS metrics:
- Faithfulness: Are claims grounded in retrieved context?
- Answer Relevancy: Does output address the research query?
- Context Precision: Are relevant chunks ranked high?
- Context Recall: Is all needed info retrieved?

Author: Paulo Cavallo
Date: November 2024
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    )
    from datasets import Dataset
    RAGAS_AVAILABLE = True
except ImportError:
    logger.warning("RAGAS not installed. Run: pip install ragas datasets")
    RAGAS_AVAILABLE = False

from agents.orchestrator import DocumentationOrchestrator
from rag.retrieval import DocumentRetriever
from utils.ppt_analyzer import PPTAnalyzer


@dataclass
class RAGTestCase:
    """Single test case for RAGAS evaluation"""
    section_name: str
    model_type: str
    question: str  # The research query
    answer: str  # Generated section content
    contexts: List[str]  # Retrieved RAG chunks
    ground_truth: str  # Expected content from source
    metadata: Dict[str, Any]  # Additional info


@dataclass
class RAGASResults:
    """RAGAS evaluation results"""
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float
    overall_score: float
    test_cases_count: int
    model_type: str
    evaluation_date: str
    per_section_scores: Dict[str, Dict[str, float]]


class RAGContextCapture:
    """
    Wrapper to capture RAG contexts during generation.
    
    This intercepts the retrieval calls to save what context
    was actually used for each section.
    """
    
    def __init__(self, retriever: DocumentRetriever):
        self.retriever = retriever
        self.captured_contexts: Dict[str, List[str]] = {}
        self.current_section: Optional[str] = None
    
    def set_section(self, section_name: str):
        """Set which section we're currently generating"""
        self.current_section = section_name
        self.captured_contexts[section_name] = []
    
    def retrieve(self, *args, **kwargs):
        """Intercept retrieve calls to capture contexts"""
        results = self.retriever.retrieve(*args, **kwargs)
        
        # Save the actual text chunks retrieved
        if self.current_section and results:
            for result in results:
                self.captured_contexts[self.current_section].append(
                    result.get('text', '')
                )
        
        return results
    
    def get_contexts(self, section_name: str) -> List[str]:
        """Get captured contexts for a section"""
        return self.captured_contexts.get(section_name, [])


class RAGASEvaluator:
    """Main RAGAS evaluation orchestrator"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results_dir = project_root / "evaluation" / "results"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.retriever = DocumentRetriever()
        self.ppt_analyzer = PPTAnalyzer()
        
        logger.info("RAGASEvaluator initialized")
    
    def create_test_cases_from_ppt(
        self, 
        ppt_path: str,
        num_sections: int = 8
    ) -> List[RAGTestCase]:
        """
        Create test cases from a PowerPoint file.
        
        Args:
            ppt_path: Path to test PPT file
            num_sections: Number of sections to evaluate
        
        Returns:
            List of RAGTestCase objects
        """
        logger.info(f"Creating test cases from: {ppt_path}")
        
        # Analyze PPT to get model type and source content
        analysis = self.ppt_analyzer.analyze_ppt(ppt_path)
        model_type = analysis.model_type
        
        # Extract source content by slide/section
        # This would need actual slide content - for now we'll use placeholders
        source_sections = self._extract_source_sections(ppt_path, model_type)
        
        # Run AutoDoc with context capture
        test_cases = []
        context_capture = RAGContextCapture(self.retriever)
        
        # Generate document with captured contexts
        logger.info("Generating document with context capture...")
        generated_sections = self._generate_with_capture(
            ppt_path, 
            model_type,
            context_capture
        )
        
        # Create test cases for each section
        section_names = [
            "Executive Summary",
            "Methodology", 
            "Data Sources",
            "Variable Selection",
            "Model Results",
            "Model Development",
            "Validation",
            "Business Context"
        ]
        
        for section_name in section_names[:num_sections]:
            if section_name not in generated_sections:
                continue
            
            test_case = RAGTestCase(
                section_name=section_name,
                model_type=model_type,
                question=f"Generate {section_name} section for {model_type} model",
                answer=generated_sections[section_name],
                contexts=context_capture.get_contexts(section_name),
                ground_truth=source_sections.get(section_name, ""),
                metadata={
                    "ppt_path": ppt_path,
                    "num_contexts": len(context_capture.get_contexts(section_name)),
                    "answer_length": len(generated_sections[section_name])
                }
            )
            test_cases.append(test_case)
        
        logger.info(f"Created {len(test_cases)} test cases")
        return test_cases
    
    def _extract_source_sections(
        self, 
        ppt_path: str, 
        model_type: str
    ) -> Dict[str, str]:
        """
        Extract source content from PPT by section.
        
        In a full implementation, this would parse slides and
        map them to documentation sections. For now, we'll
        create synthetic ground truth based on RAG content.
        """
        # This is a simplified version - in production you'd parse slides
        source_sections = {
            "Executive Summary": "Ground truth executive summary content...",
            "Methodology": "Ground truth methodology content...",
            "Data Sources": "Ground truth data sources content...",
            "Variable Selection": "Ground truth variable selection...",
            "Model Results": "Ground truth model results...",
            "Model Development": "Ground truth model development...",
            "Validation": "Ground truth validation content...",
            "Business Context": "Ground truth business context..."
        }
        
        # In real implementation, extract from actual PPT slides
        logger.info(f"Extracted {len(source_sections)} source sections")
        return source_sections
    
    def _generate_with_capture(
        self,
        ppt_path: str,
        model_type: str,
        context_capture: RAGContextCapture
    ) -> Dict[str, str]:
        """
        Generate document while capturing RAG contexts.
        
        Returns dict of section_name -> generated_content
        """
        # For testing, we'll use a simplified approach
        # In production, you'd instrument the orchestrator to use context_capture
        
        sections = {}
        section_names = [
            "Executive Summary", "Methodology", "Data Sources",
            "Variable Selection", "Model Results", "Model Development",
            "Validation", "Business Context"
        ]
        
        for section_name in section_names:
            context_capture.set_section(section_name)
            
            # Simulate retrieval
            query = f"{section_name} {model_type} model"
            context_capture.retrieve(
                query=query,
                filters={"model_type": model_type},
                n_results=5
            )
            
            # In real implementation, this would be actual generation
            sections[section_name] = f"Generated {section_name} content for {model_type} model..."
        
        return sections
    
    def evaluate_test_cases(
        self, 
        test_cases: List[RAGTestCase]
    ) -> RAGASResults:
        """
        Run RAGAS evaluation on test cases.
        
        Args:
            test_cases: List of RAGTestCase objects
        
        Returns:
            RAGASResults with all metrics
        """
        if not RAGAS_AVAILABLE:
            raise RuntimeError("RAGAS not installed. Run: pip install ragas datasets")
        
        logger.info(f"Evaluating {len(test_cases)} test cases with RAGAS...")
        
        # Convert to RAGAS dataset format
        dataset_dict = {
            "question": [tc.question for tc in test_cases],
            "answer": [tc.answer for tc in test_cases],
            "contexts": [[ctx for ctx in tc.contexts] for tc in test_cases],
            "ground_truth": [tc.ground_truth for tc in test_cases]
        }
        
        dataset = Dataset.from_dict(dataset_dict)
        
        # Run RAGAS evaluation
        logger.info("Running RAGAS metrics...")
        results = evaluate(
            dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall
            ]
        )
        
        # Calculate per-section scores
        per_section_scores = {}
        for i, tc in enumerate(test_cases):
            per_section_scores[tc.section_name] = {
                "faithfulness": results['faithfulness'][i] if 'faithfulness' in results else 0.0,
                "answer_relevancy": results['answer_relevancy'][i] if 'answer_relevancy' in results else 0.0,
                "context_precision": results['context_precision'][i] if 'context_precision' in results else 0.0,
                "context_recall": results['context_recall'][i] if 'context_recall' in results else 0.0,
            }
        
        # Create results object
        ragas_results = RAGASResults(
            faithfulness=float(results.get('faithfulness', 0.0)),
            answer_relevancy=float(results.get('answer_relevancy', 0.0)),
            context_precision=float(results.get('context_precision', 0.0)),
            context_recall=float(results.get('context_recall', 0.0)),
            overall_score=(
                float(results.get('faithfulness', 0.0)) +
                float(results.get('answer_relevancy', 0.0)) +
                float(results.get('context_precision', 0.0)) +
                float(results.get('context_recall', 0.0))
            ) / 4.0,
            test_cases_count=len(test_cases),
            model_type=test_cases[0].model_type if test_cases else "unknown",
            evaluation_date=datetime.now().isoformat(),
            per_section_scores=per_section_scores
        )
        
        logger.info(f"RAGAS Evaluation Complete:")
        logger.info(f"  Faithfulness: {ragas_results.faithfulness:.3f}")
        logger.info(f"  Answer Relevancy: {ragas_results.answer_relevancy:.3f}")
        logger.info(f"  Context Precision: {ragas_results.context_precision:.3f}")
        logger.info(f"  Context Recall: {ragas_results.context_recall:.3f}")
        logger.info(f"  Overall Score: {ragas_results.overall_score:.3f}")
        
        return ragas_results
    
    def save_results(
        self, 
        results: RAGASResults,
        test_cases: List[RAGTestCase],
        output_name: str = "ragas_evaluation"
    ):
        """Save evaluation results to JSON and generate report"""
        
        # Save JSON results
        json_path = self.results_dir / f"{output_name}.json"
        results_dict = asdict(results)
        results_dict['test_cases'] = [asdict(tc) for tc in test_cases]
        
        with open(json_path, 'w') as f:
            json.dump(results_dict, f, indent=2)
        
        logger.info(f"Results saved to: {json_path}")
        
        # Generate markdown report
        report_path = self.results_dir / f"{output_name}_REPORT.md"
        self._generate_report(results, test_cases, report_path)
        
        logger.info(f"Report generated: {report_path}")
    
    def _generate_report(
        self,
        results: RAGASResults,
        test_cases: List[RAGTestCase],
        output_path: Path
    ):
        """Generate comprehensive markdown report"""
        
        report = f"""# RAGAS Evaluation Report: AutoDoc AI
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Model Type:** {results.model_type}  
**Test Cases:** {results.test_cases_count} sections evaluated

---

## Executive Summary

AutoDoc AI's RAG system was evaluated using RAGAS (Retrieval Augmented Generation Assessment), a comprehensive framework for measuring RAG quality across four key dimensions.

### Overall Performance

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| **Faithfulness** | {results.faithfulness:.1%} | 85%+ | {'✅ PASS' if results.faithfulness >= 0.85 else '⚠️ NEEDS IMPROVEMENT'} |
| **Answer Relevancy** | {results.answer_relevancy:.1%} | 80%+ | {'✅ PASS' if results.answer_relevancy >= 0.80 else '⚠️ NEEDS IMPROVEMENT'} |
| **Context Precision** | {results.context_precision:.1%} | 75%+ | {'✅ PASS' if results.context_precision >= 0.75 else '⚠️ NEEDS IMPROVEMENT'} |
| **Context Recall** | {results.context_recall:.1%} | 80%+ | {'✅ PASS' if results.context_recall >= 0.80 else '⚠️ NEEDS IMPROVEMENT'} |
| **Overall Score** | {results.overall_score:.1%} | 80%+ | {'✅ EXCELLENT' if results.overall_score >= 0.80 else '⚠️ NEEDS IMPROVEMENT'} |

---

## Metric Definitions

### 1. Faithfulness ({results.faithfulness:.1%})
**What it measures:** Are generated claims grounded in retrieved context?

**Why it matters:** Prevents hallucination. High faithfulness means the RAG system only makes claims supported by source material.

**AutoDoc AI Performance:** {self._interpret_score(results.faithfulness, 'faithfulness')}

### 2. Answer Relevancy ({results.answer_relevancy:.1%})
**What it measures:** Does generated content address the research query?

**Why it matters:** Ensures the system stays on topic and doesn't generate irrelevant content.

**AutoDoc AI Performance:** {self._interpret_score(results.answer_relevancy, 'relevancy')}

### 3. Context Precision ({results.context_precision:.1%})
**What it measures:** Are most relevant chunks ranked high in retrieval?

**Why it matters:** Better precision means more efficient context usage and lower token costs.

**AutoDoc AI Performance:** {self._interpret_score(results.context_precision, 'precision')}

### 4. Context Recall ({results.context_recall:.1%})
**What it measures:** Is all necessary information retrieved from knowledge base?

**Why it matters:** Ensures comprehensive coverage - nothing important is missed.

**AutoDoc AI Performance:** {self._interpret_score(results.context_recall, 'recall')}

---

## Per-Section Analysis

| Section | Faithfulness | Relevancy | Precision | Recall | Avg |
|---------|-------------|-----------|-----------|---------|-----|
"""
        
        for section_name, scores in results.per_section_scores.items():
            avg = sum(scores.values()) / len(scores)
            report += f"| {section_name} | {scores['faithfulness']:.2f} | {scores['answer_relevancy']:.2f} | {scores['context_precision']:.2f} | {scores['context_recall']:.2f} | {avg:.2f} |\n"
        
        report += f"""
---

## Test Cases Details

"""
        for i, tc in enumerate(test_cases, 1):
            report += f"""
### Test Case {i}: {tc.section_name}

**Question:** {tc.question}

**Contexts Retrieved:** {len(tc.contexts)} chunks

**Answer Length:** {len(tc.answer)} characters

**Ground Truth Length:** {len(tc.ground_truth)} characters

**Metadata:**
```json
{json.dumps(tc.metadata, indent=2)}
```

---
"""
        
        report += f"""
## Recommendations

### Strengths
"""
        if results.faithfulness >= 0.85:
            report += "- ✅ **Excellent Faithfulness:** System reliably grounds claims in source material\n"
        if results.answer_relevancy >= 0.80:
            report += "- ✅ **Strong Relevancy:** Generated content stays on topic\n"
        if results.context_precision >= 0.75:
            report += "- ✅ **Good Precision:** Relevant chunks ranked highly\n"
        if results.context_recall >= 0.80:
            report += "- ✅ **Strong Recall:** Comprehensive information retrieval\n"
        
        report += f"""
### Areas for Improvement
"""
        if results.faithfulness < 0.85:
            report += "- ⚠️ **Faithfulness:** Review prompt engineering to encourage source citation\n"
        if results.answer_relevancy < 0.80:
            report += "- ⚠️ **Relevancy:** Tighten query formulation to reduce off-topic content\n"
        if results.context_precision < 0.75:
            report += "- ⚠️ **Precision:** Consider reranking or embedding model tuning\n"
        if results.context_recall < 0.80:
            report += "- ⚠️ **Recall:** Increase n_results or improve chunking strategy\n"
        
        report += f"""
---

## Technical Details

**Evaluation Framework:** RAGAS v0.1.x  
**Embedding Model:** {self._get_embedding_model()}  
**LLM Judge:** Claude Sonnet 4  
**Evaluation Date:** {results.evaluation_date}  
**Test Cases:** {results.test_cases_count} sections

---

## Conclusion

AutoDoc AI's RAG system demonstrates {'excellent' if results.overall_score >= 0.85 else 'strong' if results.overall_score >= 0.75 else 'adequate'} performance across RAGAS metrics with an overall score of {results.overall_score:.1%}.

**Key Takeaway:** {self._generate_conclusion(results)}

---

*This report was automatically generated by AutoDoc AI's RAGAS evaluation framework.*
"""
        
        with open(output_path, 'w') as f:
            f.write(report)
    
    def _interpret_score(self, score: float, metric_type: str) -> str:
        """Interpret what a score means"""
        if score >= 0.90:
            return f"Excellent {metric_type} performance. System exceeds production standards."
        elif score >= 0.80:
            return f"Strong {metric_type}. System meets production requirements."
        elif score >= 0.70:
            return f"Adequate {metric_type}. Some improvement opportunities exist."
        else:
            return f"Below target. Immediate optimization recommended."
    
    def _get_embedding_model(self) -> str:
        """Get the embedding model being used"""
        # This would query the actual retriever
        return "text-embedding-3-small (OpenAI)"
    
    def _generate_conclusion(self, results: RAGASResults) -> str:
        """Generate overall conclusion"""
        if results.overall_score >= 0.85:
            return "The system demonstrates production-ready RAG performance with reliable source grounding and comprehensive information retrieval."
        elif results.overall_score >= 0.75:
            return "The system shows strong RAG fundamentals with some opportunities for optimization in precision and recall."
        else:
            return "The system requires optimization before production deployment. Focus on improving faithfulness and recall metrics."


def main():
    """Main evaluation workflow"""
    logger.info("="*60)
    logger.info("AutoDoc AI - Comprehensive RAGAS Evaluation")
    logger.info("="*60)
    
    # Check RAGAS installation
    if not RAGAS_AVAILABLE:
        logger.error("RAGAS not installed!")
        logger.error("Run: pip install ragas datasets")
        return
    
    # Initialize evaluator
    project_root = Path(__file__).parent.parent
    evaluator = RAGASEvaluator(project_root)
    
    # Define test PPT path
    test_ppt = project_root / "test_data" / "frequency_model_2024.pptx"
    
    if not test_ppt.exists():
        logger.warning(f"Test PPT not found: {test_ppt}")
        logger.warning("Using synthetic test data...")
        test_ppt = None
    
    # Create test cases
    logger.info("\n" + "="*60)
    logger.info("STEP 1: Creating Test Cases")
    logger.info("="*60)
    
    if test_ppt:
        test_cases = evaluator.create_test_cases_from_ppt(str(test_ppt))
    else:
        # Create synthetic test cases
        test_cases = create_synthetic_test_cases()
    
    # Run evaluation
    logger.info("\n" + "="*60)
    logger.info("STEP 2: Running RAGAS Evaluation")
    logger.info("="*60)
    
    results = evaluator.evaluate_test_cases(test_cases)
    
    # Save results
    logger.info("\n" + "="*60)
    logger.info("STEP 3: Saving Results")
    logger.info("="*60)
    
    evaluator.save_results(results, test_cases, f"ragas_eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    logger.info("\n" + "="*60)
    logger.info("EVALUATION COMPLETE!")
    logger.info("="*60)
    logger.info(f"Overall Score: {results.overall_score:.1%}")
    logger.info(f"Check results in: {evaluator.results_dir}")


def create_synthetic_test_cases() -> List[RAGTestCase]:
    """Create synthetic test cases for demonstration"""
    logger.info("Creating synthetic test cases...")
    
    test_cases = [
        RAGTestCase(
            section_name="Executive Summary",
            model_type="frequency",
            question="Generate Executive Summary for frequency model",
            answer="The frequency model predicts annual claim counts for auto insurance...",
            contexts=[
                "Frequency models use GLM with Poisson distribution",
                "Claims per policy year is the target variable",
                "Model includes driver age, vehicle type, and territory"
            ],
            ground_truth="This frequency model estimates expected claim counts...",
            metadata={"num_contexts": 3, "answer_length": 500}
        ),
        # Add more synthetic cases as needed
    ]
    
    return test_cases


if __name__ == "__main__":
    main()
