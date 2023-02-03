import my_parser
import numpy as np
import logging
import argparse


def create_parser():
    ''' Create parser for file calculation '''

    parser = argparse.ArgumentParser(description='File calculator')
    parser.add_argument('exp', type=str,
                        help='Expression for file calculation')
    parser.add_argument('--outfile', type=str, required=True,
                        default='out.npz',
                        help='Output file')
    parser.add_argument('--infile', type=str, required=True, nargs='+',
                        help='Input files from file_1 to file_n')
    return parser


def create_logger(mode='w'):
    ''' Create a logger to record information'''

    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    file_handler = logging.FileHandler('my_log.log', mode=mode)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.CRITICAL)

    # Create a formatter and set it to format the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def npz_calculator(args, logger=None):
    ''' Calculate results from the input arguments '''

    if logger is None:
        logger = create_logger()

    ops = my_parser.parse(args.exp, args.infile, logger)
    result_data = my_parser.compute(ops, args.infile, logger)
    my_parser.write_npz_file(result_data, args.outfile, logger)


if __name__ == "__main__":

    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()

    # File calculation
    npz_calculator(args)
