import argparse

from API import Agent


agent = Agent()

parser = argparse.ArgumentParser(description='Process some arguements.')
parser.add_argument('uid', type=str,
                    help="user's id")
parser.add_argument('name', type=str,
                    help="user's name")

args = parser.parse_args()
print(args.accumulate(args.integers))
