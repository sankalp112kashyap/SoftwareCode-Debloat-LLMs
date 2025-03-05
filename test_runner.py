#!/usr/bin/env python3
"""
Test runner for executing Python tests and collecting results.
"""

import os
import subprocess
import sys
import logging
import re

logger = logging.getLogger(__name__)

class TestRunner:
    """
    Handles running tests and collecting test results.
    """
    
    def run_tests(self, test_file):
        """
        Run tests and collect results.
        
        Args:
            test_file: Path to the test file
            
        Returns:
            Dictionary containing test results (passed, failed, total)
        """
        # Determine test framework based on file content and name
        test_framework = self._detect_test_framework(test_file)
        
        try:
            if test_framework == "pytest":
                return self._run_pytest(test_file)
            elif test_framework == "unittest":
                return self._run_unittest(test_file)
            else:
                logger.warning(f"Unknown test framework, defaulting to pytest for {test_file}")
                return self._run_pytest(test_file)
        except Exception as e:
            logger.error(f"Error running tests {test_file}: {str(e)}")
            # Return a failed result
            return {"passed": 0, "failed": 1, "total": 1}
    
    def _detect_test_framework(self, test_file):
        """
        Detect the test framework used in the test file.
        
        Args:
            test_file: Path to the test file
            
        Returns:
            String indicating the test framework (pytest or unittest)
        """
        try:
            with open(test_file, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Check if it's using pytest fixtures or markers
                if "import pytest" in content or "@pytest" in content or "pytest.mark" in content:
                    return "pytest"
                
                # Check if it's using unittest
                if "import unittest" in content or "unittest.TestCase" in content:
                    return "unittest"
                
                # Check filename for clues
                if "test_" in os.path.basename(test_file) or "_test" in os.path.basename(test_file):
                    return "pytest"  # Default to pytest for files with test_ prefix
                
                # Default to unittest if we can't determine
                return "unittest"
        except Exception as e:
            logger.error(f"Error detecting test framework: {str(e)}")
            return "pytest"  # Default to pytest
    
    def _run_pytest(self, test_file):
        """
        Run tests using pytest.
        
        Args:
            test_file: Path to the test file
            
        Returns:
            Dictionary containing test results (passed, failed, total)
        """
        try:
            # Install pytest if not already installed
            subprocess.run([sys.executable, "-m", "pip", "install", "pytest"], 
                           capture_output=True, check=False)
            
            # Run pytest with the -v flag to get verbose output
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_file, "-v"],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Parse the output to get test results
            output = result.stdout + result.stderr
            
            # Look for the test summary
            summary_match = re.search(r'(\d+) passed, (\d+) failed', output)
            if summary_match:
                passed = int(summary_match.group(1))
                failed = int(summary_match.group(2))
                total = passed + failed
            else:
                # Alternative parsing if the standard summary is not found
                passed = len(re.findall(r'PASSED', output))
                failed = len(re.findall(r'FAILED', output))
                total = passed + failed
                
                # If we still don't have any results, check for other patterns
                if total == 0:
                    passed = len(re.findall(r'passed', output, re.IGNORECASE))
                    failed = len(re.findall(r'failed', output, re.IGNORECASE))
                    total = passed + failed
            
            # If we couldn't parse any results, use the return code
            if total == 0:
                if result.returncode == 0:
                    passed = 1
                    failed = 0
                else:
                    passed = 0
                    failed = 1
                total = 1
            
            return {"passed": passed, "failed": failed, "total": total}
        except Exception as e:
            logger.error(f"Error running pytest: {str(e)}")
            raise
    
    def _run_unittest(self, test_file):
        """
        Run tests using unittest.
        
        Args:
            test_file: Path to the test file
            
        Returns:
            Dictionary containing test results (passed, failed, total)
        """
        try:
            # Run unittest with verbosity=2 for detailed output
            result = subprocess.run(
                [sys.executable, "-m", "unittest", "-v", test_file],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Parse the output to get test results
            output = result.stdout + result.stderr
            
            # Look for unittest results
            # First try to find the final summary line
            summary_match = re.search(r'Ran (\d+) tests? in', output)
            if summary_match:
                total = int(summary_match.group(1))
                
                # Check if there were failures
                if "OK" in output:
                    passed = total
                    failed = 0
                else:
                    # Look for failures and errors
                    failures_match = re.search(r'failures=(\d+)', output)
                    errors_match = re.search(r'errors=(\d+)', output)
                    
                    failures = int(failures_match.group(1)) if failures_match else 0
                    errors = int(errors_match.group(1)) if errors_match else 0
                    
                    failed = failures + errors
                    passed = total - failed
            else:
                # If we couldn't find the summary, count successful test methods
                passed = len(re.findall(r'\.{3} ok', output))
                failed = len(re.findall(r'\.{3} FAIL', output)) + len(re.findall(r'\.{3} ERROR', output))
                total = passed + failed
            
            # If we still couldn't parse any results, use the return code
            if total == 0:
                if result.returncode == 0:
                    passed = 1
                    failed = 0
                else:
                    passed = 0
                    failed = 1
                total = 1
            
            return {"passed": passed, "failed": failed, "total": total}
        except Exception as e:
            logger.error(f"Error running unittest: {str(e)}")
            raise