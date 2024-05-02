from abc import ABC, abstractmethod
from typing import List

class IProblemSolver(ABC):
    @abstractmethod
    def compute_results(self, data: list) -> list:
        pass

    @abstractmethod
    def calc_one_fb(self, data:any) -> any:
        pass