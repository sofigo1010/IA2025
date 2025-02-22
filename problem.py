from abc import ABC, abstractmethod

class Problem(ABC):
    def __init__(self, initial_state, goal_states):
        self.initial_state = initial_state
        self.goal_states = goal_states

    @abstractmethod
    def actions(self, state):
        pass

    @abstractmethod
    def result(self, state, action):
        pass

    @abstractmethod
    def goal_test(self, state):
        pass

    @abstractmethod
    def step_cost(self, state, action, next_state):
        pass
