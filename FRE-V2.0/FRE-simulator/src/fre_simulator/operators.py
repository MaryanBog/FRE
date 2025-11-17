# operators.py
# Corrective operators for FRE Simulator V2.0
# Implements FXI update rules, contractivity κ, and operator base class.

from dataclasses import dataclass


class BaseOperator:
    """
    Abstract corrective operator E for FRE.
    All operators must implement:
      - apply(fxi): returns next FXI value
      - kappa(prev_fxi, next_fxi): computes contractivity coefficient κ
    """

    def apply(self, fxi: float) -> float:
        raise NotImplementedError("Operator must implement apply()")

    def kappa(self, prev_fxi: float, next_fxi: float) -> float:
        """
        Contractivity measure:
            κ = |FXI(t+1) − 1| / |FXI(t) − 1|
        """
        numerator = abs(next_fxi - 1.0)
        denominator = abs(prev_fxi - 1.0)
        if denominator == 0:
            # we are exactly at equilibrium — contractivity is irrelevant
            return 0.0
        return numerator / denominator


@dataclass
class DefaultOperator(BaseOperator):
    """
    Default corrective operator for FRE Simulator.
    Implements a simple linear contraction toward equilibrium:
        FXI(t+1) = 1 + α ⋅ (FXI(t) − 1)
    where 0 < α < 1 ensures contractivity.

    This is a placeholder baseline operator.
    More advanced nonlinear operators will be added later.
    """
    alpha: float = 0.7  # contraction strength (default moderate correction)

    FXI_MIN = 0.1
    FXI_MAX = 5.0

    def apply(self, fxi: float) -> float:
        """
        Apply contraction:
            next_fxi = 1 + α * (fxi − 1)
        """
        next_fxi = 1.0 + self.alpha * (fxi - 1.0)

        # enforce admissible range
        if next_fxi < self.FXI_MIN:
            next_fxi = self.FXI_MIN
        if next_fxi > self.FXI_MAX:
            next_fxi = self.FXI_MAX

        return next_fxi
