# Minimum Plant Model (MPM)

## Project Description
The Minimum Plant Model (MPM) is a simulation framework for modeling plant growth and development under different environmental conditions. It simulates carbon assimilation, resource allocation, and growth of different plant components (resource pools) over time based on environmental drivers like temperature, radiation, and other climate variables.

## Features
- Simulates photosynthesis using a sunlit/shaded canopy model
- Models plant growth based on thermal time
- Resource allocation to different plant components (canopy, roots, storage)
- Modular design allowing flexible configuration of plant components
- Visualization of simulation results

## Project Structure
- `main.py` - Main simulation module containing model implementation
- `skeleton_drw.py` - Alternative implementation with additional features
- `UML_diagram.ipynb` - Notebook with UML diagrams of model architecture
- `model input files/` - Directory containing input data for simulations
  - `drivers_*.csv` - Environmental driver data (temperature, radiation, etc.)
  - `parameters.csv` - Model parameters
  - `resource_pools_*.csv` - Configuration files for different resource pool setups
  - `temperature_scenarios/` - Specialized driver files for temperature response testing

## Getting Started
### Prerequisites
- Python 3.x
- Required libraries: numpy, pandas, matplotlib

### Running a Simulation
```python
from main import ModelHandler

# Set file paths for inputs
driver_file = "model input files/drivers_natural_all.csv"
parameter_file = "model input files/parameters.csv"
resource_pool_file = "model input files/resource_pools_3RPs.csv"

# Create model instance
model = ModelHandler(driver_file, parameter_file, resource_pool_file)

# Run simulation
model.run_simulation()

# Plot results
model.plot_outputs()
```

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

## Input Files
- `drivers_*.csv` - Hourly or daily environmental data (temperature, radiation, VPD, etc.)
- `parameters.csv` - Model parameters including photosynthetic capacity, specific leaf area, etc.
- `resource_pools_*.csv` - Defines the different plant components, their growth parameters, and allocation priorities

## Citations
The model incorporates equations and concepts from:
- De Pury, D.G.G. and Farquhar, G.D., 1997. Simple scaling of photosynthesis from leaves to canopies without the errors of big‐leaf models. Plant, Cell & Environment, 20(5), pp.537-557
- Farquhar G.D., von Caemmerer S. & Berry J.A., 1980. A biochemical model of photosynthetic CO2 assimilation in leaves of C3 species. Planta 149, 78–90
- Wang, et al., 2019. Journal of Experimental Botany (Resource pool growth rate calculation)
- Leuning R., 1995. A critical appraisal of a combined stomatal-photosynthesis model for C3 plants. Plant, Cell and Environment 18, 339–355