from typing import Dict
import os

from .parsers.parser import AbstractConfigParser


class ConfigHandler:
    def __init__(
        self,
        parsers: Dict[str, AbstractConfigParser],
        cfg_dir: str,
        cache_util
    ):
        self.parsers = parsers
        self.cfg_dir = cfg_dir
        self.directory_structure: Dict[str, set] = {}
        self.configs_cache = cache_util

        self.check_volume_valid(cfg_dir)

    def check_volume_valid(self, cfg_dir: str):
        service_names = os.listdir(cfg_dir)

        for service_name in service_names:
            # use set for fast O(1) checking is name in service structure already
            self.directory_structure[service_name] = set()
            project_path = os.path.join(cfg_dir, service_name)
            config_files = os.listdir(project_path)

            for config_name in config_files:
                if config_name in self.directory_structure[service_name]:
                    raise RuntimeError(f'{service_name} already has a {config_name} name')

                self.directory_structure[service_name].add(config_name)

    def get_config(self, service_name: str, config_name: str) -> dict:
        cache_key = f'{service_name}/{config_name}'
        config = self.configs_cache.get(cache_key)

        if config is not None:
            return config

        if service_name not in self.directory_structure or config_name not in self.directory_structure[service_name]:
            raise RuntimeError('No such service_name and/or config_name')

        config = self.parse_config_file(os.path.join(self.cfg_dir, service_name, config_name))
        self.configs_cache.set(cache_key, config)

        return config

    def parse_config_file(self, path):
        parser = self.select_suitable_parser(path)
        return parser.parse(path)

    def select_suitable_parser(self, path):
        _, extension = os.path.splitext(path)

        assert extension, ValueError(f"No extension in path {path}")

        extension = extension[1:]  # remove dot

        if extension not in self.parsers:
            raise ValueError(
                f"No suitable parser for extension {extension} of path {path}"
            )

        return self.parsers[extension]
