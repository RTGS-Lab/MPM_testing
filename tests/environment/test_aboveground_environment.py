import unittest
import numpy as np
from minimum_plant_model.environment.aboveground_environment import AbovegroundEnvironment

class TestAbovegroundEnvironment(unittest.TestCase):
    """Test cases for the AbovegroundEnvironment class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.params = {
            'temperature_min': 10.0,
            'temperature_max': 30.0,
            'radiation_max': 20.0,  # MJ/m²/day
            'latitude': 45.0,  # degrees
            'day_length': 12.0,  # hours
        }
        
        self.env = AbovegroundEnvironment(self.params)
        
    def test_initialization(self):
        """Test that AbovegroundEnvironment initializes correctly."""
        # Check that parameters were stored
        self.assertEqual(self.env.temperature_min, self.params['temperature_min'])
        self.assertEqual(self.env.temperature_max, self.params['temperature_max'])
        self.assertEqual(self.env.radiation_max, self.params['radiation_max'])
        
        # Check initial values
        self.assertEqual(self.env.temperature, 0.0)
        self.assertEqual(self.env.day_length, 0.0)
        self.assertEqual(self.env.absorbed_radiation, 0.0)
        self.assertEqual(self.env.thermal_time, 0.0)
    
    def test_update(self):
        """Test environment update with drivers."""
        # Create test drivers
        drivers = {
            'temperature': 25.0,
            'radiation': 15.0,
            'day_length': 12.0,
        }
        
        # Update the environment
        self.env.update(drivers)
        
        # Check updated values
        self.assertEqual(self.env.temperature, drivers['temperature'])
        self.assertEqual(self.env.radiation, drivers['radiation'])
        self.assertEqual(self.env.day_length, drivers['day_length'])
        
        # Thermal time should be updated (assuming temperature is above base temperature)
        self.assertGreater(self.env.thermal_time, 0.0)
    
    def test_calculate_absorbed_radiation(self):
        """Test calculation of absorbed radiation based on LAI."""
        # Set radiation to a known value
        self.env.radiation = 10.0  # MJ/m²/day
        
        # Test with different LAI values
        lai_values = [0.0, 1.0, 3.0, 5.0, 10.0]
        
        for lai in lai_values:
            absorbed = self.env.calculate_absorbed_radiation(lai)
            
            # Absorbed radiation should be between 0 and the total radiation
            self.assertGreaterEqual(absorbed, 0.0)
            self.assertLessEqual(absorbed, self.env.radiation)
            
            # Higher LAI should absorb more radiation (until saturation)
            if lai > 0:
                lower_lai_absorbed = self.env.calculate_absorbed_radiation(lai - 0.1)
                self.assertGreaterEqual(absorbed, lower_lai_absorbed)
    
    def test_temperature_range(self):
        """Test that temperature stays within defined range."""
        # Test with temperature below minimum
        drivers_low = {'temperature': self.params['temperature_min'] - 5.0, 'radiation': 10.0, 'day_length': 12.0}
        self.env.update(drivers_low)
        self.assertEqual(self.env.temperature, self.params['temperature_min'])
        
        # Test with temperature above maximum
        drivers_high = {'temperature': self.params['temperature_max'] + 5.0, 'radiation': 10.0, 'day_length': 12.0}
        self.env.update(drivers_high)
        self.assertEqual(self.env.temperature, self.params['temperature_max'])
        
        # Test with temperature within range
        temp_within_range = (self.params['temperature_min'] + self.params['temperature_max']) / 2.0
        drivers_mid = {'temperature': temp_within_range, 'radiation': 10.0, 'day_length': 12.0}
        self.env.update(drivers_mid)
        self.assertEqual(self.env.temperature, temp_within_range)


if __name__ == '__main__':
    unittest.main()
