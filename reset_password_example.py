# reset_password_example.py

from lightoracle import LightOracleConnection

# Create a connection instance with your current credentials
conn = LightOracleConnection()

# Reset the password; you will be prompted to enter a new password
conn.reset_password()

# Test the connection with the newly set password
conn.test_connection()