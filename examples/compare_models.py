#!/usr/bin/env python
"""Compare the original and refactored models."""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from original_for_comparison import ModelHandler
from minimum_plant_model import MainModel

def run_original_model():
    """Run the original model with the test data."""
    print("Running original model...")
    
    # Use the same data files
    driver_file = 'examples/data/drivers_natural_all.csv'
    parameter_file = 'examples/data/parameters.csv'
    resource_pool_file = 'examples/data/resource_pools_3RPs.csv'
    
    # Create and run the model
    model = ModelHandler(driver_file, parameter_file, resource_pool_file)
    model.run_simulation()
    
    # Create a dataframe from the model results
    original_df = pd.DataFrame({
        'thermal_age': model.log_thermal_age,
        'assimilation': model.log_assimilation,
        'lai': model.log_lai,
        'carbon_pool': model.log_carbon_pool,
        'rp_rgr': model.log_rp_rgr
    })
    
    # Add resource pool sizes
    for name, sizes in model.log_resource_pool_sizes.items():
        original_df[f'rp_{name}'] = sizes
    
    return original_df, model

def run_refactored_model():
    """Run the refactored model with the test data."""
    print("Running refactored model...")
    
    # Use the same data files
    driver_file = 'examples/data/drivers_natural_all.csv'
    parameter_file = 'examples/data/parameters.csv'
    resource_pool_file = 'examples/data/resource_pools_3RPs.csv'
    
    # Create and run the model
    model = MainModel(driver_file, parameter_file, resource_pool_file)
    model.run_simulation()
    
    # Get results as a dataframe
    refactored_df = model.get_results_dataframe()
    
    return refactored_df, model

def compare_models():
    """Run both models and compare their results."""
    print("Starting model comparison...")
    
    # Run both models
    original_df, original_model = run_original_model()
    refactored_df, refactored_model = run_refactored_model()
    
    # Save full results to CSV
    original_df.to_csv('original_results.csv', index=False)
    refactored_df.to_csv('refactored_results.csv', index=False)
    
    # Print comparison of final values
    print("\nComparison of final values:")
    
    # Common metrics to compare
    metrics = ['thermal_age', 'lai', 'carbon_pool']
    
    print(f"{'Metric':<15} {'Original':<15} {'Refactored':<15} {'Difference':<15} {'% Diff':<15}")
    print("-" * 75)
    
    for metric in metrics:
        original_value = original_df[metric].iloc[-1]
        refactored_value = refactored_df[metric].iloc[-1]
        diff = refactored_value - original_value
        percent_diff = diff / original_value * 100 if original_value != 0 else float('inf')
        
        print(f"{metric:<15} {original_value:<15.4f} {refactored_value:<15.4f} {diff:<15.4f} {percent_diff:<15.2f}%")
    
    # Compare resource pool sizes
    print("\nResource Pool Sizes:")
    for col in refactored_df.columns:
        if col.startswith('rp_') and not col.endswith('rgr') and not col.endswith('demand'):
            pool_name = col[3:]  # Remove 'rp_' prefix
            
            original_value = original_df[col].iloc[-1] if col in original_df.columns else None
            refactored_value = refactored_df[col].iloc[-1]
            
            if original_value is not None:
                diff = refactored_value - original_value
                percent_diff = diff / original_value * 100 if original_value != 0 else float('inf')
                print(f"{pool_name:<15} {original_value:<15.4f} {refactored_value:<15.4f} {diff:<15.4f} {percent_diff:<15.2f}%")
            else:
                print(f"{pool_name:<15} {'N/A':<15} {refactored_value:<15.4f} {'N/A':<15} {'N/A':<15}")
    
    # Create comparison plots
    print("\nGenerating comparison plots...")
    
    # Create plot directory if it doesn't exist
    os.makedirs('comparison_plots', exist_ok=True)
    
    # Plot thermal age vs LAI
    plt.figure(figsize=(10, 6))
    plt.plot(original_df['thermal_age'], original_df['lai'], label='Original')
    plt.plot(refactored_df['thermal_age'], refactored_df['lai'], label='Refactored')
    plt.xlabel('Thermal Age (degree days)')
    plt.ylabel('Leaf Area Index')
    plt.title('Leaf Area Index Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('comparison_plots/lai_comparison.png')
    
    # Plot thermal age vs carbon pool
    plt.figure(figsize=(10, 6))
    plt.plot(original_df['thermal_age'], original_df['carbon_pool'], label='Original')
    plt.plot(refactored_df['thermal_age'], refactored_df['carbon_pool'], label='Refactored')
    plt.xlabel('Thermal Age (degree days)')
    plt.ylabel('Carbon Pool')
    plt.title('Carbon Pool Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('comparison_plots/carbon_pool_comparison.png')
    
    # Plot assimilation
    plt.figure(figsize=(10, 6))
    x_range = range(1500, 1600)
    plt.plot(x_range, original_df['assimilation'].iloc[1500:1600], label='Original')
    plt.plot(x_range, refactored_df['assimilation'].iloc[1500:1600], label='Refactored')
    plt.xlabel('Timestep')
    plt.ylabel('Assimilation')
    plt.title('Assimilation Comparison (Sample range 1500-1600)')
    plt.legend()
    plt.grid(True)
    plt.savefig('comparison_plots/assimilation_comparison.png')
    
    print(f"Plots saved to the 'comparison_plots' directory.")

if __name__ == "__main__":
    compare_models()