"""Unit tests for ResourcePool class."""

import unittest
import math
from minimum_plant_model.resource_pool import ResourcePool

class TestResourcePool(unittest.TestCase):
    """Test cases for the ResourcePool class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.rp = ResourcePool(
            name="test_pool",
            thermal_time_initiation=10,
            allocation_priority=1,
            max_size=100,
            initial_size=1,
            growth_rate=0.01
        )
    
    def test_initialization(self):
        """Test that the resource pool initializes correctly."""
        self.assertEqual(self.rp.name, "test_pool")
        self.assertEqual(self.rp.thermal_time_initiation, 10)
        self.assertEqual(self.rp.allocation_priority, 1)
        self.assertEqual(self.rp.max_size, 100)
        self.assertEqual(self.rp.initial_size, 1)
        self.assertEqual(self.rp.current_size, 1)
        self.assertEqual(self.rp.growth_rate, 0.01)
        self.assertFalse(self.rp.is_initiated)
    
    def test_update_initiation_status(self):
        """Test the update_initiation_status method."""
        # Before thermal time initiation
        self.rp.update_initiation_status(5)
        self.assertFalse(self.rp.is_initiated)
        
        # At thermal time initiation
        self.rp.update_initiation_status(10)
        self.assertTrue(self.rp.is_initiated)
        
        # After thermal time initiation
        self.rp.update_initiation_status(15)
        self.assertTrue(self.rp.is_initiated)
    
    def test_compute_relative_growth_rate(self):
        """Test the compute_relative_growth_rate method."""
        # Test with thermal age 0
        rgr = self.rp.compute_relative_growth_rate(0, 100, 1, 0.01)
        self.assertEqual(rgr, 0.01)  # At beginning, RGR equals growth rate
        
        # Test with some thermal age
        rgr = self.rp.compute_relative_growth_rate(50, 100, 1, 0.01)
        self.assertLess(rgr, 0.01)  # RGR should decrease as pool grows
        
        # Test with large thermal age (approaching max size)
        rgr = self.rp.compute_relative_growth_rate(500, 100, 1, 0.01)
        self.assertLess(rgr, 0.001)  # RGR should be very small as pool approaches max size
    
    def test_compute_demand(self):
        """Test the compute_demand method."""
        # Test before initiation (thermal age will be set to 0)
        demand = self.rp.compute_demand(5, 0.1)
        self.assertEqual(self.rp.RP_thermal_age, 0)
        self.assertEqual(demand, 0.001)  # 0.01 (growth rate) * 1 (size) * 0.1 (increment)
        
        # Test after initiation
        demand = self.rp.compute_demand(20, 0.1)
        self.assertEqual(self.rp.RP_thermal_age, 10)  # 20 - 10 (initiation time)
        # Demand at this stage should be less than initial demand as RGR decreases
        self.assertLess(demand, 0.001)
    
    def test_receive_carbon(self):
        """Test the receive_carbon method."""
        initial_size = self.rp.current_size
        self.rp.receive_carbon(0.5)
        self.assertEqual(self.rp.current_size, initial_size + 0.5)
        
        self.rp.receive_carbon(1.5)
        self.assertEqual(self.rp.current_size, initial_size + 2.0)

if __name__ == '__main__':
    unittest.main()