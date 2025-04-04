"""Model handler module for managing simulation inputs and outputs."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mpm.plant import Plant
from mpm.atmosphere import Atmosphere
from mpm.environment import AbovegroundEnvironment

class ModelHandler:
    """Model Handler class for taking in input files and running the simulation.
    
    Attributes:
        drivers_filename (str): Path to the drivers CSV file.
        parameter_filename (str): Path to the parameters CSV file.
        resource_pool_filename (str): Path to the resource pool parameters CSV file.
    """
    def __init__(self, drivers_filename, parameter_filename, resource_pool_filename):
        self.drivers_filename = drivers_filename
        self.parameter_filename = parameter_filename
        self.resource_pool_filename = resource_pool_filename
        self.latitude = None

    def read_input_files(self):
        """Read input CSV files for drivers, parameters, and resource pools.
        
        Returns:
            tuple: (drivers, params_dict, resource_pool_params)
        """
        # Read input CSV files for drivers and parameters
        drivers = pd.read_csv(self.drivers_filename)
        params = pd.read_csv(self.parameter_filename, header=None, usecols=[0, 1])
        params_dict = params.set_index(0).to_dict()[1]
        self.latitude = float(params_dict.get("latitude", 33))  # Default to 30 if not found
        resource_pool_params = pd.read_csv(self.resource_pool_filename)
        resource_pool_params = resource_pool_params.to_dict(orient='records')
        return drivers, params_dict, resource_pool_params

    def plot_outputs(self):
        """Plot simulation outputs using matplotlib."""
        # Plot assimilation (y-axis)
        plt.plot(list(range(1500, 1600)), self.log_assimilation[1500:1600], marker='o', linestyle='-')
        plt.xlabel('Time Step')
        plt.ylabel('Assimilation')
        plt.grid(True)
        plt.show()

        # Plotting lai
        plt.plot(list(range(len(self.log_lai))), self.log_lai, linestyle='-')
        plt.xlabel('Time Step')
        plt.ylabel('lai')
        plt.grid(True)
        plt.show()

        # Plotting rp 1 demand
        plt.plot(list(range(len(self.log_rp_demand))), self.log_rp_demand, linestyle='-')
        plt.xlabel('Time Step')
        plt.ylabel('rp demand')
        plt.grid(True)
        plt.show()

        # Plotting RGR (y-axis)
        plt.plot(self.log_thermal_age, self.log_rp_rgr, linestyle='-')
        plt.xlabel('thermal time (deg day)')
        plt.ylabel('rp rgr')
        plt.grid(True)
        plt.show()

        # Plotting available C
        plt.plot(self.log_thermal_age, self.log_carbon_pool, linestyle='-')
        plt.xlabel('thermal time (deg day)')
        plt.ylabel('carbon pool')
        plt.grid(True)
        plt.show()

        # plot multiple RPs
        for name, sizes in self.log_resource_pool_sizes.items():
            plt.plot(sizes, label=name)
        plt.xlabel('timestep')
        plt.ylabel('RP Size')
        plt.legend()
        plt.show()

    def initialize_logs(self, plant_instance):
        """Initialize log containers for simulation outputs.
        
        Args:
            plant_instance (Plant): The plant instance being simulated.
        """
        self.log_thermal_age = []
        self.log_assimilation = []
        self.log_lai = []
        self.log_rp = []
        self.log_rp_demand = []
        self.log_rp_rgr = []
        self.log_carbon_pool = []
        self.log_resource_pool_sizes = {rp.name: [] for rp in plant_instance.get_resource_pools()}

    def update_logs(self, plant_instance):
        """Update logs with current plant state.
        
        Args:
            plant_instance (Plant): The plant instance being simulated.
        """
        self.log_assimilation.append(plant_instance.get_assimilation_sunlit())
        self.log_thermal_age.append(plant_instance.get_thermal_age())
        self.log_lai.append(plant_instance.get_leaf_area_index())
        self.log_rp.append(plant_instance.get_resource_pools()[0].current_size)
        self.log_rp_demand.append(plant_instance.get_resource_pools()[0].demand)
        self.log_rp_rgr.append(plant_instance.get_resource_pools()[0].rgr)
        self.log_carbon_pool.append(plant_instance.get_carbon_pool())
        # update resource pools sizes for any number of resource pools
        for rp in plant_instance.get_resource_pools():
            self.log_resource_pool_sizes[rp.name].append(rp.current_size)

    def run_simulation(self):
        """Run simulation by looping through each timestep.
        
        A plant object is instantiated once whereas atmosphere and environment objects are
        instantiated each timestep. Plant does not know about time or space.
        """
        # Runs simulation by looping through each hourly timestep
        drivers, params_dict, resource_pool_params = self.read_input_files()

        # Create a plant object with resource pools
        plant_simulated = Plant(params_dict, resource_pool_params)
        plant_simulated.create_resource_pools()

        self.initialize_logs(plant_simulated)

        for index, row in drivers.iterrows():
            DOY = row['DOY']
            latitude = self.latitude
            hour = row['Hour']

            # atmosphere object for computing atmospheric properties at this timestep
            atmosphere_instance = Atmosphere(DOY, latitude, hour)
            atmosphere_instance.compute_atmospheric_properties()

            # put together a collective exogenous inputs dict
            exogenous_inputs = atmosphere_instance.get_atmospheric_properties()
            driver_entries = {
                'temperature': row['temperature'],
                'radiation': row['radiation'],
                'precipitation': row['precipitation'],
                'wind_speed': row['wind_speed'],
                'VPD': row['VPD'],
                'latitude': self.latitude
            }
            exogenous_inputs.update(driver_entries)

            # environment object that acts as interface between plant and non-plant - just aboveground environment for now
            aboveground_environment_instance = AbovegroundEnvironment(exogenous_inputs)
            aboveground_environment_instance.compute_canopy_light_environment(
                Leaf_Blade_Angle=plant_simulated.get_parameters()['Leaf_Blade_Angle'],
                Leaf_Area_Index=plant_simulated.get_leaf_area_index()
            )

            # one simulation step of plant
            plant_simulated.simulate_plant(aboveground_environment_instance.get_environmental_variables())

            # update logs
            self.update_logs(plant_simulated)
