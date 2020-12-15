# Dynport

Simple python utility that uses the Pandas library to assist in directly importing data from a file to Amazon DynamoDB.

It can import a CSV, Excel, JSON or Parquet file.

**Important observation: Datetimes are imported as strings.**

### Installation
With pip (replace with pip3 on Ubuntu)
```
pip install -r requirement.txt
```
With Pipenv
```
pipenv install
```

### Usage
```
dynport.py [-h] [--ftype [FILE-TYPE]] FILE AWS-ACCESS-KEY AWS-SECRET-KEY AWS-REGION TABLE-NAME
```

### Examples

- **CSV**

1. Create a DynamoDB table called **_Grades_**, in the US West 1 region, with primary key **_SSN_**, of string type

  *FOR MORE INFO VISIT: [Getting Started with DynamoDB - Step 1: Create a Table](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/getting-started-step-1.html)*

2. Use dynport to import the data in [grades.csv](./test-data/grades.csv)
```
dynport.py ./test-data/grades.csv <AWS-ACCESS-KEY> <AWS-SECRET-KEY> us-west-1 Grades
```

- **Parquet**

1. Create a DynamoDB table called **_Users_**, in the US West 1 region, with primary key **_id_**, of numeric type

2. Use dynport to import the data in [userdata1.parquet](./test-data/userdata1.parquet)
```
dynport.py --ftype parquet ./test-data/userdata1.parquet <AWS-ACCESS-KEY> <AWS-SECRET-KEY> us-west-1 Users
```

For testing purposes, a sample of the other accepted file types can also be found in [test-data](./test-data)
