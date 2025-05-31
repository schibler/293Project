import os
import json
from collections import defaultdict

MAHIMAHI_TRACE_DIR = './mahimahi/'  # the output from convert_mahimahi_format.py
COOKED_TRACE_DIR = './sim/cooked_traces/'  # final format Pensieve needs

def cook_trace(file_path):
    bins = defaultdict(int)

    # Read packet arrival times (in ms)
    with open(file_path, 'r') as f:
        for line in f:
            ts_ms = int(line.strip())
            ts_s = ts_ms // 1000  # group by second
            bins[ts_s] += 1

    # Convert to throughput in Mbps
    cooked = []
    for ts in sorted(bins):
        pkt_count = bins[ts]
        # 1500 bytes * 8 bits / 1 sec = bits/sec, convert to Mbps
        mbps = (pkt_count * 1500 * 8) / 1e6
        cooked.append([ts, mbps])

    return cooked

def main():
    os.makedirs(COOKED_TRACE_DIR, exist_ok=True)
    for fname in os.listdir(MAHIMAHI_TRACE_DIR):
        if not fname.endswith('.log'):  # or whatever extension you're using
            continue
        cooked = cook_trace(os.path.join(MAHIMAHI_TRACE_DIR, fname))
        out_path = os.path.join(COOKED_TRACE_DIR, fname.replace('.log', '.json'))
        with open(out_path, 'w') as out_file:
            for line in cooked:
                out_file.write(f"[{line[0]}, {line[1]}]\n")

if __name__ == '__main__':
    main()
