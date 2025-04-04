"""Example showing how to create a custom environment in MPM."""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from minimum_plant_model import MainModel, Environment, Plant
from minimum_plant_model.utils import read_parameters_file, read_resource_pools_file, convert_parameter_types

class UndergroundEnvironment(Environment):
    """Example custom environment class for belowground processes.
    
    This class extends the base Environment class to simulate belowground
    conditions like soil temperature, moisture, and nutrient availability.
    """
    
    def __init__(self, exogenous_inputs):
        """Initialize the UndergroundEnvironment.
        
        Args:
            exogenous_inputs (dict): Dictionary of external environmental inputs
        """
        super().__init__(exogenous_inputs)
        
        # Calculate soil temperature as a function of air temperature with damping
        air_temp = exogenous_inputs.get('temperature', 20)
        self.soil_temperature = 0.8 * air_temp + 4  # Soil temp has less variation than air temp
        
        # Initialize environment variables
        self.__environmental_variables = {
            'soil_temperature': self.soil_temperature,
            'soil_moisture': exogenous_inputs.get('precipitation', 0) * 0.7,  # Simple infiltration model
            'nitrogen_availability': 10.0  # Example constant value
        }
    
    def compute_soil_properties(self, precipitation, temperature):
        """Compute soil properties based on environmental conditions.
        
        Args:
            precipitation (float): Precipitation amount
            temperature (float): Air temperature
        """
        # Update soil temperature with time lag
        self.soil_temperature = 0.9 * self.soil_temperature + 0.1 * temperature
        
        # Simple soil moisture model
        soil_moisture = self.__environmental_variables.get('soil_moisture', 0)
        
        # Add precipitation input to soil moisture
        soil_moisture += precipitation * 0.7
        
        # Simple loss from evaporation based on temperature
        evaporation = 0.05 * temperature if temperature > 0 else 0
        soil_moisture = max(0, soil_moisture - evaporation)
        
        # Update environmental variables
        self.__environmental_variables.update({
            'soil_temperature': self.soil_temperature,
            'soil_moisture': soil_moisture,
        })
    
    def get_environmental_variables(self):
        """Get the environmental variables dictionary."""
        return self.__environmental_variables

def run_custom_environment_simulation():
    """Run a simulation with a custom environment component."""
    # Get the absolute path to the input files
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    parameter_file = os.path.join(base_dir, 'model input files/parameters.csv')
    resource_pool_file = os.path.join(base_dir, 'model input files/resource_pools_2RPs.csv')
    
    # Read parameters and resource pools
    params_str = read_parameters_file(parameter_file)
    params_dict = convert_parameter_types(params_str)
    resource_pool_params = read_resource_pools_file(resource_pool_file)
    
    # Create plant instance
    plant = Plant(params_dict, resource_pool_params)
    plant.create_resource_pools()
    
    # Set up simulation variables
    n_steps = 2000
    results = {
        'thermal_age': [],
        'lai': [],
        'carbon_pool': [],
        'soil_moisture': [],
        'rp_sizes': {rp.name: [] for rp in plant.get_resource_pools()}
    }
    
    # Create custom synthetic drivers
    temperatures = np.sin(np.linspace(0, 4*np.pi, n_steps)) * 10 + 20  # Temperature varying between 10-30°C
    radiation = np.sin(np.linspace(0, 8*np.pi, n_steps)) * 400 + 500  # Radiation varying between 100-900 W/m²
    precipitation = np.zeros(n_steps)
    precipitation[::100] = 10  # Rain event every 100 steps
    
    print("Running simulation with custom environment...")
    
    # Run simulation loop
    for i in range(n_steps):
        # Progress indicator
        if i % 100 == 0:
            print(f"Step {i}/{n_steps}")
        
        # Create atmospheric inputs
        atmospheric_inputs = {
            'Sin_Beam': 0.5,
            'Solar_Constant': 1367,
            'temperature': temperatures[i],
            'radiation': radiation[i],
            'precipitation': precipitation[i],
            'wind_speed': 2.0,
            'VPD': 1.0,
            'latitude': 40
        }
        
        # Create underground environment
        underground_env = UndergroundEnvironment(atmospheric_inputs)
        underground_env.compute_soil_properties(precipitation[i], temperatures[i])
        
        # Create aboveground environment (using the standard model class)
        from minimum_plant_model.environment import AbovegroundEnvironment
        aboveground_env = AbovegroundEnvironment(atmospheric_inputs)
        aboveground_env.compute_canopy_light_environment(
            Leaf_Blade_Angle=plant.get_parameters()['Leaf_Blade_Angle'],
            Leaf_Area_Index=plant.get_leaf_area_index()
        )
        
        # Merge environmental variables
        env_vars = aboveground_env.get_environmental_variables()
        env_vars.update(underground_env.get_environmental_variables())
        
        # Simulate plant step
        plant.simulate_plant(env_vars)
        
        # Store results
        results['thermal_age'].append(plant.get_thermal_age())
        results['lai'].append(plant.get_leaf_area_index())
        results['carbon_pool'].append(plant.get_carbon_pool())
        results['soil_moisture'].append(env_vars['soil_moisture'])
        for rp in plant.get_resource_pools():
            results['rp_sizes'][rp.name].append(rp.current_size)
    
    print("Simulation complete. Generating plots...")
    
    # Plot results
    plt.figure(figsize=(12, 8))
    
    # Plot LAI
    plt.subplot(2, 2, 1)
    plt.plot(results['lai'])
    plt.xlabel('Time Step')
    plt.ylabel('LAI')
    plt.title('Leaf Area Index')
    plt.grid(True)
    
    # Plot carbon pool
    plt.subplot(2, 2, 2)
    plt.plot(results['thermal_age'], results['carbon_pool'])
    plt.xlabel('Thermal Time')
    plt.ylabel('Carbon Pool')
    plt.title('Carbon Pool vs Thermal Time')
    plt.grid(True)
    
    # Plot resource pools
    plt.subplot(2, 2, 3)
    for name, sizes in results['rp_sizes'].items():
        plt.plot(sizes, label=name)
    plt.xlabel('Time Step')
    plt.ylabel('Size')
    plt.title('Resource Pool Sizes')
    plt.legend()
    plt.grid(True)
    
    # Plot soil moisture
    plt.subplot(2, 2, 4)
    plt.plot(results['soil_moisture'])
    plt.xlabel('Time Step')
    plt.ylabel('Moisture')
    plt.title('Soil Moisture')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("Example completed!")

if __name__ == "__main__":
    run_custom_environment_simulation()