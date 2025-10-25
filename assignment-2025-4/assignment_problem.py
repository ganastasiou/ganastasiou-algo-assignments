import argparse

def initialize_parser():
    parser = argparse.ArgumentParser(description='Problem solving with Hungarian algorithm')
    parser.add_argument('costs_file', help='File that contains the costs')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print detailed steps of the algorithm')
    return parser

def read_and_parse_cost_matrix(file_name):
    cost_matrix = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                live_values_row = get_clean_row_values_from_commas(line)
                cost_matrix.append(live_values_row)
    return cost_matrix

def get_clean_row_values_from_commas(line):
    line_values = line.split(',')
    row_values = []
    for line_value in line_values:
        row_values.append(float(line_value.strip()))
    return row_values

def print_cost_matrix_content(cost_matrix):
    workers_count = len(cost_matrix)
    tasks_count = 0
    if workers_count > 0:
        tasks_count = len(cost_matrix[0])
    
    #header
    print(f"{workers_count}x{tasks_count} cost matrix:")

    for row in cost_matrix:
        formatted_values = []
        for value in row:
            formatted_value = f"{value:4.2f}"
            formatted_values.append(formatted_value)
        line_to_print = " ".join(formatted_values)
        print(line_to_print)

def print_worker_and_task_potentials(worker_potentials, task_potentials):
    formatted_worker_potentials = []
    for worker_potential in worker_potentials:
        formatted_value = f"{worker_potential:4.2f}"
        formatted_worker_potentials.append(formatted_value)

    workers_final_str = " ".join(formatted_worker_potentials)
    print(f"U: [ {workers_final_str} ]")

    formatted_task_potentials = []
    for task_potential in task_potentials:
        formatted_value = f"{task_potential:4.2f}"
        formatted_task_potentials.append(formatted_value)
    tasks_final_str = " ".join(formatted_task_potentials)

    print(f"V: [ {tasks_final_str} ]")

def print_costs_matrix(cost_matrix):
    print("=== Assignment Problem ===")
    print_cost_matrix_content(cost_matrix)
    print()

def print_initial_potentials(worker_initial_potentials, tasks_initial_potential):

    print("Initial potentials:")
    formatted_worker_potentials = []
    for initial_potential in worker_initial_potentials:
        formatted_value = f"{initial_potential:4.2f}"
        formatted_worker_potentials.append(formatted_value)
    final_workers_str = " ".join(formatted_worker_potentials)
    print(f"U: [ {final_workers_str} ]") # U stands for workers

    formatted_task_potentials = []
    for initial_potential in tasks_initial_potential:
        formatted_value = f"{initial_potential:4.2f}"
        formatted_task_potentials.append(formatted_value)
    final_tasks_str = " ".join(formatted_task_potentials)
    print(f"V: [ {final_tasks_str} ]") # V stands for workers
    print()

def get_initial_potentials_for_workers(cost_matrix):
    workers_count = len(cost_matrix)
    tasks_count = len(cost_matrix[0])
    workers = []
    for worker_index in range(workers_count):
        minimum_cost = cost_matrix[worker_index][0]
        for task_index in range(1, tasks_count):
            if cost_matrix[worker_index][task_index] < minimum_cost:
                minimum_cost = cost_matrix[worker_index][task_index]
        workers.append(minimum_cost)
    return workers

def get_initial_potentials_for_tasks(tasks_count):
    tasks = []
    for _ in range(tasks_count):
        tasks.append(0.0)
    return tasks

def get_optimal_matching_with_hungarian_algorithm(cost_matrix, print_verbose=False):
    workers_count = len(cost_matrix)
    tasks_count = len(cost_matrix[0])

    # Initialize potentials
    worker_potentials = get_initial_potentials_for_workers(cost_matrix)
    task_potentials = get_initial_potentials_for_tasks(len(cost_matrix[0]))
    if print_verbose:
        print_initial_potentials(worker_potentials, task_potentials)
        
def main():
    parser = initialize_parser()
    parser_arguments = parser.parse_args()
    cost_matrix = read_and_parse_cost_matrix(parser_arguments.costs_file)
    if parser_arguments.verbose:
        print_costs_matrix(cost_matrix)
        
    optimal_worker_to_task_matching = get_optimal_matching_with_hungarian_algorithm(cost_matrix, parser_arguments.verbose)

if __name__ == '__main__':
    main()