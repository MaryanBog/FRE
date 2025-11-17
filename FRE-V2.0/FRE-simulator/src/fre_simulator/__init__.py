# __init__.py
# Public API for FRE Simulator V2.0

from .state import State, initial_state
from .operators import BaseOperator, DefaultOperator
from .scenarios import (
    BaseScenario,
    EmptyScenario,
    SingleStepShockScenario,
    ProgressiveShockScenario,
    StochasticNoiseScenario
)
from .engine import run_simulation, SimulationResult

__all__ = [
    "State",
    "initial_state",
    "BaseOperator",
    "DefaultOperator",
    "BaseScenario",
    "EmptyScenario",
    "SingleStepShockScenario",
    "ProgressiveShockScenario",
    "StochasticNoiseScenario",
    "run_simulation",
    "SimulationResult",
]
