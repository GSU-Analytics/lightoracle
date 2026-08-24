# Configuration File Options

There are several ways to store your credentials outside of your code with LightOracle.

## Option 1: Local Project Configuration File

Create an `oracle_config.yaml` file in your project folder.

## Option 2: Global `lightoracle` Configuration File

You can use a `~/.lightoracle` file to tell `lightoracle` to look wherever you want for a `.yaml` config file.

1. Create a file called `.lightoracle` in your home directory (e.g. `~/.lightoracle`).
2. In `.lightoracle`, add a line like `ORACLE_CONFIG_PATH=???`.
   - For example, `ORACLE_CONFIG_PATH=my_credentials/oracle.yaml`.
   - The file passed as `ORACLE_CONFIG_PATH` will be relative to the user's home directory.
   - `.lightoracle` is considered a `.env` file by the `lightoracle` package, and should be structured as such.
3. Create a `.yaml` file at the path given to `ORACLE_CONFIG_PATH`.

## Option 3: Global `lightoracle` Configuration Directory

Create a directory called `.lightoracle.d/` in your home directory, and then add an `oracle_config.yaml` file to it.

## Option 4: Local `.env` Configuration File

If you do not have any of the other configuration approaches set up, the default configuration template will read a local `.env` file's values.

```env
ORACLE_USER=your_username 
ORACLE_DSN=hostname:port/service_name
ORACLE_LIB_DIR=path/to/lib/dir
```

`ORACLE_LIB_DIR` is optional, if you do not require thick mode support.

## Option 5: Passing `LightOracleConnection` Arguments

If all else fails, you may pass your configuration values directly to `LightOracleConnection`.

```python
conn = LightOracleConnection(
    user="my_user",
    dsn="host:1521/svc"
)
```