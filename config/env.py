import os
from abc import ABC
from typing import Final
from environs import Env


class Env(ABC):
    env = Env()
    env.read_env()
    BOT_TOKEN: Final = env.str("BOT_TOKEN")  # Забираем значение типа str

    # POSTGRES CONNECT
    PG_IP: Final = env.str("PG_IP")
    PG_USER: Final = env.str("PG_USER")
    PG_PASSWORD: Final = env.str("PG_PASSWORD")
    PG_HOST: Final = env.str("PG_HOST")
    PG_DATABASE: Final = env.str("PG_DATABASE")
    POSTGRES_URI: Final = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}'  # Для серверной базы
    # POSTGRES_URI: Final = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_IP}/{PG_DATABASE}'  # Для локальной базы
    ###

    # channel_id = env.list('CHANNEL_ID') # Список каналов, записывается через запятую
    # channel_link = env.str('CHANNEL_LINK')
    ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
    # IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

    SBER_CLIENT_SECRET: Final = env.str("SBER_CLIENT_SECRET")
    SBER_AUTH_DATA: Final = env.str("SBER_AUTH_DATA")
