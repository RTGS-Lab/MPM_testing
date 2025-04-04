"""Plant module that handles plant growth and resource allocation."""

from typing import Dict, List, Optional, Union, Any, Tuple
import logging

from .carbon_assimilation import CarbonAssimilation
from .resource_pool import ResourcePool

class Plant:
    """Class representing the whole plant organism and its processes.
    
    This class integrates various physiological processes including carbon assimilation,
    carbon allocation to different resource pools (e.g., leaves, stems, roots), and
    growth based on thermal time.
    
    Attributes:
        resource_pool_params (list): List of parameters for different resource pools
        latitude (float): Plant location latitude (used in some models)
        carbon_assimilation (CarbonAssimilation): Carbon assimilation process object
        __thermal_age (float): Current thermal age of the plant
        __assimilation_sunlit (float): Photosynthesis rate in sunlit leaf fraction
        __assimilation_shaded (float): Photosynthesis rate in shaded leaf fraction
        __Leaf_Area_Index (float): Leaf area index (m² leaf / m² ground)
        __carbon_pool (float): Available carbon pool for allocation
        __parameters (dict): Plant parameters dictionary
        __thermal_age_increment (float): Latest thermal age increment
        __resource_pools (list): List of ResourcePool objects
    """
    
    def __init__(self, params_dict: Dict[str, Any], resource_pool_params: List[Dict[str, Any]]):
        """Initialize Plant object with parameters and resource pool specifications.
        
        Args:
            params_dict: Dictionary of plant parameters
            resource_pool_params: List of parameters for resource pools
        """
        self.resource_pool_params = resource_pool_params
        self.__thermal_age = 0.0
        self.__assimilation_sunlit = 0.0
        self.__assimilation_shaded = 0.0
        self.__Leaf_Area_Index = 0.005
        self.__carbon_pool = 0.03
        self.__parameters = params_dict
        self.__thermal_age_increment = 0.0
        self.latitude = 0
        
        # Instantiate process objects to handle physiology
        self.carbon_assimilation = CarbonAssimilation(self.__parameters)
        self.__resource_pools = []

    def create_resource_pools(self) -> None:
        """Create resource pool objects based on resource pool parameters."""
        self.__resource_pools = [
            ResourcePool(
                name=rp['name'],
                thermal_time_initiation=rp['thermal_time_initiation'],
                allocation_priority=rp['growth_allocation_priority'],
                max_size=rp['max_size'],
                initial_size=rp['initial_size'],
                growth_rate=rp['rate']
            ) for rp in self.resource_pool_params
        ]

    def update_thermal_age(self, environmental_variables: Dict[str, float]) -> None:
        """Compute thermal age increment and update thermal age.
        
        Thermal age (in degree-days) is calculated based on the difference between
        the current temperature and the base temperature, divided by 24 to convert
        from hourly to daily units.
        
        Args:
            environmental_variables: Dictionary of environmental variables including temperature
        """
        # Calculate thermal age increase on hourly basis
        thermal_age_increment = (environmental_variables['temperature'] - 
                                self.__parameters['Base_temperature']) / 24
        
        # No negative thermal age accumulation
        if thermal_age_increment < 0:
            thermal_age_increment = 0
            
        # Update thermal age and increment
        self.__thermal_age += thermal_age_increment
        self.__thermal_age_increment = thermal_age_increment

    def carry_out_photosynthesis(self, environmental_variables: Dict[str, float]) -> None:
        """Carry out photosynthesis for sunlit and shaded components of the canopy.
        
        Args:
            environmental_variables: Dictionary of environmental variables needed for photosynthesis
        """
        self.__assimilation_sunlit, self.__assimilation_shaded = \
            self.carbon_assimilation.sunlit_shaded_photosynthesis(environmental_variables)

    def compute_carbon_assimilated(self, environmental_variables: Dict[str, float]) -> None:
        """Calculate carbon assimilated and update carbon pool.
        
        Converts photosynthesis rates from leaf area basis to plant basis by accounting for
        leaf area index, sunlit/shaded fractions, and ground area per plant.
        
        Args:
            environmental_variables: Dictionary of environmental variables
        """
        # Extract sunlit fraction of canopy
        Sunlit_Fraction = environmental_variables['Sunlit_fraction']
        
        # Calculate average photosynthesis rate weighted by sunlit and shaded fractions
        Canopy_Photosynthesis_average = (
            self.__assimilation_sunlit * Sunlit_Fraction + 
            self.__assimilation_shaded * (1 - Sunlit_Fraction)
        )  # Units: µmol CO₂ m⁻² s⁻¹ (leaf area basis)

        # Convert to total carbon assimilated
        # Step 1: Convert to ground area basis by multiplying by LAI
        # Step 2: Convert from per second to per hour (3600 seconds)
        Canopy_total_carbon_assimilated = Canopy_Photosynthesis_average * 3600 * self.__Leaf_Area_Index
        
        # Step 3: Convert from µmol CO₂ to g carbon (1E-6 mol/µmol × 12 g C/mol CO₂)
        Canopy_total_carbon_assimilated *= (1E-6) * 12
        
        # Step 4: Convert from per m² ground to per plant basis
        Canopy_total_carbon_assimilated *= self.__parameters['Single_plant_ground_area']
        
        # Add assimilated carbon to the carbon pool
        self.__carbon_pool += Canopy_total_carbon_assimilated

    def allocate_carbon(self, environmental_variables: Dict[str, float]) -> None:
        """Allocate carbon to resource pools from the plant carbon pool.
        
        Carbon is allocated to resource pools based on their priority and demand.
        Resource pools with higher priority (lower numerical value) receive carbon first.
        
        Args:
            environmental_variables: Dictionary of environmental variables
        """
        # Update initiation status of resource pools
        for rp in self.__resource_pools:
            rp.update_initiation_status(self.__thermal_age)

        # Get only initiated resource pools
        initiated_rps = [rp for rp in self.__resource_pools if rp.is_initiated]

        # Compute resource pool demand
        demands = {}
        total_demand = 0.0

        for rp in initiated_rps:
            demand = rp.compute_demand(self.__thermal_age, self.__thermal_age_increment)
            demands[rp] = demand
            total_demand += demand

        # Sort resource pools by allocation priority
        sorted_rps = sorted(initiated_rps, key=lambda x: x.allocation_priority)

        # Allocate carbon to each resource pool in priority order
        for rp in sorted_rps:
            allocation = min(demands[rp], self.__carbon_pool)
            rp.receive_carbon(allocation)
            self.__carbon_pool -= allocation

    def update_leaf_area_index(self) -> None:
        """Update leaf area index based on first resource pool (assumed to be leaves).
        
        Leaf area index is calculated as the product of specific leaf area and
        the size of the first resource pool (assumed to represent leaves).
        """
        self.__Leaf_Area_Index = self.__parameters['Specific_leaf_area'] * self.__resource_pools[0].current_size

    def simulate_plant(self, environmental_variables: Dict[str, float]) -> None:
        """Execute one model simulation step for the plant.
        
        This method coordinates the sequence of plant processes that occur in
        each simulation timestep.
        
        Args:
            environmental_variables: Dictionary of environmental variables
        """
        self.update_thermal_age(environmental_variables)
        self.carry_out_photosynthesis(environmental_variables)
        self.compute_carbon_assimilated(environmental_variables)
        self.allocate_carbon(environmental_variables)
        self.update_leaf_area_index()

    # Getter methods
    def get_parameters(self) -> Dict[str, Any]:
        """Get plant parameters dictionary."""
        return self.__parameters

    def get_assimilation_sunlit(self) -> float:
        """Get sunlit assimilation rate in µmol CO₂ m⁻² s⁻¹."""
        return self.__assimilation_sunlit

    def get_assimilation_shaded(self) -> float:
        """Get shaded assimilation rate in µmol CO₂ m⁻² s⁻¹."""
        return self.__assimilation_shaded

    def get_carbon_pool(self) -> float:
        """Get carbon pool size in g C."""
        return self.__carbon_pool

    def get_resource_pools(self) -> List[ResourcePool]:
        """Get list of resource pools."""
        return self.__resource_pools

    def get_leaf_area_index(self) -> float:
        """Get leaf area index in m² leaf / m² ground."""
        return self.__Leaf_Area_Index

    def get_thermal_age_increment(self) -> float:
        """Get thermal age increment in degree days."""
        return self.__thermal_age_increment

    def get_thermal_age(self) -> float:
        """Get thermal age in degree days."""
        return self.__thermal_age