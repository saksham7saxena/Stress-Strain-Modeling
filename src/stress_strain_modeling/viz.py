import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Union

def plot_stress_strain(strain: np.ndarray, stress: np.ndarray, label: str = 'Composite', ax: Optional[plt.Axes] = None) -> plt.Axes:
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.plot(strain, stress, label=label, linewidth=2)
    ax.set_xlabel('Strain (ε)')
    ax.set_ylabel('Stress (σ) [MPa]')
    ax.set_title('Stress-Strain Curve')
    ax.grid(True, linestyle='--', alpha=0.7)
    if label:
        ax.legend()
    return ax

def plot_vf_sweep(strain: np.ndarray, vf_results: Dict[float, np.ndarray], ax: Optional[plt.Axes] = None) -> plt.Axes:
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        
    for vf, stress in vf_results.items():
        ax.plot(strain, stress, label=f'Vf = {vf:.2f}')
        
    ax.set_xlabel('Strain (ε)')
    ax.set_ylabel('Stress (σ) [MPa]')
    ax.set_title('Effect of Volume Fraction on Stress-Strain Behavior')
    ax.legend(title='Volume Fraction')
    ax.grid(True, linestyle='--', alpha=0.7)
    return ax

def plot_tangent_modulus(strain: np.ndarray, tangent: np.ndarray, ax: Optional[plt.Axes] = None) -> plt.Axes:
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        
    ax.plot(strain, tangent, color='red', linewidth=2)
    ax.set_xlabel('Strain (ε)')
    ax.set_ylabel('Tangent Modulus (dσ/dε) [MPa]')
    ax.set_title('Tangent Modulus vs Strain')
    ax.grid(True, linestyle='--', alpha=0.7)
    return ax

def plot_stress_heatmap(strain: np.ndarray, vf_range: np.ndarray, stress_matrix: np.ndarray, ax: Optional[plt.Axes] = None) -> plt.Axes:
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        
    X, Y = np.meshgrid(strain, vf_range)
    c = ax.pcolormesh(X, Y, stress_matrix, shading='auto', cmap='viridis')
    plt.colorbar(c, ax=ax, label='Stress [MPa]')
    
    ax.set_xlabel('Strain (ε)')
    ax.set_ylabel('Volume Fraction (Vf)')
    ax.set_title('Stress Heatmap: Strain vs Volume Fraction')
    return ax

def plot_monte_carlo_uncertainty(strain: np.ndarray, mc_results: np.ndarray, base_stress: np.ndarray, ax: Optional[plt.Axes] = None) -> plt.Axes:
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        
    for i in range(min(len(mc_results), 100)):
        ax.plot(strain, mc_results[i], color='gray', alpha=0.1, linewidth=1)
        
    mean_stress = np.mean(mc_results, axis=0)
    std_stress = np.std(mc_results, axis=0)
    
    ax.plot(strain, base_stress, color='blue', label='Baseline Model', linewidth=2)
    ax.plot(strain, mean_stress, color='black', linestyle='--', label='MC Mean', linewidth=1.5)
    
    ax.fill_between(strain, mean_stress - 2*std_stress, mean_stress + 2*std_stress, 
                    color='gray', alpha=0.3, label='95% CI (±2σ)')
                    
    ax.set_xlabel('Strain (ε)')
    ax.set_ylabel('Stress (σ) [MPa]')
    ax.set_title('Uncertainty Analysis (Monte Carlo on Weights)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    return ax

def plot_angle_contributions(strain: np.ndarray, angles: List[float], contributions: np.ndarray, ax: Optional[plt.Axes] = None) -> plt.Axes:
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        
    for i, angle in enumerate(angles):
        ax.plot(strain, contributions[i], label=f'{angle}°')
        
    total = np.sum(contributions, axis=0)
    ax.plot(strain, total, 'k--', label='Total', linewidth=2)
    
    ax.set_xlabel('Strain (ε)')
    ax.set_ylabel('Stress Contribution [MPa]')
    ax.set_title('Stress Contribution by Fiber Orientation')
    ax.legend(title='Orientation')
    ax.grid(True, linestyle='--', alpha=0.7)
    return ax

def plot_tsai_hill_failure(tsai_hill_indices: np.ndarray, angles: Union[List[float], np.ndarray], output_path: str = None):
    """
    Plot Tsai-Hill failure index vs Angle.
    """
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': 'polar'})
    
    theta_rad = np.deg2rad(angles)
    ax.plot(theta_rad, tsai_hill_indices, linewidth=2, label='Tsai-Hill Index')
    
    # Add failure boundary (Index = 1)
    ax.plot(theta_rad, np.ones_like(theta_rad), 'r--', label='Failure Threshold (1.0)')
    
    ax.set_title('Tsai-Hill Failure Index vs Fiber Angle')
    ax.legend()
    
    if output_path:
        plt.savefig(output_path)
    return ax
