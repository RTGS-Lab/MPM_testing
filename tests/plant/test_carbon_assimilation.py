import unittest
import numpy as np
from minimum_plant_model.plant.carbon_assimilation import CarbonAssimilation

class TestCarbonAssimilation(unittest.TestCase):
    """Test cases for the CarbonAssimilation class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create minimal parameters for testing
        self.params = {
            'ER_ref': 0.5,  # baseline ecosystem respiration
            'Q10': 2.0,  # Q10 temperature coefficient
            'T_ref': 20.0,  # reference temperature (°C)
            'light_use_efficiency': 0.5  # generic LUE parameter
        }
        
        self.ca = CarbonAssimilation(self.params)
    
    def test_initialization(self):
        """Test that CarbonAssimilation initializes correctly."""
        # Check that params were stored
        self.assertEqual(self.ca.ER_ref, self.params['ER_ref'])
        self.assertEqual(self.ca.Q10, self.params['Q10'])
        self.assertEqual(self.ca.T_ref, self.params['T_ref'])
        self.assertEqual(self.ca.light_use_efficiency, self.params['light_use_efficiency'])
    
    def test_calculate_ecosystem_respiration(self):
        """Test ecosystem respiration calculation."""
        # At reference temperature, ER should equal ER_ref
        er_at_ref = self.ca.calculate_ecosystem_respiration(self.params['T_ref'])
        self.assertAlmostEqual(er_at_ref, self.params['ER_ref'])
        
        # At T_ref + 10°C, ER should be ER_ref * Q10
        er_at_ref_plus_10 = self.ca.calculate_ecosystem_respiration(self.params['T_ref'] + 10.0)
        self.assertAlmostEqual(er_at_ref_plus_10, self.params['ER_ref'] * self.params['Q10'])
    
    def test_calculate_gpp(self):
        """Test gross primary production calculation."""
        absorbed_radiation = 10.0  # MJ/m²/day
        
        # GPP should be absorbed_radiation * light_use_efficiency
        expected_gpp = absorbed_radiation * self.params['light_use_efficiency']
        actual_gpp = self.ca.calculate_gpp(absorbed_radiation)
        
        self.assertAlmostEqual(actual_gpp, expected_gpp)
    
    def test_calculate_npp(self):
        """Test net primary production calculation."""
        temperature = 25.0  # °C
        absorbed_radiation = 10.0  # MJ/m²/day
        
        # Calculate expected values
        expected_gpp = absorbed_radiation * self.params['light_use_efficiency']
        expected_er = self.params['ER_ref'] * (self.params['Q10'] ** ((temperature - self.params['T_ref']) / 10.0))
        expected_npp = expected_gpp - expected_er
        
        # Get actual NPP
        actual_npp = self.ca.calculate_npp(absorbed_radiation, temperature)
        
        self.assertAlmostEqual(actual_npp, expected_npp)
        
        # Test with conditions that would lead to negative NPP
        low_radiation = 0.1  # MJ/m²/day (very low)
        negative_npp = self.ca.calculate_npp(low_radiation, temperature)
        self.assertGreaterEqual(negative_npp, 0.0, "NPP should not be negative")


if __name__ == '__main__':
    unittest.main()
