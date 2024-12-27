# Scheduler Project

This project was worked on by me and 5 other group members for our AI course. Project and README
have been modified slightly so it can be presented publicly.

## Description:

Genetic Algorithm/Or-Tree repair for scheduling soccer games and practices around Calgary

# Running the code
Open the terminal and create a virtual environment inside the Scheduler folder
```
python -m venv .venv
```

Activate the virtual environment
- for windows
```
.venv\Scripts\activate 
```
- for Linux
```
source .venv/bin/activate 
```

Go into the src folder so you can run main.py
```
cd src
```
Main, however, requires certain command lines: <br>
The first argument is the file name. <br>
The test/example file must be within the examples folder, however, the command line 
can be given as either the path 
```
../Examples/filename.txt
```
Or the name
```
filename.txt
```
The next four arguments are weights, and the last four are penalties <br>
An example execution on a short example is:
```
python ./main.py ShortExample.txt 1 1 1 1 10 10 10 10
```

This will run the scheduler Genetic Algorithm with Or-Tree repair.
The output will be a .csv file. <br> This will be found in the output folders (created on execution), containing the fittest found schedule (the first one if multiple exist). <br>

## Environmental Variables

Alternatively, two Environmental variables enable users to print debug or display statements.
Debug statements are things such as the parser completing, while
display statements print each generation, schedule and fitness value.
To enable these modes, enter these commands for Windows and Linux, respectively
```
$env:DISPLAY="True"
$env:DEBUG="True"
```
```
export DISPLAY="True"
export DEBUG="True"
```
Both modes can be toggled independently and will initially be set to false unless the user toggled them on.

# Optional: number of iterations
Currently, the number of iterations set for the Genetic Algorithm to run is 2000. <br>
This can be changed within main.py and modifying the constant variable MAX_GEN.

# Timing 
The timing of the algorithm is approximated and will vary with each execution, However, <br>
2000 Iterations will take approximately 10-15 minutes. <br>
While 300 Iterations will take approximately 1-2 minutes <br>

