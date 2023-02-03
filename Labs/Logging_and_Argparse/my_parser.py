import enum
import re
import operator
import numpy as np
import logging
from logging import Logger

''' Courtesy of https://github.com/gnebehay/parser '''
''' A Math Parser for Python '''


class TokenType(enum.Enum):
    T_NUM = 0
    T_PLUS = 1
    T_MINUS = 2
    T_MULT = 3
    T_DIV = 4
    T_LPAR = 5
    T_RPAR = 6
    T_END = 7


class Node:
    def __init__(self, token_type: TokenType, value: any = None):
        self.token_type = token_type
        self.value = value
        self.children = []


operations = {
    TokenType.T_PLUS: operator.add,
    TokenType.T_MINUS: operator.sub,
    TokenType.T_MULT: operator.mul,
    TokenType.T_DIV: operator.truediv
}


def lexical_check(s: str, npz_list: list, logger: Logger = None):
    ''' Check input expression '''

    # Check logger
    if logger is None:
        logger = logging.getLogger()
    logger.debug('Check input expression: Function \'lexical_check\'.')

    # Remove spaces within expression
    string = "".join(s.split())

    # Check appearance of files within expression
    file_index = [int(obj) for obj in re.findall(r'\d+', string)]

    if np.max(file_index) > len(npz_list):
        msg = 'Invalid expression: ' \
            'Undefine file path for file%d and above!' % (len(npz_list)+1)
        logger.critical(msg)
        raise Exception(msg)

    if min(file_index) == 0:
        msg = 'Invalid expression: ' \
            'File index should start from 1, but find file0!'
        logger.critical(msg)
        raise Exception(msg)

    # Check if every number is preceded with 'file'
    num_match = re.finditer(r'\d+', string)
    for match_obj in num_match:
        ind = match_obj.span()[0]
        if (ind < 4) or (string[ind-4:ind] != 'file'):
            msg = 'Invalid expression: ' \
                'Not every number is preceded with \'file\''
            logger.critical(msg)
            raise Exception(msg)

    # Remove word 'file' in the expression
    string = string.replace('file', '')
    logger.info('Simplified expression: %s' % string)
    return string


def lexical_analysis(s: str, npz_list: list, logger: Logger = None):
    ''' Analyze input expression '''

    # Check logger
    if logger is None:
        logger = logging.getLogger()
    logger.debug('Analyze input expression: Function \'lexical_analysis\'.')

    # Mapping of operators
    mappings = {
        '+': TokenType.T_PLUS,
        '-': TokenType.T_MINUS,
        '*': TokenType.T_MULT,
        '/': TokenType.T_DIV,
        '(': TokenType.T_LPAR,
        ')': TokenType.T_RPAR}

    # Parse every character in the string
    tokens = []
    for c in s:
        if c in mappings:
            token_type = mappings[c]
            token = Node(token_type, value=c)
        elif re.match(r'\d', c):
            token = Node(TokenType.T_NUM, value=int(c))
        else:
            msg = 'Invalid token: {}'.format(c)
            logger.critical(msg)
            raise Exception(msg)
        tokens.append(token)
    tokens.append(Node(TokenType.T_END))
    return tokens


def match(tokens, token):
    if tokens[0].token_type == token:
        return tokens.pop(0)
    else:
        msg = 'Invalid syntax on token {}'.format(tokens[0].token_type)
        raise Exception(msg)


def parse_e(tokens):
    left_node = parse_e2(tokens)

    while tokens[0].token_type in [TokenType.T_PLUS, TokenType.T_MINUS]:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e2(tokens))
        left_node = node

    return left_node


def parse_e2(tokens):
    left_node = parse_e3(tokens)

    while tokens[0].token_type in [TokenType.T_MULT, TokenType.T_DIV]:
        node = tokens.pop(0)
        node.children.append(left_node)
        node.children.append(parse_e3(tokens))
        left_node = node

    return left_node


def parse_e3(tokens):
    if tokens[0].token_type == TokenType.T_NUM:
        return tokens.pop(0)

    match(tokens, TokenType.T_LPAR)
    expression = parse_e(tokens)
    match(tokens, TokenType.T_RPAR)

    return expression


def parse(inputstring, npz_list, logger=None):
    # Check logger
    if logger is None:
        logger = logging.getLogger()
    logger.debug('Start parsing input expression: Function \'parse\'.')

    string_cleaned = lexical_check(inputstring, npz_list, logger)
    tokens = lexical_analysis(string_cleaned, npz_list, logger)
    ast = parse_e(tokens)
    match(tokens, TokenType.T_END)
    return ast


def compute(node, npz_list, logger=None):

    # Check logger
    if logger is None:
        logger = logging.getLogger()

    if node.token_type == TokenType.T_NUM:
        npzfile = npz_list[node.value-1]
        logger.info('Read in file%d: %s' % (node.value, npzfile))
        return np.load(npzfile)['vec']

    left_result = compute(node.children[0], npz_list, logger)
    right_result = compute(node.children[1], npz_list, logger)
    operation = operations[node.token_type]
    return operation(left_result, right_result)


def write_npz_file(data, outfile, logger=None):

    # Check logger
    if logger is None:
        logger = logging.getLogger()

    # Write npz file
    try:
        logger.info('Write output to file %s' % outfile)
        np.savez(outfile, vec=data)

    except Exception as err:
        logger.critical(err)
        raise Exception(err)
