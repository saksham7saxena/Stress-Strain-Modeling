# Composite Stress-Strain Modeling

A Python package for modeling and analyzing the stress-strain behavior of fiber-reinforced composite materials.

## Features

- **Multiple Models**:
  - **Weighted Model**: Modified Rule of Mixtures with orientation weighting factors (Legacy/Default).
  - **Halpin-Tsai**: Semi-empirical model for effective stiffness.
- **Failure Analysis**:
  - **Tsai-Hill Criterion**: Failure envelope visualization.
- **Analysis Tools**:
  - **Volume Fraction Sweep**: Analyze impact of $V_f$ on stiffness.
  - **Monte Carlo**: Uncertainty analysis on fiber distribution weights.
  - **Heatmaps**: Stress vs. Strain and $V_f$.

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
