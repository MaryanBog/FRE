# tests/test_engine.py
# Basic tests for FRE Simulator V2.0 engine behaviour.

import math

from fre_simulator import (
    initial_state,
    DefaultOperator,
    EmptyScenario,
    SingleStepShockScenario,
    StochasticNoiseScenario,
    run_simulation,
)


def _make_default_state(fxi: float = 1.0, delta: float = 0.0):
    """
    Helper: create an admissible initial structural state S0.
    qp, qf, q, w, u are set to positive reasonable defaults.
    """
    return initial_state(
        delta=delta,
        fxi=fxi,
        qp=1.0,
        qf=1.0,
        q=1.0,
        w=1.0,
        u=1.0,
    )


def test_basic_run_no_breach():
    """
    Basic smoke test:
    - empty scenario (no shocks)
    - default operator
    - stable initial state
    Expectation: no breach and all series have length horizon+1.
    """
    S0 = _make_default_state(fxi=1.0, delta=0.0)
    op = DefaultOperator(alpha=0.7)
    scenario = EmptyScenario()

    horizon = 50
    result = run_simulation(
        initial_state=S0,
        operator=op,
        scenario=scenario,
        horizon=horizon,
    )

    assert result.breach_occurred is False
    assert len(result.fxi_series) == horizon + 1
    assert len(result.delta_series) == horizon + 1
    assert len(result.state_series) == horizon + 1
    assert len(result.kappa_series) == horizon + 1
    assert len(result.stability_zones) == horizon + 1

    assert result.kappa_series[0] is None
    for k in result.kappa_series[1:]:
        assert isinstance(k, float)


def test_convergence_toward_equilibrium():
    """
    Contractivity test:
    - start with FXI != 1
    - default operator should move FXI toward 1
    Expectation: |FXI(T) - 1| < |FXI(0) - 1|.
    """
    S0 = _make_default_state(fxi=1.5, delta=0.5)
    op = DefaultOperator(alpha=0.7)
    scenario = EmptyScenario()

    horizon = 20
    result = run_simulation(
        initial_state=S0,
        operator=op,
        scenario=scenario,
        horizon=horizon,
    )

    initial_dev = abs(result.fxi_series[0] - 1.0)
    final_dev = abs(result.fxi_series[-1] - 1.0)

    assert final_dev < initial_dev
    kappas = [k for k in result.kappa_series[1:] if k is not None]
    assert all(k < 1.0 + 1e-9 for k in kappas)


def test_capacity_breach_via_fxi():
    """
    Test capacity breach triggered by FXI limits.

    Logic:
    - Start with an initial FXI far from equilibrium (1.0).
    - Apply a very narrow admissible FXI band.
    - Even after operator correction, FXI remains outside that band.
    - Engine must detect 'fxi-capacity-breach'.
    """
    S0 = _make_default_state(fxi=2.0, delta=1.0)
    op = DefaultOperator(alpha=0.7)
    scenario = EmptyScenario()

    config = {
        "capacity_limits": {
            "delta": 10.0,      # wide delta limit, not important here
            "fxi_min": 0.95,    # very narrow band around 1.0
            "fxi_max": 1.05,
        }
    }

    result = run_simulation(
        initial_state=S0,
        operator=op,
        scenario=scenario,
        horizon=5,
        config=config,
    )

    assert result.breach_occurred is True
    assert result.breach_type == "fxi-capacity-breach"
    assert result.breach_step is not None


def test_single_step_shock_changes_state():
    """
    SingleStepShockScenario test:
    - apply a one-time positive shock to qp at step t0
    - verify qp changes exactly by the given shock at t0.
    """
    S0 = _make_default_state(fxi=1.0, delta=0.0)
    op = DefaultOperator(alpha=0.7)

    t0 = 5
    shock = 0.5
    scenario = SingleStepShockScenario(
        t0=t0,
        qp_shift=shock,
    )

    result = run_simulation(
        initial_state=S0,
        operator=op,
        scenario=scenario,
        horizon=10,
    )

    event_t0 = next(e for e in result.scenario_events if e["t"] == t0)
    assert event_t0["type"] == "scenario"

    before = event_t0["info"]["before"]
    after = event_t0["info"]["after"]

    assert math.isclose(after.qp, before.qp + shock, rel_tol=1e-9)


def test_stochastic_scenario_runs_without_breach():
    """
    StochasticNoiseScenario test:
    - apply small random noise to qp at each time step
    - use a reasonable horizon and broad capacity limits
    Expectation: simulation completes without breach.
    """
    S0 = _make_default_state(fxi=1.0, delta=0.0)
    op = DefaultOperator(alpha=0.7)

    scenario = StochasticNoiseScenario(
        sigma=0.05,
        seed=42,
    )

    config = {
        "capacity_limits": {
            "delta": 2.0,
            "fxi_min": 0.5,
            "fxi_max": 2.0,
        }
    }

    horizon = 100
    result = run_simulation(
        initial_state=S0,
        operator=op,
        scenario=scenario,
        horizon=horizon,
        config=config,
    )

    assert result.breach_occurred is False
    assert len(result.fxi_series) == horizon + 1
