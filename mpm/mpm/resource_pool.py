"""Resource pool module that handles plant component growth."""

import math

class ResourcePool:
    """The ResourcePool class is responsible for growing (and later senescing) generic resource pools (RPs).
    
    RPs represent generic plant components at any scale, e.g., canopy or leaves or leaf cohorts;
    rhizome or stems; total roots or individual root orders; etc. The minimum number of RPs for
    the model to run is simply one. In the current model structure, the first RP is assumed to
    represent total leaves (due to LAI being calculated from this RP).
    """
    def __init__(self, name, thermal_time_initiation, allocation_priority, max_size, initial_size, growth_rate):
        self.name = name
        self.is_initiated = False
        self.thermal_time_initiation = thermal_time_initiation
        self.allocation_priority = allocation_priority
        self.max_size = max_size
        self.growth_rate = growth_rate
        self.initial_size = initial_size
        self.current_size = initial_size
        self.RP_thermal_age = 0.0
        self.demand = 0.0

        # for testing
        self.rgr = 0.0 ###### tracking this for testing. --> remove later

    def update_initiation_status(self, plant_thermal_age):
        """Update whether resource pool has reached initiation thermal time.
        
        Args:
            plant_thermal_age (float): Current thermal age of the plant
        """
        if plant_thermal_age >= self.thermal_time_initiation:
            self.is_initiated = True

    def compute_relative_growth_rate(self, RP_thermal_age, max_size, initial_size, growth_rate):
        """Calculate relative growth rate for resource pool based on its thermal age.
        
        RGR is computed as the logarithmic derivative of the three-parameter logistic growth curve.
        Ref: RGR function from Wang et al., 2019 (Journal of Experimental Botany)
        
        Args:
            RP_thermal_age (float): Thermal age of the RP
            max_size (float): Maximum size RP
            initial_size (float): Initial size at RP initiation
            growth_rate (float): Growth rate (r) of the RP
            
        Returns:
            float: Relative growth rate
        """
        A = (max_size - initial_size) / initial_size
        exp_component = math.exp(-growth_rate * RP_thermal_age)
        f_prime = (max_size * A * growth_rate * exp_component) / (1 + A * exp_component) ** 2
        f = max_size / (1 + A * exp_component)
        relative_growth_rate = f_prime / f
        return relative_growth_rate

    def compute_demand(self, plant_thermal_time, thermal_time_increment):
        """Compute demand by the resource pool based on potential growth.
        
        Args:
            plant_thermal_time (float): Current thermal age of the plant
            thermal_time_increment (float): Thermal time increment for this timestep
            
        Returns:
            float: Demand value
        """
        self.RP_thermal_age = plant_thermal_time - self.thermal_time_initiation
        if self.RP_thermal_age < 0:
            self.RP_thermal_age = 0
        relative_growth_rate = self.compute_relative_growth_rate(self.RP_thermal_age, self.max_size, self.initial_size, self.growth_rate)
        self.rgr = relative_growth_rate ###### tracking this for testing. --> remove later
        demand = relative_growth_rate * self.current_size * thermal_time_increment
        self.demand = demand
        return demand

    def receive_carbon(self, allocated_carbon):
        """Increment the resource pool based on allocation from the plant.
        
        Args:
            allocated_carbon (float): Amount of carbon allocated to this pool
        """
        self.current_size += allocated_carbon
