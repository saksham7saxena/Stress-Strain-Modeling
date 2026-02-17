import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Union

@dataclass
class CompositeMaterial:
    """
    Properties of the composite constituents.
    Default values are placeholders commonly used in examples.
    """
    E_f: float = 230000.0  # Fiber modulus [MPa] (e.g., Carbon)
    E_m: float = 3000.0    # Matrix modulus [MPa] (e.g., Epoxy)
    nu_f: float = 0.2      # Fiber Poisson's ratio
    nu_m: float = 0.35     # Matrix Poisson's ratio
    G_f: float = 50000.0   # Fiber shear modulus [MPa] (approx)
    G_m: float = 1200.0    # Matrix shear modulus [MPa]
    
    # Strength limits for Tsai-Hill (Placeholder values)
    X_t: float = 2000.0    # Longitudinal tensile strength [MPa]
    X_c: float = 1000.0    # Longitudinal compressive strength [MPa]
    Y_t: float = 50.0      # Transverse tensile strength [MPa]
    Y_c: float = 150.0     # Transverse compressive strength [MPa]
    S: float = 70.0        # In-plane shear strength [MPa]

@dataclass
class CompositeModel:
    """
    A model for calculating the stress-strain behavior of a composite material.
    """
    angles: Union[List[float], np.ndarray]
    weights: Union[List[float], np.ndarray]
    vf: float = 0.1
    material: CompositeMaterial = field(default_factory=CompositeMaterial)
    E_fiber_factor: float = 525000.0 # Original 525 * 1000 for MPa conversion if assuming original was GPa? 
                                     # Actually original readme said 525 normalized units. 
                                     # Let's stick to 525.0 * 1000 to be in MPa range if 525 was GPa. 
                                     # User said "Units: MPa". 525 GPa = 525000 MPa.

    def __post_init__(self):
        self.angles = np.array(self.angles)
        self.weights = np.array(self.weights)
        if len(self.angles) != len(self.weights):
            raise ValueError("Angles and weights must have the same length.")
        if not (0.0 <= self.vf <= 1.0):
            raise ValueError("Volume fraction (vf) must be between 0.0 and 1.0")

    def compute_stress_weighted(self, strain: np.ndarray, weighting: str = 'cos4') -> np.ndarray:
        """
        Original 'Weighted' model logic.
        """
        strain_arr = np.array(strain)
        angles_rad = np.deg2rad(self.angles)
        cos_sq = np.cos(angles_rad)**2
        
        if weighting == 'cos4':
            orientation_factor = cos_sq**2
        elif weighting == 'cos2':
            orientation_factor = cos_sq
        else:
            raise ValueError("weighting must be 'cos4' or 'cos2'")
            
        weighted_orientation = np.sum(self.weights * orientation_factor)
        
        # Effective Modulus
        # Converting raw factor to MPa if it wasn't already. 
        # The prompt implies we should clarify units. 
        # Let's assume E_fiber_factor is max stiffness in MPa.
        E_total = self.E_fiber_factor * self.vf * weighted_orientation
        
        return E_total * strain_arr

    def compute_halpin_tsai_modulus(self) -> float:
        """
        Calculate E1 (longitudinal), E2 (transverse), G12 (shear), and nu12 
        using Halpin-Tsai + Rule of Mixtures.
        Returns an effective stiffness for the current angle distribution.
        
        For simplicity in this 1D stress-strain model, we will compute 
        the effective modulus E_x along the loading direction using Classical Lamination Theory (CLT) 
        approximations or simple transformation equations.
        
        Ref: E_x = 1 / (cos^4/E1 + (1/G12 - 2*nu12/E1)*sin^2*cos^2 + sin^4/E2)
        """
        E_f = self.material.E_f
        E_m = self.material.E_m
        
        # Rule of Mixtures for E1 (Longitudinal)
        E1 = E_f * self.vf + E_m * (1 - self.vf)
        
        # Halpin-Tsai for E2 (Transverse)
        # xi = 2 for circular fibers in square array implies better fit, 
        # often xi=2 used for E2.
        xi = 2.0
        eta = (E_f/E_m - 1) / (E_f/E_m + xi)
        E2 = E_m * (1 + xi * eta * self.vf) / (1 - eta * self.vf)
        
        # Major Poisson's Ratio
        nu12 = self.material.nu_f * self.vf + self.material.nu_m * (1 - self.vf)
        
        # Shear Modulus G12 (Halpin-Tsai with xi=1)
        xi_G = 1.0
        eta_G = (self.material.G_f/self.material.G_m - 1) / (self.material.G_f/self.material.G_m + xi_G)
        G12 = self.material.G_m * (1 + xi_G * eta_G * self.vf) / (1 - eta_G * self.vf)
        
        # Now average over the angle distribution
        # Integrated 1/Ex weighted by phi
        # Stiffness Q_bar matrix approach is more rigorous, but for this 1D model:
        # We'll calculate E_x for each angle and weigh it.
        
        angles_rad = np.deg2rad(self.angles)
        c = np.cos(angles_rad)
        s = np.sin(angles_rad)
        c2 = c**2
        s2 = s**2
        c4 = c**4
        s4 = s**4
        
        # Compliance transformation (S_bar_11)
        # 1/Ex = c^4/E1 + c^2 s^2 (1/G12 - 2*nu12/E1) + s^4/E2
        inv_E1 = 1.0 / E1
        inv_E2 = 1.0 / E2
        inv_G12 = 1.0 / G12
        
        term1 = c4 * inv_E1
        term2 = c2 * s2 * (inv_G12 - 2 * nu12 * inv_E1) # Check sign: S16 terms cancel in isotropic/orthotropic
        term3 = s4 * inv_E2
        
        inv_Ex_i = term1 + term2 + term3
        Ex_i = 1.0 / inv_Ex_i
        
        # Weighted Average Modulus
        # Using Parallel model assumption (Voigt-like): E_eff = Sum(phi * Ex_i)
        # Using Series model (Reuss-like) would be 1/E_eff = Sum(phi / Ex_i)
        # Composite mechanics usually implies layers in parallel for in-plane load.
        E_effective = np.sum(self.weights * Ex_i)
        
        return E_effective

    def compute_stress_halpin_tsai(self, strain: np.ndarray) -> np.ndarray:
        """
        Calculate stress using Halpin-Tsai effective modulus.
        Linear elastic up to failure (not modeled here in this method).
        """
        strain_arr = np.array(strain)
        E_eff = self.compute_halpin_tsai_modulus()
        return E_eff * strain_arr

    def compute_tsai_hill(self, stress_applied: float, angle_deg: float) -> float:
        """
        Compute Tsai-Hill failure index for a single lamina at a given angle 
        under global uniaxial stress `stress_applied` (Load along X).
        
        Global Stress: sigma_x
        Transform to Local Axes (1, 2):
        sigma_1 = sigma_x * cos^2(theta)
        sigma_2 = sigma_x * sin^2(theta)
        tau_12 = -sigma_x * sin(theta) * cos(theta)
        
        Tsai-Hill criterion:
        (sigma_1/X)^2 - (sigma_1*sigma_2/X^2) + (sigma_2/Y)^2 + (tau_12/S)^2 < 1
        
        Note: Use X_t/X_c depending on sign of sigma_1.
        """
        angle_rad = np.deg2rad(angle_deg)
        c = np.cos(angle_rad)
        s = np.sin(angle_rad)
        
        sigma_1 = stress_applied * c**2
        sigma_2 = stress_applied * s**2
        tau_12 = -stress_applied * s * c
        
        X = self.material.X_t if sigma_1 >= 0 else self.material.X_c
        Y = self.material.Y_t if sigma_2 >= 0 else self.material.Y_c
        S = self.material.S
        
        term1 = (sigma_1 / X)**2
        term2 = - (sigma_1 * sigma_2) / (X**2)
        term3 = (sigma_2 / Y)**2
        term4 = (tau_12 / S)**2
        
        return term1 + term2 + term3 + term4
