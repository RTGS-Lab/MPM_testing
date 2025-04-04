# Minimum Plant Model (MPM) Tests

This directory contains the test suite for the Minimum Plant Model (MPM) package.

## Structure

The test structure mirrors the main package structure:

- `test_main_model.py`: Tests for the main coordination class
- `test_utils.py`: Tests for utility functions
- `test_visualization.py`: Tests for visualization functions
- `plant/`: Tests for plant-related modules
  - `test_plant.py`: Tests for the Plant class
  - `test_resource_pool.py`: Tests for the ResourcePool class
  - `test_carbon_assimilation.py`: Tests for carbon assimilation functions
- `environment/`: Tests for environment-related modules
  - `test_base_environment.py`: Tests for the BaseEnvironment abstract class
  - `test_aboveground_environment.py`: Tests for the AbovegroundEnvironment class
  - `test_atmosphere.py`: Tests for the Atmosphere class
- `data/`: Test data files
  - `test_drivers.csv`: Test climate drivers
  - `test_parameters.csv`: Test model parameters
  - `test_resource_pools.csv`: Test resource pool definitions

## Running Tests

### Using pytest directly

```bash
# From the repository root
pytest

# With coverage report
pytest --cov=mpm

# Run specific test files
pytest mpm/tests/test_main_model.py
```

### Using the run_tests.py script

```bash
# From the repository root
python run_tests.py
```

## Test Fixtures

Common test fixtures are defined in `conftest.py` and include:

- `test_data_dir`: Path to test data directory
- `test_parameters_file`, `test_drivers_file`, `test_resource_pools_file`: Paths to test data files
- `test_parameters_data`: Dictionary of model parameters
- `test_resource_pools_config`: Dictionary of resource pool configurations
- `test_drivers_data`: DataFrame of environmental drivers
- `test_results_data`: DataFrame of simulation results

## Adding New Tests

When adding new functionality to the MPM, please follow these guidelines:

1. Create a corresponding test file in the appropriate subdirectory
2. Use the existing fixtures where possible
3. Add appropriate test cases for normal operation and edge cases
4. Ensure tests are independent and don't rely on state from other tests
5. Mock external dependencies when testing individual components