import configparser

def read_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config
