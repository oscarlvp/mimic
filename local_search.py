def random_search(objective, new_solution, iterations=100, initial_solution=None):
    best_solution = initial_solution if initial_solution is not None else new_solution()
    best_value = objective(best_solution)
    for it in range(iterations):
        current_solution = new_solution()
        current_value = objective(current_solution)
        if current_value < best_value:
            best_value, best_solution = current_value, current_solution
    return best_value, best_solution


def hill_climbing(objective, neighbour, evaluations, initial_solution):
    best_solution = initial_solution
    best_value = objective(best_solution)
    for ev in range(1, evaluations):
        current_solution = neighbour(best_solution)
        current_value = objective(current_solution)
        if current_value <= best_value:
            best_solution = current_solution
            best_value = current_value
    return best_value, best_solution
    
def hill_climbing_with_restarts(objective, neighbour, evaluations, neighbourhood_size, new_solution, initial_solution=None):
   
    best_solution = initial_solution if initial_solution is not None else new_solution()
    best_value = objective(best_solution)

    neighbours_explored = 0
    for ev in range(1, evaluations):

        if neighbours_explored >= neighbourhood_size:
            current_solution = new_solution()
            neighbours_explored = 0
        else:
            current_solution = neighbour(best_solution)
            neighbours_explored += 1

        current_value = objective(current_solution)
        if current_value <= best_value:
            best_value, best_solution = current_value, current_solution
            neighbours_explored = 0
    
    return best_value, best_solution
