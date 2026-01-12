# config_example.py

"""

****************************************************************************************************
*       ADD YOUR OWN CREDENTIALS AND CONNECTION DETAILS. THEN RENAME THIS FILE TO `config.py`      *
****************************************************************************************************

Configuration settings for database connections, including credentials and connection details.
This module contains configuration details used by the `oracle_connect.py` for connecting to Oracle databases. 
It specifies usernames, database names, hostnames, port numbers, and driver information required for establishing 
database connections.

The `user`, `lib_dir`, and `dsn` are used for Oracle database connections, specifying the Oracle user, 
library directory (for Oracle Client libraries), and the Data Source Name (DSN) for the Oracle database.

Attributes:

    user (str): The username for the Oracle database connection.
    lib_dir (str): The directory path where the Oracle Client libraries are located.
    dsn (str): The Data Source Name for the Oracle database connection.

Example usage with lightoracle:
    from lightoracle import LightOracleConnection
    from config import user, dsn, lib_dir
    
    oracle_conn = LightOracleConnection(user=user,
                                        dsn=dsn,
                                        lib_dir=lib_dir)
    oracle_conn.connect()

Note:
    Ensure that the driver specified in `driver` is installed and matches the version of your SQL Server.
    If the path to the Oracle Client libraries is not specified in your Windows PATH, set the `lib_dir` to 
    the location of the Oracle Client libraries on your machine otherwise leave the string empty. If the 
    Oracle Client libraries are not installed, See the Oracle Instant Client installation guide for more 
    information: https://www.oracle.com/database/technologies/instant-client.html
"""

# Oracle Connection details
user = "dummy_name"  # The Oracle user
dsn = ""  # The Data Source Name for the Oracle database
lib_dir = ""