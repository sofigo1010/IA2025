import numpy as np
from problem import Problem

class MazeProblem(Problem):
    def __init__(self, maze):
        self.maze = maze
        self.rows, self.cols = maze.shape
        self.initial_state, self.goal_states = self._find_positions()
        super().__init__(self.initial_state, self.goal_states)

    def _find_positions(self):
        start = None
        goals = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i, j] == 2:
                    start = (i, j)
                elif self.maze[i, j] == 3:
                    goals.append((i, j))
        return start, goals

    def actions(self, state):
        i, j = state
        possible_actions = []
        moves = {
            "UP": (i - 1, j),
            "DOWN": (i + 1, j),
            "LEFT": (i, j - 1),
            "RIGHT": (i, j + 1)
        }

        for action, (x, y) in moves.items():
            if 0 <= x < self.rows and 0 <= y < self.cols and self.maze[x, y] != 0:
                possible_actions.append(action)

        return possible_actions

    def result(self, state, action):
        i, j = state
        if action == "UP":
            return (i - 1, j)
        elif action == "DOWN":
            return (i + 1, j)
        elif action == "LEFT":
            return (i, j - 1)
        elif action == "RIGHT":
            return (i, j + 1)
        return state

    def goal_test(self, state):
        return state in self.goal_states

    def step_cost(self, state, action, next_state):
        return 1
