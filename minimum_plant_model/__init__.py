"""Minimum Plant Model (MPM) - A modular framework for simulating plant growth.

The Minimum Plant Model is a modular plant growth simulator that can be used to
explore plant development under varying environmental conditions. It includes
components for carbon assimilation, resource allocation, and growth based on
thermal time.

Modules:
    main_model: Core simulation coordination
    environment: Environmental factors and interfaces
    plant: Plant-level processes and components
    utils: Utility functions for input/output
    visualization: Visualization tools for simulation results

Example:
    from minimum_plant_model import MainModel
    
    model = MainModel(
        drivers_filename="path/to/drivers.csv",
        parameter_filename="path/to/parameters.csv",
        resource_pool_filename="path/to/resource_pools.csv"
    )
    
    model.run_simulation()
    model.plot_outputs()
"""

__version__ = '0.1.0'

from .main_model import MainModel
from .plant import Plant, ResourcePool, CarbonAssimilation
from .environment import Environment, AbovegroundEnvironment, Atmosphere
from .utils import read_csv_file, read_parameters_file, read_resource_pools_file

__all__ = [
    'MainModel',
    'Plant', 
    'ResourcePool', 
    'CarbonAssimilation',
    'Environment', 
    'AbovegroundEnvironment', 
    'Atmosphere'
]