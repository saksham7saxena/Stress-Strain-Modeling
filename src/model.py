import numpy as np

class CompositeModel:
    """
    A model for calculating the stress-strain behavior of a composite material
    based on fiber orientation, volume fraction, and empirical weighting factors.
    """
    
    def __init__(self, angles, weights, vf=0.1, E_fiber_factor=525.0):
        """
        Initialize the Composite Model.

        Args:
            angles (list or np.array): List of fiber orientation angles in degrees.
            weights (list or np.array): List of weighting factors (phi) for each angle.
            vf (float): Volume fraction of fibers (0.0 to 1.0). Default is 0.1.
            E_fiber_factor (float): Empirical stiffness factor for the fiber. 
                                  Original script used 5.25 * 100 = 525.
        """
        self.angles = np.array(angles)
        self.weights = np.array(weights)
        self.vf = vf
        self.E_fiber_factor = E_fiber_factor
        
        # Validate inputs
        if len(self.angles) != len(self.weights):
            raise ValueError(f"Angles and weights must have the same length. Got {len(self.angles)} angles and {len(self.weights)} weights.")
        if not (0.0 <= self.vf <= 1.0):
            raise ValueError("Volume fraction (vf) must be between 0.0 and 1.0")

    def compute_stress(self, strain, weighting='cos4'):
        """
        Calculate the stress for a given strain array.

        The model assumes a rule of mixtures approach modified by orientation factors.
        
        Original Model Logic (Effective 'cos4'):
            Stress contributions are scaled by cos^2(beta) for strain transformation
            AND cos^2(beta) for stress projection.
            Formula: Stress = Sum( E_factor * vf * strain * phi * cos^4(beta) )
            
        Alternative Logic ('cos2'):
            Stress = Sum( E_factor * vf * strain * phi * cos^2(beta) )

        Args:
            strain (list or np.array): Array of strain values (e.g. [0.001, 0.002, ...])
            weighting (str): 'cos4' (default, mimics original script) or 'cos2'.

        Returns:
            np.array: Calculated stress values corresponding to the input strain.
        """
        strain_arr = np.array(strain)
        
        # Convert angles to radians
        angles_rad = np.deg2rad(self.angles)
        
        # Calculate cosine squared term
        cos_sq = np.cos(angles_rad)**2
        
        # Select weighting power
        if weighting == 'cos4':
            orientation_factor = cos_sq**2  # cos^4
        elif weighting == 'cos2':
            orientation_factor = cos_sq     # cos^2
        else:
            raise ValueError("weighting must be 'cos4' or 'cos2'")
            
        # Vectorized calculation
        # We want to sum over the angles/weights dimensions.
        # equation: sigma = strain * vf * E_factor * sum(phi * orientation_factor)
        
        # 1. Calculate the effective modulus contribution from all fibers
        #    Sum( phi_i * orientation_factor_i )
        weighted_orientation = np.sum(self.weights * orientation_factor)
        
        # 2. Total Modulus E_total = E_fiber_factor * vf * weighted_orientation
        E_total = self.E_fiber_factor * self.vf * weighted_orientation
        
        # 3. Stress = E_total * Strain
        stress = E_total * strain_arr
        
        return stress

    def compute_stress_components(self, strain, weighting='cos4'):
        """
        Calculate the stress contribution from each fiber orientation angle.

        Args:
            strain (list or np.array): Array of strain values.
            weighting (str): 'cos4' or 'cos2'.

        Returns:
            np.array: Array of shape (n_angles, n_strain) where each row is the
                      stress contribution of that angle.
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
            
        # Component_i = E_factor * vf * strain * phi_i * orientation_factor_i
        # Reshape for broadcasting: (n_angles, 1) * (n_strain,)
        
        # Pre-calculate angle-dependent terms: (n_angles,)
        angle_terms = self.E_fiber_factor * self.vf * self.weights * orientation_factor
        
        # Broadcast multiply: (n_angles, 1) * (1, n_strain) -> (n_angles, n_strain)
        components = angle_terms[:, np.newaxis] * strain_arr[np.newaxis, :]
        
        return components
