from configparser import ConfigParser
from dotenv import find_dotenv, load_dotenv
import os


config_file = './local/config.ini'
default_config = './local/default.ini'

# Initialize
config = ConfigParser()
config.read(default_config)
config.read(config_file)

load_dotenv(find_dotenv())


def set_service(is_service: str) -> None:
    with open(config_file, 'w') as f:
        config.set('settings', 'is_service', is_service)
        config.write(f)


def get_service() -> bool:
    return config.getboolean('settings', 'is_service')


def get_theme() -> str:
    return config.get('settings', 'theme')


def set_theme(theme: str) -> None:
    with open(config_file, 'w') as f:
        config.set('settings', 'theme', theme)
        config.write(f)


def get_subscription() -> bool:
    return config.getboolean('subscription', 'enabled')


def set_subscription(sub: bool) -> None:
    with open(config_file, 'w') as f:
        config.set('subscription', 'enabled', 'yes' if sub else 'no')
        config.write(f)


# Database
db_url = config.get('database', 'url')

# Gigachat
gigachat_silent = os.environ.get('GIGACHAT_SILENT')
gigachat_token = os.environ.get('GIGACHAT_TOKEN')

# VK
vk_login = os.environ.get('VK_LOGIN')
vk_password = os.environ.get('VK_PASSWORD')
