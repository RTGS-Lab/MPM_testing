#!/usr/bin/env python3
"""
Test runner for the Minimum Plant Model package.
Discovers and runs all tests in the minimum_plant_model/tests directory.
"""

import unittest
import sys
import os

if __name__ == '__main__':
    # Get the path to the root directory and add it to Python path
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(tests_dir)
    sys.path.insert(0, project_root)
    
    print(f"Project root: {project_root}")
    print(f"Test directory: {tests_dir}")
    print(f"Python path: {sys.path}")
    
    # Discover and run all tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(tests_dir)
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return non-zero exit code if tests failed
    sys.exit(not result.wasSuccessful())