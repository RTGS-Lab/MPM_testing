"""Basic simulation example using the Minimum Plant Model."""

import os
import sys
import matplotlib.pyplot as plt
from pathlib import Path

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from minimum_plant_model import MainModel

def run_basic_simulation():
    """Run a basic simulation using sample input files."""
    # Use exactly the same files as original_for_comparison.py
    driver_file = 'examples/data/drivers_natural_all.csv'
    parameter_file = 'examples/data/parameters.csv'
    resource_pool_file = 'examples/data/resource_pools_3RPs.csv'
    
    # Create model instance
    model = MainModel(driver_file, parameter_file, resource_pool_file)
    
    # Run simulation
    print("Starting simulation...")
    
    # Define a simple progress callback
    def progress_callback(current, total):
        percent = int(current * 100 / total)
        sys.stdout.write(f"\rProgress: [{percent:3d}%] {current}/{total} timesteps")
        sys.stdout.flush()
    
    model.run_simulation(progress_callback=progress_callback)
    print("\nSimulation completed!")
    
    # Plot outputs
    print("Generating plots...")
    model.plot_outputs()
    
    # Save results
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    model.save_results(os.path.join(results_dir, 'basic_simulation_results.csv'))
    print(f"Results saved to {os.path.join(results_dir, 'basic_simulation_results.csv')}")

if __name__ == "__main__":
    run_basic_simulation()