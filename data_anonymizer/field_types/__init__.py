from pyhashxx import hashxx
import faker
from .decorators.text_formatter import apply_formatting_options


class BaseFieldType:
    def __init__(self, type_config_dict):
        self.type_config_dict = type_config_dict
        self.faker = FakerSingleton()

    @staticmethod
    def generate_seed(value):
        value = hashxx(value.encode())
        return value

    def seed_faker(self, field_value):
        seed = BaseFieldType.generate_seed(field_value)
        self.faker.seed(seed)

    def generate_obfuscated_value(self, value):
        raise NotImplementedError


class FakerSingleton:
    """
    Using the singleton pattern since we only need the one instance of Faker,
    and instantiating Faker is expensive (~0.02 seconds)
    """
    class __FakerSingleton:
        def __init__(self):
            self.faker = faker.Faker()

    instance = None

    def __init__(self):
        if not FakerSingleton.instance:
            FakerSingleton.instance = FakerSingleton.__FakerSingleton()

    def __getattr__(self, item):
        return getattr(self.instance.faker, item)
