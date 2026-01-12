# example.py

from lightoracle import LightOracleConnection
from config import oracle_user, lib_dir, oracle_dsn

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

oracle_conn = LightOracleConnection(oracle_user, oracle_dsn, lib_dir)
print("Connecting to Oracle database...")
df = oracle_conn.execute_query(query)
print("Query executed successfully.")
print("Saving query results to CSV file...")
df.to_csv('example.csv', index=False)
print("Results saved to example.csv.")

