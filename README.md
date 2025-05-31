# Project Overview

This project investigates how closely a classical adaptive bitrate (ABR) algorithm can approximate the behavior of Pensieve, a reinforcement learning-based ABR system. Pensieve learns to select bitrates based on past network and playback conditions and is often used as a benchmark for ABR performance. The central question of this work is whether a simpler, classical approach can be tuned—through a small number of parameters—to replicate the decisions made by Pensieve.

## Methodology

1. **Target Generation via Pensieve**  
   We run a pretrained Pensieve model in simulation, using the standard environment and network trace dataset from the original repository. This produces a sequence of bitrate decisions that serve as the target for comparison.

2. **Classical Algorithm and Modification**  
   The baseline classical method is the **buffer-based ABR algorithm provided by the Pensieve authors**, integrated into the same simulation loop. We modify this algorithm by introducing a single tunable hyperparameter that scales its bitrate prediction.

3. **Parameter Tuning via Genetic Algorithm**  
   We use **TOGA (Tuning Optimizing Genetic Algorithms)**, a genetic algorithm implementation available at [https://github.com/JPLMLIA/TOGA/tree/main](https://github.com/JPLMLIA/TOGA/tree/main), to optimize the scaling parameter so that the buffer-based algorithm's bitrate decisions more closely match those of Pensieve.

4. **Evaluation Metric**  
   For each matching pair of simulation runs, we extract the sequence of selected bitrates and compute the **mean absolute error (MAE)** between them. Each trace contributes equally to the final aggregate score across the dataset.

## Current Status and Limitations

This is an early-stage implementation with the following constraints:

- Pensieve is run in simulation only, using a fixed pretrained model.
- The dataset is limited to a subset of the Belgium traces used in the original Pensieve work.
- Only one hyperparameter (a scaling factor on the buffer-based bitrate prediction) is currently being tuned.
- Only the buffer-based method has been tested for now.

## Reproduction Steps

### Producing Data with Pensieve (Optional)

1. **Produce input data for Pensieve.** To produce (simulated) reference bit rate prediction data using Pensieve, the first step is to produce "cooked" traces that Pensieve will consume as input in the simulation loop. These are lists of the form [<timestamp_in_seconds>, <throughput_in_Mbps>] reflecting the state of the network over time. We implemented the script `code/pensieve/traces/belgium/cook.py` to take traces produced for mahimahi from the prexising Pensieve codebase and produce cooked traces. Our data can be found at `code/pensieve/test/cooked_traces`.
2. **Run Pensieve in simulation.** Since the original Pensieve repo uses now deprecated versions of key libraries, e.g. tensorflow, we had some difficulty in replicating it on modern Apple silicon. To get around this we created a dockerimage (see ). To run Pensieve, you may need to first build and run the docker image:
`cd code/pensieve`
`docker build --platform=linux/amd64 -t pensieve .`
`docker run -it --platform=linux/amd64 -v /full/path/to/your/pensieve:/pensieve pensieve bash`
Then, in the container,
`cd code/pensieve/test`
`python rl_no_training.py`
This will produce logs in the directory `code/pensieve/test/results`. You can skip this step and use the data we have produced in the same directory.

### Tuning with TOGA

To run toga, you will first need to create the conda environment and install TOGA:
`cd code/TOGA`
`conda env create -f envs/toga36-env.yml`
`source activate toga36`
`pip install -e .`

Afterwards, you can start a toga server using:
`toga-server --source code/TOGA/toga/config/server_settings.yml`

Then (in another prompt, or after backgrounding the server process), spawn a worker using:
`toga-client --source code/TOGA/toga/config/run_settings.yml`

The server will create a directory named `experiment_dir` in your current working directory and create hyperparameter configurations using mutation rules set in the TOGA config. The worker will run the Pensieve simulation loop using the given hyperparameters, and calculate the mean absolute error against the reference data produced in the previous section. Upon exiting the server, it will collect the current best results, and plot them in subdirectories of the experiment dir. See the TOGA repo for info.

