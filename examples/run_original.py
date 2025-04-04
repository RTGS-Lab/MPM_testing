#!/usr/bin/env python
"""Run the original model for comparison."""

import os
import sys

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the original ModelHandler class
from original_for_comparison import ModelHandler

def main():
    """Run the original model with the same data files."""
    print("Starting original model simulation...")
    
    # Use the same data files
    driver_file = 'examples/data/drivers_natural_all.csv'
    parameter_file = 'examples/data/parameters.csv'
    resource_pool_file = 'examples/data/resource_pools_3RPs.csv'
    
    # Create and run the model
    model = ModelHandler(driver_file, parameter_file, resource_pool_file)
    
    try:
        model.run_simulation()
        print("Simulation completed!")
        
        # Print the final values for comparison
        print("\nFinal simulation values:")
        print(f"  Thermal age: {model.log_thermal_age[-1]:.2f}")
        print(f"  Leaf area index: {model.log_lai[-1]:.4f}")
        print(f"  Carbon pool: {model.log_carbon_pool[-1]:.4f}")
        
        # Print resource pool sizes
        print("  Resource pool sizes:")
        for name, sizes in model.log_resource_pool_sizes.items():
            print(f"    {name}: {sizes[-1]:.4f}")
            
    except Exception as e:
        print(f"Error running simulation: {e}")

if __name__ == "__main__":
    main()