import numpy as np
import pytest
from scipy.stats import sem  # Standard Error in the Mean (SEM)

from balls_in_bins.simulation import (
    Simulation,
    analytic_collisions,
    analytic_empty_bins,
)


def test_simulation_simple_examples():
    """Test a simple example!"""

    n_bins = 1
    n_balls = 3
    simulation = Simulation.new(n_bins)
    simulation.throw_balls_(n_balls)
    assert simulation.bins[0] == 3
    assert simulation.collisions == 3


def test_simulation_stress():
    """Runs simple stress tests of the Simulation class."""

    np.random.seed(123)
    for n_bins in range(10, 100, 10):
        for n_balls in range(1, 20, 3):
            for _ in range(10):
                simulation = Simulation.new(n_bins)
                simulation.throw_balls_(n_balls)
                assert n_balls == simulation.bins.sum()


BALLS_N_BINS_COMBOS = [(3, 4), (10, 3), (5, 50), (54, 7), (8, 8)]


@pytest.mark.parametrize("n_balls,n_bins", BALLS_N_BINS_COMBOS)
def test_simulation_collisions(n_balls, n_bins):
    np.random.seed(123)
    _num = []
    for _ in range(20000):
        simulation = Simulation.new(n_bins)
        simulation.throw_balls_(n_balls)
        _num.append(simulation.collisions)
    num = np.mean(_num)
    num_sem = sem(_num)
    lower_bound = num - num_sem * 2.0  # ~97% confidence interval
    upper_bound = num + num_sem * 2.0
    ana = analytic_collisions(n_balls, n_bins)
    assert lower_bound < ana < upper_bound


@pytest.mark.parametrize("n_balls,n_bins", BALLS_N_BINS_COMBOS)
def test_simulation_empty_bins(n_balls, n_bins):
    np.random.seed(123)
    _num = []
    for _ in range(20000):
        simulation = Simulation.new(n_bins)
        simulation.throw_balls_(n_balls)
        _num.append(simulation.empty_bins)
    num = np.mean(_num)
    num_sem = sem(_num)
    lower_bound = num - num_sem * 2.0  # ~97% confidence interval
    upper_bound = num + num_sem * 2.0
    ana = analytic_empty_bins(n_balls, n_bins)
    assert lower_bound < ana < upper_bound
