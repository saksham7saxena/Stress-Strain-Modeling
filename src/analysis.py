import numpy as np
from src.model import CompositeModel

def calculate_tangent_modulus(strain, stress):
    """
    Calculate the tangent modulus (d_stress/d_strain) using numerical differentiation.
    
    Args:
        strain (np.array): Strain array.
        stress (np.array): Stress array.
        
    Returns:
        np.array: Tangent modulus array.
    """
    return np.gradient(stress, strain)

def vf_sweep(angles, weights, vfs, strain, E_fiber_factor=525.0):
    """
    Perform a volume fraction sweep.
    
    Args:
        angles (list): Fiber angles.
        weights (list): Distribution weights.
        vfs (list): List of volume fractions to simulate.
        strain (np.array): Strain array.
        
    Returns:
        dict: Mapping vf -> stress_array
    """
    results = {}
    for vf in vfs:
        model = CompositeModel(angles, weights, vf=vf, E_fiber_factor=E_fiber_factor)
        results[vf] = model.compute_stress(strain)
    return results

def monte_carlo_uncertainty(angles, weights, vf, strain, n_iter=100, noise_std=0.05, E_fiber_factor=525.0):
    """
    Perform Monte Carlo simulation by perturbing weights (phi).
    
    Args:
        noise_std (float): Standard deviation of Gaussian multiplicative noise (e.g., 0.05 for 5%).
    
    Returns:
        np.array: Array of shape (n_iter, n_strain) containing stress curves.
    """
    results = []
    base_weights = np.array(weights)
    target_sum = np.sum(base_weights)
    
    for _ in range(n_iter):
        # Multiplicative noise: w_new = w * (1 + N(0, sigma))
        noise = np.random.normal(0, noise_std, size=base_weights.shape)
        perturbed_weights = base_weights * (1 + noise)
        
        # Ensure non-negative
        perturbed_weights = np.maximum(perturbed_weights, 0)
        
        # Renormalize to maintain original sum (assumption: distribution shape uncertainty, not total amount)
        current_sum = np.sum(perturbed_weights)
        if current_sum > 0:
            perturbed_weights = perturbed_weights / current_sum * target_sum
            
        model = CompositeModel(angles, perturbed_weights, vf=vf, E_fiber_factor=E_fiber_factor)
        stress = model.compute_stress(strain)
        results.append(stress)
        
    return np.array(results)

def generate_heatmap_data(angles, weights, vf_range, strain, E_fiber_factor=525.0):
    """
    Generate 2D stress data for Heatmap (Strain vs VF).
    
    Args:
        vf_range (np.array): Array of VF values (Y-axis).
        strain (np.array): Array of strain values (X-axis).
        
    Returns:
        np.array: 2D array of Stress values with shape (len(vf_range), len(strain)).
    """
    stress_matrix = []
    for vf in vf_range:
        model = CompositeModel(angles, weights, vf=vf, E_fiber_factor=E_fiber_factor)
        stress = model.compute_stress(strain)
        stress_matrix.append(stress)
        
    return np.array(stress_matrix)
