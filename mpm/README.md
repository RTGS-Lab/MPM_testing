# Minimum Plant Model (MPM)

## Project Description
The Minimum Plant Model (MPM) is a simulation framework for modeling plant growth and development under different environmental conditions. It simulates carbon assimilation, resource allocation, and growth of different plant components (resource pools) over time based on environmental drivers like temperature, radiation, and other climate variables.

## Features
- Simulates photosynthesis using a sunlit/shaded canopy model
- Models plant growth based on thermal time
- Resource allocation to different plant components (canopy, roots, storage)
- Modular design allowing flexible configuration of plant components
- Visualization of simulation results

## Installation

```bash
# Install from PyPI (coming soon)
# pip install mpm

# Install from source
git clone https://github.com/DRWang3/MPM_testing.git
cd MPM_testing/mpm
pip install -e .
```

## Quick Start

```python
from mpm import ModelHandler

# Set file paths for inputs
driver_file = "path/to/drivers_natural_all.csv"
parameter_file = "path/to/parameters.csv"
resource_pool_file = "path/to/resource_pools_3RPs.csv"

# Create model instance
model = ModelHandler(driver_file, parameter_file, resource_pool_file)

# Run simulation
model.run_simulation()

# Plot results
model.plot_outputs()
```

## Documentation
For more detailed documentation, please refer to the `docs/` directory or the project wiki.

## Model Components

### ModelHandler
Controls simulation workflow and file I/O.

### Plant
Central model component representing the whole plant, coordinating carbon assimilation and resource allocation.

### ResourcePool
Represents different plant components (e.g., canopy, roots, storage) with dynamic growth patterns.

### Atmosphere
Calculates atmospheric properties based on location and time.

### AbovegroundEnvironment
Models the interface between plant and atmosphere, particularly the canopy light environment.

### CarbonAssimilation
Implements photosynthesis calculations, converting environmental conditions into carbon gain.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
