# Light Oracle Connection

## Description
A lightweight Oracle database connection handler for managing secure database interactions.

## Installation Instructions

### Remote Installation

This approach does not require cloning the repository as it installs the package directly from the remote repository. This is useful 
for users who only need to use the package without contributing to its development.

1. **Create a Conda Environment, Install Package, and Activate Environment**:
   Copy the `remote_install.yaml` located in the conda_env folder to your local machine. 

   ```yaml
   # remote_install.yaml

   name: lightoracle
   channels:
   - defaults
   dependencies:
   - python>=3.10
   - pip:
      - git+https://github.com/GSU-Analytics/light_conn.git
   ```

   Install the package by following these steps: 
   1. Check that conda is installed by typing `conda -v` in the command line.
   2. Create a new conda environment using the `remote_install.yaml` file with the following command:
      ```cmd
      conda env create -f remote_install.yaml
      conda activate lightoracle
      ```

2. **Install the Package in Existing Environment**:
   ```cmd
   pip install git+https://github.com/GSU-Analytics/light_conn.git
   ```
3. **Update the Package in Existing Environment**:
   ```cmd
   pip install git+https://github.com/GSU-Analytics/light_conn.git -U
   ```

### Local Installation

For local installation, particularly useful if you plan to contribute to the package or need a development setup:

1. **Clone the Repository**:
   ```cmd
   git clone https://github.com/GSU-Analytics/lightoracle.git
   cd lightoracle
   ```

2. **Create and Activate the Conda Environment**:
   Use the `local_install.yaml` located in the conda_env folder to set up an environment with all necessary dependencies 
   installed via Conda. Navigate to the directory containing `local_install.yaml`, or specify the full path to the file.

   ```cmd
   conda env create -f local_install.yaml
   conda activate lightoracle
   ```

3. **Install the Package Locally**:
   This step installs the current local version of the package into the Conda environment.
   ```cmd
   pip install .
   ```

## Usage

To establish a connection to an Oracle database using the `LightOracleConnection` class, configure your connection parameters in the `config_example.py` file. After configuring the `config_example.py` file, rename the file to `config.py` and you can use these parameters to establish a connection to your Oracle database.Here's a guide on how to do that and then utilize the configuration to connect to your Oracle database.

### Configuring Connection Parameters

The `config_example.py` file contains essential attributes for setting up your Oracle database connection. Before you begin using the `LightOracleConnection`, make sure you have correctly configured the following attributes:

- `user`: Your Oracle database username.
- `dsn`: The Data Source Name for the Oracle database connection, which typically includes the hostname, port, and database name.
- `lib_dir`: The directory path to the Oracle Client libraries on your machine. This is necessary if your Oracle Client libraries are not included in your system's PATH environment variable.

Here's an example of how to set up `config_example.py`:

```python
# config.py

# Oracle Connection details
user = "your_username_here"
dsn = "your_dsn_here"
lib_dir = "C:/path/to/your/oracle/client/libraries"  # Only set this if necessary
```

### Connecting to the Database

With your `config.py` file set up, you can use the `LightOracleConnection` class to connect to your Oracle database. Below is a step-by-step example of importing your configuration and creating a database connection:

```python

# main.py
from lightoracle import LightOracleConnection
from config import user, dsn, lib_dir

# Create a connection instance with the configured parameters
oracle_conn = LightOracleConnection(user, dsn, lib_dir)

# Test the Oracle database connection
oracle_conn.test_connection()

# Now you can use `oracle_conn` to perform database operations
```

### Important Notes

- Always ensure that the `user`, `lib_dir`, and `dsn` attributes in `config.py` are updated with the correct information corresponding to your Oracle database setup.
- Never commit sensitive information, such as your actual Oracle username or DSN, to a public repository. It's recommended to use environment variables or a secure credential management system for handling sensitive data.
- If you encounter any issues with connecting to the Oracle database, verify that the Oracle Instant Client is correctly installed and configured on your system. You can find more information and a detailed installation guide on the [Oracle Instant Client website](https://www.oracle.com/database/technologies/instant-client.html).

## Examples

### Example 1: Executing a Query and Saving Results to CSV

See the `example.py` file for a simple example of how to use the `LightOracleConnection` class to connect to an Oracle database and execute a query. This will fetch the first 20 rows of student data from the `edwprd.sdstumain` table and save the results to a CSV file.

```python
# example.py

from lightoracle import LightOracleConnection
from config import user, dsn, lib_dir

query = """
SELECT
    s.term,
    s.college, 
    s.department,
    s.degree,
    s.major,
    s.gpa
FROM edwprd.sdstumain s
WHERE s.term = '202401'
AND s.major = 'PHY'
FETCH FIRST 20 ROWS ONLY
"""

oracle_conn = LightOracleConnection(user, dsn, lib_dir)
print("Connecting to Oracle database...")
df = oracle_conn.execute_query(query)
print("Query executed successfully.")
print("Saving query results to CSV file...")
df.to_csv('example.csv', index=False)
print("Results saved to example.csv.")
```

### Example 2: Resting the User Password

See the `reset_password_example.py` file for an example of how to use the `LightOracleConnection` class to reset a user's password in an Oracle database. This script will prompt you to enter a new password and then test the connection with the new password.

```python
# reset_password_example.py

from lightoracle import LightOracleConnection
from config import user, dsn, lib_dir

# Create a connection instance with your current credentials
conn = LightOracleConnection(user, dsn, lib_dir)

# Reset the password; you will be prompted to enter a new password
conn.reset_password()

# Test the connection with the newly set password
conn.test_connection()
```

For more information, refer to the examples provided in `lightoracle/oracle_connect.py` for details on how to use this package.
