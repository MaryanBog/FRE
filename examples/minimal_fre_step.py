"""
Minimal conceptual FRE 2.0 step — standalone example.

This example demonstrates the structural update rule:
    Δ -> E(Δ) -> Δ_{t+1}
with simple surrogate definitions for Φ and κ.

It does NOT depend on FRE Simulator and does not require any packages.
"""

import math


# ---------------------------------------------------------
# Structural state X = (Δ, Φ, M, κ)
# ---------------------------------------------------------

state = {
    "delta": 0.35,      # structural deviation
    "phi":   0.12,      # structural energy
    "M":     0.04,      # memory (irreversible load)
    "kappa": 0.82,      # contractivity (>= 0 means viable)
}


# ---------------------------------------------------------
# Simple contraction operator in Δ-space (conceptual FRE)
# ---------------------------------------------------------

def E(delta, k=0.4):
    """
    FRE contraction operator:
        Δ_{t+1} = k * Δ_t
    where 0 < k < 1 ensures contraction.
    """
    return k * delta


# ---------------------------------------------------------
# One update step
# ---------------------------------------------------------

def step(state):
    delta_prev = state["delta"]

    # operator action
    delta_new = E(delta_prev, k=0.4)

    # FXI surrogate: FXI = 1 + α⋅Δ
    alpha = 0.5
    fxi = 1.0 + alpha * delta_new

    # update structural components
    state["delta"] = delta_new
    state["phi"]   = delta_new ** 2          # simple proxy for structural energy
    state["kappa"] = abs(delta_new / delta_prev)

    return fxi, state


# ---------------------------------------------------------
# Run demonstration
# ---------------------------------------------------------

if __name__ == "__main__":
    print("FRE 2.0 — Minimal Structural Step Demo")
    print("------------------------------------")

    for t in range(10):
        fxi, state = step(state)
        print(
            f"t={t:2d}  Δ={state['delta']:.4f}  "
            f"Φ={state['phi']:.4f}  κ={state['kappa']:.4f}  FXI={fxi:.4f}"
        )
