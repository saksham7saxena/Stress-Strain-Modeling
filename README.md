# Composite Stress-Strain Modeling

A Python package for modeling and analyzing the stress-strain behavior of fiber-reinforced composite materials.

## Modeling Background

Composite materials derive their stiffness and strength from the combination of high-modulus fibers (e.g., Carbon, Glass) and a binding matrix (e.g., Epoxy). This tool models the effective elastic properties of a lamina based on fiber orientation distribution, volume fraction ($V_f$), and constituent properties.

## Models

### 1. Orientation-Weighted Rule of Mixtures (OW-ROM)
*Legacy / Default Model*

This model modifies the simple Rule of Mixtures by scaling the fiber contribution based on orientation angles ($\theta$) and an empirical weighting factor ($\phi$). It effectively projects the fiber stiffness onto the loading magnitude.

$$ \sigma(\epsilon) = E_{fiber\_factor} \cdot V_f \cdot \epsilon \cdot \sum (\phi_i \cdot \cos^4 \theta_i) $$

### 2. Halpin-Tsai Model
*Semi-Empirical Micromechanics*

The Halpin-Tsai equations provide a more rigorous estimation of effective stiffness ($E_{eff}$) by accounting for the aspect ratio and geometry of the reinforcement factor ($\xi$).

$$ E_{eff} = E_m \left( \frac{1 + \xi \eta V_f}{1 - \eta V_f} \right) $$

Where:
$$ \eta = \frac{(E_f / E_m) - 1}{(E_f / E_m) + \xi} $$

> **Model Comparison**:
> *   **OW-ROM**: Best for quick, empirical approximations when specific constituent data ($E_m, \nu$) is unavailable.
> *   **Halpin-Tsai**: More physically rigorous for defined fiber/matrix systems. It better captures transverse ($E_2$) and shear ($G_{12}$) moduli.

## Failure Analysis

### Tsai-Hill Criterion
This tool implements the Tsai-Hill failure criterion for orthotropic materials under plane stress. Failure is predicted when the index exceeds 1:

$$ \left(\frac{\sigma_1}{X}\right)^2 - \frac{\sigma_1 \sigma_2}{X^2} + \left(\frac{\sigma_2}{Y}\right)^2 + \left(\frac{\tau_{12}}{S}\right)^2 \ge 1 $$

Where $X, Y, S$ are the longitudinal, transverse, and shear strengths, respectively.

## Numerical Analysis & Uncertainty

### Monte Carlo Simulation
To account for manufacturing variability, the tool performs Monte Carlo simulations by perturbing the fiber orientation weights ($\phi_i$) with multiplicative Gaussian noise (Mean $\mu=0$, Std Dev $\sigma$).

*   **Purpose**: Quantify the impact of inconsistent fiber distribution on effective stiffness.
*   **Outputs**: Generates a 95% Confidence Interval (CI) around the mean stress-strain curve.
*   **Visualization**: Shaded regions in stress-strain plots represent the uncertainty bounds.

## Scope & Limitations

*   **Linear Elasticity**: The models assume linear elastic behavior up to failure. Plasticity and non-linear matrix behavior are **not** modeled.
*   **2D Plane Stress**: Analysis assumes a thin lamina under plane stress conditions.
*   **Static Loading**: No fatigue, creep, or strain-rate effects are considered.
*   **Perfect Bonding**: Assumes perfect stress transfer between fiber and matrix (no debonding).

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
   *(Ensure `numpy` and `matplotlib` are installed)*

## Usage

Run the analysis using the Command Line Interface (CLI):

### Basic Run (Weighted Model)
```bash
python -m src.stress_strain_modeling.cli --vf 0.2
```

### Halpin-Tsai Model
```bash
python -m src.stress_strain_modeling.cli --model halpin-tsai --vf 0.2
```

### With Failure Analysis
```bash
python -m src.stress_strain_modeling.cli --model halpin-tsai --plot-failure
```

### Options
- `--vf`: Volume fraction (0.0 - 1.0). Default: 0.1
- `--mc-iter`: Monte Carlo iterations. Default: 100
- `--model`: `weighted` or `halpin-tsai`
- `--plot-failure`: Generate Tsai-Hill failure plot
- `--no-show`: Save plots without displaying window

## Output

Plots are saved to `output/plots/`:
1. Stress-Strain Curve
2. Tangent Modulus
3. Tsai-Hill Failure Envelope (if enabled)

## Development

Run tests:
```bash
pytest
```
