import configparser

INI_FILE_PATH = "config.ini"

config = configparser.RawConfigParser()

config.read(INI_FILE_PATH)