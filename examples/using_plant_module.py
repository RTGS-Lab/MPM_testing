"""Example script demonstrating how to use the plant module classes directly."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Add the parent directory to the sys.path so we can import the module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import classes from the minimum_plant_model package
from minimum_plant_model.plant import Plant, ResourcePool, CarbonAssimilation, PriorityQueue
from minimum_plant_model.environment import AbovegroundEnvironment, Atmosphere

def run_direct_example():
    """Run an example using the classes directly without the ModelHandler."""
    
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
    
    # Create plots similar to the original model
    plt.figure(figsize=(10, 6))
    plt.plot(list(range(1500, 1600)), assimilation_log[1500:1600], marker='o', linestyle='-')
    plt.xlabel('Time Step')
    plt.ylabel('Assimilation')
    plt.grid(True)
    plt.title('Assimilation Rate')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.plot(list(range(len(lai_log))), lai_log, linestyle='-')
    plt.xlabel('Time Step')
    plt.ylabel('LAI')
    plt.grid(True)
    plt.title('Leaf Area Index Over Time')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.plot(thermal_age_log, rp_rgr_log, linestyle='-')
    plt.xlabel('Thermal Time (deg day)')
    plt.ylabel('RP RGR')
    plt.grid(True)
    plt.title('Resource Pool Relative Growth Rate')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.plot(thermal_age_log, carbon_pool_log, linestyle='-')
    plt.xlabel('Thermal Time (deg day)')
    plt.ylabel('Carbon Pool')
    plt.grid(True)
    plt.title('Carbon Pool Over Time')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    for name, sizes in resource_pool_sizes_log.items():
        plt.plot(sizes, label=name)
    plt.xlabel('Timestep')
    plt.ylabel('RP Size')
    plt.legend()
    plt.title('Resource Pool Sizes Over Time')
    plt.show()

if __name__ == "__main__":
    run_direct_example()