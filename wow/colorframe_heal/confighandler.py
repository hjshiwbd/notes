import json
import logging


def save_config(info):
    with open('color2heal.json', 'w') as io:
        io.write(json.dumps(info))
        logging.info("config saved")


def load_config():
    with open('color2heal.json') as io:
        return json.loads(io.read())
