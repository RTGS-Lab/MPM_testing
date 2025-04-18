"""Example script showing how to use the separate classes imported from original_for_comparison.py"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Make sure the parent directory is in the path to import from original_for_comparison.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import classes directly from original_for_comparison.py
from original_for_comparison import Plant, ResourcePool, CarbonAssimilation, PriorityQueue
from original_for_comparison import Atmosphere, AbovegroundEnvironment, Environment

def run_with_separate_classes():
    """Run simulation using the separate classes directly without ModelHandler."""
    
    # Set up paths to data files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    # Read parameters and resource pool configurations
    params_df = pd.read_csv(os.path.join(data_dir, 'parameters.csv'), header=None, usecols=[0, 1])
    params_dict = params_df.set_index(0).to_dict()[1]
    
    resource_pool_params = pd.read_csv(os.path.join(data_dir, 'resource_pools_3RPs.csv'))
    resource_pool_params = resource_pool_params.to_dict(orient='records')
    
    # Read drivers data
    drivers = pd.read_csv(os.path.join(data_dir, 'drivers_natural_all.csv'))
    
    # Create a plant object with resource pools
    plant = Plant(params_dict, resource_pool_params)
    plant.create_resource_pools()
    
    # Initialize logs to track simulation values
    thermal_age_log = []
    assimilation_log = []
    lai_log = []
    rp_log = []
    rp_rgr_log = []
    carbon_pool_log = []
    resource_pool_sizes_log = {rp.name: [] for rp in plant.get_resource_pools()}
    
    # Get latitude from parameters (default to 33 if not found)
    latitude = float(params_dict.get("latitude", 33))
    
    # Run simulation for each timestep
    for index, row in drivers.iterrows():
        if index % 500 == 0:
            print(f"Progress: {index}/{len(drivers)} timesteps ({index/len(drivers)*100:.1f}%)")
            
        DOY = row['DOY']
        hour = row['Hour']
        
        # Create atmosphere object for this timestep
        atmosphere = Atmosphere(DOY, latitude, hour)
        atmosphere.compute_atmospheric_properties()
        
        # Combine atmospheric properties with driver data
        exogenous_inputs = atmosphere.get_atmospheric_properties()
        driver_entries = {
            'temperature': row['temperature'],
            'radiation': row['radiation'],
            'precipitation': row['precipitation'],
            'wind_speed': row['wind_speed'],
            'VPD': row['VPD'],
            'latitude': latitude
        }
        exogenous_inputs.update(driver_entries)
        
        # Create environment object
        aboveground_environment = AbovegroundEnvironment(exogenous_inputs)
        aboveground_environment.compute_canopy_light_environment(
            Leaf_Blade_Angle=plant.get_parameters()['Leaf_Blade_Angle'],
            Leaf_Area_Index=plant.get_leaf_area_index()
        )
        
        # Simulate one timestep
        plant.simulate_plant(aboveground_environment.get_environmental_variables())
        
        # Log results
        assimilation_log.append(plant.get_assimilation_sunlit())
        thermal_age_log.append(plant.get_thermal_age())
        lai_log.append(plant.get_leaf_area_index())
        rp_log.append(plant.get_resource_pools()[0].current_size)
        rp_rgr_log.append(plant.get_resource_pools()[0].rgr)
        carbon_pool_log.append(plant.get_carbon_pool())
        
        # Log resource pool sizes
        for rp in plant.get_resource_pools():
            resource_pool_sizes_log[rp.name].append(rp.current_size)
    
    print("Simulation completed!")
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(list(range(1500, 1600)), assimilation_log[1500:1600], marker='o', linestyle='-')
    plt.xlabel('Time Step')
    plt.ylabel('Assimilation')
    plt.grid(True)
    plt.title('Assimilation Rate (Original Classes)')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.plot(list(range(len(lai_log))), lai_log, linestyle='-')
    plt.xlabel('Time Step')
    plt.ylabel('LAI')
    plt.grid(True)
    plt.title('Leaf Area Index Over Time (Original Classes)')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.plot(thermal_age_log, rp_rgr_log, linestyle='-')
    plt.xlabel('Thermal Time (deg day)')
    plt.ylabel('RP RGR')
    plt.grid(True)
    plt.title('Resource Pool Relative Growth Rate (Original Classes)')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.plot(thermal_age_log, carbon_pool_log, linestyle='-')
    plt.xlabel('Thermal Time (deg day)')
    plt.ylabel('Carbon Pool')
    plt.grid(True)
    plt.title('Carbon Pool Over Time (Original Classes)')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    for name, sizes in resource_pool_sizes_log.items():
        plt.plot(sizes, label=name)
    plt.xlabel('Timestep')
    plt.ylabel('RP Size')
    plt.legend()
    plt.title('Resource Pool Sizes Over Time (Original Classes)')
    plt.show()

if __name__ == "__main__":
    run_with_separate_classes()