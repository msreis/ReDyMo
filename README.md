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

In this version of ReDyMo, all parameters are mandatory and are listed below:
 - *organism*: Name of the organism, as saved in the database (remember to add single quotation marks when using space-spearated names).
 - *cells*: Number of independent simulations to be made.
 - *resources*: Number of available forks for the replication process.
 - *speed*: Movement speed of each replication machinery (in bases per second).
 - *period*: Time between consecutive activations of a transcription region (in seconds).
 - *timeout*: Maximum allowed number of iterations of a simulation; if this value is reached, then a simulation is ended even if DNA replication is not completed yet.
 - *dormant*: Flag that either activates ('True') or disables ('False') the firing of dormant origins.

### Running the simulation

To run the program, use
```sh
$ cd ReDyMo
$ ./main.py <parameters>
```
The syntax is the following one:
```
$ ./main.py --organism '*organism*' --resources *min* *max* *step* --speed *min* *max* *step* --cells *cells* --period *period* --timout *timeout* --dormant *dormant*
```

For example, to run a simulation of seven cells of *T. brucei TREU927*, with 10 forks, replisome speed of 65 bp/sec, transcription frequency of 150 sec and no dormant origin firing:
```sh
$ ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 10 --speed 65 --period 150 --cells 7 --dormant False
```

The simulation results will be stored into a directory named *output_10_50*, which is "output_" concatenated with the number of resources plus an underline plus the transcription frequency.


### Aggregating the simulation results

If more the one cell is simulated at once, then the results may be averaged through an aggregator script, whose syntax is the following:
```
$ ./script/cell_output_aggregator.py *output_directory* *aggregation_file*
```

For example, to aggregate the aforementioned example, one could just type:
```
$ ./script/cell_output_aggregator.py output_10_150 aggregated.txt
```

   [SQLiteStudio]: <https://sqlitestudio.pl/index.rvt>

