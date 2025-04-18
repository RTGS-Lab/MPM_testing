"""Plant module for the Minimum Plant Model.

This package contains classes related to plant growth, development, and physiological
processes including carbon assimilation and resource allocation.

Classes:
    Plant: Class representing the whole plant and coordinating growth processes
    ResourcePool: Class representing different plant components (e.g., leaves, roots)
    CarbonAssimilation: Class implementing photosynthesis calculations
    PriorityQueue: Class for resource allocation to plant components
"""

from .plant import Plant
from .resource_pool import ResourcePool
from .carbon_assimilation import CarbonAssimilation
from .priority_queue import PriorityQueue

__all__ = ['Plant', 'ResourcePool', 'CarbonAssimilation', 'PriorityQueue']