from collections import deque
import heapq

def bfs(problem):
    frontier = deque([problem.initial_state])
    came_from = {problem.initial_state: None}

    while frontier:
        current = frontier.popleft()

        if problem.goal_test(current):
            return reconstruct_path(came_from, current)

        for action in problem.actions(current):
            next_state = problem.result(current, action)
            if next_state not in came_from:
                frontier.append(next_state)
                came_from[next_state] = current

    return None

def manhattan_distance(state, goal_states):
    x1, y1 = state
    return min(abs(x1 - x2) + abs(y1 - y2) for x2, y2 in goal_states)

def euclidean_distance(state, goal_states):
    x1, y1 = state
    return min(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 for x2, y2 in goal_states)
def dfs(problem):
    stack = [problem.initial_state]
    came_from = {problem.initial_state: None}
    visited = set()

    while stack:
        current = stack.pop()

        if problem.goal_test(current):
            path = reconstruct_path(came_from, current)
            print(f"DFS encontró la meta en {len(path)} pasos.")
            return path
        if current in visited:
            continue
        visited.add(current)
        next_states = []
        for action in problem.actions(current):
            next_state = problem.result(current, action)
            if next_state not in visited and next_state not in came_from:
                next_states.append(next_state)
        next_states.sort(key=lambda state: euclidean_distance(state, problem.goal_states))
        for next_state in reversed(next_states):
            stack.append(next_state)
            came_from[next_state] = current  

    return None


def a_star(problem, heuristic):
    frontier = []
    heapq.heappush(frontier, (0, problem.initial_state))
    came_from = {problem.initial_state: None}
    cost_so_far = {problem.initial_state: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if problem.goal_test(current):
            return reconstruct_path(came_from, current)

        for action in problem.actions(current):
            next_state = problem.result(current, action)
            new_cost = cost_so_far[current] + problem.step_cost(current, action, next_state)

            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + heuristic(next_state, problem.goal_states)
                heapq.heappush(frontier, (priority, next_state))
                came_from[next_state] = current

    return None

def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)  
    path.reverse()  
    return path

