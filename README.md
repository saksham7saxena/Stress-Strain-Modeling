# Stress-Strain Modeling of Composite Materials

This project implements a Python simulation to model the stress-strain behavior of composite materials. It calculates the modulus of elasticity and visualizes the stress-strain curve based on fiber orientation and volume fraction.

## Overview

The script simulates the mechanical response of a composite material by:
*   Calculating the modulus of elasticity for various fiber orientation angles ($\beta$).
*   Using cosine squared functions to model directional stiffness contributions.
*   Applying a weighted sum approach using weighting factors ($\phi$) to estimate the overall stress.
*   Plotting the resulting stress-strain curves using `matplotlib`.

## Features

*   **Composite Modeling**: Simulates stress-strain behavior for different fiber orientations.
*   **Visualization**: Generates plots of Stress vs. Strain.
*   **Customizable Parameters**: Allows adjustment of strain range, volume fraction (`vf`), and orientation angles.

## Tech Stack

*   **Language**: Python 3
*   **Libraries**: `matplotlib`, `math`

## Getting Started

### Prerequisites

*   Python 3.x
*   Matplotlib (`pip install matplotlib`)

### Usage

1.  Clone the repository:
    ```bash
    git clone https://github.com/saksham7saxena/Stress-Strain-Modeling.git
    cd Stress-Strain-Modeling
    ```

2.  Run the script:
    ```bash
    python Saksham_Saxena_2017TT10954.py
    ```

3.  The script will generate and display a stress-strain plot window.
