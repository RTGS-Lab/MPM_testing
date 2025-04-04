"""Minimum Plant Model (MPM) - A modular framework for simulating plant growth."""

__version__ = '0.1.0'

from mpm.model_handler import ModelHandler
from mpm.plant import Plant
from mpm.atmosphere import Atmosphere
from mpm.environment import Environment, AbovegroundEnvironment
from mpm.carbon_assimilation import CarbonAssimilation
from mpm.resource_pool import ResourcePool
