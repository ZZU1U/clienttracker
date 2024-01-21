from configparser import ConfigParser
import os

config_file = './local/config.ini'

# Initialize
config = ConfigParser()
config.read(config_file)


def set_service(is_service: bool) -> None:
    with open(config_file, 'w') as f:
        config.set('settings', 'is_service', str(is_service))
        config.write(f)


def get_service() -> bool:
    return config.getboolean('settings', 'is_service')


def get_theme() -> str:
    return config.get('settings', 'theme')


def set_theme(theme: str) -> None:
    with open(config_file, 'w') as f:
        config.set('settings', 'theme', theme)
        config.write(f)


# Database
db_url = config.get('database', 'url')

# Gigachat
gigachat_silent = config.get('gigachat', 'silent')
gigachat_token = config.get('gigachat', 'token')

# VK
vk_token = config.get('vk', 'token')
vk_user_id = config.get('vk', 'user_id')
