# Model Intercomparison

This directory contains scripts and output for comparing the original model implementation (`original_for_comparison.py`) with the refactored model implementation (`minimum_plant_model`).

## Contents

- `compare_models.py`: Script to run both model implementations with the same input data and compare the results
- `results/`: Directory containing CSV files with full model outputs and summary comparison
- `plots/`: Directory containing comparative plots of key model metrics

## Running the Comparison

To run the model comparison:

```bash
# Activate the virtual environment first
source ../mpm_env/bin/activate

# Run the comparison script
python compare_models.py
```

## Understanding the Results

The comparison analyzes several key metrics:

1. **Thermal Age**: The accumulated thermal time in the model
2. **Leaf Area Index (LAI)**: The leaf area per unit ground area
3. **Carbon Pool**: The available carbon for allocation to plant growth
4. **Resource Pool Sizes**: The size of the different plant component pools (canopy, root, storage)

For each metric, the comparison shows:
- Original model value
- Refactored model value
- Absolute difference
- Percentage difference

## Plots

Several plots are generated to visualize the differences between models:

- LAI comparison over thermal age
- Carbon pool comparison over thermal age
- Assimilation comparison (sample range)
- Resource pool comparisons (canopy, root, storage)
- Early growth comparison (first 1000 timesteps)

## Model Alignment Success

After recent fixes, the original and refactored models now produce identical results. The key fixes implemented were:

1. **LAI Calculation**: Fixed the Leaf Area Index calculation to properly account for the ground area per plant factor
2. **Resource Allocation**: Restored the PriorityQueue-based allocation mechanism from the original model
3. **Parameter Naming**: Ensured consistent naming for growth allocation priorities 
4. **Method Signatures**: Aligned method signatures and return values with the original implementation
5. **Interface Compatibility**: Maintained compatibility with both old and new method names through adapter methods

These fixes ensure that both models now produce exactly the same output values for all key metrics when run with identical input data.

## Validated Metrics

The following metrics have been validated to have 0% difference between the original and refactored implementations:

- Thermal age accumulation 
- Leaf Area Index (LAI)
- Carbon pool size
- All resource pool sizes (canopy, root, storage)

## Documentation and Usage

Both models can be used interchangeably, with the refactored model providing additional benefits:

- Better code organization with separate modules
- Type hints for improved code safety
- Comprehensive docstrings
- Consistent naming conventions
- Modular design for extending functionality

For new development, the refactored model is recommended while maintaining full compatibility with the original model's behavior.