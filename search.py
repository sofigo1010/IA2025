from collections import deque

def bfs(problem):
    frontier = deque([problem.initial_state])
    came_from = {problem.initial_state: None}

    print("Estado inicial:", problem.initial_state)
    print("Estados meta:", problem.goal_states)

    while frontier:
        current = frontier.popleft()
        print("Visitando:", current)

        if problem.goal_test(current):
            print("¡Solución encontrada!")
            return reconstruct_path(came_from, current)

        for action in problem.actions(current):
            next_state = problem.result(current, action)
            if next_state not in came_from:
                frontier.append(next_state)
                came_from[next_state] = current

    print("No se encontró un camino.")
    return None

def reconstruct_path(came_from, current):
    path = []
    while current:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
