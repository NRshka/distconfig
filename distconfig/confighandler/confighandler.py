from typing import Dict
import os

from .parsers.parser import AbstractConfigParser


class ConfigHandler:
    def __init__(
        self,
        parsers: Dict[str, AbstractConfigParser],
        cfg_dir: str
    ):
        self.parsers = parsers
        self.cfg_dir = cfg_dir
        self.configs: Dict[
            str, Dict[str, dict]
        ] = {}  # service name : config name: config

        service_names = os.listdir(cfg_dir)

        for project_name in service_names:
            self.configs[project_name] = {}
            project_path = os.path.join(cfg_dir, project_name)
            config_files = os.listdir(project_path)

            for config_name in config_files:
                self.configs[project_name][config_name] = self.parse_config_file(
                    os.path.join(project_path, config_name)
                )

    def parse_config_file(self, path):
        parser = self.select_suitable_parser(path)
        return parser.parse(path)

    def select_suitable_parser(self, path):
        _, extension = os.path.splitext(path)

        assert extension, ValueError(f"No extension in path {path}")

        extension = extension[1:]  # remove dot

        if extension not in self.parsers:
            raise ValueError(
                f"No suitable parse for extension {extension} of path {path}"
            )

        return self.parsers[extension]
