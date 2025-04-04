"""Unit tests for ModelHandler class."""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
import numpy as np
import pandas as pd

from minimum_plant_model.model_handler import ModelHandler
from minimum_plant_model.plant import Plant

class TestModelHandler(unittest.TestCase):
    """Test cases for the ModelHandler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary CSV files for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create drivers file
        self.drivers_file = os.path.join(self.temp_dir.name, 'drivers.csv')
        drivers_data = {
            'DOY': [1, 1, 1],
            'Hour': [1, 2, 3],
            'temperature': [20, 21, 22],
            'radiation': [500, 600, 700],
            'precipitation': [0, 0, 0],
            'wind_speed': [2, 2, 2],
            'VPD': [1, 1, 1]
        }
        pd.DataFrame(drivers_data).to_csv(self.drivers_file, index=False)
        
        # Create parameters file
        self.params_file = os.path.join(self.temp_dir.name, 'parameters.csv')
        params_data = [
            ['Ambient_CO2', 400],
            ['Fraction_AboveGround_Carbon', 0.65],
            ['Specific_leaf_area', 0.03],
            ['Leaf_Blade_Angle', 45],
            ['Activation_Energy_JMAX', 48041.88],
            ['VCMAX', 85],
            ['JMAX', 170],
            ['Photosynthetic_Light_Response_Factor', 0.7],
            ['Base_temperature', 12],
            ['Single_plant_ground_area', 0.16],
            ['latitude', 40]
        ]
        pd.DataFrame(params_data).to_csv(self.params_file, header=False, index=False)
        
        # Create resource pools file
        self.rp_file = os.path.join(self.temp_dir.name, 'resource_pools.csv')
        rp_data = {
            'name': ['canopy', 'root'],
            'thermal_time_initiation': [0, 10],
            'growth_allocation_priority': [2, 1],
            'max_size': [27, 15],
            'initial_size': [0.01, 0.01],
            'rate': [0.004, 0.004]
        }
        pd.DataFrame(rp_data).to_csv(self.rp_file, index=False)
        
        # Create model handler instance
        self.model = ModelHandler(self.drivers_file, self.params_file, self.rp_file)
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
    
    def test_initialization(self):
        """Test that the model handler initializes correctly."""
        self.assertEqual(self.model.drivers_filename, self.drivers_file)
        self.assertEqual(self.model.parameter_filename, self.params_file)
        self.assertEqual(self.model.resource_pool_filename, self.rp_file)
        self.assertIsNone(self.model.latitude)
    
    def test_read_input_files(self):
        """Test reading input files."""
        drivers, params_dict, resource_pools = self.model.read_input_files()
        
        # Check drivers
        self.assertEqual(len(drivers), 3)  # 3 rows
        self.assertEqual(list(drivers.columns), ['DOY', 'Hour', 'temperature', 'radiation', 
                                               'precipitation', 'wind_speed', 'VPD'])
        
        # Check parameters
        self.assertEqual(params_dict['VCMAX'], '85')
        self.assertEqual(params_dict['JMAX'], '170')
        self.assertEqual(params_dict['Leaf_Blade_Angle'], '45')
        self.assertEqual(params_dict['latitude'], '40')
        
        # Check latitude was set
        self.assertEqual(self.model.latitude, 40.0)
        
        # Check resource pools
        self.assertEqual(len(resource_pools), 2)
        self.assertEqual(resource_pools[0]['name'], 'canopy')
        self.assertEqual(resource_pools[1]['name'], 'root')
    
    @patch('matplotlib.pyplot.show')
    def test_initialize_logs(self, mock_show):
        """Test initializing logs."""
        # Create mock plant with mock resource pools
        mock_pool1 = MagicMock()
        mock_pool1.name = 'canopy'
        mock_pool2 = MagicMock()
        mock_pool2.name = 'root'
        mock_plant = MagicMock()
        mock_plant.get_resource_pools.return_value = [mock_pool1, mock_pool2]
        
        self.model.initialize_logs(mock_plant)
        
        # Check all log lists were initialized
        self.assertEqual(self.model.log_thermal_age, [])
        self.assertEqual(self.model.log_assimilation, [])
        self.assertEqual(self.model.log_lai, [])
        self.assertEqual(self.model.log_rp, [])
        self.assertEqual(self.model.log_rp_demand, [])
        self.assertEqual(self.model.log_rp_rgr, [])
        self.assertEqual(self.model.log_carbon_pool, [])
        
        # Check resource pool logs were initialized
        self.assertEqual(list(self.model.log_resource_pool_sizes.keys()), ['canopy', 'root'])
        self.assertEqual(self.model.log_resource_pool_sizes['canopy'], [])
        self.assertEqual(self.model.log_resource_pool_sizes['root'], [])
    
    @patch('matplotlib.pyplot.show')
    def test_update_logs(self, mock_show):
        """Test updating logs."""
        # Create mock plant with mock resource pools
        mock_pool1 = MagicMock()
        mock_pool1.name = 'canopy'
        mock_pool1.current_size = 0.5
        mock_pool1.demand = 0.1
        mock_pool1.rgr = 0.05
        
        mock_pool2 = MagicMock()
        mock_pool2.name = 'root'
        mock_pool2.current_size = 0.3
        
        mock_plant = MagicMock()
        mock_plant.get_resource_pools.return_value = [mock_pool1, mock_pool2]
        mock_plant.get_assimilation_sunlit.return_value = 10.0
        mock_plant.get_thermal_age.return_value = 5.0
        mock_plant.get_leaf_area_index.return_value = 0.015
        mock_plant.get_carbon_pool.return_value = 0.2
        
        # Initialize logs
        self.model.log_thermal_age = []
        self.model.log_assimilation = []
        self.model.log_lai = []
        self.model.log_rp = []
        self.model.log_rp_demand = []
        self.model.log_rp_rgr = []
        self.model.log_carbon_pool = []
        self.model.log_resource_pool_sizes = {'canopy': [], 'root': []}
        
        # Update logs
        self.model.update_logs(mock_plant)
        
        # Check all logs were updated
        self.assertEqual(self.model.log_thermal_age, [5.0])
        self.assertEqual(self.model.log_assimilation, [10.0])
        self.assertEqual(self.model.log_lai, [0.015])
        self.assertEqual(self.model.log_rp, [0.5])
        self.assertEqual(self.model.log_rp_demand, [0.1])
        self.assertEqual(self.model.log_rp_rgr, [0.05])
        self.assertEqual(self.model.log_carbon_pool, [0.2])
        self.assertEqual(self.model.log_resource_pool_sizes['canopy'], [0.5])
        self.assertEqual(self.model.log_resource_pool_sizes['root'], [0.3])

if __name__ == '__main__':
    unittest.main()