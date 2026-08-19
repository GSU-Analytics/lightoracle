from typing import Optional, Any, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from omegaconf import OmegaConf, DictConfig, MISSING
from omegaconf.errors import InterpolationResolutionError
from dotenv import load_dotenv
from loguru import logger
from pprint import pformat


@dataclass
class LightOracleConnection:
    user: str = MISSING
    dsn: str = MISSING
    lib_dir: Optional[str] = None


@dataclass
class LightOracleConfig:
    default: LightOracleConnection = field(default_factory=lambda: LightOracleConnection(
        user='${oc.env:ORACLE_USER}',
        dsn='${oc.env:ORACLE_DSN}',
        lib_dir='${oc.env:ORACLE_LIB_DIR,null}')
    )
    connections: Optional[dict[str, LightOracleConnection]] = None


def parse_explicit_credentials(arguments: dict[str, Any], names: Iterable[str]) -> dict[str, str] | None:
    '''Used to parse the old LightOracleConnection __init__ arguments and
    structure them for credential management.
    '''
    credentials = {
        name: str(arguments.get(name))
        for name in names
        if arguments.get(name)
    }
    if credentials:
        return credentials


def _find_config_file() -> None | Path:
    def _read_home_config(global_path: Path) -> Path | None:
        '''Check for a `.lightoracle` env file in the home dir.
        If it exists, read the 'ORACLE_CONFIG_PATH' environment
        variable and add it as a path.
        '''
        lightoracle_env = global_path
        if lightoracle_env.exists():
            import os
            load_dotenv(lightoracle_env)
            config_path = os.getenv('ORACLE_CONFIG_PATH')
            if config_path:
                return Path().home() / config_path
        logger.info(f'No env file with `ORACLE_CONFIG_PATH` value found at `{lightoracle_env}`.')

    configs: dict[str, Path | None] = {
        'local_config': Path('.') / 'oracle_config.yaml',
        'home_file_config': _read_home_config(Path.home() / '.lightoracle'),
        'home_config': Path.home() / '.lightoracle.d/oracle_config.yaml',
    }

    logger.info(f'Looking for a config file in the following places (in order):\n{pformat(configs, sort_dicts=False)}\n')

    for config, config_path in configs.items():
        if config_path and config_path.exists():
            logger.info(f'Found a config file at `{config_path}`.')
            return config_path

    logger.info('No .yaml config file found. The default configuration template will be used.')


def load_config(profile: str | None = None, explicit_credentials: dict[str, str] | None = None) -> DictConfig:
    # Initialize the config.
    global_config = OmegaConf.structured(LightOracleConfig)
    # Find a config file, if it exists.
    # If it does, merge it with the config.
    config_filepath = _find_config_file()
    if config_filepath:
        global_config = OmegaConf.merge(
            global_config,
            OmegaConf.load(config_filepath),

        )
    printable_config = OmegaConf.to_yaml(global_config)
    logger.info(f'Your loaded configuration details are:\n{printable_config}')
    # Choose the config based on the passed-in profile
    if not profile:
        config = OmegaConf.select(global_config, 'default')
    else:
        config = OmegaConf.select(global_config, f'connections.{profile}')
    # Override credentials with any explicitly passed arguments
    if explicit_credentials:
        logger.info(f'The following values were explicitly passed:\n{OmegaConf.to_yaml(explicit_credentials)}')
        config = OmegaConf.merge(config, OmegaConf.create(explicit_credentials))

    # Check structure and show configuration values.
    # If OmegaConf interpolation cannot be done successfully, warn the user.
    assert isinstance(config, DictConfig)
    try:
        printable_config = OmegaConf.to_container(config, resolve=True)
        printable_config = OmegaConf.to_yaml(printable_config)
        logger.info(f'Using the following configuration values:\n{printable_config}')
    except InterpolationResolutionError:
        import warnings
        warnings.warn('\nYour configuration file relies on interpolated values which could not be resolved.\nYou may need to rename values in a `.env` file, somewhere.\n', stacklevel=2)
        printable_config = OmegaConf.to_yaml(config)
        logger.warning(f'Using the following configuration values:\n{printable_config}')

    return config


def write_config_template(output_path: Path):
    config_template = OmegaConf.structured(LightOracleConfig(connections={'YOUR DATABASE NAME HERE': LightOracleConnection()}))
    if not output_path.exists():
        output_path.write_text(OmegaConf.to_yaml(config_template))