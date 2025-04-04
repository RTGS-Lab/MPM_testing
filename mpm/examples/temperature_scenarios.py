"""Temperature scenarios simulation example using the Minimum Plant Model."""

import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

# Add the parent directory to the path so we can import the mpm module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mpm import ModelHandler

def run_temperature_scenarios():
    """Run simulations with different temperature scenarios."""
    # Get the absolute path to the input files
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    parameter_file = os.path.join(base_dir, 'model input files/parameters.csv')
    resource_pool_file = os.path.join(base_dir, 'model input files/resource_pools_2RPs.csv')
    
    temp_scenarios_dir = os.path.join(base_dir, 'model input files/temperature_scenarios')
    scenario_files = [
        'drivers_setpoints_low_temperature.csv',
        'drivers_setpoints_medium_temperature.csv',
        'drivers_setpoints_high_temperature.csv'
    ]
    
    # Store results for comparison
    scenario_results = {}
    
    for scenario_file in scenario_files:
        scenario_name = scenario_file.replace('drivers_setpoints_', '').replace('.csv', '')
        print(f"Running {scenario_name} scenario...")
        
        driver_file = os.path.join(temp_scenarios_dir, scenario_file)
        
        # Create model instance
        model = ModelHandler(driver_file, parameter_file, resource_pool_file)
        
        # Run simulation
        model.run_simulation()
        
        # Store results
        scenario_results[scenario_name] = {
            'thermal_age': model.log_thermal_age,
            'lai': model.log_lai,
            'carbon_pool': model.log_carbon_pool,
            'rp_sizes': model.log_resource_pool_sizes
        }
    
    # Compare results across scenarios
    plt.figure(figsize=(10, 6))
    for scenario, results in scenario_results.items():
        plt.plot(range(len(results['lai'])), results['lai'], label=scenario)
    plt.xlabel('Time Step')
    plt.ylabel('Leaf Area Index')
    plt.title('Comparison of LAI Across Temperature Scenarios')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    plt.figure(figsize=(10, 6))
    for scenario, results in scenario_results.items():
        plt.plot(results['thermal_age'], results['carbon_pool'], label=scenario)
    plt.xlabel('Thermal Time (deg day)')
    plt.ylabel('Carbon Pool Size')
    plt.title('Comparison of Carbon Pool Across Temperature Scenarios')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_temperature_scenarios()
