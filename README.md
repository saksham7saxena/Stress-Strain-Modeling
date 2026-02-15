# Composite Stress-Strain Modeling

A scientific Python project for modeling and analyzing the stress-strain behavior of fiber-reinforced composite materials.

This project simulates the mechanical response of composites based on fiber orientation, volume fraction ($V_f$), and empirical weighting factors using a rule-of-mixtures approach modified for directional stiffness.

## Features

- **Vectorized Calculation**: Efficient NumPy-based implementation replacing legacy loops.
- **Parametric Analysis**: 
  - **Volume Fraction Sweep**: Analyze how fiber content ($V_f$) impacts stiffness.
  - **Angle Contribution**: Breakdown of stress contributions from different fiber orientations.
- **Advanced Visualization**: 
  - Stress-Strain curves
  - Tangent Modulus ($d\sigma/d\epsilon$) plots
  - Stress Heatmaps (Strain vs $V_f$)
  - Monte Carlo uncertainty analysis
- **Configurable Models**: Supports both `cos^4` (default) and `cos^2` weighting logic.

## Mathematical Model

The stress $\sigma$ in the composite is calculated as a weighted sum of contributions from fibers at various orientation angles $\theta$:

$$ \sigma(\epsilon) = E_{fiber} \cdot V_f \cdot \epsilon \cdot \sum_{i} \left( \phi_i \cdot \cos^4(\theta_i) \right) $$

Where:
- $E_{fiber}$: Effective fiber stiffness factor (Default: 525 GPa/normalized units)
- $V_f$: Volume fraction of fibers
- $\epsilon$: Strain
- $\phi_i$: Weighting factor for angle $i$
- $\theta_i$: Fiber orientation angle

*Note: The `cos^4` term arises from the combination of strain transformation ($\cos^2$) and stress projection ($\cos^2$) in the loading direction.*

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/saksham7saxena/Stress-Strain-Modeling.git
   cd Stress-Strain-Modeling
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main analysis script to generate plots and data:

```bash
python run_analysis.py
```

### Options

- `--vf`: DSet volume fraction (default: 0.1).
- `--mc-iter`: Number of Monte Carlo iterations for uncertainty analysis (default: 100).
- `--no-show`: Do not display plots interactively (save only).

Example:
```bash
python run_analysis.py --vf 0.2 --mc-iter 200
```

## Project Structure

- `src/model.py`: Core `CompositeModel` class.
- `src/analysis.py`: Analytical routines (sweeps, gradients, Monte Carlo).
- `src/viz.py`: Matplotlib-based visualization functions.
- `run_analysis.py`: Main entry point and orchestration script.
- `output/`: Generated plots and data.
- `legacy/`: Original script archive.

## Legacy Code

The original simulation script has been moved to `legacy/original_script.py` for reference.
