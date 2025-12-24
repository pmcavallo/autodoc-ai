"""
Validate the example PowerPoint presentations.

Tests each PPT against the validator component to ensure they meet requirements.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.components.ppt_validator import PPTValidator


def validate_presentation(filepath: Path):
    """Validate a single presentation."""
    print(f"\n{'='*60}")
    print(f"Validating: {filepath.name}")
    print(f"{'='*60}")

    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        return False

    # Read file
    with open(filepath, 'rb') as f:
        file_bytes = f.read()

    # Validate
    validator = PPTValidator()
    result = validator.validate_file(file_bytes, filepath.name)

    # Display results
    print(f"\nValidation Result: {'PASSED' if result.is_valid else 'FAILED'}")
    print(f"Slide Count: {result.slide_count}")

    if result.errors:
        print(f"\nErrors ({len(result.errors)}):")
        for error in result.errors:
            print(f"  - {error}")

    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  - {warning}")

    if result.info:
        print(f"\nInfo ({len(result.info)}):")
        for info in result.info:
            # Remove unicode characters that might cause encoding issues
            info_clean = info.replace('✓', '[OK]')
            print(f"  - {info_clean}")

    if result.detected_sections:
        print(f"\nDetected Slides ({len(result.detected_sections)}):")
        for i, title in enumerate(result.detected_sections[:10], 1):
            print(f"  {i}. {title}")
        if len(result.detected_sections) > 10:
            print(f"  ... and {len(result.detected_sections) - 10} more")

    return result.is_valid


def main():
    """Validate all example presentations."""
    print("="*60)
    print("PowerPoint Presentation Validation")
    print("="*60)

    examples_dir = Path("C:/Projects/autodoc-ai/data/examples")

    presentations = [
        examples_dir / "bodily_injury_frequency_model.pptx",
        examples_dir / "collision_severity_model.pptx",
        examples_dir / "comprehensive_coverage_model.pptx"
    ]

    results = {}
    for ppt in presentations:
        results[ppt.name] = validate_presentation(ppt)

    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")

    for name, passed in results.items():
        status = "[OK] PASSED" if passed else "[FAIL] FAILED"
        print(f"{status}: {name}")

    all_passed = all(results.values())
    print(f"\n{'='*60}")
    if all_passed:
        print("[OK] All presentations validated successfully!")
    else:
        print("[FAIL] Some presentations failed validation")
    print(f"{'='*60}")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
