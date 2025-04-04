"""Utility functions for the Minimum Plant Model."""

import os
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional, Union

def read_csv_file(file_path: str) -> pd.DataFrame:
    """Read a CSV file into a pandas DataFrame.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame containing the CSV contents
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return pd.read_csv(file_path)

def read_parameters_file(file_path: str) -> Dict[str, str]:
    """Read a parameters file into a dictionary.
    
    Parameters file is expected to have a 2-column format with parameter names
    in the first column and values in the second column (no header).
    
    Args:
        file_path: Path to the parameters CSV file
        
    Returns:
        Dictionary mapping parameter names to values (as strings)
    """
    params = pd.read_csv(file_path, header=None, usecols=[0, 1])
    return params.set_index(0).to_dict()[1]

def read_resource_pools_file(file_path: str) -> List[Dict[str, Any]]:
    """Read a resource pools file into a list of dictionaries.
    
    Args:
        file_path: Path to the resource pools CSV file
        
    Returns:
        List of dictionaries, each representing a resource pool configuration
    """
    resource_pools = pd.read_csv(file_path)
    return resource_pools.to_dict(orient='records')

def convert_parameter_types(params_dict: Dict[str, str]) -> Dict[str, Union[float, int, str]]:
    """Convert parameter values to appropriate types.
    
    Args:
        params_dict: Dictionary of parameter values as strings
        
    Returns:
        Dictionary with parameter values converted to appropriate types
    """
    converted_params = {}
    
    for key, value in params_dict.items():
        # Try to convert to numeric types
        try:
            # Check if it's an integer
            if float(value).is_integer():
                converted_params[key] = int(float(value))
            else:
                converted_params[key] = float(value)
        except (ValueError, TypeError):
            # If conversion fails, keep as string
            converted_params[key] = value
    
    return converted_params