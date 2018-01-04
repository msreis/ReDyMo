# ReDyMo

### A dynamic model of the replication process in kinetoplastida
ReDyMo is a Python-coded model that simulates the replication of the cells of organisms belonging to the kinetoplastida group (currently focused on *Trypanosoma brucei strain 927*). It is capable of:
  - Calculating various relevant data about the replication process, including the duration of the S phase, the resulting average interorigin distance of the genome, the overall replication percentage, etc.
  - Storing information about each step of the simulation, such as the replication stage at that step and whether any collisions happened during that step.
  - Storing information about each base belonging to each chromosome of the genome, for example at what instant that base was replicated.
  - Simulating conflicts with a variety of input parameters like replication machinery speed and transcription frequency.

### Requirements
To run ReDyMo, you only need a system with Python3 installed. That's done by default in most Linux distributions.

### Database
The system uses a simple *SQLite* database. Python already has plenty of functionalities to access and modify *SQLite* databases, however, if it's necessary to visualize the data in a more intuitive fashion, I recommend the use of a third-party software such as [SQLiteStudio].

### Parameters
For the moment, all parameters are mandatory and are listed below:
 - *organism*: Name of the organism, as saved in the database (remember to add single quotation marks when using space-spearated names).
 - *cells*: Number of independent simulations to be made.
 - *resources*: Number of available forks for the replication process.
 - *speed*: Movement speed of each replication machinery (in bases per second).
 - *period*: Time between consecutive activations of a transcription region (in seconds).

### Running the simulation
To run the program, use
```sh
$ cd ReDyMo
$ ./main.py <parameters>
```
For example
```sh
$ ./main.py --organism 'Trypanosoma brucei brucei TREU927' --resources 10 11 1 --speed 338 339 1 --period 150 151 60 --cells 1
```
   [SQLiteStudio]: <https://sqlitestudio.pl/index.rvt>
