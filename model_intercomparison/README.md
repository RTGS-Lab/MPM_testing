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

## Analysis Notes

Current comparisons show significant differences between the original and refactored models. These differences may be due to:

1. Parameter interpretation differences
2. Calculation method differences
3. Resource allocation algorithm differences

The refactored model currently shows much lower overall growth than the original model, indicating that some key growth factors may be calculated differently.