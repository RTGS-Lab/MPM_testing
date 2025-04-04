"""Environment module for the Minimum Plant Model.

This package contains classes related to environmental factors that affect plant growth,
including atmospheric conditions and the interface between plants and their environment.

Classes:
    Environment: Base class for environment types
    AbovegroundEnvironment: Class for handling above-ground plant-environment interactions
    Atmosphere: Class for calculating atmospheric properties based on location and time
"""

from .base_environment import Environment
from .aboveground_environment import AbovegroundEnvironment
from .atmosphere import Atmosphere

__all__ = ['Environment', 'AbovegroundEnvironment', 'Atmosphere']