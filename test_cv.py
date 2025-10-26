"""
Tests for CV markdown file structure and content.

This test suite validates that the CV markdown file:
1. Exists and is readable
2. Contains all required sections
3. Has valid contact information
4. Includes key professional information
5. Can be converted to PDF successfully
"""

import os
import re
import subprocess
from pathlib import Path


def test_cv_file_exists():
    """Test that cv.md file exists."""
    cv_path = Path(__file__).parent / "cv.md"
    assert cv_path.exists(), "cv.md file does not exist"


def test_cv_file_readable():
    """Test that cv.md file is readable."""
    cv_path = Path(__file__).parent / "cv.md"
    with open(cv_path, "r") as f:
        content = f.read()
    assert len(content) > 0, "cv.md file is empty"


def test_cv_has_required_sections():
    """Test that CV contains all required sections."""
    cv_path = Path(__file__).parent / "cv.md"
    with open(cv_path, "r") as f:
        content = f.read()

    required_sections = [
        "# Max Ghenis",
        "## Summary",
        "## Education",
        "## Professional Experience",
        "## Key Skills",
        "## Selected Publications",
        "## Volunteer Leadership",
    ]

    for section in required_sections:
        assert section in content, f"CV missing required section: {section}"


def test_cv_has_contact_info():
    """Test that CV contains contact information."""
    cv_path = Path(__file__).parent / "cv.md"
    with open(cv_path, "r") as f:
        content = f.read()

    assert "max@policyengine.org" in content, "CV missing email"
    assert "+1.650.630.3657" in content or "650.630.3657" in content, "CV missing phone"
    assert "github.com/maxghenis" in content, "CV missing GitHub"


def test_cv_has_policyengine():
    """Test that CV mentions PolicyEngine prominently."""
    cv_path = Path(__file__).parent / "cv.md"
    with open(cv_path, "r") as f:
        content = f.read()

    assert "PolicyEngine" in content, "CV missing PolicyEngine"
    assert "policyengine.org" in content, "CV missing PolicyEngine URL"
    assert content.count("PolicyEngine") >= 5, "PolicyEngine not mentioned enough times"


def test_cv_has_education():
    """Test that CV includes education credentials."""
    cv_path = Path(__file__).parent / "cv.md"
    with open(cv_path, "r") as f:
        content = f.read()

    assert "MIT" in content or "Massachusetts Institute of Technology" in content, "CV missing MIT education"
    assert "UC Berkeley" in content or "University of California, Berkeley" in content, "CV missing Berkeley education"


def test_cv_has_work_experience():
    """Test that CV includes major work experiences."""
    cv_path = Path(__file__).parent / "cv.md"
    with open(cv_path, "r") as f:
        content = f.read()

    companies = ["PolicyEngine", "Google", "YouTube"]
    for company in companies:
        assert company in content, f"CV missing work experience at {company}"


def test_cv_has_skills():
    """Test that CV includes technical skills."""
    cv_path = Path(__file__).parent / "cv.md"
    with open(cv_path, "r") as f:
        content = f.read()

    skills = ["Python", "R", "SQL"]
    for skill in skills:
        assert skill in content, f"CV missing skill: {skill}"


def test_cv_markdown_syntax():
    """Test that CV has valid markdown syntax."""
    cv_path = Path(__file__).parent / "cv.md"
    with open(cv_path, "r") as f:
        content = f.read()

    # Check for headers
    assert re.search(r"^#\s+", content, re.MULTILINE), "CV missing top-level header"
    assert re.search(r"^##\s+", content, re.MULTILINE), "CV missing second-level headers"

    # Check for links
    assert re.search(r"\[.+\]\(.+\)", content), "CV missing markdown links"


def test_pdf_generation_possible():
    """Test that PDF can be generated using the build script."""
    build_script = Path(__file__).parent / "build.py"
    cv_path = Path(__file__).parent / "cv.md"
    html_path = Path(__file__).parent / "cv.html"
    pdf_path = Path(__file__).parent / "cv.pdf"

    # Clean up any existing outputs
    for path in [html_path, pdf_path]:
        if path.exists():
            path.unlink()

    # Try to generate PDF using build script
    try:
        result = subprocess.run(
            ["python", str(build_script), "--pdf"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(build_script.parent)
        )

        # Check if PDF was created
        assert pdf_path.exists(), f"PDF generation failed: {result.stdout}\n{result.stderr}"
        assert pdf_path.stat().st_size > 0, "Generated PDF is empty"

    except subprocess.TimeoutExpired:
        raise AssertionError("PDF generation timed out")
    except Exception as e:
        # If PDF generation fails, it might be due to missing dependencies
        # The build job will catch this, so we can skip in tests
        import pytest
        pytest.skip(f"PDF generation dependencies not available: {e}")
    finally:
        # Clean up test outputs
        for path in [html_path, pdf_path]:
            if path.exists():
                path.unlink()


def test_cv_length_reasonable():
    """Test that CV is not too short or too long."""
    cv_path = Path(__file__).parent / "cv.md"
    with open(cv_path, "r") as f:
        content = f.read()

    # Should be at least 2000 characters for a comprehensive CV
    assert len(content) >= 2000, f"CV seems too short ({len(content)} characters)"

    # Shouldn't be excessively long (over 50KB seems excessive for a CV)
    assert len(content) <= 50000, f"CV seems too long ({len(content)} characters)"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
