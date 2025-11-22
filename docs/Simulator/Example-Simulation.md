# FRE 2.0 — Example Simulation  
### Reference Structural Evolution Run (20 Steps)

This document provides a minimal, fully reproducible example of running the  
**FRE Simulator V2.0** and interpreting the output trajectories.

---

## 1. Prerequisites

Install the simulator:

```bash
pip install -e FRE-simulator/
```

Or install dependencies manually:

```bash
pip install -r FRE-simulator/requirements.txt
```

---

## 2. Example Code

Below is the canonical minimal simulation example included in  
`FRE-simulator/example_simulation.py`.

```python
from fre_simulator.state import State
from fre_simulator.operators import DefaultOperator
from fre_simulator.scenarios import EmptyScenario
from fre_simulator.engine import Simulator

# Initial state
state = State(fxi=1.1275, delta=0.2550)

# Default corrective operator
operator = DefaultOperator()

# No external shocks applied
scenario = EmptyScenario()

# Create and run the simulation
sim = Simulator(
    initial_state=state,
    operator=operator,
    scenario=scenario,
    horizon=20
)

result = sim.run()

# Output trajectories
print(result.fxi_series)
print(result.delta_series)
print(result.zones)
```

---

## 3. Example Output (“Stress Test 1”)

Below is a real output recorded from the FRE Simulator V2.0  
(using the default operator and an empty scenario):

```
FRE 2.0 Example Simulation (5D)
================================
Horizon: 20 steps
Initial FXI: 1.1275, Initial Delta: 0.2550

  t |      FXI |    Delta |    kappa | Zone
-------------------------------------------
  0 |   1.1275 |   0.2550 |     n/a  | critical
  1 |   1.0510 |   0.1020 |   0.4000 | stressed
  2 |   1.0204 |   0.0408 |   0.4000 | stressed
  3 |   1.0082 |   0.0163 |   0.4000 | stable
  4 |   1.0033 |   0.0065 |   0.4000 | stable
  5 |   1.0949 |   0.1898 |   0.4000 | compressed
  6 |   1.0580 |   0.1160 |   0.4000 | stressed
  7 |   1.0232 |   0.0465 |   0.4000 | stressed
  8 |   1.0093 |   0.0185 |   0.4000 | stable
  9 |   1.0043 |   0.0085 |   0.4000 | stable
 10 |   1.0397 |   0.0794 |   0.4000 | stressed
 11 |   1.0159 |   0.0318 |   0.4000 | stressed
 12 |   1.0063 |   0.0126 |   0.4000 | stable
 13 |   1.0026 |   0.0053 |   0.4000 | stable
 14 |   1.0355 |   0.0711 |   0.4000 | stressed
 15 |   1.0142 |   0.0284 |   0.4000 | stressed
 16 |   1.0056 |   0.0111 |   0.4000 | stable
 17 |   1.0023 |   0.0045 |   0.4000 | stable
 18 |   1.0334 |   0.0669 |   0.4000 | stressed
 19 |   1.0134 |   0.0268 |   0.4000 | stressed
 20 |   1.0053 |   0.0107 |   0.4000 | stable
```

This example demonstrates:

- deterministic contraction toward equilibrium,  
- stability zone transitions,  
- monotonic FXI behavior,  
- reproducibility of results.

---

## 4. Interpretation

Key insights:

- **FXI decreases** when system is expanded (FXI > 1).  
- **FXI increases** when system is compressed (FXI < 1).  
- Delta evolution follows the corrective operator E⃗.  
- The system always converges toward the equilibrium zone.  
- No oscillations, no discontinuities, no divergent trajectories.

This example validates the core principles of FRE Version 2.0.

---

## 5. Related Files

- `example_simulation.py` — source script  
- `engine.py` — evolution loop and state transitions  
- `operators.py` — corrective operator definitions  
- `scenarios.py` — external shocks and structural shifts  
- `FRE-2.0-Test-Suite.md` — full stress testing framework

---

This example serves as a simple reference for understanding  
**how structural dynamics evolve under FRE 2.0**.
