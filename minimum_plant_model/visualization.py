"""Visualization module for the Minimum Plant Model."""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional, Any, Tuple

def plot_thermal_time_variable(thermal_age: List[float], variable: List[float], 
                              title: str, ylabel: str, xlabel: Optional[str] = 'Thermal Time (degree days)',
                              figsize: Tuple[int, int] = (10, 6)) -> None:
    """Plot a variable against thermal time.
    
    Args:
        thermal_age: List of thermal age values
        variable: List of variable values to plot
        title: Plot title
        ylabel: Label for y-axis
        xlabel: Label for x-axis, defaults to 'Thermal Time (degree days)'
        figsize: Figure size (width, height) in inches
    """
    plt.figure(figsize=figsize)
    plt.plot(thermal_age, variable, linestyle='-')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_time_series(variable: List[float], title: str, ylabel: str, 
                    xlabel: str = 'Time Step', figsize: Tuple[int, int] = (10, 6),
                    start: Optional[int] = None, end: Optional[int] = None,
                    marker: Optional[str] = None) -> None:
    """Plot a time series variable.
    
    Args:
        variable: List of variable values to plot
        title: Plot title
        ylabel: Label for y-axis
        xlabel: Label for x-axis, defaults to 'Time Step'
        figsize: Figure size (width, height) in inches
        start: Starting index (optional)
        end: Ending index (optional)
        marker: Marker style (optional)
    """
    plt.figure(figsize=figsize)
    
    # Handle slicing if start/end provided
    if start is not None or end is not None:
        start = start or 0
        end = end or len(variable)
        x_values = list(range(start, end))
        plt.plot(x_values, variable[start:end], marker=marker, linestyle='-')
    else:
        plt.plot(list(range(len(variable))), variable, marker=marker, linestyle='-')
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_resource_pools(resource_pool_sizes: Dict[str, List[float]], 
                       title: Optional[str] = 'Resource Pool Sizes Over Time',
                       xlabel: str = 'Time Step', ylabel: str = 'Resource Pool Size',
                       figsize: Tuple[int, int] = (10, 6)) -> None:
    """Plot resource pool sizes over time.
    
    Args:
        resource_pool_sizes: Dictionary mapping resource pool names to size time series
        title: Plot title
        xlabel: Label for x-axis
        ylabel: Label for y-axis
        figsize: Figure size (width, height) in inches
    """
    plt.figure(figsize=figsize)
    
    # Plot each resource pool
    for name, sizes in resource_pool_sizes.items():
        plt.plot(list(range(len(sizes))), sizes, label=name)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_model_outputs(model: 'MainModel') -> None:
    """Plot standard model outputs.
    
    Args:
        model: MainModel instance with simulation results
    """
    # Plot assimilation (windowed view)
    if len(model.log_assimilation) > 1600:
        plot_time_series(
            model.log_assimilation[1500:1600],
            title='Photosynthesis Rate',
            ylabel='Assimilation (µmol CO₂ m⁻² s⁻¹)',
            start=1500,
            end=1600,
            marker='o'
        )

    # Plot LAI
    plot_time_series(
        model.log_lai,
        title='Leaf Area Index Over Time',
        ylabel='LAI (m² leaf / m² ground)'
    )

    # Plot resource pool demand
    plot_time_series(
        model.log_rp_demand,
        title='Resource Pool Demand Over Time',
        ylabel='Demand (g C)'
    )

    # Plot relative growth rate vs thermal time
    plot_thermal_time_variable(
        model.log_thermal_age,
        model.log_rp_rgr,
        title='Relative Growth Rate vs Thermal Time',
        ylabel='RGR (g g⁻¹ degree-day⁻¹)'
    )

    # Plot carbon pool vs thermal time
    plot_thermal_time_variable(
        model.log_thermal_age,
        model.log_carbon_pool,
        title='Carbon Pool vs Thermal Time',
        ylabel='Carbon Pool (g C)'
    )

    # Plot resource pools
    plot_resource_pools(model.log_resource_pool_sizes)