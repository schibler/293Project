import os
import numpy as np

INPUT_DIR = './sim/cooked_traces/'        # Change this to your cooked traces folder
OUTPUT_DIR = './sim/cooked_traces_filtered/'  # Folder to save filtered traces

AVG_THRESHOLD = 6.0      # Mbps
MIN_THRESHOLD = 0.2      # Mbps

def filter_traces(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    trace_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    kept = 0
    discarded = 0

    for filename in trace_files:
        filepath = os.path.join(input_dir, filename)
        data = []

        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 2:
                    continue
                # Assume throughput is in Mbps (float)
                throughput = float(parts[1])
                data.append(throughput)
        
        if not data:
            print(f"Skipping empty trace {filename}")
            discarded += 1
            continue

        avg_throughput = np.mean(data)
        min_throughput = np.min(data)

        if avg_throughput < AVG_THRESHOLD and min_throughput > MIN_THRESHOLD:
            # Keep trace, copy to output dir
            outpath = os.path.join(output_dir, filename)
            with open(outpath, 'w') as out_f:
                with open(filepath, 'r') as in_f:
                    out_f.write(in_f.read())
            kept += 1
        else:
            discarded += 1
    
    print(f"Kept {kept} traces, discarded {discarded} traces")

if __name__ == '__main__':
    filter_traces(INPUT_DIR, OUTPUT_DIR)
