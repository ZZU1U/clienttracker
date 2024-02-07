from configparser import ConfigParser
import os

config_file = './local/config.ini'
secret_file = './local/secret.ini'

# Initialize
config = ConfigParser()
config.read(config_file)

secret = ConfigParser()
secret.read(secret_file)


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
gigachat_silent = secret.get('gigachat', 'silent')
gigachat_token = secret.get('gigachat', 'token')

# VK
vk_token = secret.get('vk', 'token')
vk_user_id = secret.get('vk', 'user_id')
