## 1. Purpose

The FRE Simulator V2.0 provides a practical execution environment for the Flexionization
Risk Engine (FRE) Version 2.0. Its purpose is to reproduce FRE structural dynamics
step-by-step in a controlled and transparent manner.

The simulator focuses on the following tasks:

- executing the FRE evolution rule for Δ / Δ⃗ and FXI;
- testing corrective operators \(E\) under deterministic and stochastic conditions;
- validating contractivity, boundedness, and stability properties;
- running reproducible stress tests;
- generating numerical and visual outputs for analysis.

The simulator does **not**:
- define new theory,
- alter FRE 2.0 rules,
- or introduce any model-specific logic.

Its only role is to execute FRE 2.0 **exactly as specified**, and provide traceable,
diagnosable results for research, testing, and integration workflows.

---

## 2. Theoretical Basis (Short Reference)

The FRE Simulator V2.0 follows the mathematical rules defined in the **FRE Risk Engine
Specification V2.0**.  
This section provides only a minimal reference to the theoretical elements required for
executing the simulation. The full theory is described in the specification and is not
duplicated here.

### 2.1 Deviation (Δ or Δ⃗)
The deviation represents the structural imbalance of the system.  
It is computed from the State object at each step.

### 2.2 Equilibrium Indicator (FXI)
FXI is a scalar measure of structural equilibrium:
- FXI > 1 — expanded state  
- FXI < 1 — compressed state  
- FXI = 1 — perfect symmetry  

### 2.3 Corrective Operator (E or E⃗)
The operator defines the next-step target deviation:
\[
\Delta_{t+1} = E(\Delta_t)
\]

The operator must be:
- continuous,  
- bounded,  
- contraction-seeking,  
- consistent with FRE dynamics.

### 2.4 Evolution Rule
The simulator implements the formal FRE transition:
\[
F(S_{t+1}) = E(F(S_t))
\]

### 2.5 Role of the Simulator
The simulator does **not** modify any FRE formulas.  
It simply:
- evaluates Δ and FXI,
- applies the operator E,
- steps the state forward,
- records all outputs.

This short reference provides the theoretical minimum required to understand how the simulator
executes FRE 2.0 dynamics.

---

## 3. Project Structure

The FRE Simulator V2.0 is implemented as a modular Python package, organized to separate
core logic, scenarios, operators, and visualization tools.  
This structure ensures clarity, extensibility, and a direct mapping to the FRE 2.0 model.

```
FRE-simulator/
├── README.md
├── requirements.txt
├── notebooks/
│   └── FRE-Simulator-V2.0-demo.ipynb
└── src/
    └── fre_simulator/
        ├── __init__.py
        ├── state.py
        ├── operators.py
        ├── scenarios.py
        ├── engine.py
        └── visualization.py
```

### 3.1 Module Overview

- **state.py**  
  Defines the State model, deviation calculation, FXI evaluation, and admissibility checks.

- **operators.py**  
  Contains corrective operators \(E\), contractivity utilities, and FXI update logic.

- **scenarios.py**  
  Provides deterministic, stochastic, and composite scenario classes.

- **engine.py**  
  Implements the FRE evolution loop, step-by-step state transitions, and diagnostics.

- **visualization.py**  
  Provides plotting and export functions for trajectories and stability zones.

### 3.2 Design Principles

- **Modularity** — each component has a single responsibility.  
- **Traceability** — every step of evolution is logged and reproducible.  
- **Consistency** — the structure mirrors FRE 2.0 concepts directly.  
- **Extensibility** — custom operators and scenarios can be added without modifying core code.

This project structure forms the foundation for all simulation capabilities.

---

### 3.3 docs/ directory

The `docs/` folder contains all documentation files related to the simulator.  
This includes:

- `FRE-V2.0-Simulator-Documentation.md` — the main user documentation  
- `FRE-2.0-Test-Suite.md` — internal validation and test design notes  

These documents describe simulator behavior, reference examples, and development notes.

---

## 4. Core Components

The FRE Simulator V2.0 is built around a small set of modular components that correspond
directly to FRE 2.0 concepts. Each component performs one clearly defined function and can
be extended or replaced without modifying the rest of the system.

### 4.1 State
Represents the complete structural snapshot of the system at a single time step.
Responsible for:
- storing Δ / Δ⃗ values,
- storing FXI,
- holding κ (contractivity),
- encoding the stability zone,
- providing data for the operator and engine.

### 4.2 Operators (E)
Corrective operators implement the FRE update rule:
\[
\Delta_{t+1} = E(\Delta_t)
\]
They:
- compute next-step Δ / Δ⃗,
- update FXI,
- enforce bounded, continuous corrections,
- return diagnostics used by the engine.

Operators are fully modular and may be swapped or customized.

### 4.3 Scenarios
Scenarios apply external effects before each FRE step.
Used for:
- deterministic shocks,
- stochastic noise,
- combined stress sequences,
- structural parameter changes.

Scenarios modify the state **before** the operator is applied.

### 4.4 Engine
The central executor of FRE evolution.
Handles:
- scenario execution,
- Δ and FXI calculation,
- operator application,
- κ and zone computation,
- constructing the next State,
- logging all steps.

### 4.5 Visualization
Optional tools for plotting and exporting results, including:
- FXI trajectories,
- Δ trajectories,
- κ history,
- stability zones,
- stress overlays.

### 4.6 Result Object
The final output of the simulation, containing:
- FXI series,
- Δ series,
- κ series,
- zone labels,
- all State instances,
- export utilities (CSV/JSON/PNG).

Together, these components form the complete FRE simulation workflow.

---

## 5. Installation & Environment

The FRE Simulator V2.0 is implemented in Python and runs on any standard environment with
basic scientific packages. No GPU or specialized hardware is required.

### 5.1 Requirements

- Python 3.9+
- NumPy
- Matplotlib
- Packages listed in `requirements.txt`

### 5.2 Installation

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

This prepares all modules under `src/fre_simulator/` for import.

### 5.3 Environment Notes

- Works in scripts, terminals, and Jupyter notebooks.
- All computations are CPU-based and lightweight.
- No hidden dependencies or external services.
- Deterministic execution unless a scenario injects randomness.

### 5.4 Import Structure

All components can be imported as:

```python
from fre_simulator.state import State
from fre_simulator.operators import DefaultOperator
from fre_simulator.scenarios import EmptyScenario
from fre_simulator.engine import Simulator
```

The simulator is ready immediately after installation.

---

### 5.5 requirements.txt

The file `requirements.txt` lists the exact dependency versions used during development.

To install dependencies directly:

```bash
pip install -r requirements.txt
```

This ensures full reproducibility of the environment.

---

## 6. Quickstart Example

This example demonstrates how to run a minimal FRE V2.0 simulation using the default
corrective operator and an empty scenario. It is the recommended starting point for all
tests and experiments.

### 6.1 Minimal Script

```python
from fre_simulator.state import State
from fre_simulator.operators import DefaultOperator
from fre_simulator.scenarios import EmptyScenario
from fre_simulator.engine import Simulator

# Step 1 — initial state
initial_state = State(
    fxi=1.12,    # initial FXI
    delta=0.24   # initial deviation
)

# Step 2 — corrective operator
operator = DefaultOperator()

# Step 3 — scenario (no external effects)
scenario = EmptyScenario()

# Step 4 — simulator
sim = Simulator(
    initial_state=initial_state,
    operator=operator,
    scenario=scenario,
    horizon=20
)

# Step 5 — run simulation
result = sim.run()

# Step 6 — access output
print(result.fxi_series)
print(result.delta_series)
print(result.zones)
```

### 6.2 What Happens in This Example

This script:
1. Creates the initial structural state.  
2. Applies the default operator \(E\).  
3. Uses an empty scenario (pure FRE dynamics).  
4. Runs 20 steps of the FRE evolution loop.  
5. Outputs FXI, Δ, and stability zone history.

This is the simplest template for building custom simulations, stress tests, and validation workflows.

### 6.3 Full Example Script (example_simulation.py)

The repository includes a ready-to-run example located at:

```
example_simulation.py
```

This script demonstrates:

- importing simulator modules,
- constructing the initial State,
- selecting an operator,
- running a full FRE 2.0 evolution loop,
- printing FXI and Δ trajectories.

It serves as a complete standalone reference for users who want to run the simulator
without modifying any code.

---

## 7. State, Operators, and Scenarios

This section describes the three functional elements that define how the FRE Simulator V2.0
represents system structure (State), applies corrective dynamics (Operators), and introduces
external influences (Scenarios).

### 7.1 State

The `State` object represents a full snapshot of the system at a single simulation step.

It contains:
- **fxi** — equilibrium indicator FXI  
- **delta** — deviation (scalar or vector)  
- **kappa** — contractivity factor  
- **zone** — stability classification  
- **meta** — optional additional data injected by scenarios  

Responsibilities:
- compute Δ / Δ⃗,
- compute FXI,
- validate admissibility,
- store diagnostics for logging and visualization.

A new `State` is created at every simulation step.

---

### 7.2 Operators (E)

Corrective operators implement the FRE update rule:
\[
\Delta_{t+1} = E(\Delta_t)
\]

Operators:
- compute the next Δ / Δ⃗,
- update FXI,
- calculate κ (contractivity),
- ensure corrections are bounded and continuous,
- return diagnostics for the engine.

Example:

```python
from fre_simulator.operators import DefaultOperator
operator = DefaultOperator()
```

Custom operators can be created by subclassing the base operator class.

---

### 7.3 Scenarios

Scenarios apply controlled external effects **before** the FRE corrective step.

They are used to simulate:
- deterministic shocks,
- stochastic noise,
- parameter shifts,
- multi-step stress sequences.

Example:

```python
from fre_simulator.scenarios import EmptyScenario
scenario = EmptyScenario()
```

Scenarios do **not** modify the FRE rules — they only adjust the input to the evolution
loop, enabling stress testing, randomness, and parameter experiments.

---

Together, the State, Operators, and Scenarios define the full behavior of each simulation
step within the FRE Simulator V2.0.

---

## 8. Simulation Engine

The Simulation Engine is the core executor of FRE dynamics. It processes scenarios,
evaluates the structural state, applies the corrective operator, and logs each step of
the evolution according to the FRE 2.0 specification.

### 8.1 Responsibilities

The engine performs the following tasks on every step:

1. **Apply scenario effects**  
   Modifies the current State before FRE dynamics are applied.

2. **Compute Δ / Δ⃗ and FXI**  
   Using the State module.

3. **Apply the corrective operator \(E\)**  
   Produces the next-step deviation, updated FXI, κ, and diagnostics.

4. **Create next State**  
   A new State object is generated to represent step \(t+1\).

5. **Record results**  
   All metrics (FXI, Δ, κ, zones) are logged into a trajectory.

6. **Repeat until horizon**  
   The loop continues for the defined number of steps.

---

### 8.2 Simulator Class

The engine is accessed through the `Simulator` class:

```python
from fre_simulator.engine import Simulator

sim = Simulator(
    initial_state=state,
    operator=operator,
    scenario=scenario,
    horizon=40
)

result = sim.run()
```

Parameters:
- **initial_state** — starting State  
- **operator** — corrective operator \(E\)  
- **scenario** — external effects  
- **horizon** — number of steps to simulate  

---

### 8.3 Execution Flow

Step-by-step:

```
current_state
    → apply scenario
    → compute Δ, FXI
    → operator.apply()
    → compute κ and stability zone
    → build next_state
    → append to log
```

This flow strictly follows FRE 2.0 rules and ensures deterministic behavior.

---

### 8.4 Diagnostics and Consistency

At each step, the engine computes:
- FXI,
- Δ / Δ⃗,
- κ,
- stability zone,
- admissibility flags.

It validates:
- operator output,
- domain boundaries,
- numerical stability,
- continuity of evolution.

Violations produce clear errors to prevent invalid trajectories.

---

### 8.5 Determinism

The simulation engine guarantees:
- repeatable trajectories,
- no randomness unless introduced by scenarios,
- consistent execution across environments.

It is the authoritative implementation of FRE evolution in code.

---

## 9. Output & Visualization

After a simulation run completes, the engine returns a `SimulationResult` object containing
all recorded values, diagnostics, and utilities for exporting or visualizing the trajectory.
This section describes what is produced and how it can be displayed.

---

### 9.1 SimulationResult Structure

The result object includes:

- **fxi_series** — FXI values per step  
- **delta_series** — Δ or Δ⃗ trajectory  
- **kappa_series** — κ (contractivity) history  
- **zones** — stability zone labels  
- **states** — full list of State objects  
- **meta** — optional scenario/operator metadata  

Every list includes all steps from \(t = 0\) to the final horizon.

---

### 9.2 Accessing Output

Example:

```python
print(result.fxi_series)
print(result.delta_series)
print(result.zones)
print(result.kappa_series)
```

These values can be used for debugging, testing, or analysis.

---

### 9.3 Exporting Results

The simulator supports exporting results to:

- **CSV** — numeric tables  
- **JSON** — full trajectory including state data  
- **PNG** — plots via visualization module  

Example:

```python
result.to_csv("run.csv")
result.to_json("run.json")
```

---

### 9.4 Visualization Tools

The `visualization.py` module offers functions for plotting:

- FXI trajectories  
- Δ / Δ⃗ evolution  
- κ history  
- stability zones  
- stress/shock markers  

Example:

```python
from fre_simulator.visualization import plot_fxi, plot_delta

plot_fxi(result)
plot_delta(result)
```

These functions automatically read the `SimulationResult`.

---

### 9.5 Combined Views

The visualization system supports overlays such as:

- FXI curve + zone coloring  
- Δ curve + shock events  
- κ curve + threshold bands  

These views help understand stability behavior and operator performance.

---

### 9.6 Recommended Workflow

1. Run the simulation.  
2. Inspect numeric output (FXI, Δ, κ, zones).  
3. Generate plots to validate correctness visually.  
4. Compare trajectories across scenarios or operators.

This combination of numeric and visual output provides a complete analysis toolkit for FRE dynamics.

---

## 10. Reference Example: Stress Test 1

This section provides a canonical reference simulation (“Stress Test 1”).  
It serves as the baseline example for validating that the FRE Simulator V2.0 correctly
implements core FRE evolution rules.

This example uses no scenarios and the default operator, ensuring pure FRE dynamics.

---

### 10.1 Configuration

- **Horizon:** 20 steps  
- **Initial FXI:** 1.1275  
- **Initial Δ:** 0.2550  
- **Operator:** DefaultOperator  
- **Scenario:** EmptyScenario  

This configuration corresponds exactly to the official FRE 2.0 demonstration run.

---

### 10.2 Output Table

```
FRE 2.0 Example Simulation (Reference)
=====================================
Horizon: 20 steps
Initial FXI: 1.1275, Initial Delta: 0.2550

  t |      FXI |    Delta |   kappa |   Zone
--------------------------------------------
  0 |   1.1275 |   0.2550 |    n/a  | critical
  1 |   1.0510 |   0.1020 |  0.4000 | stressed
  2 |   1.0204 |   0.0408 |  0.4000 | stressed
  3 |   1.0082 |   0.0163 |  0.4000 | stable
  4 |   1.0033 |   0.0065 |  0.4000 | stable
  5 |   1.0949 |   0.1898 |    ...  |   ...
```

(Full table may be included or referenced externally depending on file size.)

---

### 10.3 Reproducing the Run

```python
from fre_simulator.state import State
from fre_simulator.operators import DefaultOperator
from fre_simulator.scenarios import EmptyScenario
from fre_simulator.engine import Simulator

state = State(fxi=1.1275, delta=0.2550)
operator = DefaultOperator()
scenario = EmptyScenario()

sim = Simulator(
    initial_state=state,
    operator=operator,
    scenario=scenario,
    horizon=20
)

result = sim.run()
```

This code produces the exact reference trajectory above.

---

### 10.4 Purpose of the Reference Test

Stress Test 1 is used to:

- verify that all FRE evolution rules are applied correctly;  
- test contractivity and stability zone transitions;  
- ensure consistent Δ and FXI progression;  
- detect errors in operator implementation;  
- serve as a benchmark for future development.

It is the **official baseline** for FRE Simulator V2.0 correctness.

---

### 10.5 Interpretation

This example demonstrates:

- smooth contraction toward equilibrium,  
- correct FXI → Δ mapping,  
- stable zone transitions (critical → stressed → stable),  
- absence of discontinuities or divergence,  
- strict adherence to FRE 2.0 dynamics.

It is the final validation step confirming that the simulator is functioning as intended.

---

## Development Notes (Internal)

### run_tests.py

The repository includes an internal test runner:

```
run_tests.py
```

Running this script executes the automated validation suite to verify:

- correctness of the FRE evolution loop,
- stability zone classification,
- contractivity logic,
- consistency of operators and scenarios.

Usage:

```bash
python run_tests.py
```

This script is intended for developers and contributors to ensure that
modifications to the simulator do not break FRE 2.0 compliance.

---

### Test Suite

The repository includes a test suite located in:

```
tests/
```

It contains automated checks validating:

- correct operation of the FRE evolution loop  
- stability zone classification  
- contractivity and operator behavior  
- consistency of the resulting trajectory  

Tests can be executed using:

```bash
pytest
```

This suite ensures long-term reliability of the simulator during development.
