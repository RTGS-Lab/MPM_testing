"""Example script demonstrating how to use the original model structure."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import sys

# Add the parent directory to the sys.path so we can import the module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import original classes
from original_for_comparison import ModelHandler, Plant, ResourcePool, Atmosphere, Environment, AbovegroundEnvironment, CarbonAssimilation, PriorityQueue

# Set up paths to data files
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, 'data')

# Using local data files with full paths
driver_file = os.path.join(data_dir, 'drivers_natural_all.csv')
parameter_file = os.path.join(data_dir, 'parameters.csv')
resource_pool_file = os.path.join(data_dir, 'resource_pools_3RPs.csv')

# Create and run the model
model = ModelHandler(driver_file, parameter_file, resource_pool_file)
model.run_simulation()

# Plot outputs
model.plot_outputs()