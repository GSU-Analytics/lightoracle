# lightoracle

A lightweight Oracle database connection handler. Reads credentials automatically, and can execute queries with Pandas or produce a SQLAlchemy engine so you can use your tool of choice.

## Installation

```bash
pip install git+https://github.com/GSU-Analytics/lightoracle.git
```

To pin a version:

```bash
pip install git+https://github.com/GSU-Analytics/lightoracle.git@v0.3.0
```

## Configuration

### Configuration File Support

`lightoracle` supports at least 5 different configuration approaches.

See the [configuration guide](/docs/configuration_guide.md) for details on where to place your configuration files.

### Configuration File Structure

A `.yaml` configuration file in any of the places listed in the [configuration guide](/docs/configuration_guide.md) will work if it has the following structure:

```yaml
default:
  user: ???
  dsn: ???
  lib_dir: ???
# You may provide as many entries in "connections" as you like
connections:
  YOUR DATABASE NAME HERE:
    user: ???
    dsn: ???
    lib_dir: null
```

- You may specify as many database connections as you want in the `connections` section, including none. It is optional.
- Unless you overwrite the values, the values for your default section will look like this:

  ```yaml
  default:
    user: ${oc.env:ORACLE_USER}
    dsn: ${oc.env:ORACLE_DSN}
    lib_dir: ${oc.env:ORACLE_LIB_DIR,null}
  ```

  This is how [OmegaConf](https://omegaconf.readthedocs.io/en/latest/) is used to parse any values provided to an `.env` file. You may override them, if you wish.

- If you like, `lightoracle.credentials` contains a function which will create a starting configuration template for you.

  ```python
  from lightoracle import credentials
  from pathlib import Path
  # This will get you started
  credentials.write_config_template(Path('oracle_config.yaml'))
  ```

### Password Management

Your password is loaded in priority order:

1. (NOT RECOMMENDED) Get the `ORACLE_PASSWORD` passed to `.env` or set as an environment variable
2. System keyring
3. Interactive prompt (stored in keyring for future use)

To reset a stored keyring password:

```python
conn.reset_password()
```
## Usage

### Executing with Pandas

Import `LightOracleConnection` and create an instance. Credentials will be loaded automatically.

```python
from lightoracle import LightOracleConnection

conn = LightOracleConnection()
df = conn.execute_query("SELECT * FROM my_table FETCH FIRST 10 ROWS ONLY")
df.to_csv('output.csv', index=False)
```

### SQLAlchemy Engine Support

Some libraries, like `polars` and `ibis`, are most easily interfaced with if you have an `SQLAlchemy` engine instance.

Use `LightOracleConnection.create_engine()` to get an engine instance pre-configured for you.

```python
conn = LightOracleConnection()
engine = conn.create_engine()
```

### Dynamic Connection Support

If you have entries in a `connections` block in your configuration file, you can change your credentials by using the `LightOracleConnection().with_profile()` method. Pass a profile name to use the credentials in that block.

Here's an example configuration scheme:

```yaml
# Imagine we have the following blocks
connections:
  DB-development:
    user: ???
    dsn: ???
    lib_dir: null
  DB-production:
    user: ???
    dsn: ???
    lib_dir: null
```

We can switch between these parameters at runtime.

```python
# We start by using the development server
conn = LightOracleConnection(profile='DB-development')
# At some point, we decide to switch to the production server
# NOTE! Your connection won't change until you explicitly call `.connect()`!
conn.with_profile(profile='DB-production').connect()
```

### Thin mode vs. thick mode

By default, lightoracle uses **thin mode** — no Oracle Instant Client required.

To use thick mode (Oracle Instant Client), set the `lib_dir`:

```python
# thick mode — explicit library path
# Note: You can also specify `lib_dir` in your config file
conn = LightOracleConnection(lib_dir="/path/to/oracle/client")
```

`lib_dir` can also be set via `ORACLE_LIB_DIR` in your `.env` file.
