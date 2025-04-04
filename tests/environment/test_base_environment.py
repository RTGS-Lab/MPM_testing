import unittest
import numpy as np
from minimum_plant_model.environment.base_environment import BaseEnvironment

class TestBaseEnvironment(unittest.TestCase):
    """Test cases for the BaseEnvironment class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.params = {
            'temperature_min': 10.0,
            'temperature_max': 30.0,
            'latitude': 45.0,  # degrees
            'day_length': 12.0,  # hours
        }
    
    def test_initialization(self):
        """Test that BaseEnvironment raises NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            BaseEnvironment()
    
    def test_interface_methods(self):
        """Test that interface methods are defined."""
        # Create a minimal subclass of BaseEnvironment
        class MinimalEnvironment(BaseEnvironment):
            def __init__(self):
                super().__init__
                self.temperature = 20.0
                self.day_length = 12.0
                self.absorbed_radiation = 10.0
                self.thermal_time = 100.0
                
            def calculate_absorbed_radiation(self, lai):
                return self.absorbed_radiation
                
        env = MinimalEnvironment()
        
        # Test absorbed radiation calculation
        self.assertEqual(env.calculate_absorbed_radiation(2.0), env.absorbed_radiation)
        
        # Test that the environment has the required attributes
        self.assertTrue(hasattr(env, 'temperature'))
        self.assertTrue(hasattr(env, 'day_length'))
        self.assertTrue(hasattr(env, 'absorbed_radiation'))
        self.assertTrue(hasattr(env, 'thermal_time'))


if __name__ == '__main__':
    unittest.main()
