from ruamel import yaml
from ruamel.yaml.comments import CommentedMap
import logging


class Config:
    def __init__(self, yaml_path=None, key_file_path=None):
        if yaml_path is not None:
            with open(yaml_path) as config_file:
                self.config_dict = yaml.load(config_file, Loader=yaml.Loader)
        else:
            self.config_dict = CommentedMap()
            self.config_dict['columns_to_anonymize'] = {}
        if key_file_path is not None:
            with open(key_file_path) as key_file:
                self.secret_key = key_file.read().strip()
        else:
            self.secret_key = 'default-key'

    @property
    def logger(self):
        return logging.getLogger('config')

    @property
    def columns_to_anonymize(self):
        return self.config_dict.get('columns_to_anonymize')

    def add_column_config(self, column_name, column_config_dict):
        self.config_dict['columns_to_anonymize'][column_name] = column_config_dict

    def save_config(self, save_name=None):
        if save_name is None:
            from datetime import date
            save_name = date.today().strftime('%Y-%m-%d_generated_config.yml')
        with open(save_name, 'w') as save_file:
            yaml.round_trip_dump(self.config_dict, save_file, default_flow_style=False)


class SecretKeyNotSetException(Exception):
    pass
