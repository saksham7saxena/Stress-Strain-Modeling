import numpy as np
import matplotlib.pyplot as plt

def plot_stress_strain(strain, stress, label='Composite', ax=None):
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

def plot_vf_sweep(strain, vf_results, ax=None):
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

def plot_tangent_modulus(strain, tangent, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        
    ax.plot(strain, tangent, color='red', linewidth=2)
    ax.set_xlabel('Strain (ε)')
    ax.set_ylabel('Tangent Modulus (dσ/dε) [MPa]')
    ax.set_title('Tangent Modulus vs Strain')
    ax.grid(True, linestyle='--', alpha=0.7)
    return ax

def plot_stress_heatmap(strain, vf_range, stress_matrix, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        
    # Create meshgrid for pcolormesh
    X, Y = np.meshgrid(strain, vf_range)
    
    # Plot
    c = ax.pcolormesh(X, Y, stress_matrix, shading='auto', cmap='viridis')
    plt.colorbar(c, ax=ax, label='Stress [MPa]')
    
    ax.set_xlabel('Strain (ε)')
    ax.set_ylabel('Volume Fraction (Vf)')
    ax.set_title('Stress Heatmap: Strain vs Volume Fraction')
    return ax

def plot_monte_carlo_uncertainty(strain, mc_results, base_stress, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        
    # Plot individual MC runs with low alpha
    for i in range(min(len(mc_results), 100)): # Limit to 100 lines
        ax.plot(strain, mc_results[i], color='gray', alpha=0.1, linewidth=1)
        
    # Plot mean and base
    mean_stress = np.mean(mc_results, axis=0)
    std_stress = np.std(mc_results, axis=0)
    
    ax.plot(strain, base_stress, color='blue', label='Baseline Model', linewidth=2)
    ax.plot(strain, mean_stress, color='black', linestyle='--', label='MC Mean', linewidth=1.5)
    
    # Fill standard deviation
    ax.fill_between(strain, mean_stress - 2*std_stress, mean_stress + 2*std_stress, 
                    color='gray', alpha=0.3, label='95% CI (±2σ)')
                    
    ax.set_xlabel('Strain (ε)')
    ax.set_ylabel('Stress (σ) [MPa]')
    ax.set_title('Uncertainty Analysis (Monte Carlo on Weights)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    return ax

def plot_angle_contributions(strain, angles, contributions, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
        
    # contributions shape: (n_angles, n_strain)
    # Stack plot or lines?
    # Lines is better for comparison.
    
    for i, angle in enumerate(angles):
        ax.plot(strain, contributions[i], label=f'{angle}°')
        
    # Plot total
    total = np.sum(contributions, axis=0)
    ax.plot(strain, total, 'k--', label='Total', linewidth=2)
    
    ax.set_xlabel('Strain (ε)')
    ax.set_ylabel('Stress Contribution [MPa]')
    ax.set_title('Stress Contribution by Fiber Orientation')
    ax.legend(title='Orientation')
    ax.grid(True, linestyle='--', alpha=0.7)
    return ax
