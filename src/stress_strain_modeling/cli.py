import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
from src.stress_strain_modeling.model import CompositeModel
from src.stress_strain_modeling import analysis, viz

def main():
    parser = argparse.ArgumentParser(description="Stress-Strain Modeling CLI")
    parser.add_argument("--vf", type=float, default=0.1, help="Volume Fraction (default: 0.1)")
    parser.add_argument("--mc-iter", type=int, default=100, help="Monte Carlo iterations (default: 100)")
    parser.add_argument("--no-show", action="store_true", help="Do not show plots interactively")
    parser.add_argument("--model", type=str, choices=['weighted', 'halpin-tsai'], default='weighted', 
                        help="Model type: 'weighted' (original) or 'halpin-tsai'")
    parser.add_argument("--plot-failure", action="store_true", help="Generate Tsai-Hill failure plot")
    
    args = parser.parse_args()

    # Setup directories
    os.makedirs("output/plots", exist_ok=True)
    
    # Parameters
    angles = [0, 10, 20, 30, 40, 50, 60, 70, 80]
    weights = [0.0693, 0.1360, 0.1360, 0.1226 , 0.1146, 0.1054, 0.0974, 0.0920, 0.0880]
    strain = np.linspace(0.001, 0.3, 300)
    
    print(f"Running Analysis with Model: {args.model}, Vf={args.vf}")
    
    # Initialize Model
    model = CompositeModel(angles=angles, weights=weights, vf=args.vf)
    
    # 1. Compute Stress-Strain
    if args.model == 'weighted':
        stress = model.compute_stress_weighted(strain)
        label = f'Weighted Model (Vf={args.vf})'
    elif args.model == 'halpin-tsai':
        stress = model.compute_stress_halpin_tsai(strain)
        label = f'Halpin-Tsai Model (Vf={args.vf})'
        
    # Plot Stress-Strain
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    viz.plot_stress_strain(strain, stress, label=label, ax=ax1)
    fig1.savefig(f"output/plots/stress_strain_{args.model}.png")
    
    # 2. Tangent Modulus
    tangent = analysis.calculate_tangent_modulus(strain, stress)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    viz.plot_tangent_modulus(strain, tangent, ax=ax2)
    fig2.savefig("output/plots/tangent_modulus.png")
    
    # 3. Tsai-Hill Failure (Optional)
    if args.plot_failure:
        print("Generating Tsai-Hill Failure Envelope...")
        # Evaluate for a fixed stress to see failure index across angles
        # Or better: Plot failure index vs angle for the current max stress in simulation
        max_stress = np.max(stress)
        test_angles = np.linspace(0, 90, 91)
        indices = [model.compute_tsai_hill(max_stress, theta) for theta in test_angles]
        
        fig3, ax3 = plt.subplots(figsize=(8, 6))
        ax3.plot(test_angles, indices, label=f'Tsai-Hill Index @ {max_stress:.1f} MPa')
        ax3.axhline(1.0, color='r', linestyle='--', label='Failure Threshold')
        ax3.set_xlabel('Fiber Angle (deg)')
        ax3.set_ylabel('Failure Index')
        ax3.set_title('Tsai-Hill Failure Prediction')
        ax3.legend()
        ax3.grid(True)
        fig3.savefig("output/plots/tsai_hill_failure.png")

    print(f"Analysis complete. Plots saved to output/plots/")
    
    if not args.no_show:
        plt.show()

if __name__ == "__main__":
    main()
