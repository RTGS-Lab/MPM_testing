#!/usr/bin/env python
"""Run the minimum plant model directly."""

import os
import sys

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from minimum_plant_model import MainModel

def main():
    """Run the minimum plant model with example data."""
    print("Starting minimum plant model simulation...")
    
    # Use the same data files as in the examples
    driver_file = 'examples/data/drivers_natural_all.csv'
    parameter_file = 'examples/data/parameters.csv'
    resource_pool_file = 'examples/data/resource_pools_3RPs.csv'
    
    # Create model instance
    model = MainModel(driver_file, parameter_file, resource_pool_file)
    
    # Define a simple progress callback
    def progress_callback(current, total):
        percent = int(current * 100 / total)
        sys.stdout.write(f"\rProgress: [{percent:3d}%] {current}/{total} timesteps")
        sys.stdout.flush()
    
    # Run simulation
    model.run_simulation(progress_callback=progress_callback)
    print("\nSimulation completed!")
    
    # Save results to file
    results_file = 'mpm_results.csv'
    model.save_results(results_file)
    print(f"Results saved to {results_file}")
    
    # Print final values for key metrics
    results = model.get_results_dataframe()
    last_row = results.iloc[-1]
    
    print("\nFinal simulation values:")
    print(f"  Thermal age: {last_row['thermal_age']:.2f}")
    print(f"  Leaf area index: {last_row['lai']:.4f}")
    print(f"  Carbon pool: {last_row['carbon_pool']:.4f}")
    
    # Print final resource pool sizes
    print("  Resource pool sizes:")
    for col in results.columns:
        if col.startswith('rp_') and not col.endswith('rgr') and not col.endswith('demand'):
            print(f"    {col[3:]}: {last_row[col]:.4f}")

if __name__ == "__main__":
    main()