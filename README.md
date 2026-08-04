# lightoracle

A lightweight Oracle database connection handler. Reads credentials from a `.env` file and returns query results as a pandas DataFrame.

## Installation

```bash
pip install git+https://github.com/GSU-Analytics/lightoracle.git
```

To pin a version:

```bash
pip install git+https://github.com/GSU-Analytics/lightoracle.git@v0.3.0
```

## Configuration

Create a `.env` file in your project root. Never commit it to version control.

```env
ORACLE_USER=your_username
ORACLE_PASSWORD=your_password
ORACLE_DSN=hostname:port/service_name
```

`ORACLE_PASSWORD` is optional — if omitted, the package falls back to keyring, then prompts interactively.

## Usage

```python
from lightoracle import LightOracleConnection

conn = LightOracleConnection()
df = conn.execute_query("SELECT * FROM my_table FETCH FIRST 10 ROWS ONLY")
df.to_csv('output.csv', index=False)
```

Credentials are loaded from `.env` automatically. You can also pass them explicitly:

```python
conn = LightOracleConnection(user="my_user", dsn="host:1521/svc")
```

## Thin mode vs. thick mode

By default, lightoracle uses **thin mode** — no Oracle Instant Client required.

To use thick mode (Oracle Instant Client), pass `thick_mode=True` or set `lib_dir`:

```python
# thick mode — Oracle Client in system PATH
conn = LightOracleConnection(thick_mode=True)

# thick mode — explicit library path
conn = LightOracleConnection(lib_dir="/path/to/oracle/client")
```

`lib_dir` can also be set via `ORACLE_LIB_DIR` in your `.env` file.

## Password management

Passwords are resolved in priority order:

1. `ORACLE_PASSWORD` in `.env`
2. System keyring
3. Interactive prompt (stored in keyring for future use)

To reset a stored keyring password:

```python
conn.reset_password()
```
