"""Main model module for coordinating simulation execution."""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple, Union
import logging

from .plant import Plant
from .environment.atmosphere import Atmosphere
from .environment.aboveground_environment import AbovegroundEnvironment
from .utils import read_parameters_file, read_resource_pools_file, convert_parameter_types
from .visualization import plot_model_outputs

class MainModel:
    """Main model class for coordinating simulation execution.
    
    This class handles input/output, coordinates the simulation workflow,
    and manages connections between different model components.
    
    Attributes:
        drivers_filename (str): Path to the drivers CSV file
        parameter_filename (str): Path to the parameters CSV file
        resource_pool_filename (str): Path to the resource pool parameters CSV file
        latitude (float): Latitude in degrees
        log_thermal_age (list): Log of thermal age values
        log_assimilation (list): Log of assimilation values
        log_lai (list): Log of LAI values
        log_rp (list): Log of primary resource pool size
        log_rp_demand (list): Log of resource pool demand
        log_rp_rgr (list): Log of relative growth rate
        log_carbon_pool (list): Log of carbon pool size
        log_resource_pool_sizes (dict): Dictionary of resource pool sizes by name
    """
    def __init__(self, drivers_filename: str, parameter_filename: str, resource_pool_filename: str):
        """Initialize the MainModel with input file paths.
        
        Args:
            drivers_filename: Path to CSV file with environmental driver data
            parameter_filename: Path to CSV file with model parameters
            resource_pool_filename: Path to CSV file with resource pool configurations
        """
        self.drivers_filename = drivers_filename
        self.parameter_filename = parameter_filename
        self.resource_pool_filename = resource_pool_filename
        self.latitude = None
        
        # Log containers for simulation results
        self.log_thermal_age = []
        self.log_assimilation = []
        self.log_lai = []
        self.log_rp = []
        self.log_rp_demand = []
        self.log_rp_rgr = []
        self.log_carbon_pool = []
        self.log_resource_pool_sizes = {}

    def read_input_files(self) -> Tuple[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]:
        """Read and process input files for the simulation.
        
        Returns:
            Tuple containing:
            - drivers (DataFrame): Environmental driver data
            - params_dict (dict): Model parameters
            - resource_pool_params (list): Resource pool configurations
        """
        # Read environmental drivers
        drivers = pd.read_csv(self.drivers_filename)
        
        # Read model parameters
        params_str = read_parameters_file(self.parameter_filename)
        params_dict = convert_parameter_types(params_str)
        
        # Set latitude from parameters or use default
        self.latitude = float(params_dict.get("latitude", 33))
        
        # Read resource pool configurations
        resource_pool_params = read_resource_pools_file(self.resource_pool_filename)
        
        return drivers, params_dict, resource_pool_params

    def initialize_logs(self, plant_instance: Plant) -> None:
        """Initialize log containers for simulation outputs.
        
        Args:
            plant_instance: The plant instance being simulated
        """
        self.log_thermal_age = []
        self.log_assimilation = []
        self.log_lai = []
        self.log_rp = []
        self.log_rp_demand = []
        self.log_rp_rgr = []
        self.log_carbon_pool = []
        self.log_resource_pool_sizes = {rp.name: [] for rp in plant_instance.get_resource_pools()}

    def update_logs(self, plant_instance: Plant) -> None:
        """Update logs with current plant state.
        
        Args:
            plant_instance: The plant instance being simulated
        """
        self.log_assimilation.append(plant_instance.get_assimilation_sunlit())
        self.log_thermal_age.append(plant_instance.get_thermal_age())
        self.log_lai.append(plant_instance.get_leaf_area_index())
        self.log_rp.append(plant_instance.get_resource_pools()[0].current_size)
        self.log_rp_demand.append(plant_instance.get_resource_pools()[0].demand)
        self.log_rp_rgr.append(plant_instance.get_resource_pools()[0].rgr)
        self.log_carbon_pool.append(plant_instance.get_carbon_pool())
        
        # Update resource pools sizes for any number of resource pools
        for rp in plant_instance.get_resource_pools():
            self.log_resource_pool_sizes[rp.name].append(rp.current_size)

    def run_simulation(self, max_steps: Optional[int] = None, 
                      progress_callback: Optional[callable] = None) -> None:
        """Run the simulation by stepping through environmental driver data.
        
        Args:
            max_steps: Maximum number of timesteps to simulate (optional)
            progress_callback: Callback function for progress updates (optional)
        """
        # Read input files
        drivers, params_dict, resource_pool_params = self.read_input_files()
        
        # Limit steps if specified
        if max_steps is not None:
            drivers = drivers.iloc[:max_steps]
        
        total_steps = len(drivers)
        
        # Create plant instance and resource pools
        plant_simulated = Plant(params_dict, resource_pool_params)
        plant_simulated.create_resource_pools()
        
        # Initialize logs
        self.initialize_logs(plant_simulated)
        
        # Run simulation timesteps
        for index, row in drivers.iterrows():
            # Report progress if callback provided
            if progress_callback and index % 100 == 0:
                progress_callback(index, total_steps)
            
            # Get time and location data
            DOY = row['DOY']
            latitude = self.latitude
            hour = row['Hour']
            
            # Create atmosphere instance and compute properties
            atmosphere_instance = Atmosphere(DOY, latitude, hour)
            atmosphere_instance.compute_atmospheric_properties()
            
            # Combine atmospheric properties with other environmental drivers
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
            
            # Create aboveground environment instance
            aboveground_environment_instance = AbovegroundEnvironment(exogenous_inputs)
            
            # Compute canopy light environment
            aboveground_environment_instance.compute_canopy_light_environment(
                Leaf_Blade_Angle=plant_simulated.get_parameters()['Leaf_Blade_Angle'],
                Leaf_Area_Index=plant_simulated.get_leaf_area_index()
            )
            
            # Simulate one timestep for the plant
            plant_simulated.simulate_plant(
                aboveground_environment_instance.get_environmental_variables()
            )
            
            # Update logs with current plant state
            self.update_logs(plant_simulated)
        
        # Final progress update
        if progress_callback:
            progress_callback(total_steps, total_steps)

    def plot_outputs(self) -> None:
        """Plot simulation outputs using matplotlib."""
        plot_model_outputs(self)
    
    def get_results_dataframe(self) -> pd.DataFrame:
        """Get simulation results as a pandas DataFrame.
        
        Returns:
            DataFrame with simulation results
        """
        results = pd.DataFrame({
            'thermal_age': self.log_thermal_age,
            'assimilation': self.log_assimilation,
            'lai': self.log_lai,
            'carbon_pool': self.log_carbon_pool,
            'rp_demand': self.log_rp_demand,
            'rp_rgr': self.log_rp_rgr
        })
        
        # Add resource pool sizes
        for name, sizes in self.log_resource_pool_sizes.items():
            results[f'rp_{name}'] = sizes
            
        return results
    
    def save_results(self, output_file: str) -> None:
        """Save simulation results to a CSV file.
        
        Args:
            output_file: Path to save the results CSV
        """
        results_df = self.get_results_dataframe()
        results_df.to_csv(output_file, index=False)