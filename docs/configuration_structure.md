# Configuration File Structure

## General Structure

A `.yaml` configuration file in any of the places listed in the [configuration guide](/docs/configuration_guide.md) will work if it has the following structure:

```yaml
default:
  user: ${oc.env:ORACLE_USER}
  dsn: ${oc.env:ORACLE_DSN}
  lib_dir: ${oc.env:ORACLE_LIB_DIR,null}
  credential_account: ${.user}
# You may provide as many entries in "connections" as you like.
# You may also omit it entirely.
connections:
  Example Connection:
    user: ???
    dsn: ???
    lib_dir: null
    credential_account: ${.user}
  Another Connection:
    user: ???
    dsn: ???
    lib_dir: null
    credential_account: ${.user}
```

- If you pass a value for `lib_dir`, thick mode will be used.
- You only need to provide values where the default value is `???`. Any default values shown above will be provided automatically.
  
  For example, the following is a valid connection block:

  ```yaml
  # We don't need to pass `lib_dir` or `credential_account`.
  connections:
    db-dev:
      user: developer
      dsn: my-dsn:port/SID
      # `lib_dir` is missing, so thin mode will be used
      # `credential_account` will equal `${.user}` i.e. `developer`
  ```

  To use it, specify the proper profile:

  ```python
  conn = LightOracleConnection(profile='db-dev')
  ```

- You may specify as many database connections as you want in the `connections` section, including none. It is optional.

## Default Section

This section will be used if no profile is passed to `LightOracleConnection`.

Unless you overwrite the values, the values for your default section will look like this:

```yaml
default:
  user: ${oc.env:ORACLE_USER}
  dsn: ${oc.env:ORACLE_DSN}
  lib_dir: ${oc.env:ORACLE_LIB_DIR,null}
  credential_account: ${.user}
```

This is how [OmegaConf](https://omegaconf.readthedocs.io/en/latest/) is used to parse any values provided to an `.env` file. You may override them, if you wish.

