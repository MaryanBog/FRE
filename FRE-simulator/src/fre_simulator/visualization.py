# visualization.py
# Plotting utilities for FRE Simulator V2.0
# Provides FXI, Δ, stability zone and combined trajectory visualization.

import matplotlib.pyplot as plt
from typing import Optional

from .engine import SimulationResult


def plot_fxi(result: SimulationResult,
             figsize=(10, 4),
             title: Optional[str] = "FXI Trajectory"):
    """
    Plot FXI(t) over time.
    """
    plt.figure(figsize=figsize)
    plt.plot(result.fxi_series, linewidth=2)
    plt.axhline(1.0, color="gray", linestyle="--", linewidth=1)
    plt.title(title)
    plt.xlabel("t")
    plt.ylabel("FXI(t)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_delta(result: SimulationResult,
               figsize=(10, 4),
               title: Optional[str] = "Δ (delta) Trajectory"):
    """
    Plot Δ(t) over time.
    """
    plt.figure(figsize=figsize)
    plt.plot(result.delta_series, linewidth=2, color="orange")
    plt.axhline(0.0, color="gray", linestyle="--", linewidth=1)
    plt.title(title)
    plt.xlabel("t")
    plt.ylabel("Δ(t)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_stability_zones(result: SimulationResult,
                         figsize=(10, 3),
                         title: Optional[str] = "Stability Zones"):
    """
    Visualize stability zones as colored segments.
    stable    -> green
    stressed  -> yellow
    critical  -> red
    """
    colors = {
        "stable": "green",
        "stressed": "gold",
        "critical": "red"
    }

    zone_color_series = [colors[z] for z in result.stability_zones]

    plt.figure(figsize=figsize)
    plt.bar(range(len(zone_color_series)),
            [1] * len(zone_color_series),
            color=zone_color_series,
            width=1.0)

    plt.title(title)
    plt.xlabel("t")
    plt.yticks([])  # zone bar only
    plt.tight_layout()
    plt.show()


def plot_combined(result: SimulationResult,
                  figsize=(12, 8),
                  title: Optional[str] = "FRE Combined Visualization"):
    """
    Combined dashboard:
        - FXI(t)
        - Δ(t)
        - stability zones
    """
    fig, axs = plt.subplots(3, 1, figsize=figsize, sharex=True)

    # FXI
    axs[0].plot(result.fxi_series, linewidth=2)
    axs[0].axhline(1.0, color="gray", linestyle="--", linewidth=1)
    axs[0].set_title("FXI(t)")
    axs[0].grid(True, alpha=0.3)

    # Δ
    axs[1].plot(result.delta_series, linewidth=2, color="orange")
    axs[1].axhline(0.0, color="gray", linestyle="--", linewidth=1)
    axs[1].set_title("Δ(t)")
    axs[1].grid(True, alpha=0.3)

    # Stability zones
    colors = {
        "stable": "green",
        "stressed": "gold",
        "critical": "red"
    }
    zone_color_series = [colors[z] for z in result.stability_zones]

    axs[2].bar(range(len(zone_color_series)),
               [1] * len(zone_color_series),
               color=zone_color_series,
               width=1.0)
    axs[2].set_title("Stability Zones")
    axs[2].set_yticks([])

    plt.suptitle(title)
    plt.tight_layout()
    plt.show()
