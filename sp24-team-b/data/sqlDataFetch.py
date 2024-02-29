import os
import requests
import pandas as pd

def get_sql_cast(column, data_type):
  """
  Generate an SQL cast expression for a given column and its desired data type.

  Args:
  - column (str): The name of the column to cast.
  - data_type: The Python data type to map to an SQL data type.

  Returns:
  - str: An SQL expression that casts the column to the desired SQL data type.
  """

  # Define a mapping from Python data types to SQL data types and functions
  type_mapping = {
      str: "TEXT",
      int: "INT",
      float: "FLOAT",
      bool: "BOOLEAN",
      # Additional mappings based on the provided SQL examples
      'timestamp': lambda col: f"TO_CHAR(\"{col}\"::timestamp, 'YYYY-MM-DD')",
      'value': lambda col: f"CAST(REPLACE(\"{col}\", ',', '') AS INT) AS \"{col}\"",
      'money': lambda col: f"CAST(REPLACE(REPLACE(\"{col}\", '$', ''), ',', '') AS FLOAT) AS \"{col}\"",
  }

  # Get the SQL data type or function for the given Python data type
  sql_expression = type_mapping.get(data_type)

  # If a direct mapping exists, return the SQL cast expression
  if callable(sql_expression):
      return sql_expression(column)
  elif sql_expression:
      return f"CAST(\"{column}\" AS {sql_expression}) AS \"{column}\""
  else:
      # If no mapping is found, return the column without casting
      return f"\"{column}\""

def fetch_data(database_id: str, sql_condition: str = '', **kwargs) -> pd.DataFrame:
  """
    Fetch data from the specified database using SQL query.

    Parameters:
    - database_id (int): The ID of the database.
    - **kwargs: Optional dictionary where keys are column names and values are the desired data types.


    Returns:
    pd.DataFrame: A DataFrame containing the fetched data.
  """

  # Set the base URL for the API
  url = "https://data.boston.gov/api/3/action/datastore_search_sql"

  # Construct the SQL query string with type casting if specified
  columns = [get_sql_cast(column, data_type) for column, data_type in kwargs.items()]

  if columns:
      sql_query = f"SELECT {', '.join(columns)} FROM \"{database_id}\" {sql_condition}"
  else:
      sql_query = f"SELECT * FROM \"{database_id}\" {sql_condition}"


  # Prepare the request parameters
  params = {"sql": sql_query}

  # Send the request
  response = requests.get(url, params=params)

  # Check if the request was successful
  if response.status_code == 200:
      data = response.json()

      # Check if there is data in the response
      if data['success'] and 'result' in data and 'records' in data['result']:
          records = data['result']['records']

          # Convert the records to a Pandas DataFrame
          return pd.DataFrame.from_records(records)
      else:
          print("No data found or error in response.")
          return pd.DataFrame()  # Return an empty DataFrame
  else:
      print("Failed to fetch data:", response.status_code)
      return pd.DataFrame()  # Return an empty DataFrame

def describe_database(resource_id: str) -> None:
    """
    Describe the database by fetching and printing its structure, such as column names.

    :param resource_id: The ID of the resource to describe.
    """
    # Set the base URL for the API to get the resource structure
    url = f"https://data.boston.gov/api/3/action/datastore_search?resource_id={resource_id}&limit=0"

    # Send the request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Check if there is data in the response
        if data['success'] and 'result' in data and 'fields' in data['result']:
            fields = data['result']['fields']

            # Print the column names (keys)
            print(f"{'Column Name':<20} | {'Type':<10}")
            print("-" * 32)

            for field in fields:
              print(f"{field['id']:<20} | {field['type']:<10}")
        else:
            print("No data found or error in response.")
    else:
        print("Failed to fetch data:", response.status_code)

def load_database_mapping() -> dict:
  """
  Load the database name-ID mappings from a given text file.

  Args:
  file_path (str): The path to the text file containing the database mappings.

  Returns:
  dict: A dictionary with database names as keys and their corresponding IDs as values.
  """
  file_path = "ds-boston-remodeling/sp24-team-b/data/dataId.txt"
  home_dir = os.path.expanduser('~')
  file_path = home_dir + "/" + file_path
  database_mapping = {}

  try:
    with open(file_path, 'r') as file:
      for line in file:
        # Split the line into name and ID based on the delimiter
        database_name, database_id = line.strip().split(' / ')
        database_mapping[database_name] = database_id
  except FileNotFoundError:
      print(f"File not found: {file_path}")

  return database_mapping

def get_id_by_name(database_name: str) -> str:
  """
    Retrieve the database ID based on the full name of the database.

    Args:
    database_name (str): The full name of the database for which the ID is required.

    Returns:
    str: The ID of the specified database. Returns 'Database ID not found' if the name does not match.
  """

  # Load the database mappings from the 'dataId.txt' file
  database_mapping = load_database_mapping()

  # Return the ID for the given database name
  return database_mapping.get(database_name, 'Database ID not found')

def get_id_by_year(year: int) -> str:
  """
    Retrieve the database ID for the 'PROPERTY ASSESSMENT FY' database of a specific year.

    Args:
    year (int): The year for which the 'PROPERTY ASSESSMENT FY' database ID is required.

    Returns:
    str: The ID of the 'PROPERTY ASSESSMENT FY' database for the specified year. Returns 'Invalid year, please provide a year between 2004 and 2024' if the year is out of range.
  """

  # Check if the year is within the valid range
  if 2004 <= year <= 2024:
      # Construct the database name for PROPERTY ASSESSMENT FY databases
      database_name = f'PROPERTY ASSESSMENT FY{year}'
      return get_id_by_name(database_name)
  else:
      return 'Invalid year, please provide a year between 2004 and 2024'

