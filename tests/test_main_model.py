import unittest
import os
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
from minimum_plant_model.main_model import MainModel

class TestMainModel(unittest.TestCase):
    """Test cases for the MainModel class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a minimal configuration for testing
        self.config = {
            'input_dir': './model input files',
            'output_dir': './outputs',
            'params_file': 'parameters.csv',
            'drivers_file': 'drivers_setpoints.csv',
            'resource_pools_file': 'resource_pools_single.csv',
            'start_date': '2020-01-01',
            'end_date': '2020-01-10',
            'visualization': True
        }
        
        # Create the model instance with mocked file reading
        with patch('minimum_plant_model.main_model.pd.read_csv', return_value=pd.DataFrame()):
            with patch('minimum_plant_model.main_model.os.path.exists', return_value=True):
                self.model = MainModel(self.config)
                
                # Mock the internal plant and environment objects
                self.model.plant = MagicMock()
                self.model.environment = MagicMock()
                
                # Mock the results data
                self.model.results = pd.DataFrame({
                    'date': pd.date_range(start='2020-01-01', end='2020-01-10'),
                    'temperature': np.random.uniform(15, 25, 10),
                    'radiation': np.random.uniform(5, 15, 10),
                    'canopy_mass': np.linspace(0.1, 1.0, 10),
                    'roots_mass': np.linspace(0.1, 0.8, 10),
                    'LAI': np.linspace(0.5, 5.0, 10),
                    'NPP': np.linspace(0.1, 0.5, 10)
                })
    
    def test_initialization(self):
        """Test that MainModel initializes correctly."""
        # Check that configuration was stored
        self.assertEqual(self.model.input_dir, self.config['input_dir'])
        self.assertEqual(self.model.output_dir, self.config['output_dir'])
        self.assertEqual(self.model.params_file, self.config['params_file'])
        self.assertEqual(self.model.drivers_file, self.config['drivers_file'])
        self.assertEqual(self.model.resource_pools_file, self.config['resource_pools_file'])
        
        # Check that start and end dates were parsed correctly
        self.assertEqual(self.model.start_date.strftime('%Y-%m-%d'), self.config['start_date'])
        self.assertEqual(self.model.end_date.strftime('%Y-%m-%d'), self.config['end_date'])
    
    @patch('minimum_plant_model.main_model.pd.read_csv')
    @patch('minimum_plant_model.main_model.os.path.exists')
    def test_read_input_files(self, mock_exists, mock_read_csv):
        """Test reading input files."""
        # Mock the file existence check
        mock_exists.return_value = True
        
        # Mock the read_csv function to return test DataFrames
        mock_params_df = pd.DataFrame({'parameter': ['leaf_mass_per_area'], 'value': [0.02]})
        mock_drivers_df = pd.DataFrame({'date': pd.date_range(start='2020-01-01', end='2020-01-10')})
        mock_rp_df = pd.DataFrame({'pool': ['canopy'], 'initial_mass': [0.1]})
        
        mock_read_csv.side_effect = [mock_params_df, mock_drivers_df, mock_rp_df]
        
        # Create a new model instance and call read_input_files explicitly
        model = MainModel(self.config)
        model.read_input_files()
        
        # Verify that read_csv was called with the correct file paths
        expected_paths = [
            os.path.join(self.config['input_dir'], self.config['params_file']),
            os.path.join(self.config['input_dir'], self.config['drivers_file']),
            os.path.join(self.config['input_dir'], self.config['resource_pools_file'])
        ]
        
        actual_paths = [call_args[0][0] for call_args in mock_read_csv.call_args_list]
        self.assertEqual(actual_paths, expected_paths)
    
    def test_run_simulation(self):
        """Test the simulation run process."""
        # Configure mocks
        self.model.drivers = pd.DataFrame({
            'date': pd.date_range(start='2020-01-01', end='2020-01-10'),
            'temperature': np.random.uniform(15, 25, 10),
            'radiation': np.random.uniform(5, 15, 10)
        })
        
        # Run the simulation
        self.model.run_simulation()
        
        # Verify that update methods were called on environment and plant
        expected_calls = len(self.model.drivers)
        self.assertEqual(self.model.environment.update.call_count, expected_calls)
        self.assertEqual(self.model.plant.update.call_count, expected_calls)
        
        # Verify that results DataFrame was created with the correct length
        self.assertEqual(len(self.model.results), expected_calls)
    
    @patch('minimum_plant_model.main_model.plt.figure')
    @patch('minimum_plant_model.main_model.plt.savefig')
    @patch('minimum_plant_model.main_model.os.makedirs')
    def test_plot_outputs(self, mock_makedirs, mock_savefig, mock_figure):
        """Test the plotting functionality."""
        # Configure mock figure to return a mock Figure and Axes
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_fig.add_subplot.return_value = mock_ax
        mock_figure.return_value = mock_fig
        
        # Call the plotting method
        self.model.plot_outputs()
        
        # Verify that plots were created and saved
        self.assertGreater(mock_figure.call_count, 0)
        self.assertGreater(mock_savefig.call_count, 0)
        self.assertGreaterEqual(mock_makedirs.call_count, 1)
    
    @patch('minimum_plant_model.main_model.pd.DataFrame.to_csv')
    @patch('minimum_plant_model.main_model.os.makedirs')
    def test_save_results(self, mock_makedirs, mock_to_csv):
        """Test saving simulation results to CSV."""
        # Call the save_results method
        self.model.save_results()
        
        # Verify that the output directory was created
        mock_makedirs.assert_called_once_with(self.model.output_dir, exist_ok=True)
        
        # Verify that to_csv was called
        self.assertEqual(mock_to_csv.call_count, 1)


if __name__ == '__main__':
    unittest.main()
