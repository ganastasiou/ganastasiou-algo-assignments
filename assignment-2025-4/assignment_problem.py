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

def print_alternating_tree_sets(current_worker_set, current_task_set):

    sorted_worker_indices = current_worker_set
    worker_indices_str_list = []
    for worker_index in sorted_worker_indices:
        worker_indices_str_list.append(str(worker_index))
    worker_indices_final_str = ", ".join(worker_indices_str_list)

    sorted_task_indices = current_task_set
    task_indices_str_list = []
    for task_index in sorted_task_indices:
        task_indices_str_list.append(str(task_index))
    task_indices_final_str = ", ".join(task_indices_str_list)

    # Workers is S and tasks is T
    print(f"Set S: {{{worker_indices_final_str}}}")
    print(f"Set T: {{{task_indices_final_str}}}")

def print_augmentation(worker_to_task_matching):
    formatted_work_task_pairs = []
    sorted_matching = sorted(worker_to_task_matching.items())
    for worker, task in sorted_matching:
        formatted_worker_task_str = f"R{worker}->C{task}"
        formatted_work_task_pairs.append(formatted_worker_task_str)
    matching_str = ", ".join(formatted_work_task_pairs)
    print(f"Matching: {matching_str}")

def print_final_result(worker_to_task_matching, cost_matrix, print_verbose):
    if(print_verbose):
        print("=== Final Result ===")
    total_cost = 0.0
    #task_index -> column
    #worker_index -> row
    for worker_index in sorted(worker_to_task_matching.keys()):
        task_index = worker_to_task_matching[worker_index]
        cost = cost_matrix[worker_index][task_index]
        print(f"row {worker_index} -> col {task_index} cost={cost}")
        total_cost += cost
    print(f"Total cost: {total_cost}")

# workers_potentials corresponds to l(x)
# tasks_potentials corresponds to l(y)
# cost_matrix corresponds to w(x,y)
def is_tight_edge(worker_index, task_index, workers_potentials, tasks_potentials, cost_matrix):
    potential_sum = workers_potentials[worker_index] + tasks_potentials[task_index]
    assignment_cost = cost_matrix[worker_index][task_index]
    difference = abs(potential_sum - assignment_cost)
    return difference < 1e-9

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

def update_potentials(current_worker_set, worker_potentials, current_task_set, task_potentials, delta):
    for index in sorted(current_worker_set):
        worker_potentials[index] += delta
    for index in current_task_set:
        task_potentials[index] -= delta

# workers_potentials corresponds to l(x)
# tasks_potentials corresponds to l(y)
# cost_matrix corresponds to w(x,y)
def get_tight_neighbors_indices(worker_index, workers_potentials, tasks_potentials, cost_matrix):
    tight_neighbor_tasks_lst = []
    tasks_count = len(cost_matrix[0])
    for task_index in range(tasks_count):
        is_task_index_tight_edge = is_tight_edge(worker_index, task_index, workers_potentials, tasks_potentials, cost_matrix)
        if is_task_index_tight_edge:
            tight_neighbor_tasks_lst.append(task_index)
    
    return tight_neighbor_tasks_lst
# worker_set is a subset of workers (rows) in the bipartite graph
# workers_potentials corresponds to l(x)
# tasks_potentials corresponds to l(y)
# cost_matrix corresponds to w(x,y)
def get_tight_neighbors_of_set(worker_set, workers_potentials, tasks_potentials, cost_matrix):
    tight_neighbor_tasks_set = set()
    for worker_index in worker_set:
        tight_neibour_indices = get_tight_neighbors_indices(worker_index, workers_potentials, tasks_potentials, cost_matrix)
        for task_index in tight_neibour_indices:
            tight_neighbor_tasks_set.add(task_index)
    return tight_neighbor_tasks_set


def get_calculated_delta(current_worker_set, worker_potentials, task_potentials, tasks_count, current_task_set, cost_matrix):
    # Set to infinity
    delta = float('inf')
    for current_worker_index in sorted(current_worker_set):
        for task in range(tasks_count):
            if task not in current_task_set:
                cost_diff = cost_matrix[current_worker_index][task] - worker_potentials[current_worker_index] - task_potentials[task]
                delta = min(delta, cost_diff)
    return delta

def find_worker_matched_to_task(task_index, matching):
    matching_items = matching.items()
    for worker_index, matched_task_index in matching_items:
        if matched_task_index == task_index:
            return worker_index
    return -1


def augment_matching(worker_to_task_matching, parent_pointers, ending_task_index, print_verbose):

    # Rebuilding the path starting from the end following alternating parents
    path_nodes = []
    current_task_index = ending_task_index
    
    # Trace backwards through alternating parents task --> worker --> task --> worker
    while current_task_index is not None:
        path_nodes.append(('task', current_task_index))
        
        if current_task_index not in parent_pointers['task_parent']:
            current_task_index = None
        else:
            parent_worker = parent_pointers['task_parent'][current_task_index]
            path_nodes.append(('worker', parent_worker))
            
            if parent_worker not in parent_pointers['worker_parent']:
                current_task_index = None
            else:
                current_task_index = parent_pointers['worker_parent'][parent_worker]
    
    path_nodes.reverse()
    
    if print_verbose:
        node_labels = []
        for node_type, node_index in path_nodes:
            if node_type == 'worker':
                label = f"R{node_index}"  # R stands for worker row
            elif node_type == 'task':
                label = f"C{node_index}"  # C stands for task column
            node_labels.append(label)
        
        augmenting_path = ""
        for index, label in enumerate(node_labels):
            if index == 0:
                augmenting_path += label
            elif 'R' in label:
                augmenting_path += "=>" + label
            else:
                augmenting_path += "->" + label
        print(f"Augmenting path: {augmenting_path}")
        
        # Print current matching prior to augmentation
        matching_str_list = []
        for worker, task in sorted(worker_to_task_matching.items()):
            matching_str_list.append(f"R{worker}->C{task}")
        matching_str_final = ", ".join(matching_str_list)
        print(f"Matching: {matching_str_final}")
    
    edges_to_remove = []
    edges_to_add = []
    
    # Traverse the path and identify which edges to Remove or Add edges appropriately
    for index in range(len(path_nodes) - 1):
        current_type, current_index = path_nodes[index]
        next_type, next_index = path_nodes[index + 1]
        if current_type == 'worker' and next_type == 'task':
            edges_to_add.append((current_index, next_index))
        elif current_type == 'task' and next_type == 'worker':
            edges_to_remove.append((next_index, current_index))
    
    # Remove edges
    for worker_index, task_index in edges_to_remove:
        if print_verbose:
            print(f"Removing edge R{worker_index}->C{task_index}")
        if worker_index in worker_to_task_matching:
            del worker_to_task_matching[worker_index]
    
    # Add edges 
    for worker_index, task_index in edges_to_add:
        if print_verbose:
            print(f"Adding edge R{worker_index}->C{task_index}")
        worker_to_task_matching[worker_index] = task_index
    
    if print_verbose:
        print_augmentation(worker_to_task_matching)

def get_optimal_matching_with_hungarian_algorithm(cost_matrix, print_verbose=False):

    workers_count = len(cost_matrix)
    tasks_count = len(cost_matrix[0])

    # Initialize potentials
    worker_potentials = get_initial_potentials_for_workers(cost_matrix)
    task_potentials = get_initial_potentials_for_tasks(len(cost_matrix[0]))

    if print_verbose:
        print_initial_potentials(worker_potentials, task_potentials)

    # Initialize matching
    optimal_worker_to_task_matching = {}

    # While finding ideal match
    while len(optimal_worker_to_task_matching) < workers_count:
        # Find a free row
        empty_worker = None
        for index_worker in range(workers_count):
            if index_worker not in optimal_worker_to_task_matching:
                empty_worker = index_worker
                break

        if print_verbose:
            print(f"--- Matching size {len(optimal_worker_to_task_matching)}, start from free row r={empty_worker} ---")

        current_worker_set = {empty_worker}
        current_task_set = set()

        path_information = {
            'worker_parent': {}, 
            'task_parent': {} 
        }

        matching_increased = False
        just_updated_potentials = False

        while not matching_increased:
            # Get all tight neighbors of current_worker_set S
            current_worker_set_neibours = get_tight_neighbors_of_set(current_worker_set, worker_potentials, task_potentials, cost_matrix)
            
            # Only print if we did not just update potentials
            if print_verbose and not just_updated_potentials:
                print_alternating_tree_sets(current_worker_set, current_task_set)
            
            just_updated_potentials = False
            
            if current_worker_set_neibours == current_task_set:
                # No tight edge outside current_task_set stands update potentials
                if print_verbose:
                    print("No tight edge outside T. Update potentials by delta", end="")

                delta = get_calculated_delta(current_worker_set, worker_potentials, task_potentials, tasks_count, current_task_set, cost_matrix)
                if print_verbose:
                    print(f"={delta:.0f}")

                update_potentials(current_worker_set, worker_potentials, current_task_set, task_potentials, delta)
                current_worker_set_neibours = get_tight_neighbors_of_set(current_worker_set, worker_potentials, task_potentials, cost_matrix)

                if print_verbose:
                    print_worker_and_task_potentials(worker_potentials, task_potentials)
                
                just_updated_potentials = True

            else:
                task_index = None
                connected_worker_index = None
                found_edge = False
                
                for worker_index in current_worker_set:
                    # Get tight neighbor indices tasks for this specific worker
                    tight_tasks_of_worker = get_tight_neighbors_indices(worker_index, worker_potentials, task_potentials, cost_matrix)
                    # Find first task of this worker that is not in tasks
                    for task_idx in tight_tasks_of_worker:
                        if task_idx not in current_task_set:
                            task_index = task_idx
                            connected_worker_index = worker_index
                            found_edge = True
                            break
                    
                    if found_edge:
                        break
                
                if print_verbose:
                    print(f"Tight edge discovered: ({connected_worker_index}, {task_index}).", end=" ")
                
                matched_worker_to_task = find_worker_matched_to_task(task_index, optimal_worker_to_task_matching)
                
                if matched_worker_to_task == -1:
                    if print_verbose:
                        print(f"Column {task_index} is free: AUGMENT MATCHING")
                    path_information['task_parent'][task_index] = connected_worker_index
                    augment_matching(optimal_worker_to_task_matching, path_information, task_index, print_verbose)
                    matching_increased = True
                else:
                    if print_verbose:
                        print(f"Column {task_index} is matched to row {matched_worker_to_task}: EXTEND TREE")
                    path_information['task_parent'][task_index] = connected_worker_index
                    path_information['worker_parent'][matched_worker_to_task] = task_index 
                    current_worker_set.add(matched_worker_to_task)
                    current_task_set.add(task_index)

        if print_verbose:
            print()
    return optimal_worker_to_task_matching

def main():
    parser = initialize_parser()
    parser_arguments = parser.parse_args()
    cost_matrix = read_and_parse_cost_matrix(parser_arguments.costs_file)
    if parser_arguments.verbose:
        print_costs_matrix(cost_matrix)
        
    optimal_worker_to_task_matching = get_optimal_matching_with_hungarian_algorithm(cost_matrix, parser_arguments.verbose)
    print_final_result(optimal_worker_to_task_matching, cost_matrix, parser_arguments.verbose)  

if __name__ == '__main__':
    main()