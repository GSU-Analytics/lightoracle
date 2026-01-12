# oracle_connect.py

"""
Provides functionality for connecting to and interacting with an Oracle database.

This module encapsulates the process of connecting to an Oracle database, executing queries, and managing
database passwords securely using the keyring library. It utilizes the oracledb module for database operations
and pandas for returning query results in a convenient DataFrame format.

Classes:
    LightOracleConnection: Facilitates connections to an Oracle database and provides methods for
                           executing queries and managing database passwords securely.

Examples:
    Creating a connection object and connecting to the database:
    >>> from oracle_connect import LightOracleConnection
    >>> conn = LightOracleConnection(user='my_user', dsn='my_dsn')
    >>> conn.connect()
    
    Testing the database connection:
    >>> conn.test_connection()
    Connection test successful. Cursor object: <oracledb.Cursor object at 0x...>
    
    Executing a query and retrieving results in a DataFrame:
    >>> query = "SELECT * FROM my_table WHERE rownum <= 10"
    >>> df = conn.execute_query(query)
    >>> print(df)

    Resetting the password stored in the keyring for the user:
    >>> conn.reset_password()
    Enter the new password for my_user: 
    Password has been reset successfully.

Notes:
    - This module requires the `oracledb` and `pandas` libraries for database operations and handling
      query results, respectively.
    - The `keyring` library is used for secure password management, storing the database password
      securely in the system's keyring service.
    - Passwords are managed through the keyring and not stored in plain text or in the script,
      enhancing security.
    - The `LightOracleConnection` class provides a method to reset the stored password, which
      can be useful if the database password changes.
    - Before using this module, ensure that the Oracle Instant Client libraries are correctly
      installed and accessible on your system, as they are required by the `oracledb` library.
"""

import keyring
import warnings
import oracledb
import pandas as pd
from getpass import getpass

class LightOracleConnection:
    def __init__(self, user, dsn, lib_dir=None):
        self.user = user
        self.dsn = dsn
        self.lib_dir = lib_dir
        self.connection = None
        self.initialize_oracle_client()

    def initialize_oracle_client(self):
        # Initialize the Oracle Client with the provided library directory, if specified
        if self.lib_dir:
            oracledb.init_oracle_client(lib_dir=self.lib_dir)
        else:
            oracledb.init_oracle_client()

    def get_password(self):
        # Retrieve the password from the keyring
        password = keyring.get_password('LightOracleConnection', self.user)
        if password is None:
            # If not found, prompt the user to enter the password
            #password = input(f"Enter the password for {self.user}: ")
            password = getpass(prompt = f"Enter the password for {self.user}: ")
            # Store the password in the keyring
            keyring.set_password('LightOracleConnection', self.user, password)
        return password

    def reset_password(self):
        # Prompt the user to enter a new password
        #new_password = input(f"Enter the new password for {self.user}: ")
        new_password = getpass(prompt = f"Enter the password for {self.user}: ")
        # Store the new password in the keyring
        keyring.set_password('LightOracleConnection', self.user, new_password)
        print("Password has been reset successfully.")

    def connect(self):
        # Get the password
        password = self.get_password()
        
        # Connect to the database
        self.connection = oracledb.connect(user=self.user, password=password, dsn=self.dsn)
        
    def test_connection(self):
        if self.connection is None:
            self.connect()
        
        # Test the connection
        try:
            cursor = self.connection.cursor()
            print("Connection test successful. Cursor object:", cursor)
        except Exception as e:
            print(f"Connection test failed: {e}")

    def execute_query(self, query):
        if self.connection is None:
            self.connect()

        # Temporarily suppress the specific Pandas warning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            return pd.read_sql(query, con=self.connection)
        
        # Execute the query and return a DataFrame
        return pd.read_sql(query, con=self.connection)
