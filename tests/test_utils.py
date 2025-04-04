import unittest
import os
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock
from minimum_plant_model.utils import read_csv_file, parse_date_column, create_output_directory

class TestUtils(unittest.TestCase):
    """Test cases for the utilities module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_csv_content = """col1,col2,date
1,2,2020-01-01
3,4,2020-01-02
5,6,2020-01-03"""
    
    @patch('minimum_plant_model.utils.pd.read_csv')
    @patch('minimum_plant_model.utils.os.path.exists')
    def test_read_csv_file(self, mock_exists, mock_read_csv):
        """Test reading a CSV file."""
        # Mock file existence
        mock_exists.return_value = True
        
        # Mock DataFrame returned from read_csv
        mock_df = pd.DataFrame({'col1': [1, 3, 5], 'col2': [2, 4, 6]})
        mock_read_csv.return_value = mock_df
        
        # Call the function
        result = read_csv_file('/path/to/file.csv')
        
        # Check the result
        pd.testing.assert_frame_equal(result, mock_df)
        mock_read_csv.assert_called_once_with('/path/to/file.csv')
        
        # Test handling of non-existent file
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            read_csv_file('/path/to/nonexistent.csv')
    
    def test_parse_date_column(self):
        """Test parsing dates in a DataFrame."""
        # Create a test DataFrame
        df = pd.DataFrame({
            'col1': [1, 3, 5],
            'col2': [2, 4, 6],
            'date': ['2020-01-01', '2020-01-02', '2020-01-03']
        })
        
        # Parse the date column
        result = parse_date_column(df, 'date')
        
        # Check that the date column was parsed correctly
        self.assertTrue(pd.api.types.is_datetime64_dtype(result['date']))
        
        # Check with a non-existent column name
        with self.assertRaises(KeyError):
            parse_date_column(df, 'nonexistent_column')
        
        # Check with invalid date format
        invalid_df = pd.DataFrame({
            'date': ['not-a-date', '2020-01-02', '2020-01-03']
        })
        with self.assertRaises(ValueError):
            parse_date_column(invalid_df, 'date')
    
    @patch('minimum_plant_model.utils.os.makedirs')
    def test_create_output_directory(self, mock_makedirs):
        """Test creating an output directory."""
        # Call the function
        dir_path = '/path/to/output'
        create_output_directory(dir_path)
        
        # Check that makedirs was called with the right parameters
        mock_makedirs.assert_called_once_with(dir_path, exist_ok=True)


if __name__ == '__main__':
    unittest.main()
