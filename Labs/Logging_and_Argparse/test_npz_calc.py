import my_parser
import numpy as np
import os
from npz_calc import create_parser, create_logger, npz_calculator


def createVector(filename, vecsz):
    vec = np.random.rand(vecsz)
    np.savez(filename, vec=vec)


# NPZ files
npz_list = ['labVec0.npz', 'labVec1.npz', 'labVec2.npz', 'labVec3.npz',
            'labVec4.npz', 'labVec5.npz', 'labVec6.npz', 'labVec7.npz']

try:
    np.load(npz_list[0])
except Exception:
    os.system('python3 makeVectors.py')

# Create a parser
parser = create_parser()

# Create a logger
logger = create_logger('w+')


def test_compute():
    ''' Test correctness of computation result '''

    expr = "file7 * file5 / (file1 + file2)"
    expected_result = np.load(npz_list[6])['vec'] \
        * np.load(npz_list[4])['vec'] \
        / (np.load(npz_list[0])['vec'] + np.load(npz_list[1])['vec'])

    ast = my_parser.parse(expr, npz_list, logger)
    actual_result = my_parser.compute(ast, npz_list, logger)
    abs_err = np.sum(np.abs(actual_result - expected_result))

    assert abs_err == 0.0


def test_logger():
    ''' Test logger output '''

    expr = "file9 * file3"
    try:
        ast = my_parser.parse(expr, npz_list, logger)
        res = my_parser.compute(ast, npz_list, logger)
    except Exception as err:
        print(err)

    expr = "ffile2 * file3"
    try:
        ast = my_parser.parse(expr, npz_list, logger)
        res = my_parser.compute(ast, npz_list, logger)
    except Exception as err:
        print(err)

    expr = "file2 +* file3"
    try:
        ast = my_parser.parse(expr, npz_list, logger)
        res = my_parser.compute(ast, npz_list, logger)
    except Exception as err:
        print(err)

    expr = "file + 2 * file3"
    try:
        ast = my_parser.parse(expr, npz_list, logger)
        res = my_parser.compute(ast, npz_list, logger)
    except Exception as err:
        print(err)


def test_parse():
    ''' Test parser '''

    argv = ["file3 * (file1 - file2)", "--outfile", "test_out.npz",
            "--infile", "labVec0.npz", "labVec1.npz", "labVec2.npz"]
    args = parser.parse_args(argv)

    npz_calculator(args, logger)

    actual_result = np.load(args.outfile)['vec']
    expected_result = np.load(npz_list[2])['vec'] \
        * (np.load(npz_list[0])['vec'] - np.load(npz_list[1])['vec'])
    abs_err = np.sum(np.abs(actual_result - expected_result))

    assert abs_err == 0.0
