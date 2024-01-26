# task_interface.py
from abc import ABC, abstractmethod


class Task(ABC):
    @abstractmethod
    def get_plot(self):
        pass

