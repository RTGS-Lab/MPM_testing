import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
from minimum_plant_model.visualization import plot_time_series, plot_growth_curve, save_plot

class TestVisualization(unittest.TestCase):
    """Test cases for the visualization module."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a test DataFrame with simulation results
        self.results = pd.DataFrame({
            'date': pd.date_range(start='2020-01-01', end='2020-01-10'),
            'temperature': np.random.uniform(15, 25, 10),
            'radiation': np.random.uniform(5, 15, 10),
            'canopy_mass': np.linspace(0.1, 1.0, 10),
            'roots_mass': np.linspace(0.1, 0.8, 10),
            'LAI': np.linspace(0.5, 5.0, 10),
            'NPP': np.linspace(0.1, 0.5, 10)
        })
    
    @patch('minimum_plant_model.visualization.plt.figure')
    def test_plot_time_series(self, mock_figure):
        """Test plotting a time series."""
        # Configure mock figure to return a mock Figure and Axes
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_fig.add_subplot.return_value = mock_ax
        mock_figure.return_value = mock_fig
        
        # Call the function
        result_fig, result_ax = plot_time_series(
            self.results, 
            'date', 
            'temperature', 
            title='Temperature over time', 
            xlabel='Date', 
            ylabel='Temperature (°C)'
        )
        
        # Check the results
        self.assertEqual(result_fig, mock_fig)
        self.assertEqual(result_ax, mock_ax)
        
        # Verify that plotting methods were called
        mock_ax.plot.assert_called_once()
        mock_ax.set_title.assert_called_once_with('Temperature over time')
        mock_ax.set_xlabel.assert_called_once_with('Date')
        mock_ax.set_ylabel.assert_called_once_with('Temperature (°C)')
    
    @patch('minimum_plant_model.visualization.plt.figure')
    def test_plot_growth_curve(self, mock_figure):
        """Test plotting a growth curve."""
        # Configure mock figure to return a mock Figure and Axes
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_fig.add_subplot.return_value = mock_ax
        mock_figure.return_value = mock_fig
        
        # Call the function
        result_fig, result_ax = plot_growth_curve(
            self.results, 
            'LAI', 
            'canopy_mass', 
            title='Canopy mass vs LAI', 
            xlabel='LAI', 
            ylabel='Canopy mass (kg)'
        )
        
        # Check the results
        self.assertEqual(result_fig, mock_fig)
        self.assertEqual(result_ax, mock_ax)
        
        # Verify that plotting methods were called
        mock_ax.scatter.assert_called_once()
        mock_ax.set_title.assert_called_once_with('Canopy mass vs LAI')
        mock_ax.set_xlabel.assert_called_once_with('LAI')
        mock_ax.set_ylabel.assert_called_once_with('Canopy mass (kg)')
    
    @patch('minimum_plant_model.visualization.plt.savefig')
    @patch('minimum_plant_model.visualization.os.makedirs')
    def test_save_plot(self, mock_makedirs, mock_savefig):
        """Test saving a plot to a file."""
        # Create a mock figure
        mock_fig = MagicMock()
        
        # Call the function
        output_dir = '/path/to/output'
        filename = 'test_plot.png'
        save_plot(mock_fig, output_dir, filename)
        
        # Verify that directories were created
        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
        
        # Verify that savefig was called
        expected_path = '/path/to/output/test_plot.png'
        mock_savefig.assert_called_once_with(expected_path, dpi=300, bbox_inches='tight')


if __name__ == '__main__':
    unittest.main()
