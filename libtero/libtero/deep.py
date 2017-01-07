from pathlib import PurePath
import configparser
import subprocess
import shlex
import os


def parse_predicted(line):
    data = dict(
        fname=line[0].strip(b'>>> Processed: '),
        ptime=line[1].strip(b'>>> Predicted in: '),
        saved=line[-1].strip(b'>>> Saved to: '),
        labels=line[2:-1],
        person_detected=False,
    )
    for label in data['labels']:
        if b'person' in label:
            data['person_detected'] = True
    return data


def run_detector(image_path, cfg=None):
    predictions = []

    config = configparser.ConfigParser()
    config.read(cfg or os.getenv('DEEPINI'))

    deepnet = config['DEEPNET']
    os.chdir(deepnet['Chdir'])

    cmd = './{deepneuralbinary} detector test {data} {cfg} {weights} {path}'.format(
        path=image_path, **deepnet
    )

    cmd = shlex.split(cmd)

    completed_process = subprocess.check_output(cmd)
    data = parse_predicted(completed_process.split(b'\n'))
    data.update({'saved': PurePath(deepnet['Chdir'], data['saved'].decode('utf-8'))})

    return data 
