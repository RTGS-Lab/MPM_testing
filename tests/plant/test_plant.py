import unittest
import numpy as np
from minimum_plant_model.plant.plant import Plant
from minimum_plant_model.plant.resource_pool import ResourcePool
from minimum_plant_model.environment.base_environment import BaseEnvironment

class TestPlant(unittest.TestCase):
    """Test cases for the Plant class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create minimal resource pools configuration for testing
        self.resource_pools_config = {
            'canopy': {'initial_mass': 0.1, 'max_mass': 10.0, 'growth_rate': 0.1},
            'roots': {'initial_mass': 0.1, 'max_mass': 5.0, 'growth_rate': 0.08}
        }
        
        # Create minimal parameters for testing
        self.params = {
            'leaf_mass_per_area': 0.02,  # kg/m²
            'ER_ref': 0.5,  # baseline ecosystem respiration
            'Q10': 2.0,  # Q10 temperature coefficient
            'T_ref': 20.0,  # reference temperature (°C)
            'light_use_efficiency': 0.5  # generic LUE parameter
        }
        
    def test_initialization(self):
        """Test that Plant initializes correctly."""
        plant = Plant(self.resource_pools_config, self.params)
        
        # Check that resource pools were created
        self.assertIsInstance(plant.resource_pools['canopy'], ResourcePool)
        self.assertIsInstance(plant.resource_pools['roots'], ResourcePool)
        
        # Check that params were stored
        self.assertEqual(plant.leaf_mass_per_area, self.params['leaf_mass_per_area'])
        
    def test_calculate_lai(self):
        """Test LAI calculation."""
        plant = Plant(self.resource_pools_config, self.params)
        
        # Set canopy mass to a known value
        plant.resource_pools['canopy'].current_mass = 1.0  # kg
        
        # Calculate expected LAI: mass (kg) / leaf_mass_per_area (kg/m²) = area (m²)
        expected_lai = 1.0 / self.params['leaf_mass_per_area']
        
        # Get actual LAI
        lai = plant.calculate_lai()
        
        self.assertAlmostEqual(lai, expected_lai)
    
    def test_update(self):
        """Test the update method with a mock environment."""
        plant = Plant(self.resource_pools_config, self.params)
        
        # Create a simple mock environment
        class MockEnvironment(BaseEnvironment):
            def __init__(self):
                self.temperature = 25.0
                self.absorbed_radiation = 10.0  # MJ/m²/day
                self.day_length = 12.0  # hours
                self.thermal_time = 10.0  # degree-days
                
            def calculate_absorbed_radiation(self, lai):
                return self.absorbed_radiation
                
        env = MockEnvironment()
        
        # Initial masses
        initial_canopy_mass = plant.resource_pools['canopy'].current_mass
        initial_roots_mass = plant.resource_pools['roots'].current_mass
        
        # Update plant for one day
        plant.update(env)
        
        # Check that masses have increased
        self.assertGreater(plant.resource_pools['canopy'].current_mass, initial_canopy_mass)
        self.assertGreater(plant.resource_pools['roots'].current_mass, initial_roots_mass)


if __name__ == '__main__':
    unittest.main()
