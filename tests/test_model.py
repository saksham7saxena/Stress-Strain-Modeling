import pytest
import numpy as np
from src.stress_strain_modeling.model import CompositeModel, CompositeMaterial

@pytest.fixture
def default_args():
    return {
        'angles': [0, 45, 90],
        'weights': [0.5, 0.3, 0.2],
        'vf': 0.1
    }

def test_model_initialization(default_args):
    """Test valid initialization."""
    model = CompositeModel(**default_args)
    assert len(model.angles) == 3
    assert model.vf == 0.1

def test_invalid_initialization():
    """Test validation logic."""
    with pytest.raises(ValueError, match="Angles and weights must have the same length"):
        CompositeModel(angles=[0, 10], weights=[0.5])
    
    with pytest.raises(ValueError, match="Volume fraction"):
        CompositeModel(angles=[0], weights=[1.0], vf=1.5)

def test_compute_stress_weighted(default_args):
    """Test shape and basic values of weighted model."""
    model = CompositeModel(**default_args)
    strain = np.array([0.001, 0.002])
    stress = model.compute_stress_weighted(strain)
    assert stress.shape == strain.shape
    assert np.all(stress > 0)

def test_compute_stress_halpin_tsai(default_args):
    """Test shape and basic values of Halpin-Tsai model."""
    model = CompositeModel(**default_args)
    strain = np.array([0.001, 0.002])
    stress = model.compute_stress_halpin_tsai(strain)
    assert stress.shape == strain.shape
    assert np.all(stress > 0)
    
def test_tsai_hill_failure(default_args):
    """Test failure index calculation."""
    model = CompositeModel(**default_args)
    
    # Simple case: Stress along fiber (0 deg) exceeding strength
    # X_t = 2000
    idx_safe = model.compute_tsai_hill(stress_applied=100.0, angle_deg=0)
    idx_fail = model.compute_tsai_hill(stress_applied=2500.0, angle_deg=0)
    
    assert idx_safe < 1.0
    assert idx_fail > 1.0
