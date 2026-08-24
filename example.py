# example.py

from lightoracle import LightOracleConnection
from loguru import logger

logger.enable('lightoracle.credentials')

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


logger.info('Creating a LightOracle instance...')
oracle_conn = LightOracleConnection()
try:
    logger.info('Checking your connection...')
    oracle_conn.test_connection()
    logger.success('Connection test successful!')
except Exception as e:
    logger.error(f'Failed to connect! {e}')
    raise e

logger.info("Connecting to Oracle database...")
df = oracle_conn.execute_query(query)
logger.success("Query executed successfully.")

logger.info("Saving query results to CSV file...")
df.to_csv('example.csv', index=False)
logger.success("Results saved to example.csv.")

