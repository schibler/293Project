import os

# Go up one directory from where load_trace.py is located
COOKED_TRACE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cooked_traces/')


def load_trace(cooked_trace_folder=COOKED_TRACE_FOLDER):
    cooked_files = os.listdir(cooked_trace_folder)
    print(f"Showing cooked files in directory {cooked_trace_folder}")
    print(f"{cooked_files}")
    all_cooked_time = []
    all_cooked_bw = []
    all_file_names = []
    for cooked_file in cooked_files:
        file_path = cooked_trace_folder + cooked_file
        cooked_time = []
        cooked_bw = []
        # print file_path
        with open(file_path, 'r') as f:
            for line in f:
                parse = line.split()
                cooked_time.append(float(parse[0]))
                cooked_bw.append(float(parse[1]))
        all_cooked_time.append(cooked_time)
        all_cooked_bw.append(cooked_bw)
        all_file_names.append(cooked_file)

    return all_cooked_time, all_cooked_bw, all_file_names
