# Logging and Argparse modules

## Exercise: Math parser working on numpy .npz files

### File description

makeVectors.py: Create several large vector files (e.g. labVec[0-7].npz)

my_parser.py: Functions do parsing, calculation and writing outputs

npz_calc.py: Main program 

submit.sh: Slurm script (for handling large files) with example file calculation expression

test_np_calc.py: Test functions

### Usage

Example is provided in submit.sh. Format of input arguments can be shown by command 'python npz_calc.py'.

For test functions, with pytest package installed, command 'pytest -s -v' is recommended to see all screen outputs.

Running test functions will automatically create large vector files for you.