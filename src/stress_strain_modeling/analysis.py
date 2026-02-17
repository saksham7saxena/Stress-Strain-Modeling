import numpy as np
from typing import List, Dict, Union
from src.stress_strain_modeling.model import CompositeModel

def calculate_tangent_modulus(strain: np.ndarray, stress: np.ndarray) -> np.ndarray:
    """
    Calculate the tangent modulus (d_stress/d_strain).
    """
    return np.gradient(stress, strain)

def vf_sweep(angles: List[float], weights: List[float], vfs: List[float], strain: np.ndarray, 
             model_type: str = 'weighted') -> Dict[float, np.ndarray]:
    """
    Perform a volume fraction sweep.
    """
    results = {}
    for vf in vfs:
        model = CompositeModel(angles, weights, vf=vf)
        if model_type == 'weighted':
            results[vf] = model.compute_stress_weighted(strain)
        # Add other model types if needed
    return results

def monte_carlo_uncertainty(angles: List[float], weights: List[float], vf: float, strain: np.ndarray, 
                            n_iter: int = 100, noise_std: float = 0.05, model_type: str = 'weighted') -> np.ndarray:
    """
    Perform Monte Carlo simulation by perturbing weights (phi).
    """
    results = []
    base_weights = np.array(weights)
    target_sum = np.sum(base_weights)
    
    for _ in range(n_iter):
        noise = np.random.normal(0, noise_std, size=base_weights.shape)
        perturbed_weights = base_weights * (1 + noise)
        perturbed_weights = np.maximum(perturbed_weights, 0)
        
        current_sum = np.sum(perturbed_weights)
        if current_sum > 0:
            perturbed_weights = perturbed_weights / current_sum * target_sum
            
        model = CompositeModel(angles, perturbed_weights, vf=vf)
        
        if model_type == 'weighted':
            stress = model.compute_stress_weighted(strain)
        # Add logical branch for other models if needed
        
        results.append(stress)
        
    return np.array(results)

def generate_heatmap_data(angles: List[float], weights: List[float], vf_range: np.ndarray, strain: np.ndarray) -> np.ndarray:
    """
    Generate 2D stress data for Heatmap (Strain vs VF).
    """
    stress_matrix = []
    for vf in vf_range:
        model = CompositeModel(angles, weights, vf=vf)
        stress = model.compute_stress_weighted(strain)
        stress_matrix.append(stress)
        
    return np.array(stress_matrix)
