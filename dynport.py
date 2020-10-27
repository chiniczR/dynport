# Author: Rebeca Chinicz
# Description: Utility for importing a whole file's content (data) directly into a DynamoDB table

# Import python libraries
import pandas as pd
import boto3
import argparse
import sys
from tqdm import tqdm 

# Parse the necessary arguments
parser = argparse.ArgumentParser(prog='dynport', description='Import data from file to DynamoDB.')
parser.add_argument('infile', metavar='FILE',  type=str, nargs=1,
    help='file with the data to be imported')
parser.add_argument('key', metavar='AWS-ACCESS-KEY', type=str, nargs=1,
    help='aws access key')
parser.add_argument('secret', metavar='AWS-SECRET-KEY', type=str, nargs=1,
    help='aws secret access key')
parser.add_argument('region', metavar='AWS-REGION', type=str, nargs=1,
    help='aws region')
parser.add_argument('table', metavar='TABLE-NAME', type=str, nargs=1,
    help='the destination table')
parser.add_argument('--ftype', metavar='FILE-TYPE', required=False, default='csv', choices=['csv', 'json', 'excel', 'orc', 'parquet', 'avro' ], type=str, nargs='?',
    help='type of the file to be imported')

args = parser.parse_args()

# Import data
dataset = None

if args.ftype == 'csv':
    try:
        dataset = pd.read_csv(args.infile[0], encoding='utf-8')
    except:
        sys.exit(f'Error: {sys.exc_info()[1]}')
elif args.ftype == 'excel':
    try:
        dataset = pd.read_excel(args.infile[0])
    except:
        sys.exit(f'Error: {sys.exc_info()[1]}')
elif args.ftype == 'json':
    try:
        dataset = pd.read_json(args.infile[0], encoding='utf-8')
    except:
        sys.exit(f'Error: {sys.exc_info()[1]}')

try:
    dataset = dataset.rename(columns=lambda x: x.strip()) # Trim whitespace from column names
    for col in dataset.columns:
        dataset[col] = dataset[col].astype(str)
except:
    sys.exit(f'Error: {sys.exc_info()[1]}')

print('File has been read. Going to import:')

dataset = dataset.T.to_dict().values()

# Setting up the AWS credentials
MY_ACCESS_KEY_ID = args.key[0]
MY_SECRET_ACCESS_KEY = args.secret[0]
MY_REGION = args.region[0]

# The table we want the data imported to
table_name = args.table[0]

# The DynamoDB client and the table in question
try:
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=MY_ACCESS_KEY_ID, aws_secret_access_key=MY_SECRET_ACCESS_KEY, region_name=MY_REGION)
    table = dynamodb.Table(table_name)
except:
    sys.exit(f'Error: {sys.exc_info()[1]}')

# For each item on the file, put it on the table
for item in tqdm (dataset, desc="Putting items"):
    try:
        table.put_item(Item=item)
    except:
        sys.exit(f'Error: {sys.exc_info()[1]}')

print('Complete')

