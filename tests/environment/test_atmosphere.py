import unittest
import numpy as np
from minimum_plant_model.environment.atmosphere import Atmosphere

class TestAtmosphere(unittest.TestCase):
    """Test cases for the Atmosphere class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.params = {
            'latitude': 45.0,  # degrees
            'elevation': 100.0,  # meters
        }
        
        self.atmosphere = Atmosphere(self.params)
    
    def test_initialization(self):
        """Test that Atmosphere initializes correctly."""
        # Check that parameters were stored
        self.assertEqual(self.atmosphere.latitude, self.params['latitude'])
        self.assertEqual(self.atmosphere.elevation, self.params['elevation'])
    
    def test_calculate_day_length(self):
        """Test day length calculation for different days of year."""
        # Test summer solstice in Northern Hemisphere (approx. day 172)
        summer_day_length = self.atmosphere.calculate_day_length(172)
        
        # Test winter solstice in Northern Hemisphere (approx. day 355)
        winter_day_length = self.atmosphere.calculate_day_length(355)
        
        # Summer day should be longer than winter day in Northern Hemisphere
        self.assertGreater(summer_day_length, winter_day_length)
        
        # Test that day length is between 0 and 24 hours
        self.assertGreaterEqual(summer_day_length, 0.0)
        self.assertLessEqual(summer_day_length, 24.0)
        self.assertGreaterEqual(winter_day_length, 0.0)
        self.assertLessEqual(winter_day_length, 24.0)
    
    def test_calculate_solar_radiation(self):
        """Test solar radiation calculation for different days and cloud cover."""
        # Test clear day in summer
        summer_clear = self.atmosphere.calculate_solar_radiation(172, 0.0)
        
        # Test cloudy day in summer
        summer_cloudy = self.atmosphere.calculate_solar_radiation(172, 0.8)
        
        # Test clear day in winter
        winter_clear = self.atmosphere.calculate_solar_radiation(355, 0.0)
        
        # Test cloudy day in winter
        winter_cloudy = self.atmosphere.calculate_solar_radiation(355, 0.8)
        
        # Clear day should have more radiation than cloudy day
        self.assertGreater(summer_clear, summer_cloudy)
        self.assertGreater(winter_clear, winter_cloudy)
        
        # Summer should have more radiation than winter in Northern Hemisphere
        self.assertGreater(summer_clear, winter_clear)
        self.assertGreater(summer_cloudy, winter_cloudy)
        
        # Radiation should be non-negative
        self.assertGreaterEqual(summer_clear, 0.0)
        self.assertGreaterEqual(summer_cloudy, 0.0)
        self.assertGreaterEqual(winter_clear, 0.0)
        self.assertGreaterEqual(winter_cloudy, 0.0)
    
    def test_calculate_temperature(self):
        """Test temperature calculation for different days."""
        # Test temperature on different days
        summer_temp = self.atmosphere.calculate_temperature(172)
        winter_temp = self.atmosphere.calculate_temperature(355)
        
        # Temperature fluctuation should follow expected seasonal pattern
        # Northern Hemisphere: summer (day 172) warmer than winter (day 355)
        self.assertGreater(summer_temp, winter_temp)


if __name__ == '__main__':
    unittest.main()
