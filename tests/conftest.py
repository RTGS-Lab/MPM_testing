"""
Test fixtures for the Minimum Plant Model tests.
"""

import os
import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def test_data_dir():
    """Return the path to the test data directory."""
    return os.path.join(os.path.dirname(__file__), 'data')


@pytest.fixture
def test_parameters_file(test_data_dir):
    """Return the path to the test parameters file."""
    return os.path.join(test_data_dir, 'test_parameters.csv')


@pytest.fixture
def test_drivers_file(test_data_dir):
    """Return the path to the test drivers file."""
    return os.path.join(test_data_dir, 'test_drivers.csv')


@pytest.fixture
def test_resource_pools_file(test_data_dir):
    """Return the path to the test resource pools file."""
    return os.path.join(test_data_dir, 'test_resource_pools.csv')


@pytest.fixture
def test_parameters_data():
    """Return a dictionary of test parameters."""
    return {
        'leaf_mass_per_area': 0.02,
        'ER_ref': 0.5,
        'Q10': 2.0,
        'T_ref': 20.0,
        'light_use_efficiency': 0.5,
        'temperature_min': 5.0,
        'temperature_max': 35.0,
        'radiation_max': 25.0,
        'latitude': 45.0
    }


@pytest.fixture
def test_resource_pools_config():
    """Return a dictionary of test resource pool configurations."""
    return {
        'canopy': {'initial_mass': 0.1, 'max_mass': 10.0, 'growth_rate': 0.1},
        'roots': {'initial_mass': 0.1, 'max_mass': 5.0, 'growth_rate': 0.08}
    }


@pytest.fixture
def test_drivers_data():
    """Return a DataFrame of test drivers."""
    return pd.DataFrame({
        'date': pd.date_range(start='2020-01-01', periods=10),
        'temperature': np.linspace(15, 24, 10),
        'radiation': np.linspace(10, 19, 10),
        'day_length': np.linspace(8, 8.9, 10)
    })


@pytest.fixture
def test_results_data():
    """Return a DataFrame of test simulation results."""
    return pd.DataFrame({
        'date': pd.date_range(start='2020-01-01', periods=10),
        'temperature': np.random.uniform(15, 25, 10),
        'radiation': np.random.uniform(5, 15, 10),
        'canopy_mass': np.linspace(0.1, 1.0, 10),
        'roots_mass': np.linspace(0.1, 0.8, 10),
        'LAI': np.linspace(0.5, 5.0, 10),
        'NPP': np.linspace(0.1, 0.5, 10)
    })