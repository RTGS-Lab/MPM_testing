"""Plant module that handles plant growth and resource allocation."""

from mpm.carbon_assimilation import CarbonAssimilation
from mpm.resource_pool import ResourcePool

class Plant:
    """This class represents the whole plant."""
    
    def __init__(self, params_dict, resource_pool_params):
        self.resource_pool_params = resource_pool_params
        self.__thermal_age = 0.0
        self.__assimilation_sunlit = 0.0
        self.__assimilation_shaded = 0.0
        self.__Leaf_Area_Index = 0.005
        self.__carbon_pool = 0.03
        self.__parameters = params_dict
        self.__thermal_age_increment = 0.0
        self.latitude = 0
        self.carbon_assimilation = CarbonAssimilation(self.__parameters) # instantiate process objects to handle physiology
        self.__resource_pools = []

    def create_resource_pools(self):
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

    def update_thermal_age(self, environmental_variables):
        """Compute thermal age increment and update thermal age.
        
        Args:
            environmental_variables (dict): Environmental variables dictionary
        """
        thermal_age_increment = (environmental_variables['temperature'] - self.__parameters['Base_temperature'])/24 # thermal age increase hour basis
        if thermal_age_increment < 0:
            thermal_age_increment = 0
        # update thermal age and increment
        self.__thermal_age += thermal_age_increment
        self.__thermal_age_increment = thermal_age_increment

    def carry_out_photosynthesis(self, environmental_variables):
        """Carry out photosynthesis for sunlit and shaded components of the canopy.
        
        Args:
            environmental_variables (dict): Environmental variables dictionary
        """
        self.__assimilation_sunlit, self.__assimilation_shaded = self.carbon_assimilation.sunlit_shaded_photosynthesis(environmental_variables)

    def compute_carbon_assimilated(self, environmental_variables):
        """Calculate carbon assimilated and update carbon pool.
        
        Args:
            environmental_variables (dict): Environmental variables dictionary
        """
        Sunlit_Fraction = environmental_variables['Sunlit_fraction']
        Canopy_Photosynthesis_average = self.__assimilation_sunlit * Sunlit_Fraction + \
                                       self.__assimilation_shaded * (1 - Sunlit_Fraction) # In units µmol CO₂ m⁻² s⁻¹ leaf area basis

        # get total carbon for canopy
        Canopy_total_carbon_assimilated = Canopy_Photosynthesis_average * 3600 * self.__Leaf_Area_Index # In units µmol CO₂ m⁻² ground area for this timestep (hour)
        Canopy_total_carbon_assimilated *= (1E-6) * 12  # In units g carbon m⁻² ground area; (12 g carbon per mol CO₂ )
        Canopy_total_carbon_assimilated *= self.__parameters['Single_plant_ground_area'] # in units g C on a plant basis
        self.__carbon_pool += Canopy_total_carbon_assimilated

    def allocate_carbon(self, environmental_variables):
        """Allocate carbon to resource pools from the plant carbon pool.
        
        Args:
            environmental_variables (dict): Environmental variables dictionary
        """
        # Update initiation status of resource pools
        for rp in self.__resource_pools:
            rp.update_initiation_status(self.__thermal_age)

        initiated_rps = [rp for rp in self.__resource_pools if rp.is_initiated]

        # Compute resource pool demand
        demands = {}
        total_demand = 0.0

        for rp in initiated_rps:
            demand = rp.compute_demand(self.__thermal_age, self.__thermal_age_increment)
            demands[rp] = demand
            total_demand += demand

        sorted_rps = sorted(initiated_rps, key=lambda x: x.allocation_priority)

        for rp in sorted_rps:
            allocation = min(demands[rp], self.__carbon_pool)
            rp.receive_carbon(allocation)
            self.__carbon_pool -= allocation

    def update_leaf_area_index(self):
        """Update leaf area index based on first resource pool (assumed to be leaves)."""
        self.__Leaf_Area_Index = self.__parameters['Specific_leaf_area'] * self.__resource_pools[0].current_size

    def simulate_plant(self, environmental_variables):
        """Execute one model simulation step for the plant.
        
        Args:
            environmental_variables (dict): Environmental variables dictionary
        """
        self.update_thermal_age(environmental_variables)
        self.carry_out_photosynthesis(environmental_variables)
        self.compute_carbon_assimilated(environmental_variables)
        self.allocate_carbon(environmental_variables)
        self.update_leaf_area_index()

    # getter functions
    def get_parameters(self):
        """Get plant parameters dictionary."""
        return self.__parameters

    def get_assimilation_sunlit(self):
        """Get sunlit assimilation rate."""
        return self.__assimilation_sunlit

    def get_assimilation_shaded(self):
        """Get shaded assimilation rate."""
        return self.__assimilation_shaded

    def get_carbon_pool(self):
        """Get carbon pool size."""
        return self.__carbon_pool

    def get_resource_pools(self):
        """Get list of resource pools."""
        return self.__resource_pools

    def get_leaf_area_index(self):
        """Get leaf area index."""
        return self.__Leaf_Area_Index

    def get_thermal_age_increment(self):
        """Get thermal age increment."""
        return self.__thermal_age_increment

    def get_thermal_age(self):
        """Get thermal age."""
        return self.__thermal_age
