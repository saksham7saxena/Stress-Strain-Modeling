import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from src.model import CompositeModel
from src.analysis import (calculate_tangent_modulus, vf_sweep, 
                         monte_carlo_uncertainty, generate_heatmap_data)
import src.viz as viz

def main():
    parser = argparse.ArgumentParser(description="Run Composite Stress-Strain Analysis")
    parser.add_argument("--vf", type=float, default=0.1, help="Volume Fraction (default: 0.1)")
    parser.add_argument("--mc-iter", type=int, default=100, help="Monte Carlo iterations (default: 100)")
    parser.add_argument("--no-show", action="store_true", help="Do not show plots interactively")
    args = parser.parse_args()

    # Setup directories
    os.makedirs("output/plots", exist_ok=True)
    os.makedirs("output/data", exist_ok=True)
    
    print("Initializing Model parameters...")
    # Parameters from original script
    angles = [0, 10, 20, 30, 40, 50, 60, 70, 80]
    weights = [0.0693, 0.1360, 0.1360, 0.1226 , 0.1146, 0.1054, 0.0974, 0.0920, 0.0880]
    
    # Strain range: 0.1% to 30% (replicating original 0.001 * 1 to 0.001 * 300)
    strain = np.linspace(0.001, 0.3, 300)
    
    # 1. Base Analysis
    print(f"Running Base Analysis (Vf={args.vf})...")
    model = CompositeModel(angles, weights, vf=args.vf, E_fiber_factor=525.0)
    stress_base = model.compute_stress(strain)
    
    # Tangent Modulus
    tangent = calculate_tangent_modulus(strain, stress_base)
    
    # Contributions
    contributions = model.compute_stress_components(strain)
    
    # Plot Base Stress-Strain
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    viz.plot_stress_strain(strain, stress_base, label=f'Baseline (Vf={args.vf})', ax=ax1)
    fig1.savefig("output/plots/1_stress_strain_baseline.png")
    
    # Plot Tangent Modulus
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    viz.plot_tangent_modulus(strain, tangent, ax=ax2)
    fig2.savefig("output/plots/2_tangent_modulus.png")
    
    # Plot Contributions
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    viz.plot_angle_contributions(strain, angles, contributions, ax=ax3)
    fig3.savefig("output/plots/3_angle_contributions.png")
    
    # 2. VF Sweep
    print("Running Volume Fraction Sweep...")
    vfs = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
    sweep_results = vf_sweep(angles, weights, vfs, strain)
    
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    viz.plot_vf_sweep(strain, sweep_results, ax=ax4)
    fig4.savefig("output/plots/4_vf_sweep.png")
    
    # 3. Heatmap
    print("Generating Heatmap...")
    vf_range = np.linspace(0.01, 0.6, 50)
    heatmap_data = generate_heatmap_data(angles, weights, vf_range, strain)
    # The plotting function expects X, Y, Z. 
    # meshgrid in viz.py handles vectors. 
    # Viz function expects arrays of values.
    # Note: viz.plot_stress_heatmap's pcolormesh needs careful checking of dimensions.
    # generate_heatmap_data returns (len(vf), len(strain)).
    # viz.py uses np.meshgrid(strain, vf_range). dimension X is (len(vf), len(strain)).
    # This matches.
    
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    viz.plot_stress_heatmap(strain, vf_range, heatmap_data, ax=ax5)
    fig5.savefig("output/plots/5_stress_heatmap.png")
    
    # 4. Monte Carlo
    print(f"Running Monte Carlo Uncertainty Analysis ({args.mc_iter} iterations)...")
    mc_results = monte_carlo_uncertainty(angles, weights, args.vf, strain, n_iter=args.mc_iter)
    
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    viz.plot_monte_carlo_uncertainty(strain, mc_results, stress_base, ax=ax6)
    fig6.savefig("output/plots/6_uncertainty_analysis.png")
    
    print("Analysis complete! Plots saved to output/plots/")
    
    if not args.no_show:
        plt.show()

if __name__ == "__main__":
    main()
