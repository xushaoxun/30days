# coding:utf-8
import argparse
import os

filepath = os.path.join(os.path.dirname(__file__), 'data.csv')
print(filepath)
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user_id', type=int)
args = parser.parse_args()

print(args)
print(args.user_id)