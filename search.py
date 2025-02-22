from collections import deque
import heapq

from collections import deque

def bfs(problem):
    start = problem.initial_state
    goals = problem.goal_states.copy()

    if len(goals) == 0:
        
        return None, None
    elif len(goals) == 1:
        
        path1 = find_path_bfs(problem, start, goals[0])
        return path1, None  
    elif len(goals) > 1:
        

        first_goal = min(goals, key=lambda goal: manhattan_distance(start, [goal]))
        goals.remove(first_goal) 


        second_goal = goals[0]

        path1 = find_path_bfs(problem, start, first_goal)
        path2 = find_path_bfs(problem, start, second_goal)

        return path1, path2


def find_path_bfs(problem, start, goal):
    frontier = deque([(start, [])])
    came_from = {start: None}

    while frontier:
        current, path = frontier.popleft()
        if current == goal:
            return path + [current]

        for action in problem.actions(current):
            next_state = problem.result(current, action)
            if next_state not in came_from:
                frontier.append((next_state, path + [current]))
                came_from[next_state] = current

    return None


def manhattan_distance(state, goal_states):
    x1, y1 = state
    return min(abs(x1 - x2) + abs(y1 - y2) for x2, y2 in goal_states)

""" Justificación
Se utiliza cuando el movimiento permitido es únicamente en direcciones ortogonales (arriba, abajo, izquierda, derecha).
Es adecuada para laberintos en grilla donde no se permite moverse en diagonal.
Es admisible (nunca sobreestima el costo real) y consistente (cumple la desigualdad triangular), garantizando que A* encuentra el camino óptimo. """

def euclidean_distance(state, goal_states):
    x1, y1 = state
    return min(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 for x2, y2 in goal_states)

""" Justificación
Se usa cuando el movimiento permitido incluye diagonales, lo que hace que las distancias reales sean más parecidas a una línea recta.
Es ideal para entornos donde los movimientos no están restringidos a una grilla ortogonal.
Es admisible, ya que nunca sobreestima el costo real del camino. """



def dfs(problem):
    start = problem.initial_state
    goals = problem.goal_states.copy()

    if len(goals) == 0:
        
        return None, None
    elif len(goals) == 1:
        
        path1 = find_path_dfs(problem, start, goals[0])
        return path1, None
    elif len(goals) > 1:
        

        first_goal = min(goals, key=lambda goal: euclidean_distance(start, [goal]))
        goals.remove(first_goal)  

        second_goal = goals[0]

        path1 = find_path_dfs(problem, start, first_goal)
        path2 = find_path_dfs(problem, start, second_goal)

        return path1, path2
def find_path_dfs(problem, start, goal):
    stack = [(start, [])]
    came_from = {start: None}
    visited = set()

    while stack:
        current, path = stack.pop()

        if current == goal:
            return path + [current]

        if current in visited:
            continue
        visited.add(current)

        next_states = []
        for action in problem.actions(current):
            next_state = problem.result(current, action)
            if next_state not in visited and next_state not in came_from:
                next_states.append(next_state)

        next_states.sort(key=lambda state: euclidean_distance(state, [goal]))
        for next_state in reversed(next_states):
            stack.append((next_state, path + [current]))
            came_from[next_state] = current  

    return None


def a_star(problem, heuristic):
    start = problem.initial_state
    goals = problem.goal_states.copy()

    if len(goals) == 0:
        
        return None, None
    elif len(goals) == 1:
        
        path1 = find_path_a_star(problem, start, goals[0], heuristic)
        return path1, None
    elif len(goals) > 1:
       


        first_goal = min(goals, key=lambda goal: heuristic(start, [goal]))
        goals.remove(first_goal) 

        second_goal = goals[0]

        path1 = find_path_a_star(problem, start, first_goal, heuristic)
        path2 = find_path_a_star(problem, start, second_goal, heuristic)

        return path1, path2





def find_path_a_star(problem, start, goal, heuristic):
    frontier = []
    heapq.heappush(frontier, (0, start, []))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current, path = heapq.heappop(frontier)

        if current == goal:
            return path + [current]

        for action in problem.actions(current):
            next_state = problem.result(current, action)
            new_cost = cost_so_far[current] + 1  

            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + heuristic(next_state, [goal])
                heapq.heappush(frontier, (priority, next_state, path + [current]))
                came_from[next_state] = current

    return None


def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)  
    path.reverse()  
    return path

