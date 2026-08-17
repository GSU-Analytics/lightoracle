from typing import Optional
from dataclasses import dataclass, field
from pathlib import Path
from omegaconf import OmegaConf, DictConfig, MISSING
from dotenv import load_dotenv

load_dotenv()


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


def find_config_file() -> None | Path:
    configs = {
        'local_config': Path('.') / 'oracle_config.yaml',
        'home_config': Path.home() / '.lightoracle.d/oracle_config.yaml'
    }
    # Check for a `.lightoracle` env file in the home dir.
    # If it exists, read the 'ORACLE_CONFIG_PATH' environment
    # variable and add it as a path.
    lightoracle_env = Path.home() / '.lightoracle'
    if lightoracle_env.exists():
        import os
        load_dotenv(lightoracle_env)
        config_path = os.getenv('ORACLE_CONFIG_PATH')
        if config_path:
            configs['home_custom_config'] = Path().home() / config_path

    for config, config_path in configs.items():
        if config_path.exists():
            return config_path


def load_config(profile: str | None = None, **kwargs) -> DictConfig:
    # Initialize the config.
    global_config = OmegaConf.structured(LightOracleConfig)
    # Find a config file, if it exists.
    # If it does, merge it with the config.
    config_filepath = find_config_file()
    if config_filepath:
        global_config = OmegaConf.merge(
            global_config,
            OmegaConf.load(config_filepath),

        )
    # Choose the config based on the passed-in profile
    if not profile:
        config = OmegaConf.select(global_config, 'default')
    else:
        config = OmegaConf.select(global_config, f'connections.{profile}')
    # Parse the passed keyword arguments, keep the non-null values,
    # and merge any remaining ones
    filtered_kwargs = {k: kwargs[k] for k in kwargs if kwargs[k]}
    if filtered_kwargs:
        config = OmegaConf.merge(config, OmegaConf.create(filtered_kwargs))

    assert isinstance(config, DictConfig)
    return config


def write_config_template(output_path: Path):
    config_template = OmegaConf.structured(LightOracleConfig(connections={'YOUR DATABASE NAME HERE': LightOracleConnection()}))
    if not output_path.exists():
        output_path.write_text(OmegaConf.to_yaml(config_template))