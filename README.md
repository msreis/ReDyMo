# ReDyMo

### A dynamic model of the replication process in kinetoplastida

ReDyMo is a Python-coded, stochastic dynamic model simulator that reproduces the DNA replication process of cellular organisms belonging to the kinetoplastida group. Initially, we focused on *Trypanosoma brucei* strain *TREU927*.

This simulator is capable of:
  - Calculation of various relevant properties about the replication process, including S-phase duration, mean inter-origin distance between replication origin sites, the achieved replication percentage given a time limit, etc.
  - Storage of information about each step of the simulation, such as the replication stage at each model simulation iteration and whether any collisions happened during a given iteration.
  - Storage of information regarding the replication timing program, that is, for each base pair it is recorded at which simulation iteration it was replicated.
  - Simulation of replication-transcription conflicts with a variety of input parameters like replication machinery speed and transcription frequency.
  - Simulation of dormant origins firing.

### Requirements

To run ReDyMo, you only need a system with Python3 installed, which is done by default in most Linux distributions.

### Database

The system uses a simple *SQLite* database. Python already has plenty of functionalities to access and modify *SQLite* databases. However, if it is necessary to visualize the data in a more intuitive fashion, we recommend the usage of a third-party software such as [SQLiteStudio].

### Parameters
To view information about the configuration parameters, run:
```
$ ./src/main.py -h
```

### Running the simulation

To run the program, the syntax of the main simulator program is the following one:
```
$ ./src/main.py --cells number_of_cells --dormant dormant_flag --organism 'organism_name' --resources number_of_forks --speed speed_value --timeout timeout_value [--constitutive range] [--period period_value]
```

The command above must be executed within the project main directory. For example, to run a simulation of 7 cells of *T. brucei TREU927*, with 10 forks, replisome speed of 65 bp/iteration, transcription period of 150 iterations between two transcription initiations, a timeout of one million iterations and with dormant origin firing, one must type at the project main directory:
```
$ ./src/main.py --cells 7 --organism 'Trypanosoma brucei brucei TREU927' --resources 10 --speed 65 --period 150 --timeout 1000000 --dormant True
```
The simulation results will be stored into a directory named *output/True_10_150/*, in which "output" is the outer directory name and the inner directory name of composed of the concatenation of the used parameter values for dormant origin firing, resources and period.

Another example: if one wants to simulate 30 cells of *T. brucei TREU927*, with 50 forks, replisome speed of 1 bp/iteration, no transcription, no dormant origin firing, using constitutive origins with a firing initiation range of 200 Kb, and the same timeout of the previous example:
```
$ ./src/main.py --cells 30 --organism 'Trypanosoma brucei brucei TREU927' --resources 50 --speed 1 --timeout 1000000 --dormant False --constitutive 200000
```

In this case, the simulation results will be stored into the directory *output/False_50_0*.

### Aggregating the simulation results

If more than one cell is simulated at once, then the results may be averaged through the usage of an aggregator script, whose syntax is the following:
```
$ ./script/cell_output_aggregator.py *output_directory* > *aggregation_file_and_path*
```
where *output_directory* is the output directory of the simulation and *aggregation_file_and_path* is both the path and name for the file containing the result of data aggregation. For example, to aggregate the aforementioned first example, one could just type:
```
$ ./script/cell_output_aggregator.py output/False_10_150 > output/aggregated.txt
```

### Bug report and contact

If you have any bug report and/or want to contact for other subjects (e.g., to collaborate in this project), please do not hesitate to contact us!

Please, address your message to:

msreis at butantan dot gov dot br.


   [SQLiteStudio]: <https://sqlitestudio.pl/index.rvt>

