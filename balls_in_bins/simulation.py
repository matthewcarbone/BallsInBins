from collections import Counter

from monty.json import MSONable
import numpy as np
from scipy.special import comb


def analytic_collisions(N, M):
    """Gets the predicted number of collisions by the analytic formula of
    (N choose 2) / M.

    Parameters
    ----------
    N : int
        The number of balls.
    M : int
        The number of bins.

    Returns
    -------
    float
    """

    return comb(N, 2) / M


def analytic_empty_bins(N, M):
    """Gets the predicted number of empty bins given N balls and M bins.

    Parameters
    ----------
    N : int
        The number of balls.
    M : int
        The number of bins.

    Returns
    -------
    float
    """

    return M * (1.0 - 1.0 / M) ** N


class Simulation(MSONable):
    """A simulation of throwing ``N`` distinguishable balls in to ``M``
    distinguishable bins."""

    @classmethod
    def new(cls, M):
        """Creates a new instance of the Simulation class with zero balls
        in each bin using ``N`` bins.

        Parameters
        ----------
        M : int
            The number of bins.

        Returns
        -------
        Simulation
        """

        return cls(bins=np.array([0 for _ in range(M)]))

    @property
    def bins(self):
        return self._bins

    @property
    def collisions(self):
        """Gets the total number of collisions in the bins. A collision is
        defined as a unique pairing of balls in the same bin. For example,
        three balls in the same bin will produce three collisions. Two balls
        in the same bin will produce only a single collision.

        Returns
        -------
        int
        """

        return (self._bins * (self._bins - 1.0) / 2.0).sum().astype(int)

    @property
    def empty_bins(self):
        """Gets the total number of empty bins."""

        return len(np.where(self._bins == 0)[0])

    def __init__(self, bins):
        """Note: init is not designed to be called by humans. Use the ``new``
        classmethod."""

        self._bins = bins

    def throw_balls_(self, n_balls):
        """Throws ``n_balls`` into the predefined bins in a uniform random
        fashion.

        Parameters
        ----------
        n_balls : int
            The number of balls to throw.
        """

        new_balls = np.random.randint(
            low=0, high=len(self._bins), size=n_balls
        ).tolist()

        counter = Counter(new_balls)

        # TODO: Slow in Python! Might want to code this in C++ for fun!
        for key, value in counter.items():
            self._bins[key] += value
