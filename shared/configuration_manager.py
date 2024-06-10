import logging
from azure.appconfiguration import AzureAppConfigurationClient


class ConfigurationManager:
    def __init__(self, connection_string: str):
        self.client = AzureAppConfigurationClient.from_connection_string(connection_string)
        self.settings = {}
        logging.basicConfig(level=logging.INFO)

    def load(self):
        try:
            fetched_kv = self.client.list_configuration_settings()
            for item in fetched_kv:
                self.settings[item.key] = item.value
            logging.info("Configuration loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load configuration: {e}")

    def save(self):
        try:
            for key, value in self.settings.items():
                self.client.set_configuration_setting(key=key, value=value)
            logging.info("Configuration saved successfully.")
        except Exception as e:
            logging.error(f"Failed to save configuration: {e}")

    def __getattr__(self, name):
        try:
            return self.settings[name]
        except KeyError:
            logging.error(f"No such setting: {name}")
            raise AttributeError(f"No such setting: {name}")

    def __setattr__(self, name, value):
        if name in ['client', 'settings']:
            super().__setattr__(name, value)
        else:
            self.settings[name] = value
            logging.info(f"Setting updated - {name}: {value}")