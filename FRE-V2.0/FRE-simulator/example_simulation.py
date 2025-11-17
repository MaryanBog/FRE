"""
Example FRE 2.0 simulation run.

- Automatically adds ./src to sys.path
- Uses fre_simulator.engine.run_simulation
- Defines a minimal ExampleState, Operator and Scenario for demonstration
- Does NOT modify or depend on internal State implementation from fre_simulator.state
"""

import sys
import os
from dataclasses import dataclass

# ---------------------------------------------------------
# 1. Add ./src to sys.path so that `import fre_simulator` works
# ---------------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Now we can safely import the simulator engine
from fre_simulator.engine import run_simulation, SimulationResult  # type: ignore


# ---------------------------------------------------------
# 2. Minimal example state compatible with engine.run_simulation
# ---------------------------------------------------------


@dataclass
class ExampleState:
    """
    Minimal stand-alone state object that is compatible with fre_simulator.engine.run_simulation.

    The engine uses:
      - instance attrs:  fxi, delta
      - class attrs:     DELTA_MAX, FXI_MIN, FXI_MAX
      - methods:         validate(), compute_delta(), update_from_operator(new_fxi)
    """

    qp: float      # synthetic mass (примерная структура)
    qf: float      # reference mass
    delta: float   # structural deviation Δ = qp - qf
    fxi: float     # FXI indicator

    # Capacity limits (used as defaults by engine)
    DELTA_MAX: float = 1.0
    FXI_MIN: float = 0.5
    FXI_MAX: float = 1.5

    def validate(self) -> None:
        """
        Simple sanity checks; in реальном проекте тут могут быть более строгие ограничения.
        """
        if not (self.FXI_MIN <= self.fxi <= self.FXI_MAX):
            raise ValueError(f"FXI out of bounds: {self.fxi}")
        if abs(self.delta) > self.DELTA_MAX * 2:
            # оставим запас, чтобы пример не падал слишком агрессивно
            raise ValueError(f"Delta too large: {self.delta}")

    def compute_delta(self) -> None:
        """
        Recompute delta from qp and qf.

        Engine calls this each step:
            state.compute_delta()
        """
        self.delta = self.qp - self.qf

    def update_from_operator(self, new_fxi: float) -> None:
        """
        Update state from operator result.

        Engine calls:
            state.update_from_operator(next_fxi)

        Здесь мы делаем простую игрушечную связь:
            - FXI -> ближе к 1.0
            - Delta привязываем к FXI: чем ближе FXI к 1, тем ближе delta к 0.
        """
        self.fxi = new_fxi

        # Простое линейное соответствие: delta ~ (FXI - 1)
        # Чтобы не вылезать за DELTA_MAX, нормируем.
        self.qp = self.qf + (self.fxi - 1.0) * self.DELTA_MAX
        self.compute_delta()


# ---------------------------------------------------------
# 3. Simple contractive operator E and trivial scenario
# ---------------------------------------------------------


class SimpleContractiveOperator:
    """
    Very simple contractive operator:

        FXI_{t+1} = 1 + k * (FXI_t - 1),  0 < k < 1

    Это даёт геометрическую сходимость FXI -> 1.
    """

    def __init__(self, k: float = 0.4) -> None:
        if not (0.0 < k < 1.0):
            raise ValueError("k must be in (0, 1) for contraction")
        self.k = k

    def apply(self, fxi: float) -> float:
        """
        Called by engine as:
            next_fxi = operator.apply(prev_fxi)
        """
        return 1.0 + self.k * (fxi - 1.0)

    def kappa(self, prev_fxi: float, new_fxi: float) -> float:
        """
        Contraction ratio kappa:

            kappa_t = |FXI_{t+1} - 1| / |FXI_t - 1|

        В идеале ~= k.
        """
        prev_dist = abs(prev_fxi - 1.0)
        new_dist = abs(new_fxi - 1.0)
        if prev_dist == 0:
            return 0.0
        return new_dist / prev_dist


class NoShockScenario:
    """
    Trivial scenario: no external shocks, state is unchanged.

    Engine calls:
        state = scenario.apply(state, t)
    """

    def apply(self, state: ExampleState, t: int) -> ExampleState:
        # Можно добавить стресс, например:
        # if t == 5:
        #     state.qp += 0.2
        #     state.compute_delta()
        return state


# ---------------------------------------------------------
# 4. Run example simulation
# ---------------------------------------------------------


def main() -> None:
    # Initial structural state: небольшой перекос и FXI > 1
    initial_state = ExampleState(
        qp=1.2,      # actual structural mass
        qf=1.0,      # reference mass
        delta=0.2,   # qp - qf
        fxi=1.15,    # slightly expanded state
    )

    operator = SimpleContractiveOperator(k=0.4)
    scenario = NoShockScenario()

    horizon = 20

    result: SimulationResult = run_simulation(
        initial_state=initial_state,
        operator=operator,
        scenario=scenario,
        horizon=horizon,
        config=None,  # используем дефолтные пороги из двигателя
    )

    # ---- Output ----
    print("FRE 2.0 Example Simulation")
    print("==========================")
    print(f"Horizon: {horizon} steps")
    print(
        f"Initial FXI: {result.fxi_series[0]:.4f}, "
        f"Initial Delta: {result.delta_series[0]:.4f}"
    )
    print()

    header = f"{'t':>3} | {'FXI':>8} | {'Delta':>8} | {'kappa':>8} | Zone"
    print(header)
    print("-" * len(header))

    for t, (fxi, delta, kappa, zone) in enumerate(
        zip(
            result.fxi_series,
            result.delta_series,
            result.kappa_series,
            result.stability_zones,
        )
    ):
        kappa_str = f"{kappa:.4f}" if kappa is not None else "   n/a "
        print(f"{t:3d} | {fxi:8.4f} | {delta:8.4f} | {kappa_str:>8} | {zone}")

    print()
    print(f"Breach occurred: {result.breach_occurred}")
    if result.breach_occurred:
        print(f"  Step : {result.breach_step}")
        print(f"  Type : {result.breach_type}")


if __name__ == "__main__":
    main()
