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
def main():
    parser = initialize_parser()
    parser_arguments = parser.parse_args()
    cost_matrix = read_and_parse_cost_matrix(parser_arguments.costs_file)
    print(cost_matrix)

if __name__ == '__main__':
    main()