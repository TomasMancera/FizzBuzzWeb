# Module docstring

from abc import ABC, abstractmethod

class IProblemSolver(ABC):
    """Abstract base class defining methods for solving problems."""

    @abstractmethod
    def compute_results(self, data: list) -> list:
        """
        Computes and returns results for a given list of data.
        Args:
            data (list): The data on which computations are to be performed.
        Returns:
            list: The results of the computations.
        """   
    @abstractmethod
    def calc_one_fb(self, data: any) -> any:
        """
        Calculates and returns a single result based on the given data.

        Args:
            data (any): The data for which a single result is to be calculated.

        Returns:
            any: The result of the calculation.
        """
        