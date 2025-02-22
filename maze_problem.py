class MazeProblem:
    def __init__(self, grid, initial_state, goal_states):
        self.grid = grid
        self.initial_state = initial_state
        self.goal_states = goal_states

    def actions(self, state):
        x, y = state
        acciones = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]) and self.grid[nx, ny] != 0:
                acciones.append((dx, dy))
        return acciones

    def result(self, state, action):
        x, y = state
        dx, dy = action
        return (x + dx, y + dy)

    def goal_test(self, state):
        return state in self.goal_states
