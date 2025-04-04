
# MPM Development Plan

# Target Directory Structure
```
minimum_plant_model/
├── LICENSE
├── README.md
├── pyproject.toml
├── setup.py
├── .gitignore
├── docs/
│   ├── conf.py
│   ├── index.rst
│   └── scientific_background.md
├── tests/
│   ├── __init__.py
│   ├── test_main_model.py
│   ├── environment/               # Directory for environment-related tests
│   │   ├── __init__.py
│   │   ├── test_base_environment.py
│   │   ├── test_atmosphere.py
│   │   └── test_aboveground_environment.py
│   ├── plant/                     # Directory for plant-related tests
│   │   ├── __init__.py
│   │   ├── test_plant.py
│   │   ├── test_resource_pool.py
│   │   └── test_carbon_assimilation.py
│   └── data/
│       ├── test_drivers.csv
│       ├── test_parameters.csv
│       └── test_resource_pools.csv
├── minimum_plant_model/
│   ├── __init__.py
│   ├── main_model.py
│   ├── environment/                     # New directory for environment modules
│   │   ├── __init__.py
│   │   ├── base_environment.py          # Renamed from environment.py
│   │   ├── atmosphere.py                # Moved here from parent directory
│   │   └── aboveground_environment.py   # Extracted from base_environment.py
│   ├── plant/
│   │   ├── __init__.py
│   │   ├── resource_pool.py
│   │   └── carbon_assimilation.py
│   ├── utils.py
│   └── visualization.py
├── examples/
│   ├── __init__.py
│   ├── basic_simulation.py
│   ├── custom_environment.py
│   └── data/
│       ├── drivers_natural_all.csv
│       ├── parameters.csv
│       └── resource_pools_2RPs.csv
```
