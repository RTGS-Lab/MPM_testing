"""Basic simulation example using the Minimum Plant Model."""

import os
import sys
import matplotlib.pyplot as plt

# Add the parent directory to the path so we can import the mpm module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mpm import ModelHandler

def run_basic_simulation():
    """Run a basic simulation using sample input files."""
    # Get the absolute path to the input files
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    driver_file = os.path.join(base_dir, 'model input files/drivers_natural_all.csv')
    parameter_file = os.path.join(base_dir, 'model input files/parameters.csv')
    resource_pool_file = os.path.join(base_dir, 'model input files/resource_pools_3RPs.csv')
    
    # Create model instance
    model = ModelHandler(driver_file, parameter_file, resource_pool_file)
    
    # Run simulation
    print("Starting simulation...")
    model.run_simulation()
    print("Simulation completed!")
    
    # Plot outputs
    print("Generating plots...")
    model.plot_outputs()

if __name__ == "__main__":
    run_basic_simulation()
