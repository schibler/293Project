import pandas as pd
import numpy as np
import pylab as p
import sys
import glob
import os
import yaml
import time
import math
import random
import bb

cwd = os.getcwd()

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", default='', help='/path/to/config.yml')

    args = parser.parse_args()

    if not os.path.exists(args.c):
        print("Configuration File does not exist")
        sys.exit(0)

    #print('sleep for 10 seconds')
    #time.sleep(10)
    #print('run program')
    Optimization(parameters_config=args.c)


class Optimization(object):
    """
    Optimization wrapper object for TOGA test case
    """

    def __init__(self, parameters_config=''):
        self.param_config = self.read_input_params(parameters_config)

        f1, f2 = self.optimize_this_function(self.param_config['hyperparams'])
        self.write_metrics(f1, f2)
        if self.param_config['debug'] == True:
            self.test()

    @staticmethod
    def optimize_this_function(hyperparams):
        bb_weight = hyperparams["bb_weight"]
        bb.run(bb_weight)

        # Paths
        cwd_results_dir = os.path.join(os.getcwd(), 'results')
        script_results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
        
        # Collect files
        bb_files = glob.glob(os.path.join(cwd_results_dir, 'log_sim_bb_*.json'))
        rl_files = glob.glob(os.path.join(script_results_dir, 'log_sim_rl_*.json'))
        
        # Map suffixes to full paths
        def suffix_map(files, prefix):
            return {
                os.path.basename(f).replace(prefix, ''): f
                for f in files
            }
        
        bb_map = suffix_map(bb_files, 'log_sim_bb_')
        rl_map = suffix_map(rl_files, 'log_sim_rl_')
        
        # Find matching suffixes
        common_suffixes = set(bb_map.keys()) & set(rl_map.keys())
        if not common_suffixes:
            print("No matching file pairs found.")
            exit()
        
        # Extract second column values
        def extract_second_column(filepath):
            values = []
            with open(filepath, 'r') as f:
                for line in f:
                    if line.strip():  # skip blank lines
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            values.append(float(parts[1]))  # second column
            return np.array(values)
        
        # Compute MAE per file, then average
        mae_values = []
        
        for suffix in sorted(common_suffixes):
            bb_values = extract_second_column(bb_map[suffix])
            rl_values = extract_second_column(rl_map[suffix])
        
            min_len = min(len(bb_values), len(rl_values))
            if min_len == 0:
                print(f"Skipping {suffix} (empty data)")
                continue
        
            mae = np.mean(np.abs(bb_values[:min_len] - rl_values[:min_len]))
            mae_values.append(mae)
        
        # Final aggregate closeness
        if mae_values:
            aggregate_mae = np.mean(mae_values)
            print(f"\nAggregate closeness (average MAE across files): {aggregate_mae:.4f}")
        else:
            print("No valid data to compare.")
    
        return bb_weight, aggregate_mae

    @staticmethod
    def read_input_params(paramater_config=''):
        """

        Insert YAML config reading code to obtain values for x and y

        :param paramater_config:
        :return:
        """
        with open(paramater_config) as f:
            _config = yaml.safe_load(f)

        return _config

    def write_metrics(self, a, b):
        d = {'fixed-axis': [a], 'metric': [b]}
        df = pd.DataFrame(data=d)

        work_dir = os.path.join(cwd, self.param_config['output'])
        if not os.path.exists(work_dir):
            os.mkdir(work_dir)

        output = os.path.join(work_dir, self.param_config['metrics'])

        df.to_csv(output, index=False, sep=',', encoding='utf-8')


if __name__ == "__main__":
    main()
