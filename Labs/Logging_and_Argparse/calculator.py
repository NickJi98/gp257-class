import argparse

# create the parser
parser = argparse.ArgumentParser(description='A simple calculator')

# add arguments to the parser
parser.add_argument('--operation', type=str, choices=['add', 'subtract', 'multiply', 'divide'], required=True, help='The operation to perform')
parser.add_argument('--first_number', type=float, required=True, help='The first number')
parser.add_argument('--second_number', type=float, required=True, help='The second number')

# parse the arguments
args = parser.parse_args()

# perform the operation
if args.operation == 'add':
    result = args.first_number + args.second_number
elif args.operation == 'subtract':
    result = args.first_number - args.second_number
elif args.operation == 'multiply':
    result = args.first_number * args.second_number
elif args.operation == 'divide':
    result = args.first_number / args.second_number

# print the result
print(result)
